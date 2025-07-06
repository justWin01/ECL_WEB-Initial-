from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data
devices = [
    {"id": 1, "name": "NVIDIA RTX 4070", "type": "Graphics Card", "specs": "12GB GDDR6X", "price": "$599", "is_favorite": False},
    {"id": 2, "name": "Intel i7-13700K", "type": "Processor", "specs": "16-Core, 24-Thread", "price": "$399", "is_favorite": False},
    {"id": 3, "name": "Corsair Vengeance 16GB", "type": "RAM", "specs": "DDR5 5600MHz", "price": "$89", "is_favorite": False},
      {"id": 4, "name": "Corsair Vengeance 16GB", "type": "RAM", "specs": "DDR5 5600MHz", "price": "$89", "is_favorite": False},
        {"id": 5, "name": "Corsair Vengeance 16GB", "type": "RAM", "specs": "DDR5 5600MHz", "price": "$89", "is_favorite": False}

]

@app.route("/")
def index():
    return render_template("index.html", devices=devices)

@app.route("/favorite/<int:device_id>", methods=["POST"])
def favorite(device_id):
    for device in devices:
        if device["id"] == device_id:
            device["is_favorite"] = not device["is_favorite"]
            break
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
