import GetParameters as gp
import os
from datetime import datetime, timedelta
import requests
import pyodbc

# Load credentials from parameter file via custom GetParam module variables
COMPANY_ID = gp.getParam('qb_sandbox_CompId')
CLIENT_ID = gp.getParam('qb_clientId')
CLIENT_SECRET = gp.getParam('qb_apiSec')
REDIRECT_URI = 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl'
environment = 'sandbox'
REFRESH_TOKEN = gp.getParam('qb_Oauth_RefreshToken')

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
        'query': f"SELECT * FROM {entity} ",
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

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Items' AND xtype='U')
    CREATE TABLE QB.Items (
        Id NVARCHAR(50) PRIMARY KEY,
        Name NVARCHAR(255),
        Type NVARCHAR(50),
        UnitPrice DECIMAL(18,2),
        PurchaseCost DECIMAL(18,2),
        IncomeAccountRef NVARCHAR(50)
    )
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Payments' AND xtype='U')
    CREATE TABLE QB.Payments (
        Id NVARCHAR(50) PRIMARY KEY,
        CustomerId NVARCHAR(50),
        TxnDate DATE,
        TotalAmount DECIMAL(18,2),
        UnappliedAmount DECIMAL(18,2),
        FOREIGN KEY (CustomerId) REFERENCES QB.Customers(Id)
    )
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Vendors' AND xtype='U')
    CREATE TABLE QB.Vendors (
        Id NVARCHAR(50) PRIMARY KEY,
        DisplayName NVARCHAR(255),
        CompanyName NVARCHAR(255),
        Email NVARCHAR(255),
        Phone NVARCHAR(50),
        Balance DECIMAL(18,2)
    )
    """)
    
    cursor.commit()

def upsert_customer_data(cursor, customers):
    for customer in customers:
        cursor.execute("""
        MERGE QB.Customers AS target
        USING (VALUES (?, ?, ?, ?, ?, ?)) AS source (Id, DisplayName, CompanyName, Email, Phone, Balance)
        ON target.Id = source.Id
        WHEN MATCHED THEN
            UPDATE SET
                DisplayName = source.DisplayName,
                CompanyName = source.CompanyName,
                Email = source.Email,
                Phone = source.Phone,
                Balance = source.Balance
        WHEN NOT MATCHED THEN
            INSERT (Id, DisplayName, CompanyName, Email, Phone, Balance)
            VALUES (source.Id, source.DisplayName, source.CompanyName, source.Email, source.Phone, source.Balance);
        """, (
            customer['Id'],
            customer['DisplayName'],
            customer.get('CompanyName', ''),
            customer.get('PrimaryEmailAddr', {}).get('Address', ''),
            customer.get('PrimaryPhone', {}).get('FreeFormNumber', ''),
            customer.get('Balance', 0)
        ))
    cursor.commit()

def upsert_invoice_data(cursor, invoices):
    for invoice in invoices:
        cursor.execute("""
        MERGE QB.Invoices AS target
        USING (VALUES (?, ?, ?, ?, ?, ?, ?)) AS source (Id, CustomerId, TxnDate, DueDate, TotalAmount, Balance, Status)
        ON target.Id = source.Id
        WHEN MATCHED THEN
            UPDATE SET
                CustomerId = source.CustomerId,
                TxnDate = source.TxnDate,
                DueDate = source.DueDate,
                TotalAmount = source.TotalAmount,
                Balance = source.Balance,
                Status = source.Status
        WHEN NOT MATCHED THEN
            INSERT (Id, CustomerId, TxnDate, DueDate, TotalAmount, Balance, Status)
            VALUES (source.Id, source.CustomerId, source.TxnDate, source.DueDate, source.TotalAmount, source.Balance, source.Status);
        """, (
            invoice['Id'],
            invoice['CustomerRef']['value'],
            invoice['TxnDate'],
            invoice.get('DueDate'),
            invoice['TotalAmt'],
            invoice['Balance'],
            'Paid' if invoice['Balance'] == 0 else 'Unpaid'
        ))
        
        for line in invoice.get('Line', []):
            if line['DetailType'] == 'SalesItemLineDetail':
                item = line['SalesItemLineDetail']
                cursor.execute("""
                MERGE QB.InvoiceLineItems AS target
                USING (VALUES (?, ?, ?)) AS source (InvoiceId, ItemName, Amount)
                ON target.InvoiceId = source.InvoiceId AND target.ItemName = source.ItemName
                WHEN MATCHED THEN
                    UPDATE SET Amount = source.Amount
                WHEN NOT MATCHED THEN
                    INSERT (InvoiceId, ItemName, Amount)
                    VALUES (source.InvoiceId, source.ItemName, source.Amount);
                """, (
                    invoice['Id'],
                    item['ItemRef']['name'],
                    line['Amount']
                ))
    cursor.commit()

def upsert_item_data(cursor, items):
    for item in items:
        cursor.execute("""
        MERGE QB.Items AS target
        USING (VALUES (?, ?, ?, ?, ?, ?)) AS source (Id, Name, Type, UnitPrice, PurchaseCost, IncomeAccountRef)
        ON target.Id = source.Id
        WHEN MATCHED THEN
            UPDATE SET
                Name = source.Name,
                Type = source.Type,
                UnitPrice = source.UnitPrice,
                PurchaseCost = source.PurchaseCost,
                IncomeAccountRef = source.IncomeAccountRef
        WHEN NOT MATCHED THEN
            INSERT (Id, Name, Type, UnitPrice, PurchaseCost, IncomeAccountRef)
            VALUES (source.Id, source.Name, source.Type, source.UnitPrice, source.PurchaseCost, source.IncomeAccountRef);
        """, (
            item['Id'],
            item['Name'],
            item['Type'],
            item.get('UnitPrice', 0),
            item.get('PurchaseCost', 0),
            item.get('IncomeAccountRef', {}).get('value', '')
        ))
    cursor.commit()

def upsert_payment_data(cursor, payments):
    for payment in payments:
        cursor.execute("""
        MERGE QB.Payments AS target
        USING (VALUES (?, ?, ?, ?, ?)) AS source (Id, CustomerId, TxnDate, TotalAmount, UnappliedAmount)
        ON target.Id = source.Id
        WHEN MATCHED THEN
            UPDATE SET
                CustomerId = source.CustomerId,
                TxnDate = source.TxnDate,
                TotalAmount = source.TotalAmount,
                UnappliedAmount = source.UnappliedAmount
        WHEN NOT MATCHED THEN
            INSERT (Id, CustomerId, TxnDate, TotalAmount, UnappliedAmount)
            VALUES (source.Id, source.CustomerId, source.TxnDate, source.TotalAmount, source.UnappliedAmount);
        """, (
            payment['Id'],
            payment['CustomerRef']['value'],
            payment['TxnDate'],
            payment['TotalAmt'],
            payment.get('UnappliedAmt', 0)
        ))
    cursor.commit()

def upsert_vendor_data(cursor, vendors):
    for vendor in vendors:
        cursor.execute("""
        MERGE QB.Vendors AS target
        USING (VALUES (?, ?, ?, ?, ?, ?)) AS source (Id, DisplayName, CompanyName, Email, Phone, Balance)
        ON target.Id = source.Id
        WHEN MATCHED THEN
            UPDATE SET
                DisplayName = source.DisplayName,
                CompanyName = source.CompanyName,
                Email = source.Email,
                Phone = source.Phone,
                Balance = source.Balance
        WHEN NOT MATCHED THEN
            INSERT (Id, DisplayName, CompanyName, Email, Phone, Balance)
            VALUES (source.Id, source.DisplayName, source.CompanyName, source.Email, source.Phone, source.Balance);
        """, (
            vendor['Id'],
            vendor['DisplayName'],
            vendor.get('CompanyName', ''),
            vendor.get('PrimaryEmailAddr', {}).get('Address', ''),
            vendor.get('PrimaryPhone', {}).get('FreeFormNumber', ''),
            vendor.get('Balance', 0)
        ))
    cursor.commit()

def main():
    try:
        access_token = get_access_token()
        
        customers = get_all_data(access_token, 'Customer')
        invoices = get_all_data(access_token, 'Invoice')
        items = get_all_data(access_token, 'Item')
        payments = get_all_data(access_token, 'Payment')
        vendors = get_all_data(access_token, 'Vendor')
        
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        create_tables(cursor)
        
        upsert_customer_data(cursor, customers)
        upsert_invoice_data(cursor, invoices)
        upsert_item_data(cursor, items)
        upsert_payment_data(cursor, payments)
        upsert_vendor_data(cursor, vendors)
        
        print(f"Successfully upserted {len(customers)} customers, {len(invoices)} invoices, {len(items)} items, {len(payments)} payments, and {len(vendors)} vendors into the database.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()