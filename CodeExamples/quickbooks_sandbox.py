import GetParameters as gp
import os
from datetime import datetime, timedelta
import requests
import pyodbc
# Load credentials from parameter file via custom GetParam module variables
COMPANY_ID = gp.getParam('qb_sandbox_CompId')
CLIENT_ID=gp.getParam('qb_clientId')
CLIENT_SECRET=gp.getParam('qb_apiSec')
COMPANY_ID =gp.getParam('qb_sandbox_CompId')
REDIRECT_URI ='https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl'
environment='sandbox'
REFRESH_TOKEN=gp.getParam('qb_Oauth_RefreshToken')
# QuickBooks API endpoints
TOKEN_ENDPOINT = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
API_BASE_URL = 'https://sandbox-quickbooks.api.intuit.com/v3/company'  # Use 'https://quickbooks.api.intuit.com/v3/company' for production

# SQL Server connection details
SQL_SERVER = gp.getParam('SQL_Server')
SQL_DATABASE = gp.getParam('SQL_DB')
SQL_USERNAME = gp.getParam('SQL_User')
SQL_PASSWORD = gp.getParam('SQL_PW')

def get_access_token():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def get_all_data(access_token, entity):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    params = {
        'query': f"SELECT * FROM {entity} MAXRESULTS 1000",
        'minorversion': '65'
    }
    url = f"{API_BASE_URL}/{COMPANY_ID}/query"
    
    all_data = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            entities = data['QueryResponse'].get(entity, [])
            all_data.extend(entities)
            
            # Check if there are more results
            query_response = data.get('QueryResponse', {})
            start_position = query_response.get('startPosition', 0)
            max_results = query_response.get('maxResults', 0)
            total_count = query_response.get('totalCount', 0)
            
            if total_count == 0 or start_position + max_results >= total_count:
                break
            
            params['startPosition'] = start_position + max_results
        else:
            raise Exception(f"Failed to get {entity}: {response.text}")
    
    return all_data

def create_tables(cursor):
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Customers' AND xtype='U')
    CREATE TABLE QB.Customers (
        Id NVARCHAR(50) PRIMARY KEY,
        DisplayName NVARCHAR(255),
        CompanyName NVARCHAR(255),
        Email NVARCHAR(255),
        Phone NVARCHAR(50),
        Balance DECIMAL(18,2)
    )
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Invoices' AND xtype='U')
    CREATE TABLE QB.Invoices (
        Id NVARCHAR(50) PRIMARY KEY,
        CustomerId NVARCHAR(50),
        TxnDate DATE,
        DueDate DATE,
        TotalAmount DECIMAL(18,2),
        Balance DECIMAL(18,2),
        Status NVARCHAR(50),
        FOREIGN KEY (CustomerId) REFERENCES QB.Customers(Id)
    )
    """)
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='InvoiceLineItems' AND xtype='U')
    CREATE TABLE QB.InvoiceLineItems (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        InvoiceId NVARCHAR(50),
        ItemName NVARCHAR(255),
        Amount DECIMAL(18,2),
        FOREIGN KEY (InvoiceId) REFERENCES QB.Invoices(Id)
    )
    """)
    
    cursor.commit()

def insert_customer_data(cursor, customers):
    for customer in customers:
        cursor.execute("""
        INSERT INTO QB.Customers (Id, DisplayName, CompanyName, Email, Phone, Balance)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer['Id'],
            customer['DisplayName'],
            customer.get('CompanyName', ''),
            customer.get('PrimaryEmailAddr', {}).get('Address', ''),
            customer.get('PrimaryPhone', {}).get('FreeFormNumber', ''),
            customer.get('Balance', 0)
        ))
    cursor.commit()

def insert_invoice_data(cursor, invoices):
    for invoice in invoices:
        # Insert invoice
        cursor.execute("""
        INSERT INTO QB.Invoices (Id, CustomerId, TxnDate, DueDate, TotalAmount, Balance, Status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice['Id'],
            invoice['CustomerRef']['value'],
            invoice['TxnDate'],
            invoice.get('DueDate'),
            invoice['TotalAmt'],
            invoice['Balance'],
            'Paid' if invoice['Balance'] == 0 else 'Unpaid'
        ))
        
        # Insert line items
        for line in invoice.get('Line', []):
            if line['DetailType'] == 'SalesItemLineDetail':
                item = line['SalesItemLineDetail']
                cursor.execute("""
                INSERT INTO QB.InvoiceLineItems (InvoiceId, ItemName, Amount)
                VALUES (?, ?, ?)
                """, (
                    invoice['Id'],
                    item['ItemRef']['name'],
                    line['Amount']
                ))
    
    cursor.commit()

def main():
    try:
        # Get QuickBooks data
        access_token = get_access_token()
        customers = get_all_data(access_token, 'Customer')
        invoices = get_all_data(access_token, 'Invoice')
        
        # Connect to SQL Server
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        create_tables(cursor)
        
        # Insert data
        insert_customer_data(cursor, customers)
        insert_invoice_data(cursor, invoices)
        
        print(f"Successfully inserted {len(customers)} customers and {len(invoices)} invoices into the database.")
        
        # Close the database connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()