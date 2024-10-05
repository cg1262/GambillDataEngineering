select DisplayName, email, 
        (Select Avg(balance) 
                from qb.customers) as AverageBalance, 
        Balance,
        Balance - (Select Avg(balance) 
                from qb.customers) VarianceToAverage
from qb.customers

Select  Name,
        Email,
        Phone,
        TxnDate,
        DueDate,
        TotalAmount,
        Balance,
        Status,
        AverageBalance
from qb.invoices i 
inner join
(Select Id CustomerId, 
       DisplayName Name,
       Email,
       Phone,
       (Select Avg(balance) 
                from qb.customers) as AverageBalance
       from qb.customers 
       where balance >0) c 
on i.customerid = c.CustomerId


Select  DisplayName,
        Email,
        Phone,
        Balance
from qb.Customers c 
where balance > (Select Avg(balance) 
                from qb.customers)
order by Balance desc