
SELECT
order_id,
cast(order_date as date) Order_Date_Cast,
convert(varchar,order_date,1) Order_Date_Convert,
convert(varchar,order_date,101) Order_Date_Convert2,
order_date

FROM orders;













/*
CAST is ANSI standard, while CONVERT is not and as such not supported
in all dbs.

MySQL:
SELECT CONVERT('2024-01-01', DATE);

Postgres:
SELECT '2024-01-01'::DATE;

Oracle:
SELECT TO_DATE('2024-01-01', 'YYYY-MM-DD') FROM dual;

SELECT TO_CHAR('2024-01-01', 'YYYY-MM-DD') FROM dual;

*/