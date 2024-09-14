--create schema code_challenge;

CREATE TABLE code_challenge.customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    customer_address VARCHAR(200),
    customer_city VARCHAR(50),
    customer_state VARCHAR(50),
    customer_zip VARCHAR(10),
    customer_country VARCHAR(50),
    registration_date DATE
);

CREATE TABLE code_challenge.orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_total DECIMAL(10, 2),
    order_status VARCHAR(50),
    shipping_address VARCHAR(200),
    shipping_city VARCHAR(50),
    shipping_state VARCHAR(50),
    shipping_zip VARCHAR(10),
    shipping_country VARCHAR(50) 
);

CREATE TABLE code_challenge.order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),
    product_category VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2) 
);
