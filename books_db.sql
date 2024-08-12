create database books;
use books;

create table Book(
book_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
title varchar(255),
author varchar(255),
price float(5,2),
stock float(5,2)
);

CREATE TABLE users (
  user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  address VARCHAR(255),
  phonenumber VARCHAR(20)
);

CREATE TABLE orders (
  order_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  ordertotal FLOAT,
  paymentmethod ENUM('...'),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

ALTER TABLE orders
MODIFY paymentmethod ENUM('Cash','UPI', 'Net Banking', 'Credit Card', 'Debit Card');

CREATE TABLE orderitems (
  order_id INT NOT NULL,
  item_name VARCHAR(255) NOT NULL,
  quantity INT,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
select * from users;
select * from orders;
select * from orderitems;
select * from book;
drop table book;
SET SESSION sql_mode = '';