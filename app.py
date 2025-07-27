from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from flask import session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample category and device data
categories = [
    {"id": 1, "name": "Graphics Cards", "description": "High-performance GPUs for gaming and creative work."},
    {"id": 2, "name": "Processors", "description": "Latest generation CPUs from Intel and AMD."},
    {"id": 3, "name": "Memory (RAM)", "description": "DDR4 and DDR5 memory modules."},
    {"id": 4, "name": "Storage", "description": "Fast and reliable SSDs and HDDs."},
    {"id": 5, "name": "Motherboards", "description": "Compatible boards for Intel and AMD builds."}
]

devices = [
    {"id": 1, "name": "NVIDIA RTX 4070", "type": "Graphics Card", "specs": "12GB GDDR6X", "price": "\u20b133,999", "is_favorite": False, "category_id": 1},
    {"id": 2, "name": "Intel i7-13700K", "type": "Processor", "specs": "16-Core, 24-Thread", "price": "\u20b122,499", "is_favorite": False, "category_id": 2},
    {"id": 3, "name": "Corsair Vengeance 16GB", "type": "RAM", "specs": "DDR5 5600MHz", "price": "\u20b14,999", "is_favorite": False, "category_id": 3},
    {"id": 4, "name": "Samsung 980 PRO 1TB", "type": "SSD", "specs": "PCIe 4.0 NVMe", "price": "\u20b17,299", "is_favorite": False, "category_id": 4},
    {"id": 5, "name": "ASUS ROG Strix B650E", "type": "Motherboard", "specs": "AM5, DDR5", "price": "\u20b113,999", "is_favorite": False, "category_id": 5}
]

USER_CREDENTIALS = {
    "admin@example.com": "admin123",
    "sherwin@example.com": "scl2025",
    "tester@example.com": "test456"
}

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("home.html", categories=categories)

@app.route('/favorites')
def favorites_page():
    favorite_devices = [d for d in devices if d.get('is_favorite')]
    return render_template('favorites.html', devices=favorite_devices)


@app.route('/search')
def search():
    query = request.args.get('search', '').lower()

    # Filter categories and devices based on search keyword
    matched_categories = [c for c in categories if query in c['name'].lower()]
    matched_devices = [d for d in devices if query in d['name'].lower()]

    return render_template(
        'search_results.html',
        categories=matched_categories,
        devices=matched_devices,
        query=query
    )



@app.route('/category/<int:category_id>')
def view_category(category_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    selected_category = next((c for c in categories if c['id'] == category_id), None)
    if not selected_category:
        return "Category not found", 404

    filtered_devices = [d for d in devices if d['category_id'] == category_id]
    return render_template("category_view.html", category=selected_category, devices=filtered_devices)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if USER_CREDENTIALS.get(email) == password:
            session['user'] = email
            session.setdefault('cart', [])
            session.setdefault('orders', [])
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid email or password")
    return render_template('login.html')

@app.route('/favorite/<int:device_id>', methods=['POST'])
def favorite(device_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    for device in devices:
        if device['id'] == device_id:
            device['is_favorite'] = not device['is_favorite']
            break
    return redirect(request.referrer or url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('cart', None)
    session.pop('orders', None)
    return redirect(url_for('login'))

@app.route("/cart")
def view_cart():
    cart = session.get("cart", [])
    return render_template("cart.html", cart=cart)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    item_name = request.form.get("name")
    item_price = request.form.get("price")

    if not item_name or not item_price:
        return redirect(url_for("home"))  # Or show an error

    # Initialize cart if not exists
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({
        "name": item_name,
        "price": item_price
    })
    session.modified = True  # Important!

    return redirect(url_for("view_cart"))

@app.route('/buy/<int:device_id>', methods=['POST'])
def buy(device_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    for device in devices:
        if device['id'] == device_id:
            orders = session.get('orders', [])
            new_order = {
                'id': len(orders) + 1,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'items': [device],
                'total': device['price']
            }
            orders.append(new_order)
            session['orders'] = orders
            break
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('orders.html', orders=session.get('orders', []))

@app.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    orders = session.get('orders', [])
    updated_orders = [order for order in orders if order['id'] != order_id]
    session['orders'] = updated_orders
    return redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(debug=True)
