import datetime
import time
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-please-use-env-variable')

# ==============================================================================
#                               1. الكيانات (Classes)
# ==============================================================================

class Product:
    def __init__(self, p_id, name, price, stock, category):
        self.id = p_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

        # خصائص العروض
        self.offer_discount = 0
        self.offer_gift = None
        self.offer_limit = 0  # 0 تعني مفتوح (بدون حد)

    def set_offer(self, discount, gift_name, limit=0):
        self.offer_discount = discount
        self.offer_gift = gift_name
        self.offer_limit = limit

    def to_dict(self):
        new_price = self.price - (self.price * self.offer_discount / 100) if self.offer_discount > 0 else self.price
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'offer_discount': self.offer_discount,
            'offer_gift': self.offer_gift,
            'offer_limit': self.offer_limit,
            'new_price': round(new_price, 2),
            'has_offer': self.offer_discount > 0 or self.offer_gift is not None
        }

    def get_admin_row(self):
        offer_parts = []
        if self.offer_discount > 0: offer_parts.append(f"خصم {self.offer_discount}%")
        if self.offer_gift: offer_parts.append(f"+ {self.offer_gift}")
        if self.offer_limit > 0: offer_parts.append(f"(الحد: {self.offer_limit})")

        offer_txt = " ".join(offer_parts) if offer_parts else "---"
        return f"{self.id:<5} | {self.name:<22} | {self.price:<8} | {self.stock:<8} | {offer_txt}"

class User:
    def __init__(self, username, password, role="Customer"):
        self.username = username
        self.password = password
        self.role = role
        self.cart = []

class Order:
    def __init__(self, order_id, customer, items, total, address, pay_method, pay_status):
        self.order_id = order_id
        self.customer_name = customer
        self.items_txt = items
        self.total = total
        self.address = address
        self.pay_method = pay_method
        self.pay_status = pay_status
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# ==============================================================================
#                           2. نظام التحكم (Controller)
# ==============================================================================

