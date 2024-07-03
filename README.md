# Introduction

Our project aims to build a comprehensive database management system for an online retail store specializing in electronics and related consumer goods. This system will focus exclusively on the online platform, excluding any physical store operations. The scope of the project includes the management of products, user profiles, procurement of electronic goods from suppliers, and inventory control. The database application will also assist in the administration of item distribution, which encompasses both orders placed by users and stock replenishment orders. By concentrating solely on the online platform, the implementation of the database system remains precise and manageable. The design separates back-end functions into distinct entities, such as inventory, distribution, and procurement, ensuring a modular architecture that enhances scalability and maintainability. The code provided implements key functionalities for customers and sellers, such as login and registration, product viewing and searching, cart management, order tracking, and profile management, aligning with the project's goals to create a robust and user-friendly online retail experience.

# Features Implemented

**Login Page**
Users can choose to log in or register as a Customer or log in as an Admin. For customers, selecting "Customer" offers the option to either log in or register. If they choose to register, they are redirected to a form to create an account. If they opt to log in, they can enter their credentials using either their phone number or email ID. Admins, on the other hand, select "Admin" to log in.

**Customer Home Page**
Once logged in, customers are presented with several options: "View Products", "View Cart", "My Wishlist", "Customer Profile", "Edit Profile", "Order History", and "Logout". These options are accessible via a navigation bar on the left side of the screen.

In the "View Products" section, customers can search for products using keywords. The search results display relevant products, and clicking "View Details" provides comprehensive information about the product, including its description, price, rating, and reviews. Customers can also add products to their cart or wishlist from this page.

The "View Cart" section allows customers to view and edit the quantities of items in their cart. They can place orders if the quantities in the cart match the available inventory. After placing an order, the items in the cart are removed.

In the "My Wishlist" section, customers can view products they have added to their wishlist, along with the date each item was added.

The "Customer Profile" section displays the customer's details, including name, contact number, email, and addresses. Customers can edit their profile information in the "Edit Profile" section, choosing which fields to update via a dropdown menu.

The "Order History" section provides a record of the customer's previously purchased products, including the quantities purchased and the dates of the last purchase.

**Seller Home Page**
Once logged in, sellers are presented with several options: "View Products", "Add Product", "Manage Inventory", "View Orders", "Seller Profile", "Edit Profile", and "Logout". These options are accessible via a navigation bar on the left side of the screen.

In the "View Products" section, sellers can see the products they have listed for sale. They can also view detailed information about each product and manage their listings.

The "Add Product" section allows sellers to add new products to their listings. They can provide details such as product name, description, price, and quantity.

In the "Manage Inventory" section, sellers can update product quantities and remove products from their listings.

The "View Orders" section displays all orders placed for the seller's products, including order details and customer information.

The "Seller Profile" section shows the seller's details, such as name, contact information, and business address. Sellers can update this information in the "Edit Profile" section.

This structured approach ensures that customers, sellers, and admins each have tailored features and functionalities to enhance their experience and streamline the management of the online retail store.


# Instructions to Run
To run this application, run all the SQL files to create the necessary tables required for this prototype
and then navigate to the Customer.py file and change the password to your local SQL password at line 9
and then run the following commands:
 
 .\env\Scripts\activate.ps1
 
 python python Customer.py
