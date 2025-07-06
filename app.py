from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data
devices = [
    {"id": 1, "name": "NVIDIA RTX 4070", "type": "Graphics Card", "specs": "12GB GDDR6X", "price": "₱33,999", "is_favorite": False},
    {"id": 2, "name": "Intel i7-13700K", "type": "Processor", "specs": "16-Core, 24-Thread", "price": "₱22,499", "is_favorite": False},
    {"id": 3, "name": "Corsair Vengeance 16GB", "type": "RAM", "specs": "DDR5 5600MHz", "price": "₱4,999", "is_favorite": False},
    {"id": 4, "name": "Samsung 980 PRO 1TB", "type": "SSD", "specs": "PCIe 4.0 NVMe", "price": "₱7,299", "is_favorite": False},
    {"id": 5, "name": "ASUS ROG Strix B650E", "type": "Motherboard", "specs": "AM5, DDR5", "price": "₱13,999", "is_favorite": False}
]


@app.route("/")
def index():
    # Check if the "Show Only Favorites" checkbox was selected
    show_favorites = request.args.get('favorites') == '1'
    filtered_devices = [d for d in devices if d['is_favorite']] if show_favorites else devices

    # Check if we just favorited something to trigger toast
    just_favorited = request.args.get('favorited') == '1'

    return render_template("index.html", devices=filtered_devices, just_favorited=just_favorited)

@app.route("/favorite/<int:device_id>", methods=["POST"])
def favorite(device_id):
    for device in devices:
        if device["id"] == device_id:
            device["is_favorite"] = not device["is_favorite"]
            break
    # Redirect with toast notification flag
    return redirect(url_for("index", favorited=1))

if __name__ == "__main__":
    app.run(debug=True)
