Create view staging.vwContent_Ideas as
Select 
Case when audience_appeal like '%SMB%' then 1 else 0 end as SMB_AUDIENCE,
CASE WHEN AUDIENCE_APPEAL LIKE '%data engineer%' then 1 else 0 end as DE_AUDIENCE,
CASE when AUDIENCE_APPEAL LIKE '%data engineer%' AND  audience_appeal like '%SMB%' then 1 else 0 end as COMBINED_AUDIENCE,
* from staging.content_ideas














with user_state AS (Select * 
                        from staging.sqenix_mmo_cust_2
                        where state = 'CA'),

AVG_MONTHLY_REV AS (SELECT AVG(CAST(MONTHLY_REVENUE AS FLOAT)) AVG_MO_REV FROM staging.SQENIX_MMO_CUST_2)

SELECT 
ROW_NUMBER() OVER (ORDER BY USER_ID) ROW_NUM,
ROUND(AVG_MO_REV,2) AVG_MO_REV,
ROUND((AVG_MO_REV - CAST(MONTHLY_REVENUE AS float)),2) VARIANCE_TO_AVG,
* 
FROM USER_STATE US, AVG_MONTHLY_REV AMR







SELECT * from staging.SQENIX_MMO_CUST_2














SELECT  
case when Publisher = Developer then 'Published and Developed By: ' + Publisher 
else 'Developed By: ' + Developer + ' published by: ' + Publisher end as Published_Developed,
ProductID
      ,ProductName
      ,ProductType
      ,Platform
      ,Publisher
      ,Developer
      ,Genre
      ,MSRP
      ,ProductDescription
      ,ReleaseDate
  FROM STAGING.SqEn_Products3

  Select * from staging.CocaColaSales