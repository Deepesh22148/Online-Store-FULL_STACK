-- transaction 1
start transaction;

lock tables Product write;
update Product set quantity = quantity + 10 where ProductID = 2;
do sleep(2);
commit;
unlock tables;

select * from Product;


-- transaction 2
start transaction;

lock tables Product write;
update Product set quantity = quantity + 10 where ProductID = 2;
do sleep(2);
commit;
unlock tables;

select * from Product;


-- transaction 3
start transaction;

lock tables deliveryagent write;
update deliveryagent set Availability = 0 where DeliveryAgentID = 
(SELECT p.DeliveryAgentID
FROM deliveryagent AS d 
JOIN deliver AS p ON p.DeliveryAgentID = d.DeliveryAgentID 
WHERE DATE_ADD(p.DeliveryDate, INTERVAL 7 DAY) <= NOW());

commit;
unlock tables; 


-- transaction 4
-- SET SQL_SAFE_UPDATES = 0;

START TRANSACTION;
LOCK TABLES cart WRITE, product WRITE;
INSERT INTO cart (CustomerID, ProductID, Quantity) VALUES (1, 4, 5);
UPDATE product SET Quantity = Quantity - 2 WHERE ProductID = 1;
COMMIT;
UNLOCK TABLES;


select * from Product where ProductID = 1; 
-- Start Transaction 1
start TRANSACTION;
-- Read the current quantity of ProductID 1
SELECT Quantity FROM product WHERE ProductID = 1;
-- Simulate a delay to allow Transaction 2 to start
do sleep(5);
-- Update the quantity of ProductID 1
UPDATE Product SET Quantity = Quantity - 5 WHERE ProductID = 1;
-- Commit Transaction 1
COMMIT;

select * from Product where ProductID = 1; 
start TRANSACTION;
-- Read the current quantity of ProductID 1
SELECT Quantity FROM Product WHERE ProductID = 1;
-- Update the quantity of ProductID 1
UPDATE Product SET Quantity = Quantity + 10 WHERE ProductID = 1;
-- Commit Transaction 2
COMMIT;

select * from Product where ProductID = 1; 


-- conflicted transaction
-- Start Transaction 1
START TRANSACTION;

-- Update the quantity of ProductID 1
UPDATE Product SET Quantity = Quantity - 5 WHERE ProductID = 1;

-- Record the purchase
INSERT INTO Purchase (CustomerID, ProductID, PurchaseDate, Quantity, SupplierID) 
VALUES (1, 1, NOW(), 5, 1);

-- Commit Transaction 1
COMMIT;
-- Start Transaction 2
START TRANSACTION;

-- Update the quantity of ProductID 1
UPDATE Product SET Quantity = Quantity - 3 WHERE ProductID = 1;
-- Record the purchase
INSERT INTO Purchase (CustomerID, ProductID, PurchaseDate, Quantity, SupplierID) 
VALUES (2, 1, NOW(), 3, 1);

-- Commit Transaction 2
COMMIT;
-- Reason::Both transactions are trying to update the Quantity of ProductID = 1 at the
--  same time. Transaction 1 is reducing the quantity by 5, and Transaction 2 is reducing it by 3. 
-- If these updates happen simultaneously, the final state of the Quantity can be different based on
--  which transaction commits first.