class ShopSystem:
    def __init__(self):
        self.products = []
        self.users = []
        self.orders = []
        # الحسابات: (admin/123) و (place/123)
        self.users.append(User("place", "123", "Admin"))
        self.users.append(User("admin", "123", "Admin"))
        self._seed_data()

    def _seed_data(self):
        # القائمة الكاملة (30 منتج)
        data = [
            (101, "Laptop HP Pavilion", 850, 10, "Electronics"),
            (102, "iPhone 14 Pro", 1100, 5, "Electronics"),
            (103, "Samsung S23 Ultra", 1050, 8, "Electronics"),
            (104, "Sony WH-1000XM5", 350, 15, "Electronics"),
            (105, "iPad Air 5", 600, 12, "Electronics"),
            (106, "Logitech Mouse", 40, 50, "Electronics"),
            (107, "Mechanical Keyboard", 80, 20, "Electronics"),
            (108, "Monitor Dell 24\"", 150, 10, "Electronics"),
            (201, "Cotton T-Shirt", 20, 100, "Clothing"),
            (202, "Blue Jeans", 45, 40, "Clothing"),
            (203, "Leather Jacket", 120, 10, "Clothing"),
            (204, "Running Shoes", 70, 25, "Clothing"),
            (205, "Formal Shirt", 35, 30, "Clothing"),
            (206, "Sports Cap", 15, 60, "Clothing"),
            (301, "Coffee Maker", 90, 8, "Home"),
            (302, "Blender 500W", 40, 15, "Home"),
            (303, "Air Fryer", 80, 12, "Home"),
            (304, "Desk Lamp LED", 25, 30, "Home"),
            (305, "Towel Set", 15, 50, "Home"),
            (401, "Yoga Mat", 20, 40, "Sports"),
            (402, "Dumbbell Set", 50, 10, "Sports"),
            (403, "Tennis Racket", 90, 5, "Sports"),
            (404, "Football", 25, 20, "Sports"),
            (501, "Python Programming", 40, 50, "Books"),
            (502, "Notebook A4", 5, 200, "Stationery"),
            (503, "Luxury Pen", 10, 100, "Stationery"),
            (504, "Novel: 1984", 15, 30, "Books"),
            (505, "Scientific Calc", 20, 25, "Stationery"),
            (506, "Backpack", 45, 15, "Travel"),
            (507, "Water Bottle", 12, 60, "Travel")
        ]
        for p in data:
            self.products.append(Product(*p))

    def login(self, u, p):
        for user in self.users:
            if user.username == u and user.password == p: return user
        return None

    def register(self, u, p):
        for user in self.users:
            if user.username == u: return None
        new_u = User(u, p, "Customer")
        self.users.append(new_u)
        return new_u

    def get_product_by_id(self, p_id):
        for p in self.products:
            if p.id == p_id:
                return p
        return None

    def get_cart_total(self, user):
        total = 0
        for item in user.cart:
            p = item['product']
            price = p.price * item['qty']
            if p.offer_discount > 0:
                price -= price * (p.offer_discount / 100)
            total += price
        return total

    def checkout(self, user, address, pay_method):
        if not user.cart: return False, "السلة فارغة"

        # تحقق أخير للأمان
        for item in user.cart:
            if item['qty'] > item['product'].stock:
                return False, f"الكمية نفدت لـ {item['product'].name}"

        pay_status = "Pending"
        if pay_method == "Online Payment":
            pay_status = "Paid"
        elif pay_method in ["Cash on Delivery", "Visa on Delivery"]:
            pay_status = "Upon Delivery"

        items_report = []
        final_total = 0

        for item in user.cart:
            prod = item['product']
            qty = item['qty']
            prod.stock -= qty

            original_price = prod.price * qty
            discount_val = 0
            if prod.offer_discount > 0:
                discount_val = original_price * (prod.offer_discount / 100)
            final_item_price = original_price - discount_val

            items_report.append(f"{prod.name} x{qty}")
            final_total += final_item_price

        self.orders.append(Order(len(self.orders)+100, user.username, items_report, final_total, address, pay_method, pay_status))
        user.cart.clear()
        return True, final_total

    def admin_edit_product(self, p_id, nn, np, ns):
        for p in self.products:
            if p.id == p_id:
                if nn: p.name = nn
                if np: p.price = float(np)
                if ns: p.stock = int(ns)
                return True
        return False

    def admin_apply_offer(self, p_id, d, g, l):
        for p in self.products:
            if p.id == p_id:
                p.set_offer(d, g, l)
                return True
        return False

# Global shop system instance
shop_system = ShopSystem()

# ==============================================================================
#                           3. Flask Routes
# ==============================================================================

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = shop_system.login(username, password)
        if user:
            session['user'] = username
            session['role'] = user.role
            if user.role == 'Admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('customer_dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = shop_system.register(username, password)
        if user:
            session['user'] = username
            session['role'] = user.role
            return redirect(url_for('customer_dashboard'))
        else:
            flash('اسم المستخدم موجود بالفعل', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', products=shop_system.products, orders=shop_system.orders)

@app.route('/admin/edit_product', methods=['POST'])
def admin_edit_product():
    if 'user' not in session or session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'غير مصرح'})
    
    p_id = int(request.form.get('product_id'))
    name = request.form.get('name')
    price = request.form.get('price')
    stock = request.form.get('stock')
    
    success = shop_system.admin_edit_product(p_id, name, price, stock)
    return jsonify({'success': success})

@app.route('/admin/apply_offer', methods=['POST'])
def admin_apply_offer():
    if 'user' not in session or session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'غير مصرح'})
    
    p_id = int(request.form.get('product_id'))
    discount = float(request.form.get('discount', 0))
    gift = request.form.get('gift') if request.form.get('gift') else None
    limit = int(request.form.get('limit', 0))
    
    success = shop_system.admin_apply_offer(p_id, discount, gift, limit)
    return jsonify({'success': success})

@app.route('/customer/dashboard')
def customer_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user = shop_system.login(username, '')  # We'll find user by username
    for u in shop_system.users:
        if u.username == username:
            user = u
            break
    
    cart_count = len(user.cart) if user else 0
    return render_template('customer_dashboard.html', products=shop_system.products, cart_count=cart_count)

