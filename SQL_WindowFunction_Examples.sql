SELECT 
    Date,
    CustomerName, 
    Address CurrentAddress,
    LAG(Address, 1) OVER (PARTITION BY CustomerName ORDER BY date) AS previous_address,
    LEAD(Address, 1) OVER (PARTITION BY CustomerName  ORDER BY date) AS next_address
FROM 
    staging.customers
    order by CustomerName ,date DESC
    ;

SELECT '"RANK"' WIN_FUNCTION,
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM 
    staging.employees;

SELECT '"DENSE_RANK"' WIN_FUNCTION,
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_dense_rank
FROM 
    staging.employees;

Select 
employee_name,
Salary,
Department,
avg(Salary) over (partition by department) AvgSalaryByDepartment,
Salary - avg(salary) over(partition by department) Variance_From_Department_Avg,
percentile_cont(0.5) within group(order by salary desc) over(partition by department) Median_Dept_Salary,
Salary - percentile_cont(0.5) within group(order by salary desc) over(partition by department) Varaince_From_Dept_Median
from staging.employees 
order by Department,salary desc
