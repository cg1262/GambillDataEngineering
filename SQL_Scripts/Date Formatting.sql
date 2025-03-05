-- SQL Script: Handling Different Date Formats

-- Section 1: CAST and CONVERT Examples
SELECT 
    CAST('12/26/2024' AS DATE) AS StandardDate,
    CONVERT(DATE, 'December 26, 2024', 23) AS ISODate;

-- Section 2: FORMAT Example
SELECT 
    FORMAT(GETDATE(), 'MMMM dd, yyyy') AS FormattedDate;

-- Section 3: Handling Non-Standard Date Formats Without PARSE
-- Convert '24th Dec 2024' to a standard date format
SELECT 
    CONVERT(DATE, REPLACE('24th Dec 2024', 'th', ''), 113) AS ParsedNonStandardDate;

-- Explanation:
-- - The REPLACE function removes the 'th' from '12th'.
-- - The format code 113 corresponds to 'dd MMM yyyy' in SQL Server.

-- Section 4: Handling Unix Epoch Time
-- Convert Epoch time (1706303400) to a readable date
SELECT 
    DATEADD(SECOND, 1706303400, '1970-01-01') AS ConvertedEpochDate;

-- Section 5: Handling Excel Serial Dates
-- Convert Excel serial date (45000) to a readable date
SELECT 
    DATEADD(DAY, 45000.52, '1900-01-01') AS ConvertedExcelDate;

-- Section 6: Handling Partial Dates
-- Example 1: Default to a specific year (e.g., 2024)
SELECT 
    CAST('Oct 25' + ' 2024' AS DATE) AS CompleteDate;

-- Example 2: Append the current year dynamically
SELECT 
    CAST('Oct 31 ' + CAST(YEAR(GETDATE()) AS VARCHAR) AS DATE) AS CompleteDateDynamic;

-- Example 3: Extract Month and Day for recurring dates
SELECT 
    YEAR(CAST('Oct 25 2024' AS DATE)) AS Year,
    MONTH(CAST('Oct 25 2024' AS DATE)) AS Month,
    DAY(CAST('Oct 25 2024' AS DATE)) AS Day;

-- Bonus Section: Identifying Date Formats
-- Example of testing large and small numbers
-- Epoch time test
SELECT 
    DATEADD(SECOND, 1706303400, '1970-01-01') AS ConvertedEpochTestDate;

-- Excel serial date test
SELECT 
    DATEADD(DAY, 45000, '1900-01-01') AS ConvertedExcelTestDate;


-- Bonus Section: Identifying Date Formats
-- Example of testing large and small numbers
-- Epoch time test
SELECT 
    DATEADD(SECOND, 1706303400, '1970-01-01') AS DateAddEpochTestDate
 --,cast(1706303400 as datetime) ConvertDate;

-- Excel serial date test
SELECT 
    DATEADD(DAY, 45355.5, '1900-01-01') AS ConvertedExcelTestDate
    , convert(datetime, 45355.75 ) Convert_date;

 
