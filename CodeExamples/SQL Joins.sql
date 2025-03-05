-- INNER JOIN
SELECT DISTINCT
c.FirstName, 
c.LastName,
c.EmailAddress, 
i.SalesOrderNumber, 
i.OrderDate
FROM DimCustomer c
INNER JOIN FactInternetSales i 
    ON c.CustomerKey = i.CustomerKey;


-- LEFT JOIN
SELECT c.FirstName, c.LastName, i.SalesOrderNumber, i.OrderDate
FROM DimCustomer c
LEFT JOIN FactInternetSales i 
    ON c.CustomerKey = i.CustomerKey
order by salesordernumber  
;











-- RIGHT JOIN
SELECT c.FirstName, c.LastName, i.SalesOrderNumber, i.OrderDate
FROM DimCustomer c
RIGHT JOIN FactInternetSales i 
    ON c.CustomerKey = i.CustomerKey;












-- FULL OUTER JOIN
SELECT c.FirstName, c.LastName, i.SalesOrderNumber, i.OrderDate
FROM DimCustomer c
FULL OUTER JOIN FactInternetSales i 
    ON c.CustomerKey = i.CustomerKey;












-- Practical Example Using WITH Clause
WITH CustomerOrders AS (
    SELECT c.FirstName, c.LastName, i.SalesOrderNumber, i.OrderDate
    FROM DimCustomer c
    LEFT JOIN FactInternetSales i 
        ON c.CustomerKey = i.CustomerKey
)
SELECT FirstName, LastName,
       COUNT(SalesOrderNumber) AS TotalOrders,
       CASE WHEN COUNT(SalesOrderNumber) = 0 THEN 'No Orders' ELSE 'Active' END AS Status
FROM CustomerOrders
GROUP BY FirstName, LastName
order by CASE WHEN COUNT(SalesOrderNumber) = 0 THEN 'No Orders' ELSE 'Active' END;
