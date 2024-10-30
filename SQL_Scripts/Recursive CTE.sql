WITH FibonacciCTE (n, fib_value, prev_fib) AS (
    -- Base cases
    SELECT 1 AS n, 0 AS fib_value, 1 AS prev_fib
    UNION ALL
    SELECT 2, 1, 0
    UNION ALL
    -- Recursive member
    SELECT 
        n + 1, 
        fib_value + prev_fib,
        fib_value
    FROM FibonacciCTE
    WHERE n < 20
)
SELECT n, fib_value FROM FibonacciCTE;