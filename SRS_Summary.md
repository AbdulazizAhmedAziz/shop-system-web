# 📋 SRS Document Summary

## Quick Reference Guide

### Document Structure
- **Full SRS**: See `SRS_Document.md` (comprehensive 50+ pages)
- **This Summary**: Quick reference for key requirements

---

## Key Requirements at a Glance

### Functional Requirements

#### 1. User Management
- ✅ Login/Logout
- ✅ Registration (customers)
- ✅ Role-based access (Admin/Customer)

#### 2. Product Management
- ✅ View products
- ✅ Edit products (Admin)
- ✅ Manage inventory
- ✅ Category organization

#### 3. Shopping Features
- ✅ Browse products
- ✅ Filter by offers
- ✅ Add to cart
- ✅ View cart
- ✅ Remove from cart

#### 4. Order Processing
- ✅ Checkout process
- ✅ Address entry
- ✅ Payment method selection
- ✅ Order confirmation

#### 5. Promotional Offers
- ✅ Discount percentages
- ✅ Free gifts
- ✅ Purchase limits per customer

#### 6. Admin Features
- ✅ Product management
- ✅ Offer management
- ✅ Sales reporting

---

## Technical Specifications

### Technology Stack
- **Backend**: Python 3.11, Flask 3.0.0
- **Frontend**: HTML, CSS, JavaScript
- **Server**: Gunicorn
- **Deployment**: Railway
- **Architecture**: MVC Pattern

### Performance Targets
- Page load: < 2 seconds
- API response: < 500ms
- Concurrent users: 50+

### Security Requirements
- Authentication: Username/password
- Session management: Flask sessions
- HTTPS: Required (Railway provides)

---

## User Roles

### Administrator
- Manage products and inventory
- Create/modify offers
- View sales reports
- Full system access

### Customer
- Browse products
- Add to cart
- Place orders
- Limited access

---

## Key Use Cases

1. **Customer Registration** → Browse → Add to Cart → Checkout
2. **Admin Login** → Manage Products → Create Offers → View Sales
3. **Customer** → View Offers → Add Limited Items → Checkout

---

## Data Model

### Core Entities
- **Product**: id, name, price, stock, category, offers
- **User**: username, password, role, cart
- **Order**: order_id, customer, items, total, payment, date

---

## Deployment

### Platform
- **Railway**: https://railway.app
- **Build**: Automatic from GitHub
- **Runtime**: Python 3.11
- **Port**: Dynamic (set by Railway)

---

## Testing Status

- ✅ Manual testing completed
- ⚠️ Automated tests: Not implemented
- ⚠️ UAT: Pending

---

## Future Enhancements

1. Database integration
2. Password hashing
3. Email notifications
4. Payment gateway
5. Product images
6. Search functionality

---

**For complete details, refer to `SRS_Document.md`**

