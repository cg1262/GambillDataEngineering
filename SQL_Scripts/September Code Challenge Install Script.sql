--create schema code_challenge; 
CREATE TABLE code_challenge.customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(max),
    customer_phone VARCHAR(max),
    customer_address VARCHAR(max),
    customer_city VARCHAR(max),
    customer_state VARCHAR(max),
    customer_zip VARCHAR(max),
    customer_country VARCHAR(max),
    registration_date DATE
);


CREATE TABLE code_challenge.orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_total DECIMAL(10, 2),
    order_status VARCHAR(50),
    shipping_address VARCHAR(max),
    shipping_city VARCHAR(max),
    shipping_state VARCHAR(max),
    shipping_zip VARCHAR(10),
    shipping_country VARCHAR(max) 
);

CREATE TABLE code_challenge.order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    product_name VARCHAR(max),
    product_category VARCHAR(max),
    quantity INT,
    unit_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2) 
);

--Insert data from staging to code_challenge tables
insert into code_challenge.customers select * from staging.customers_cc;
insert into code_challenge.orders select * from staging.orders_cc;
insert into code_challenge.order_items select * from staging.order_items_cc;
select * from staging.customers_cc;