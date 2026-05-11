from flask import Flask, render_template, request

app = Flask(__name__)


# Food database
foods = [
    {"category": "India Food", "name": "Banana Leaf", "price": 18},
    {"category": "Bevereges", "name": "Coffee", "price":20},
    {"category": "Mamak", "name": "mee goreng", "price": 3},
    {"category": "Western", "name": "Chickcen Chop", "price": 5},
    {"category": "Western", "name": "Mac and Cheese", "price": 12}
]

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    message =""

    if request.method == "POST":
        category = request.form["category"]
        budget_range = request.form["budget"]

        min_budget, max_budget = map(int, budget_range.split("-"))

        #Filter food
        recommendations = [
            food for food in foods
            if food["category"] == category and 
            min_budget <= food["prices"] <= max_budget
        ]


        if recommendations:
            message =f"{len(recommendations)}"
        else:
            message = "No matching food. Try different options!"
    
    return render_template(
        "index.html",
        recommendations=recommendations,
        message=message

    )

if __name__ == "_main_":
    app.run(debug=True)

        

        