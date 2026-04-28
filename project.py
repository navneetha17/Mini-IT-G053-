from flask import Flask, render_template, request

app = Flask(__name__)

# Food database
foods = [
    {"name": "Nasi Lemak", "type": "spicy", "price": 8},
    {"name": "Fried Rice", "type": "savory", "price": 7},
    {"name": "Burger", "type": "fast food", "price": 10},
    {"name": "Pizza", "type": "fast food", "price": 15},
    {"name": "Ice Cream", "type": "sweet", "price": 5},
    {"name": "Tomyam", "type": "spicy", "price": 12}
]

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []

    if request.method == "POST":
        craving = request.form["craving"]

        # Recommendation logic
        for food in foods:
            if food["type"] == craving:
                recommendations.append(food)