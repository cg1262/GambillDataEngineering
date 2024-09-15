SELECT 
    c.customer_name,
    c.customer_country,
    SUM(o.order_total) AS total_spent
FROM 
    code_challenge.customers c
LEFT JOIN 
    code_challenge.orders o ON c.customer_id = o.customer_id
LEFT JOIN 
    code_challenge.order_items oi ON o.order_id = oi.order_id
WHERE 
    o.order_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY 
    c.customer_country,c.customer_name
ORDER BY 
    total_spent DESC;