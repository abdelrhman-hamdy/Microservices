CREATE USER IF NOT EXISTS 'auth_user'@'%' IDENTIFIED BY "root" ;

CREATE DATABASE IF NOT EXISTS auth; 

GRANT ALL PRIVILEGES ON  auth.* TO  'auth_user'@'%';  

USE auth;

CREATE TABLE IF NOT EXISTS user (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR (255) NOT NULL
);


INSERT IGNORE INTO user (ID,email, Password) VALUES (1,'hamdy@gmail.com','root'); 