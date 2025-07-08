from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample device data
devices = [
    {"id": 1, "name": "NVIDIA RTX 4070", "type": "Graphics Card", "specs": "12GB GDDR6X", "price": "₱33,999", "is_favorite": False},
    {"id": 2, "name": "Intel i7-13700K", "type": "Processor", "specs": "16-Core, 24-Thread", "price": "₱22,499", "is_favorite": False},
    {"id": 3, "name": "Corsair Vengeance 16GB", "type": "RAM", "specs": "DDR5 5600MHz", "price": "₱4,999", "is_favorite": False},
    {"id": 4, "name": "Samsung 980 PRO 1TB", "type": "SSD", "specs": "PCIe 4.0 NVMe", "price": "₱7,299", "is_favorite": False},
    {"id": 5, "name": "ASUS ROG Strix B650E", "type": "Motherboard", "specs": "AM5, DDR5", "price": "₱13,999", "is_favorite": False}
]

# User login credentials
USER_CREDENTIALS = {
    "admin@example.com": "admin123",
    "sherwin@example.com": "scl2025",
    "tester@example.com": "test456"
}

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    show_favorites = request.args.get('favorites') == '1'
    filtered_devices = [d for d in devices if d['is_favorite']] if show_favorites else devices
    just_favorited = request.args.get('favorited') == '1'

    return render_template("home.html", devices=filtered_devices, just_favorited=just_favorited)

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

@app.route("/favorite/<int:device_id>", methods=["POST"])
def favorite(device_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    for device in devices:
        if device["id"] == device_id:
            device["is_favorite"] = not device["is_favorite"]
            break
    return redirect(url_for("home", favorited=1))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('cart', None)
    session.pop('orders', None)
    return redirect(url_for('login'))

@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/add-to-cart/<int:device_id>', methods=['POST'])
def add_to_cart(device_id):
    device = next((d for d in devices if d['id'] == device_id), None)
    if device:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(device)
    return redirect(url_for('cart'))


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

if __name__ == "__main__":
    app.run(debug=True)
