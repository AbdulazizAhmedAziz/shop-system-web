# 📋 Software Requirements Specification (SRS)
## نظام المتجر الذكي (Smart Shop System)

**Version:** 1.0  
**Date:** December 11, 2025  
**Author:** Development Team  
**Status:** Approved

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [System Architecture](#5-system-architecture)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [User Stories](#7-user-stories)
8. [Use Cases](#8-use-cases)
9. [Data Model](#9-data-model)
10. [Security Requirements](#10-security-requirements)
11. [Performance Requirements](#11-performance-requirements)
12. [Testing Requirements](#12-testing-requirements)
13. [Deployment Requirements](#13-deployment-requirements)
14. [Appendices](#14-appendices)

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for the Smart Shop System, a web-based e-commerce platform that enables online shopping with advanced features including product management, shopping cart functionality, order processing, and promotional offers.

### 1.2 Scope
The Smart Shop System is designed to:
- Provide a user-friendly web interface for customers to browse and purchase products
- Enable administrators to manage inventory, products, and promotional offers
- Support multiple user roles (Admin and Customer)
- Handle order processing and payment methods
- Implement promotional offers with discounts, gifts, and purchase limits

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS**: Software Requirements Specification
- **UI**: User Interface
- **API**: Application Programming Interface
- **Admin**: Administrator user role
- **Customer**: Regular user role
- **COD**: Cash on Delivery
- **POS**: Point of Sale (Visa on Delivery)

### 1.4 References
- Flask Framework Documentation: https://flask.palletsprojects.com/
- Python 3.11 Documentation: https://docs.python.org/3.11/
- Railway Deployment Guide: https://docs.railway.app/

### 1.5 Overview
This document is organized into sections covering functional requirements, system architecture, user interfaces, and non-functional requirements.

---

## 2. Overall Description

### 2.1 Product Perspective
The Smart Shop System is a standalone web application built using:
- **Backend**: Python 3.11 with Flask framework
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Railway cloud platform
- **Architecture**: Model-View-Controller (MVC) pattern

### 2.2 Product Functions
The system provides the following main functions:
1. User authentication and authorization
2. Product catalog management
3. Shopping cart functionality
4. Order processing
5. Promotional offer management
6. Inventory management
7. Sales reporting

### 2.3 User Classes and Characteristics

#### 2.3.1 Administrator
- **Responsibilities**: Manage products, inventory, offers, and view sales
- **Access Level**: Full system access
- **Default Credentials**: admin/123 or place/123

#### 2.3.2 Customer
- **Responsibilities**: Browse products, add to cart, place orders
- **Access Level**: Limited to shopping features
- **Registration**: Can create new account

### 2.4 Operating Environment
- **Development**: Local machine with Python 3.11
- **Production**: Railway cloud platform
- **Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Operating Systems**: Windows, macOS, Linux (for users)

### 2.5 Design and Implementation Constraints
- Must use Python 3.11+
- Must use Flask framework
- Must be deployable on Railway platform
- Must support RTL (Right-to-Left) for Arabic language
- Must be responsive for mobile devices

### 2.6 Assumptions and Dependencies
- Users have modern web browsers
- Internet connection is available
- Railway platform is operational
- Data is stored in memory (no database required for MVP)

---

## 3. System Features

### 3.1 User Authentication

#### 3.1.1 Login
- **Priority**: High
- **Description**: Users can log in with username and password
- **Input**: Username, Password
- **Output**: Redirect to appropriate dashboard
- **Validation**: 
  - Username and password must match existing account
  - Case-sensitive username

#### 3.1.2 Registration
- **Priority**: High
- **Description**: New customers can create accounts
- **Input**: Username, Password
- **Output**: New user account created, auto-login
- **Validation**:
  - Username must be unique
  - Username cannot be empty
  - Password cannot be empty

#### 3.1.3 Logout
- **Priority**: Medium
- **Description**: Users can log out from the system
- **Output**: Session cleared, redirect to home page

### 3.2 Product Management (Admin)

#### 3.2.1 View Products
- **Priority**: High
- **Description**: Admin can view all products with details
- **Display**: Table format with ID, Name, Price, Stock, Offers

#### 3.2.2 Edit Product
- **Priority**: High
- **Description**: Admin can modify product information
- **Editable Fields**: Name, Price, Stock
- **Validation**:
  - Price must be positive number
  - Stock must be non-negative integer

#### 3.2.3 Manage Offers
- **Priority**: High
- **Description**: Admin can create/modify promotional offers
- **Offer Types**:
  - Discount percentage (0-100%)
  - Free gift (text description)
  - Purchase limit per customer (0 = unlimited)
- **Validation**:
  - Discount must be between 0-100
  - Limit must be non-negative integer

### 3.3 Product Browsing (Customer)

#### 3.3.1 View All Products
- **Priority**: High
- **Description**: Customers can browse all available products
- **Display**: Grid layout with product cards
- **Information Shown**: Name, Price, Stock, Category, Offers

#### 3.3.2 View Offers Only
- **Priority**: Medium
- **Description**: Customers can filter to see only products with offers
- **Filter**: Products with discount > 0 OR gift != null

#### 3.3.3 Product Details
- **Priority**: Medium
- **Description**: Display detailed product information
- **Information**: Name, Category, Price, Stock, Discount, Gift, Limit

### 3.4 Shopping Cart

#### 3.4.1 Add to Cart
- **Priority**: High
- **Description**: Customers can add products to shopping cart
- **Input**: Product ID, Quantity
- **Validation**:
  - Quantity must be positive
  - Quantity cannot exceed available stock
  - If offer limit exists, total quantity in cart cannot exceed limit
- **Output**: Product added to cart, cart count updated

#### 3.4.2 View Cart
- **Priority**: High
- **Description**: Customers can view cart contents
- **Display**: List of items with quantities and prices
- **Information**: Product name, Quantity, Unit price, Total price, Discounts

#### 3.4.3 Remove from Cart
- **Priority**: Medium
- **Description**: Customers can remove items from cart
- **Input**: Product ID
- **Output**: Item removed, cart updated

#### 3.4.4 Calculate Total
- **Priority**: High
- **Description**: System calculates cart total with discounts
- **Calculation**: 
  - Apply discount percentage to each item
  - Sum all item totals
  - Display final total

### 3.5 Checkout Process

#### 3.5.1 Enter Shipping Address
- **Priority**: High
- **Description**: Customer enters delivery address
- **Input**: Address text (optional, default: "استلام من الفرع")
- **Validation**: None (optional field)

#### 3.5.2 Select Payment Method
- **Priority**: High
- **Description**: Customer selects payment method
- **Options**:
  1. Online Payment (immediate payment)
  2. Cash on Delivery (COD)
  3. Visa on Delivery (POS)
- **Output**: Payment method and status set

#### 3.5.3 Process Order
- **Priority**: High
- **Description**: System processes the order
- **Steps**:
  1. Validate cart is not empty
  2. Validate stock availability
  3. Calculate final total
  4. Update product stock
  5. Create order record
  6. Clear shopping cart
  7. Display order confirmation

### 3.6 Order Management

#### 3.6.1 View Orders (Admin)
- **Priority**: Medium
- **Description**: Admin can view all orders
- **Display**: Table with Order ID, Customer, Total, Payment Method, Status, Date

#### 3.6.2 Order Details
- **Priority**: Low
- **Description**: View detailed order information
- **Information**: Items, Quantities, Prices, Discounts, Total

### 3.7 Promotional Offers

#### 3.7.1 Discount Offers
- **Priority**: High
- **Description**: Products can have percentage discounts
- **Calculation**: New Price = Original Price × (1 - Discount%)
- **Display**: Show original price crossed out, new price highlighted

#### 3.7.2 Gift Offers
- **Priority**: Medium
- **Description**: Products can include free gifts
- **Display**: Gift icon with gift name
- **Application**: Shown in product card and invoice

#### 3.7.3 Purchase Limits
- **Priority**: High
- **Description**: Limit quantity per customer for promotional items
- **Validation**: 
  - Check current cart quantity
  - Check remaining limit
  - Prevent exceeding limit
- **Display**: Warning message if limit reached

---

## 4. External Interface Requirements

### 4.1 User Interfaces

#### 4.1.1 Home Page
- **Layout**: Centered welcome card
- **Elements**: 
  - Title: "نظام المتجر الذكي"
  - Two buttons: Admin, Customer
  - Information box with test credentials

#### 4.1.2 Login Page
- **Layout**: Centered form
- **Elements**:
  - Username input field
  - Password input field
  - Login button
  - Link to registration
  - Link to home

#### 4.1.3 Admin Dashboard
- **Layout**: Tabbed interface
- **Tabs**: 
  - Products (Inventory)
  - Offers Management
  - Sales (Orders)
- **Elements**: Data tables, Action buttons, Modals

#### 4.1.4 Customer Dashboard
- **Layout**: Card-based grid
- **Cards**:
  - Browse All Products
  - View Offers Only
  - Shopping Cart
- **Elements**: Navigation buttons, Cart count badge

#### 4.1.5 Products Page
- **Layout**: Responsive grid
- **Elements**: 
  - Product cards
  - Offer badges
  - Add to cart buttons
  - Stock indicators
- **Filters**: All products / Offers only

#### 4.1.6 Shopping Cart Page
- **Layout**: Table + Summary card
- **Elements**:
  - Cart items table
  - Remove buttons
  - Total calculation
  - Checkout button

#### 4.1.7 Checkout Page
- **Layout**: Two-column (form + summary)
- **Elements**:
  - Address textarea
  - Payment method radio buttons
  - Order summary
  - Confirm button

### 4.2 Hardware Interfaces
- **Server**: Railway cloud infrastructure
- **Client**: Standard web browser on any device

### 4.3 Software Interfaces
- **Web Server**: Gunicorn WSGI server
- **Framework**: Flask 3.0.0
- **Python**: 3.11+
- **Deployment**: Railway platform

### 4.4 Communication Interfaces
- **Protocol**: HTTP/HTTPS
- **Port**: Dynamic (set by Railway via PORT environment variable)
- **Format**: HTML, JSON (for API endpoints)

---

## 5. System Architecture

### 5.1 Architecture Overview
The system follows MVC (Model-View-Controller) pattern:

```
┌─────────────┐
│   Client    │ (Browser)
└──────┬──────┘
       │ HTTP/HTTPS
       ▼
┌─────────────────┐
│  Flask Routes    │ (Controller)
└──────┬──────────┘
       │
       ├──► Models (Product, User, Order)
       │
       └──► Views (HTML Templates)
```

### 5.2 Component Structure

#### 5.2.1 Models (Classes)
- **Product**: Product information and offers
- **User**: User accounts and authentication
- **Order**: Order records
- **ShopSystem**: Main controller class

#### 5.2.2 Views (Templates)
- `base.html`: Base template
- `home.html`: Home page
- `login.html`: Login page
- `register.html`: Registration page
- `admin_dashboard.html`: Admin interface
- `customer_dashboard.html`: Customer interface
- `customer_products.html`: Product listing
- `customer_cart.html`: Shopping cart
- `checkout.html`: Checkout page

#### 5.2.3 Controllers (Routes)
- Authentication routes: `/login`, `/register`, `/logout`
- Admin routes: `/admin/dashboard`, `/admin/edit_product`, `/admin/apply_offer`
- Customer routes: `/customer/dashboard`, `/customer/products`, `/customer/cart`, `/customer/checkout`
- API routes: `/api/product/<id>`, `/customer/add_to_cart`

### 5.3 Data Flow

```
User Request → Flask Route → Business Logic → Model Update → Response (HTML/JSON)
```

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements
- **Page Load Time**: < 2 seconds
- **Response Time**: < 500ms for API calls
- **Concurrent Users**: Support at least 50 simultaneous users
- **Database Queries**: N/A (in-memory storage)

### 6.2 Security Requirements
- **Authentication**: Username/password based
- **Session Management**: Flask sessions with secret key
- **Password Storage**: Plain text (for MVP - should be hashed in production)
- **Input Validation**: All user inputs validated
- **CSRF Protection**: Should be implemented in production
- **HTTPS**: Required in production (Railway provides automatically)

### 6.3 Reliability Requirements
- **Uptime**: 99% availability
- **Error Handling**: Graceful error messages
- **Data Backup**: Not implemented (in-memory data)
- **Recovery**: Application restart required for data reset

### 6.4 Usability Requirements
- **Language**: Arabic (RTL support)
- **Responsive Design**: Works on desktop, tablet, mobile
- **Accessibility**: Semantic HTML, clear labels
- **User Feedback**: Flash messages for actions
- **Navigation**: Clear navigation paths

### 6.5 Scalability Requirements
- **Horizontal Scaling**: Supported by Railway
- **Vertical Scaling**: Limited by Railway free tier
- **Data Storage**: In-memory (not scalable - database needed for production)

### 6.6 Maintainability Requirements
- **Code Organization**: Modular structure
- **Documentation**: Code comments, SRS document
- **Version Control**: Git repository
- **Testing**: Manual testing (automated tests recommended)

---

## 7. User Stories

### 7.1 Admin Stories

**US-ADM-001**: As an admin, I want to view all products so that I can monitor inventory.

**US-ADM-002**: As an admin, I want to edit product details so that I can update prices and stock.

**US-ADM-003**: As an admin, I want to create promotional offers so that I can attract customers.

**US-ADM-004**: As an admin, I want to set purchase limits on offers so that I can control inventory.

**US-ADM-005**: As an admin, I want to view all orders so that I can track sales.

### 7.2 Customer Stories

**US-CUS-001**: As a customer, I want to browse products so that I can find items to purchase.

**US-CUS-002**: As a customer, I want to see products with offers so that I can find deals.

**US-CUS-003**: As a customer, I want to add products to cart so that I can purchase multiple items.

**US-CUS-004**: As a customer, I want to see my cart total so that I know how much I'll pay.

**US-CUS-005**: As a customer, I want to checkout so that I can complete my purchase.

**US-CUS-006**: As a customer, I want to choose payment method so that I can pay as preferred.

**US-CUS-007**: As a customer, I want to see discounts applied so that I know I'm getting a deal.

---

## 8. Use Cases

### 8.1 UC-001: Admin Login
- **Actor**: Administrator
- **Precondition**: Admin has valid credentials
- **Main Flow**:
  1. Admin navigates to login page
  2. Enters username and password
  3. System validates credentials
  4. System redirects to admin dashboard
- **Postcondition**: Admin is logged in and can access admin features

### 8.2 UC-002: Customer Registration
- **Actor**: New Customer
- **Precondition**: Customer is not registered
- **Main Flow**:
  1. Customer navigates to registration page
  2. Enters desired username and password
  3. System checks username availability
  4. System creates new account
  5. System auto-logs in customer
  6. System redirects to customer dashboard
- **Postcondition**: Customer account created and logged in

### 8.3 UC-003: Add Product to Cart
- **Actor**: Customer
- **Precondition**: Customer is logged in, product exists
- **Main Flow**:
  1. Customer browses products
  2. Customer clicks "Add to Cart" on a product
  3. System shows quantity selection modal
  4. Customer enters quantity
  5. System validates quantity (stock, limits)
  6. System adds product to cart
  7. System shows success message
- **Alternative Flow 3a**: Quantity exceeds stock → Show error
- **Alternative Flow 3b**: Quantity exceeds offer limit → Show error
- **Postcondition**: Product added to cart

### 8.4 UC-004: Process Order
- **Actor**: Customer
- **Precondition**: Customer has items in cart
- **Main Flow**:
  1. Customer navigates to checkout
  2. Customer enters shipping address
  3. Customer selects payment method
  4. Customer confirms order
  5. System validates cart and stock
  6. System calculates total with discounts
  7. System creates order record
  8. System updates product stock
  9. System clears cart
  10. System shows order confirmation
- **Alternative Flow 4a**: Stock insufficient → Show error, prevent order
- **Postcondition**: Order created, stock updated, cart cleared

### 8.5 UC-005: Admin Create Offer
- **Actor**: Administrator
- **Precondition**: Admin is logged in, product exists
- **Main Flow**:
  1. Admin navigates to Offers tab
  2. Admin clicks "Manage Offer" on a product
  3. Admin enters discount percentage (optional)
  4. Admin enters gift name (optional)
  5. Admin enters purchase limit (optional)
  6. Admin clicks "Apply"
  7. System saves offer to product
  8. System shows success message
- **Postcondition**: Offer applied to product

---

## 9. Data Model

### 9.1 Product Entity
```
Product {
    id: Integer (Primary Key)
    name: String
    price: Float
    stock: Integer
    category: String
    offer_discount: Float (0-100)
    offer_gift: String (nullable)
    offer_limit: Integer (0 = unlimited)
}
```

### 9.2 User Entity
```
User {
    username: String (Primary Key)
    password: String
    role: String ("Admin" | "Customer")
    cart: Array<CartItem>
}

CartItem {
    product: Product
    qty: Integer
}
```

### 9.3 Order Entity
```
Order {
    order_id: Integer (Primary Key)
    customer_name: String
    items_txt: Array<String>
    total: Float
    address: String
    pay_method: String
    pay_status: String
    date: DateTime
}
```

### 9.4 Relationships
- User has many CartItems
- CartItem belongs to one Product
- Order belongs to one User
- Order contains many Products (via items_txt)

---

## 10. Security Requirements

### 10.1 Authentication
- **Method**: Username/password
- **Session**: Flask session management
- **Timeout**: Session expires on browser close
- **Password Policy**: None (for MVP)

### 10.2 Authorization
- **Role-based**: Admin vs Customer
- **Access Control**: Routes protected by role check
- **Default Admin**: admin/123, place/123

### 10.3 Data Protection
- **Input Validation**: All inputs validated
- **SQL Injection**: N/A (no database)
- **XSS Protection**: Template escaping (Flask default)
- **CSRF**: Not implemented (should be added)

### 10.4 Secrets Management
- **Secret Key**: Environment variable (SECRET_KEY)
- **Credentials**: Hardcoded for MVP (should be in database)

---

## 11. Performance Requirements

### 11.1 Response Times
- **Page Load**: < 2 seconds
- **API Response**: < 500ms
- **Cart Update**: < 300ms
- **Checkout**: < 1 second

### 11.2 Throughput
- **Concurrent Users**: 50+ users
- **Requests per Second**: 100+ requests
- **Database Operations**: N/A (in-memory)

### 11.3 Resource Usage
- **Memory**: < 512MB (Railway free tier)
- **CPU**: Minimal (Python/Flask)
- **Storage**: Minimal (no file uploads)

---

## 12. Testing Requirements

### 12.1 Unit Testing
- **Coverage**: Business logic functions
- **Tools**: pytest (recommended)
- **Status**: Not implemented (manual testing)

### 12.2 Integration Testing
- **Scope**: API endpoints, route handlers
- **Status**: Manual testing

### 12.3 System Testing
- **Scenarios**: 
  - User registration and login
  - Product browsing and cart
  - Order processing
  - Admin operations
- **Status**: Manual testing performed

### 12.4 User Acceptance Testing
- **Testers**: End users
- **Scenarios**: All user stories
- **Status**: Pending

---

## 13. Deployment Requirements

### 13.1 Deployment Platform
- **Platform**: Railway
- **URL**: https://railway.app
- **Build**: Automatic from GitHub
- **Runtime**: Python 3.11

### 13.2 Environment Variables
- **PORT**: Set automatically by Railway
- **SECRET_KEY**: Should be set in Railway dashboard

### 13.3 Dependencies
- **Python**: 3.11+
- **Packages**: See requirements.txt
  - Flask==3.0.0
  - Werkzeug==3.0.1
  - gunicorn==21.2.0

### 13.4 Build Process
1. Railway detects Python project
2. Installs dependencies from requirements.txt
3. Runs gunicorn with Procfile command
4. Application starts on assigned PORT

### 13.5 Domain Configuration
- **Default**: Railway provides subdomain
- **Custom**: Can be configured in Railway settings

---

## 14. Appendices

### 14.1 Glossary
- **MVP**: Minimum Viable Product
- **RTL**: Right-to-Left (text direction)
- **WSGI**: Web Server Gateway Interface
- **COD**: Cash on Delivery
- **POS**: Point of Sale

### 14.2 Sample Data
The system comes with 30 pre-loaded products across categories:
- Electronics (8 products)
- Clothing (6 products)
- Home (5 products)
- Sports (4 products)
- Books/Stationery (4 products)
- Travel (2 products)

### 14.3 API Endpoints

#### GET Endpoints
- `/` - Home page
- `/home` - Home page
- `/login` - Login page
- `/register` - Registration page
- `/admin/dashboard` - Admin dashboard
- `/customer/dashboard` - Customer dashboard
- `/customer/products` - Product listing
- `/customer/cart` - Shopping cart
- `/customer/checkout` - Checkout page
- `/api/product/<id>` - Get product info (JSON)

#### POST Endpoints
- `/login` - Process login
- `/register` - Process registration
- `/admin/edit_product` - Update product
- `/admin/apply_offer` - Apply offer
- `/customer/add_to_cart` - Add item to cart
- `/customer/remove_from_cart` - Remove item
- `/customer/checkout` - Process order

### 14.4 Error Codes
- **400**: Bad Request (invalid input)
- **401**: Unauthorized (not logged in)
- **403**: Forbidden (wrong role)
- **404**: Not Found (product/user not found)
- **500**: Internal Server Error

### 14.5 Future Enhancements
1. Database integration (PostgreSQL)
2. User password hashing
3. Email notifications
4. Payment gateway integration
5. Product images
6. Search functionality
7. Product reviews
8. Wishlist feature
9. Order tracking
10. Admin analytics dashboard

---

## Document Approval

**Prepared by:** Development Team  
**Reviewed by:** [To be filled]  
**Approved by:** [To be filled]  
**Date:** December 11, 2025

---

**End of Document**

