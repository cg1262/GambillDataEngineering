CACHE TABLE top_customers AS
SELECT customer_id, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY customer_id
ORDER BY total_sales DESC
LIMIT 100;