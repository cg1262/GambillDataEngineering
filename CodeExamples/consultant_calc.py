# Define the given values for the calculation
hourly_rate = 150  # hourly consulting rate
hours_per_week = 40  # hours per week
weeks_per_year = 52  # weeks per year
day_job_salary = 151000  # day job salary
self_employment_tax_rate = 0.153  # self-employment tax rate (Social Security and Medicare)
federal_tax_bracket = 0.24  # assuming a 24% federal tax bracket

# Calculate gross consulting income for the year
consulting_income = hourly_rate * hours_per_week * weeks_per_year

# Calculate self-employment tax (Social Security and Medicare)
self_employment_tax = consulting_income * self_employment_tax_rate

# Calculate federal taxes
federal_taxes = consulting_income * federal_tax_bracket

# Calculate total taxes
total_taxes = self_employment_tax + federal_taxes

# Calculate net income from consulting after taxes
net_income = consulting_income - total_taxes

# Return the consulting income and net income after taxes
consulting_income, net_income
print(hourly_rate)
print(f"{net_income},{consulting_income} ")
print(net_income/52)
print(net_income/12)