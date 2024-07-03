create database project;
use project;
create table Admin( AdminID INT NOT NULL PRIMARY KEY UNIQUE,
					PassID VARCHAR(50) NOT NULL);
    

create table Address( AddressID int UNIQUE PRIMARY KEY NOT NULL,
					Street VARCHAR(50),
                    City VARCHAR(50),
                    State VARCHAR(50),
                    Country VARCHAR(50));

create table Customer( CustomerID INT NOT NULL PRIMARY KEY UNIQUE auto_increment,
					Name VARCHAR(50) NOT NULL,
                    Age INT NOT NULL ,
                    PassID VARCHAR(50) NOT NULL,
                    Phone BIGINT NOT NULL,
                    AddressID INT,
                    foreign key(AddressID) references Address(AddressID)
                    );


create table Supplier( SupplierID INT NOT NULL PRIMARY KEY UNIQUE auto_increment,
					Name VARCHAR(50) NOT NULL,
                    Age INT NOT NULL ,
                    PassID VARCHAR(50) NOT NULL,
                    Phone BIGINT NOT NULL,
                    AddressID INT,
                    foreign key(AddressID) references Address(AddressID)
                    );



create table DeliveryAgent( DeliveryAgentID INT NOT NULL PRIMARY KEY auto_increment,
					Name VARCHAR(50) NOT NULL,
					Availability bool default true,
                    PassID VARCHAR(50) NOT NULL,
                    Phone bigint NOT NULL
                    );
			
create table Product( ProductID INT NOT NULL PRIMARY KEY auto_increment,
					Description varchar(100),
					Name VARCHAR(50) NOT NULL,
                    Price INT,
                    Quantity INT);

create table Order_ ( OrderID INT NOT NULL PRIMARY KEY auto_increment,
					CustomerID INT,
                    SupplierID INT,
                    Price INT,
                    Quantity INT,
                    EstArrivalTime DATE,
                    foreign key(SupplierID) references Supplier(SupplierID),
                    foreign key(CustomerID) references Customer(CustomerID)
                    );
  
create table Product_Info(ProductID int PRIMARY KEY auto_increment,
				Description varchar(100) not null,
                foreign key(ProductID) references Product(ProductID));
                
create table Product_Review ( ReviewID INT NOT NULL PRIMARY KEY auto_increment,
					CustomerID INT,
                    ProductID INT,
                    foreign key(CustomerID) references Customer(CustomerID),
                    foreign key(ProductID) references Product(ProductID),
                    Star INT CHECK (Star >= 0 and Star <= 5),
                    Posted_Date Date ,
                    Content VARCHAR(70)
                    );
                    
-- tables from here will be updated according to the usage  
-- not relevant to add dummy data  from here                  
				
CREATE TABLE Deliver (
    DeliveryID INT AUTO_INCREMENT PRIMARY KEY,
    DeliveryAgentID INT,
    CustomerID INT,
    ProductID INT,
    DeliveryDate DATETIME,
    FOREIGN KEY (DeliveryAgentID) REFERENCES DeliveryAgent(DeliveryAgentID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

         

create table Cart ( CustomerID int,
					ProductID int,
                    Quantity int,
                    foreign key(ProductID) references Product(ProductID),
                    foreign key(CustomerID) references Customer(CustomerID),
                    primary key(CustomerID,ProductID));
  
create table Sells ( SupplierID int,
					ProductID int,
                    foreign key(SupplierID) references Supplier(SupplierID),
                    foreign key(ProductID) references Product(ProductID),
                    primary key(SupplierID,ProductID));
          
-- supplier sold to the store 
create table Sold ( SupplierID int,
					ProductID int,
                    SellingDate datetime,
                    Quantity int,
                    foreign key(SupplierID) references Supplier(SupplierID),
                    foreign key(ProductID) references Product(ProductID),
                    primary key(SupplierID,ProductID,SellingDate)
                    );
              
-- customer purchases from the store
create table Purchase (
						CustomerID int,
                        ProductID int,
                        PurchaseDate datetime,
                        Quantity int,
                        SupplierID int,
                        foreign key(ProductID) references Product(ProductID),
                        foreign key(CustomerID) references Customer(CustomerID),
                        foreign key(SupplierID) references Supplier(SupplierID),
                        primary key(CustomerID,ProductID,PurchaseDate)
                        );

