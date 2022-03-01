-- CREATE TABLE products (FOREIGN KEY (User_id) REFERENCES user(User_id), Date TEXT NOT NULL, Title TEXT NOT NULL PRIMARY KEY, Price TEXT NOT NULL); 

 -- INSERT INTO products (User_id, Date, Title, Price)
 -- VALUES("01", "14-02-2022", "Cream", "14");





-- CREATE TABLE users (User_id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT NOT NULL, hash TEXT NOT NULL); 
-- INSERT INTO users (User_id, Username, hash)
-- VALUES("01", "lu", "1" );

-- DELETE TABLE users;


--DELETE FROM products
--WHERE User_id="6";

-- ALTER TABLE products
-- ADD Url TEXT;