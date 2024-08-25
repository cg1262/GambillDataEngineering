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


