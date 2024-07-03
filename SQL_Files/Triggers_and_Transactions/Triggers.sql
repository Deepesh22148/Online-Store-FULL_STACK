
select * from Purchase;
select * from Order_;
select * from DeliveryAgent;
select * from Deliver;
select * from Cart;


DROP TRIGGER updatingOrder;
DROP TRIGGER updatingPurchase;
DROP TRIGGER updatingDeliver;
DROP TRIGGER updatingDeliveryAgent;


DELIMITER //
CREATE TRIGGER updatingOrder
BEFORE DELETE ON Cart
FOR EACH ROW
BEGIN
    INSERT INTO Order_ (CustomerID, SupplierID, Quantity, EstArrivalTime,Price)
    VALUES (OLD.CustomerID, OLD.ProductID, OLD.Quantity, NOW() + INTERVAL 7 DAY,(select Price from Product where ProductID = Old.ProductID));
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER updatingPurchase
BEFORE DELETE ON Cart
FOR EACH ROW
BEGIN
    INSERT INTO Purchase(CustomerID, ProductID,Quantity, PurchaseDate,SupplierID)
    VALUES (OLD.CustomerID,OLD.ProductID,OLD.Quantity,NOW(),(select SupplierID from Product where ProductID = OLD.ProductID));
END//
DELIMITER ;


DELIMITER //

CREATE TRIGGER updatingDeliver
BEFORE DELETE ON Cart
FOR EACH ROW
BEGIN
    DECLARE agent_id INT;

    -- Select a single DeliveryAgentID where Availability is true
    SELECT DeliveryAgentID INTO agent_id
    FROM DeliveryAgent
    WHERE Availability = TRUE
    LIMIT 1;

    -- Insert into Deliver table using the selected DeliveryAgentID
    INSERT INTO Deliver (CustomerID, ProductID, DeliveryAgentID,DeliveryDate)
    VALUES (OLD.CustomerID, OLD.ProductID, agent_id,NOW());
    
END//
DELIMITER ;

DELIMITER //

CREATE TRIGGER updatingDeliveryAgent
After DELETE ON Cart
FOR EACH ROW
BEGIN
	UPDATE DeliveryAgent
    SET Availability = FALSE
    WHERE DeliveryAgentID = (select DeliveryAgentID from Deliver order by DeliveryDate Desc limit 1);
    
END//
DELIMITER ;








select * from Cart;
insert into cart values (1,20,4);
insert into cart values (1,30,4);

delete from Cart where CustomerID = 1;
select * from Purchase order by PurchaseDate Desc;
select * from Order_ where CustomerID = 1 order by EstArrivalTime desc;
select * from Deliver;

select c.ProductID,p.Name,c.SupplierID,c.Quantity from Purchase as c join Product as p on p.productID = c.productID join order_ as o on o.CustomerID = c.CustomerID where c.customerID = 1 and o.EstArrivalTime > NOW();



