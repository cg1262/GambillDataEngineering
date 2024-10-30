SELECT 
    order_id ID, 
    format(order_date,'MM-dd-yy') Ordered, 
    format(shipped_date,'MM-dd-yy') Shipped, 
    format(received_date,'MM-dd-yy') Received, 
    case when received_date is not null 
    then 'Received'
    when shipped_date is not null 
    then 'Shipped'
    when order_date is not null
    then 'Ordered'
    end as Status,
    COALESCE(received_date, 
             shipped_date, 
             order_date) AS status_date
FROM orders;