-- Triggers
-- Triggers for updating items to the cart
-- Drop the existing trigger if it exists
-- Drop the existing trigger if it exists
-- Drop the existing trigger if it exists
DROP TRIGGER IF EXISTS Add_To_Cart;

-- Recreate the trigger with updated logic
DELIMITER //
CREATE TRIGGER Add_To_Cart
BEFORE INSERT ON Cart
FOR EACH ROW
BEGIN
    -- Check if the combination of CustomerID and ProductID already exists in the Cart table
    IF EXISTS (
        SELECT 1 FROM Cart WHERE CustomerID = NEW.CustomerID AND ProductID = NEW.ProductID
    ) THEN
        -- If the combination exists, update the Quantity column
        UPDATE Cart 
        SET Quantity = Quantity + NEW.Quantity
        WHERE CustomerID = NEW.CustomerID AND ProductID = NEW.ProductID;
        
        -- Set NEW.Quantity to 0 to prevent insertion of a new row
        SET NEW.Quantity = 0;
    END IF;
END //
DELIMITER ;

insert into Cart values(301,1,3) on duplicate key update Quantity = Quantity + 2;

select * from Cart;
-- If an item with the same CustomerID and ProductID already exists in the cart,
-- the trigger will automatically update the quantity of the existing item.
-- If not, a new item will be inserted into the cart.

-- Example where the same item is added again
INSERT INTO Cart (CustomerID, ProductID, Quantity) VALUES (301, 102, 3);
 
 
 