@app.route('/customer/products')
def customer_products():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user = None
    for u in shop_system.users:
        if u.username == username:
            user = u
            break
    
    show_offers_only = request.args.get('offers_only', 'false') == 'true'
    products = shop_system.products
    if show_offers_only:
        products = [p for p in products if p.offer_discount > 0 or p.offer_gift]
    
    return render_template('customer_products.html', products=products, user=user, show_offers_only=show_offers_only)

@app.route('/customer/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'يجب تسجيل الدخول'})
    
    username = session['user']
    user = None
    for u in shop_system.users:
        if u.username == username:
            user = u
            break
    
    if not user:
        return jsonify({'success': False, 'message': 'المستخدم غير موجود'})
    
    product_id = int(request.json.get('product_id'))
    qty = int(request.json.get('qty', 1))
    
    product = shop_system.get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'المنتج غير موجود'})
    
    # Check current cart quantity
    current_in_cart = 0
    for item in user.cart:
        if item['product'].id == product_id:
            current_in_cart += item['qty']
    
    # Check limits
    max_allowed = product.stock
    if product.offer_limit > 0:
        remaining_limit = product.offer_limit - current_in_cart
        if remaining_limit <= 0:
            return jsonify({'success': False, 'message': f'لقد استهلكت الحد الأقصى لهذا العرض ({product.offer_limit} قطع)'})
        max_allowed = min(product.stock, remaining_limit)
    
    if qty <= 0 or qty > max_allowed:
        return jsonify({'success': False, 'message': f'الكمية غير صحيحة. الحد المسموح: {max_allowed}'})
    
    # Add to cart
    user.cart.append({'product': product, 'qty': qty})
    return jsonify({'success': True, 'message': f'تم إضافة {qty} من {product.name} بنجاح', 'cart_count': len(user.cart)})

@app.route('/customer/cart')
def customer_cart():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user = None
    for u in shop_system.users:
        if u.username == username:
            user = u
            break
    
    if not user:
        return redirect(url_for('login'))
    
    total = shop_system.get_cart_total(user)
    return render_template('customer_cart.html', user=user, total=total)

@app.route('/customer/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'user' not in session:
        return jsonify({'success': False})
    
    username = session['user']
    user = None
    for u in shop_system.users:
        if u.username == username:
            user = u
            break
    
    if not user:
        return jsonify({'success': False})
    
    product_id = int(request.json.get('product_id'))
    user.cart = [item for item in user.cart if item['product'].id != product_id]
    return jsonify({'success': True, 'cart_count': len(user.cart)})

@app.route('/customer/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user = None
    for u in shop_system.users:
        if u.username == username:
            user = u
            break
    
    if not user or not user.cart:
        return redirect(url_for('customer_cart'))
    
    if request.method == 'POST':
        address = request.form.get('address', 'استلام من الفرع')
        pay_method = request.form.get('pay_method')
        
        success, result = shop_system.checkout(user, address, pay_method)
        if success:
            flash(f'تم إتمام الطلب بنجاح! المبلغ: {result:.2f}$', 'success')
            return redirect(url_for('customer_dashboard'))
        else:
            flash(result, 'error')
    
    total = shop_system.get_cart_total(user)
    return render_template('checkout.html', user=user, total=total)

@app.route('/api/product/<int:product_id>')
def get_product_info(product_id):
    if 'user' not in session:
        return jsonify({'error': 'غير مصرح'})
    
    username = session['user']
    user = None
    for u in shop_system.users:
        if u.username == username:
            user = u
            break
    
    product = shop_system.get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'المنتج غير موجود'})
    
    current_in_cart = 0
    for item in user.cart:
        if item['product'].id == product_id:
            current_in_cart += item['qty']
    
    max_allowed = product.stock
    remaining_limit = None
    if product.offer_limit > 0:
        remaining_limit = product.offer_limit - current_in_cart
        max_allowed = min(product.stock, remaining_limit)
    
    return jsonify({
        'product': product.to_dict(),
        'current_in_cart': current_in_cart,
        'max_allowed': max_allowed,
        'remaining_limit': remaining_limit
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)

