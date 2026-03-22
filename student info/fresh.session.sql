CREATE DATABASE IF NOT EXISTS setdb;

USE setdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    university VARCHAR(100),
    class VARCHAR(50),
    age INT,
    mobile VARCHAR(15),
    password VARCHAR(255)
);