import pandas as pd 

def create_kpi_template_layoutB():
  """Generates a sample layout for a KPI Template in dictionary format."""

  # Header Section
  header = {
    "Title": "KPI Template",
    "Company Name": "[Company Name]",  # Placeholder for user input
  }

  # Business Information Section
  business_info = {
    "Industry": "",
    "Core Products/Services": "",
    "Target Market": "",
    "Contact Name": "",
    "Contact Number": "",
    "Business Address": "",
  }

  # KPI List Section
  kpi_list = [
    {"KPI": "Customer Acquisition Cost (CAC)", "Definition": "Cost of acquiring a new customer", "Measurement Method": "Total marketing spend / Number of new customers acquired"},
    {"KPI": "Customer Lifetime Value (CLTV)", "Definition": "Total revenue a customer generates over their lifetime", "Measurement Method": "Average order value * Purchase frequency * Customer lifespan"},
    {"KPI": "Sales Growth Rate", "Definition": "Percentage increase in sales over a specific period", "Measurement Method": "((Current Period Sales - Previous Period Sales) / Previous Period Sales) * 100"},
    {"KPI": "Employee Turnover Rate", "Definition": "Percentage of employees who leave the company in a given period", "Measurement Method": "Number of employees who left / Average number of employees * 100"},
  ]

  # KPI Measurement Section
  kpi_measurement = [
    {"KPI": "", "Definition": "", "Measurement Method": "", "Data Source": "", "Target Value": "", "Frequency of Measurement": "", "Responsible Party": ""},
    {"KPI": "", "Definition": "", "Measurement Method": "", "Data Source": "", "Target Value": "", "Frequency of Measurement": "", "Responsible Party": ""},
    {"KPI": "", "Definition": "", "Measurement Method": "", "Data Source": "", "Target Value": "", "Frequency of Measurement": "", "Responsible Party": ""},
    # Add more rows for additional KPIs
  ]

  # Combine all sections
  template_layout = {**header, **business_info, "KPI List": kpi_list, "KPI Measurement": kpi_measurement}
  return template_layout

# Print the sample KPI Template Layout
 


def create_kpi_template_layout():
  """Generates a sample layout for a KPI Template."""

  # Header Section
  header = {
    "Title": "KPI Template",
    "Company Name": "[Company Name]",  # Placeholder for user input
  }

  # Business Information Section
  business_info = {
    "Industry": "",
    "Core Products/Services": "",
    "Target Market": "",
    "Contact Name": "",
    "Contact Number": "",
    "Business Address": "",
  }

  # KPI List Section (Replace with a table structure)
  kpi_list_placeholder = """
  **KPI List**

  This section will be replaced with a table containing a comprehensive list of KPIs categorized by business function (Financial, Operational, Marketing, Sales, HR, Customer Service, Productivity). 
  Each KPI will have a brief definition and space to mark its priority or relevance to the business.
  """

  # Target Setting and Analysis Section (Placeholder)
  target_setting_analysis = """
  **Target Setting and Analysis**

  This section will guide users on how to set target values for each KPI and perform basic KPI analysis techniques (e.g., variance analysis, trend analysis). It will also provide space to record target values, actual values, and variances.
  """

  # Action Plan Section (Placeholder)
  action_plan = """
  **Action Plan**

  This section will provide a framework for developing action plans to address performance gaps identified through KPI analysis. It will include guidance on defining the problem statement, setting goals, outlining action steps, assigning responsibilities, and tracking progress.
  """

  # Combine all sections
  template_layout = {**header, **business_info, "KPI List": kpi_list_placeholder, "Target Setting and Analysis": target_setting_analysis, "Action Plan": action_plan}
  return template_layout

# Print the sample KPI Template Layout
template_layout = create_kpi_template_layoutB()
print(template_layout)
for tab in template_layout:
    print(tab)
    try:
        df = pd.json_normalize(template_layout[tab])
        print(df)
        df.to_excel(f'D:/data/{tab}.xlsx')
    except Exception as e:
        print(e)