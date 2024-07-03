from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'project'
mysql = MySQL(app)

#global variable
#login details 
# Current logic for adding items 
# whenever the add to the cart is placed 
# it will add the items to the cart not handling the request regarding multiple items beign added
custID = 0
custVar = False
sellID = 0
sellVar = False
searchItems = ""

@app.route('/login', methods=['POST', 'GET'])
def helloworld():
    global custID, custVar
    message = ""  # Initialize the message variable
    variable = False
    if request.method == "POST":
        enteredDetails = request.form
        phone = enteredDetails.get('Phone')
        password = enteredDetails.get('Password')
        if phone and password:  
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Customer WHERE Phone = %s AND PassID = %s", (phone, password))
            records = cur.fetchall()
            
            if not records:
                message = "Either Phone or Password is incorrect"
                variable = True
            else:
                message = "Login Successful"
                variable = False
                custID = records[0][0]
                custVar = True
                return redirect(url_for('homePageCustomer'))    
        else:
            message = "Please provide both Phone and Password"
    return render_template("login.html", message=message,variable= variable)


@app.route('/', methods=['POST', 'GET'])
@app.route('/home',methods=['POST','GET'])
def homePageCustomer():
    global searchItems,product,mostSelledItems
    cur = mysql.connection.cursor()
    cur.execute("select c.ProductID, p.Name, i.Description, p.Price from Purchase as c join Product as p join Product_Info as i on c.ProductID = p.ProductID and i.ProductID = c.ProductID group by c.ProductID order by sum(c.Quantity) desc limit 3;")
    mostSelledItems = cur.fetchall()
    cur.execute("select p.ProductId,p.Name,i.Description,p.price from Product as p join Product_Info as i on i.ProductID = p.ProductID order by Name limit 20;")
    product = cur.fetchall()
    if request.method == "POST":
        enteredDetails = request.form
        searchItems = enteredDetails['searhingItems']
        if(searchItems != ""):
            return redirect(url_for('searchPage'))    
    return render_template("home.html",custID= custID,custVar= custVar,mostSelledItems = mostSelledItems,product = product)


@app.route('/products',methods=['POST','GET'])
def productPage():
    entry = 30
    page = request.args.get('page', 1, type=int) 
    offset = (page - 1) * entry
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.ProductId, p.Name, i.Description, p.price FROM Product AS p JOIN Product_Info AS i ON i.ProductID = p.ProductID ORDER BY Name LIMIT %s OFFSET %s", (entry, offset))
    product = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM Product")
    total_entries = cur.fetchone()[0]
    total_pages = (total_entries + entry - 1) // entry

    return render_template("allProduct.html", custID=custID, custVar=custVar, product=product, page=page, total_pages=total_pages)


@app.route('/searchProduct', methods=['GET', 'POST'])
def searchPage():
    global searchItems
    if request.method == "POST":
        enteredDetails = request.form
        searchItems = enteredDetails['searhingItems']
        if searchItems != "":
            return redirect(url_for('searchResults'))  # Redirect to a different route for search results
    return render_template('searchProduct.html', searchItems=searchItems, results=[])

@app.route('/searchResults', methods=['GET', 'POST'])
def searchResults():
    global searchItems,custVar
    if searchItems != "":
        searchItem = searchItems
        searchItems = ""
        cur = mysql.connection.cursor()
        cur.execute("SELECT p.ProductId, p.Name, i.Description, p.price, t.AverageRating FROM Product AS p JOIN Product_Info AS i ON i.ProductID = p.ProductID JOIN (SELECT P.ProductID, IFNULL(AVG(D.Star), 0) AS AverageRating FROM Product AS P LEFT JOIN Product_Review AS D ON D.ProductID = P.ProductID GROUP BY P.ProductID) AS t ON t.ProductID = p.ProductID WHERE p.Name = %s ORDER BY p.Name;", (searchItem,))
        results = cur.fetchall()
        print(len(results))
        return render_template('searchProduct.html',custVar = custVar, searchItems=searchItem, results=results)
    else:
        return render_template('searchProduct.html',custVar = custVar, searchItems="", results=[])

