CREATE DATABASE StockApp;

USE StockApp;


CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username NVARCHAR(100) UNIQUE NOT NULL,
    hashed_password NVARCHAR(200) NOT NULL,
    full_name NVARCHAR(200) NOT NULL,
    date_of_birth DATE,
    email NVARCHAR(255) UNIQUE NOT NULL,
    phone NVARCHAR(20) NOT NULL,
    country NVARCHAR(200),
    quantity_coin DECIMAL(17, 0) NOT NULL,
    quantity_astra DECIMAL(10, 3) NOT NULL
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    order_type NVARCHAR(20),
    direction NVARCHAR(20),
    quantity INT,
    price DECIMAL(18, 4),
    status NVARCHAR(20),
    order_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE stock_price (
    id INT PRIMARY KEY AUTO_INCREMENT,
    time_stamp DATETIME NOT NULL,
    open_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    volume INT
);

CREATE TABLE book_orders (
    book_order_id INT PRIMARY KEY AUTO_INCREMENT,
    quantity_coin DECIMAL(17, 0) NOT NULL,
    quantity_astra DECIMAL(10, 3) NOT NULL,
    order_types NVARCHAR(20),
    status NVARCHAR(20)
);

CREATE TABLE market_transaction (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    book_order_id INT,
    quantity_coin DECIMAL(17, 0) NOT NULL,
    quantity_astra DECIMAL(10, 3) NOT NULL,
    transaction_date DATETIME NOT NULL,
    FOREIGN KEY (book_order_id) REFERENCES book_orders(book_order_id)
);



-- mysql -u root -p -P 3307 -h 127.0.0.1 < /Users/macos/Downloads/WORKSPACE/stock_project/sql/stockApp.sql
