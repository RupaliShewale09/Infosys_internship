CREATE DATABASE online_bookstore;

USE online_bookstore;

CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200),
    author VARCHAR(200),
    description TEXT,
    copies INT,
    price FLOAT
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    total_amount FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    book_id INT,
    qty INT,
    price FLOAT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);


CREATE TABLE carts (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    book_id INT,
    qty INT,
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);