@app.route('/product/<int:product_id>',methods=['GET','POST'])
def product_details(product_id):
    print(product_id)
    global custVar
    cur = mysql.connection.cursor()
    cur.execute("select p.Price,p.Name,p.SupplierID,s.Name,i.Description from Product as p join Supplier as s on p.SupplierID = s.SupplierID join Product_Info as i on i.ProductID = p.ProductID where p.ProductID = %s;",(product_id,))
    result = cur.fetchall()
    cur.execute("select c.Name,p.Posted_Date,p.Star,p.Content from Product_Review as p join Customer as c on c.CustomerID = p.CustomerID where p.ProductID = %s;",(product_id,))
    productComments = cur.fetchall()
    cur.execute("CREATE TEMPORARY TABLE IF NOT EXISTS temp_result AS SELECT p2.Price, p2.Name, p2.SupplierID, s2.Name AS SupplierName, i2.Description, p2.ProductID FROM Product AS p2 JOIN Supplier AS s2 ON p2.SupplierID = s2.SupplierID JOIN Product_Info AS i2 ON i2.ProductID = p2.ProductID;")
    cur.execute("CREATE TEMPORARY TABLE IF NOT EXISTS temp1_result AS SELECT p2.Price, p2.Name, p2.SupplierID, s2.Name AS SupplierName, i2.Description, p2.ProductID FROM Product AS p2 JOIN Supplier AS s2 ON p2.SupplierID = s2.SupplierID JOIN Product_Info AS i2 ON i2.ProductID = p2.ProductID WHERE p2.ProductID = %s;", (product_id,))
    cur.execute("SELECT t1.Name AS Name1,t1.Price AS Price1, t1.ProductID AS ProductID, t1.SupplierID FROM temp_result AS t1 JOIN temp1_result AS t2 ON t1.Name = t2.Name AND t1.ProductID != t2.ProductID;")
    similar_products = cur.fetchall()  
    return render_template('Product.html',custVar = custVar,ProductID = product_id,Price = result[0][0],ProductName = result[0][1],SupplierID = result[0][2],SupplierName = result[0][3],ProductDescription = result[0][4],productComments = productComments,similar_products = similar_products) 
    
@app.route('/addToCart/<int:ProductID>',methods=['GET','POST'])
def add_to_cart(ProductID):
    global custID
    if request.method == 'POST':
        # Get the product name and quantity from the form submission
        cur = mysql.connection.cursor()
        cur.execute("select * from Cart where ProductID = %s and CustomerID =%s" , (ProductID,custID))
        records = cur.fetchall()
        print(len(records))
        if len(records) == 1:
            cur.execute("UPDATE Cart SET quantity = quantity + 1 WHERE ProductID = %s;",(ProductID,))
        else:
            cur.execute("INSERT INTO Cart (CustomerID, ProductID, Quantity) VALUES (%s, %s, 1);",(custID,ProductID))
        
        mysql.connection.commit() 
        print(ProductID)
        cur.close()  
        return redirect(url_for('homePageCustomer'))
     

@app.route('/consumer_profile',methods=['GET','POST'])
def CustomerProfile():
    # Assuming you have data to populate the customer details
    global custVar,custID
    cur = mysql.connection.cursor()
    cur.execute("select Name,Phone from Customer where CustomerID=%s",(custID,))
    data = cur.fetchall()
    customer_name = data[0][0]
    customer_phone = data[0][1]
    return render_template("customer.html", custVar = custVar,CustomerName=customer_name, CustomerPhone=customer_phone)

@app.route('/orders',methods=['GET','POST'])
def orders():
    # Endpoint for displaying the ordered items
    global custID,custVar
    cur = mysql.connection.cursor()
    cur.execute("SELECT c.ProductID, p.Name, c.SupplierID, SUM(c.Quantity) AS TotalQuantity, DATE(c.PurchaseDate) AS PurchaseDate FROM Purchase AS c JOIN Product AS p ON p.ProductID = c.ProductID JOIN Order_ AS o ON o.CustomerID = c.CustomerID WHERE c.CustomerID = %s AND o.EstArrivalTime > NOW() GROUP BY DATE(c.PurchaseDate), c.ProductID, p.Name, c.SupplierID ORDER BY DATE(c.PurchaseDate) DESC;",(custID,))
    records = cur.fetchall()
    return render_template("order.html",custVar = custVar,results = records)

