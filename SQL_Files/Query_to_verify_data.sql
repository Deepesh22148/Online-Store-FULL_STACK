-- query1 when customer add items to  the cart and viewing their cart
-- for running query we have created a special customer to conduct test
-- (CustomerID, ProductID, Quantity) -> cart
insert into Cart values(301,1,3);
insert into Cart values(301,2,3);

insert into Cart values(301,1,3) on duplicate key update Quantity = Quantity + 3;
insert into Cart values(301,2,3) on duplicate key update Quantity = Quantity + 3;
insert into Cart values(301,3,3) on duplicate key update Quantity = Quantity + 3;
-- Giving product Name and the toatl price
SELECT c.ProductID,
       p.Name AS ProductName,
       c.Quantity,
       p.Price AS UnitPrice,
       c.Quantity * p.Price AS TotalPrice
FROM Cart c
JOIN Product p ON c.ProductID = p.ProductID
where c.CustomerID = 301;


-- query2 when customer purchase the items and and 
-- the order is given to the deleviery agent 
-- information is stored in the sold table between transaction of consumer and supplier
-- as the customer will place order from cart so the data needs to be removed 
-- (SupplierID, ProductID, SellingDate, Quantity) -> Sold
-- (CustomerID, SupplierID, Price, Quantity, EstArrivalTime) ->Order_

-- Adding the Cart items into Order_ Table
insert into Order_ (CustomerID, SupplierID, Price, Quantity, EstArrivalTime)
select Cart.CustomerID, Product.SupplierID, Product.Price, Cart.Quantity, CURDATE() + INTERVAL 7 DAY
from Cart
join Product on Cart.ProductID = Product.ProductID
where Cart.CustomerID = 301;

-- Update the Quantity of that items for each items present in cart
update Product
set Quantity = Quantity - (
    select Quantity
    from Cart
    where Cart.CustomerID = 301
      and Cart.ProductID = Product.ProductID
)
where exists (
    select 1
    from Cart
    where Cart.CustomerID = 301
      and Cart.ProductID = Product.ProductID
);

-- Updating the sold table
insert into Sold (SupplierID, ProductID, SellingDate, Quantity) 
select Product.SupplierID,Cart.ProductID,curdate(),Cart.Quantity 
from Product join Cart on Cart.ProductID = Product.ProductID 
where Cart.CustomerID = 301;

-- Deleting the cart items of the particular customerID
delete from Cart where CustomerID = 301;

-- Updating Purchase table
insert into Purchase (CustomerID) values (301);

select * from Order_ where CustomerID = 1;
select * from Sold;


-- Query 3 Assigning the Delivery Agent to the Customer and updating its availability 

set @DeliveryAgentID := (
    select DeliveryAgentID
    from DeliveryAgent
    where Availability = true
    limit 1
);

update DeliveryAgent
SET Availability = false
WHERE DeliveryAgentID = @DeliveryAgentID;

INSERT INTO Deliver (DeliveryAgentID, CustomerID)
VALUES (@DeliveryAgentID, 301);

select * from DeliveryAgent where DeliveryAgentID = @DeliveryAgentID;

-- query4 when supplier place items in our database
-- Assuming it is some unique product for better clarity
INSERT INTO Product (SupplierID, Name, Price, Quantity)
VALUES (1, 'Example', 10, 100);

SET @LastProductID = LAST_INSERT_ID();
-- Inserting into the Sells table using the retrieved ProductID
INSERT INTO Sells (SupplierID, ProductID)
VALUES (1, @LastProductID);

select * from Sells;
-- query4 when consumer search an items and view other things like product
SET @PartialProductName = 'oo';

-- Retrieve product information and reviews
SELECT
    P.ProductID,
    P.Name AS ProductName,
    PR.ReviewID,
    PR.Star,
    PR.Posted_Date,
    PR.Content
FROM
    Product P
JOIN
    Product_Review PR ON P.ProductID = PR.ProductID
WHERE
	P.Name LIKE CONCAT('%', @PartialProductName, '%');
    
-- query5 for when supplier search their most selled items are to increase their product
SELECT
    SupplierID,
    ProductID,
    MAX(Quantity) AS MaxQuantitySold
FROM
    Sold
GROUP BY
    SupplierID, ProductID
ORDER BY
    MaxQuantitySold DESC;
    
-- query6 to update the status when the product is delivered
SELECT
    P.PurchaseID,
    P.CustomerID,
    O.OrderID,
    O.SupplierID,
    O.Price,
    O.Quantity,
    O.EstArrivalTime
FROM
    Purchase P
JOIN
    Order_ O ON P.CustomerID = O.CustomerID
WHERE
    P.CustomerID = 301;

-- query8 when supplier wants to remove some product thus cancelling all the order for the same item number
SELECT DISTINCT s.SupplierID, s.Name
FROM Supplier s
JOIN Sold so ON s.SupplierID = so.SupplierID
WHERE so.SellingDate IS NULL OR so.SellingDate < CURDATE() - INTERVAL 1 YEAR;

-- query9 Supplier wants to view their average income generated from this portal
SELECT
    Sold.SupplierID,
    AVG(Sold.Quantity * Product.Price) AS AverageIncome
FROM
    Sold
JOIN
    Product ON Sold.ProductID = Product.ProductID
GROUP BY
    Sold.SupplierID;
-- query10 Consumer wants to view their cart and increase the quantity

