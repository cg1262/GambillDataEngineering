select 
case when Publisher = Developer then 'Published and Developed By: ' Publisher 
else Developer + ' published by: ' + Publisher end Published_Developed
from staging.sqen_products3