@app.route('/logout',methods=['GET','POST'])
def logout():
    # Endpoint for displaying the ordered items
    global custID,custVar
    cur = mysql.connection.cursor()
    custID = 0
    custVar = False
    return redirect(url_for('homePageCustomer'))


@app.route('/OrderingItems',methods=['GET','POST'])
def OrderingItems():
    # Endpoint for displaying the ordered items
    global custID
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("delete from Cart where CustomerID = %s;",(custID,))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('CustomerProfile'))

@app.route('/track_order',methods=['GET','POST'])
def track_order():
    # Endpoint for tracking orders
    global custVar,custID
    cur = mysql.connection.cursor()
    cur.execute("select c.ProductID,p.Name,c.SupplierID,c.Quantity,o.EstArrivalTime from Purchase as c join Product as p on p.productID = c.productID join order_ as o on o.CustomerID = c.CustomerID where c.customerID = %s and o.EstArrivalTime >= NOW();",(custID,))
    records = cur.fetchall()
    cur.close()
    return render_template("track_order.html",custVar = custVar,results =records)

@app.route('/cart',methods=['GET','POST'])
def visitCart():
    global custVar,custID
    cur = mysql.connection.cursor()
    cur.execute("select c.ProductID,p.Name,p.Price,c.Quantity from Cart as c join Product as p on p.productID = c.productID where c.customerID = %s;",(custID,))
    results = cur.fetchall()
    return render_template("cart.html",custVar = custVar,results = results)


# seller view
@app.route('/SellerLog', methods =['GET','POST'])
def loginSeller():
    global sellID, sellVar
    message = ""  # Initialize the message variable
    variable = False
    if request.method == "POST":
        enteredDetails = request.form
        phone = enteredDetails.get('Phone')
        password = enteredDetails.get('Password')
        if phone and password:  
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Supplier WHERE Phone = %s AND PassID = %s", (phone, password))
            records = cur.fetchall()
            
            if not records:
                message = "Either Phone or Password is incorrect"
                variable = True
            else:
                message = "Login Successful"
                variable = False
                sellID = records[0][0]
                sellVar = True
                return redirect(url_for('homePageSeller'))    
        else:
            message = "Please provide both Phone and Password"
    return render_template("loginSeller.html", message=message,variable= variable)
    
@app.route('/SellerHome',methods=['POST','GET'])
def homePageSeller():
    global sellVar,sellID
    cur = mysql.connection.cursor()
    cur.execute("select Name,Phone from Supplier where SupplierID=%s",(sellID,))
    data = cur.fetchall()
    SellerName = data[0][0]
    SellerPhone = data[0][1]
    return render_template("Seller.html", sellVar = sellVar,SellerName=SellerName, SellerPhone=SellerPhone)
    
@app.route('/SellerProducts',methods=['POST','GET'])
def yourProduct():
    global sellVar,sellID
    cur = mysql.connection.cursor()
    cur.execute("select p.ProductID,p.Name,p.Price,p.Quantity from product as p join sold as s on s.SupplierID = p.SupplierID and s.ProductID = p.ProductID where s.SupplierID = %s order by s.SellingDate desc;",(sellID,))
    data = cur.fetchall()   
    return render_template("supplierProduct.html", sellVar = sellVar,results = data)

@app.route('/SellerLogout',methods=['POST','GET'])
def sellerLogout():
    global custID,custVar
    cur = mysql.connection.cursor()
    custID = 0
    custVar = False
    sellID = 0
    sellVar = False
    return redirect(url_for('homePageCustomer'))
    
