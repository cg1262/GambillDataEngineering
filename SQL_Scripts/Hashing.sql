SELECT  
    -- 1. Standard MD5 Hash for the customer_email column
    HASHBYTES('MD5', COALESCE(CAST(customer_email AS NVARCHAR(MAX)), '')) AS MD5_Hash_CustomerEmail,

    -- 2. MD5 Hash with CONVERT to CHAR(32) for hex representation of customer_email
    CONVERT(CHAR(32), HASHBYTES('MD5', COALESCE(CAST(customer_email AS NVARCHAR(MAX)), '')), 2) AS MD5_Hash_CustomerEmail_Char32,

    -- 3. Row Hash combining multiple columns (customer_name, customer_email, customer_phone, etc.)
    HASHBYTES('sha2_256', 
              COALESCE(CAST(customer_id AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_name AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_email AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_phone AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_address AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_city AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_state AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_zip AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(customer_country AS NVARCHAR(MAX)), '') + '|' +
              COALESCE(CAST(registration_date AS NVARCHAR(MAX)), '')
             ) AS Row_Hash_SHA256,
             *

FROM [code_challenge].[customers];