@app.route('/SellerSoldHistory',methods=['POST','GET'])
def soldHistory():
    global sellVar,sellID
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.ProductID, pr.Name, SUM(p.Quantity) AS TotalProductSold FROM purchase AS p JOIN product AS pr ON pr.ProductID = p.ProductID where pr.SupplierID = %s GROUP BY p.ProductID, pr.Name, pr.Price;",(sellID,))
    data = cur.fetchall()   
    return render_template("soldHistory.html", sellVar = sellVar,results = data)
  
@app.route('/SellerAddItems', methods=['POST', 'GET'])
def addItems():
    global sellVar, sellID
    if request.method == 'POST':
        product_name = request.form.get('Name')
        product_description = request.form.get('info')
        product_quantity = request.form.get('Quantity')
        product_price = request.form.get('Price')
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Product (SupplierID, Name, Quantity, Price) VALUES ( %s, %s, %s, %s);",
                    (sellID, product_name, product_quantity, product_price))
        mysql.connection.commit()
        cur.execute("SELECT LAST_INSERT_ID();")
        product_id = cur.fetchone()[0]

        cur.execute("INSERT INTO product_info (ProductID, Description) VALUES (%s, %s);",
                    (product_id, product_description))
        
        
        SellingDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert into sold table
        cur.execute(f"INSERT INTO sold (SupplierID, ProductID, SellingDate, Quantity) VALUES ({sellID}, {product_id}, '{SellingDate}', {product_quantity});")
        mysql.connection.commit()
        return redirect(url_for('homePageSeller'))
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name, Phone FROM Supplier WHERE SupplierID=%s", (sellID,))
    data = cur.fetchall()
    SellerName = data[0][0]
    SellerPhone = data[0][1]
    
    return render_template("addProduct.html", sellVar=sellVar, SellerName=SellerName, SellerPhone=SellerPhone)


#Register as Supplier
#Register as Customer
@app.route('/Register', methods=['POST', 'GET'])
def register_user():
    global custID, custVar, sellID, sellVar
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['Name']
        age = request.form['Age']
        password = request.form['PassID']
        phone = request.form['Phone']
        street = request.form['Street']
        city = request.form['City']
        state = request.form['State']
        country = request.form['Country']
        
        # Initialize the cursor
        cur = mysql.connection.cursor()
        
        cur.execute("Select * from Address;")
        result = cur.fetchall()
        address_id = len(result) + 1
        # Insert address data into the Address table
        cur.execute("INSERT INTO Address (AddressID, Street, City, State, Country) VALUES (%s, %s, %s, %s, %s);",
                    (address_id,street, city, state, country))
        
        # Commit the transaction
        mysql.connection.commit()
        
        # Close the cursor
        cur.close()
        
        if role == 'customer':
            # Initialize a new cursor
            cur = mysql.connection.cursor()
            
            # Insert customer data into the Customer table
            cur.execute("INSERT INTO Customer (Name, Age, PassID, Phone, AddressID) VALUES (%s, %s, %s, %s, %s);",
                        (name, age, password, phone, address_id))
            
            # Retrieve the last inserted customer ID
            cur.execute("SELECT LAST_INSERT_ID();")
            customer_id = cur.fetchone()[0]
            
            # Set session variables
            custVar = True
            custID = customer_id
            
            # Commit the transaction
            mysql.connection.commit()
            
            # Close the cursor
            cur.close()
            
            return redirect(url_for('homePageCustomer'))
        
        elif role == 'supplier':
            # Initialize a new cursor
            cur = mysql.connection.cursor()
            
            # Insert supplier data into the Supplier table
            cur.execute("INSERT INTO Supplier (Name, Age, PassID, Phone, AddressID) VALUES (%s, %s, %s, %s, %s);",
                        (name, age, password, phone, address_id))
            
            # Retrieve the last inserted supplier ID
            cur.execute("SELECT LAST_INSERT_ID();")
            sellID = cur.fetchone()[0]
            
            # Set session variable
            sellVar = True
            
            # Commit the transaction
            mysql.connection.commit()
            
            # Close the cursor
            cur.close()
            
            return redirect(url_for('homePageSeller'))
        
    return render_template('Register.html')


if __name__ == "__main__":
    app.run(debug=True)
