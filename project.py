from flask import Flask, render_template, request

app = Flask(__name__)


foods = [

    {"category": "indian", "name": "Banana Leaf", "price": 18},
    {"category": "bevereges", "name": "Coffee", "price":20},
    {"category": "mamak", "name": "mee goreng", "price": 3},
    {"category": "western", "name": "Chickcen Chop", "price": 5},
    {"category": "western", "name": "Mac and Cheese", "price": 12},
    {"category": "western", "name": "Lamb Chop", "price": 15},
    {"category": "malay food", "name": "Laksa", "price": 8},
    {"category": "malay food", "name": "Nasi Lemak", "price": 6},
    {"category": "indonesia food", "name": "Ayam Gempuk", "price": 11.90}
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
            min_budget <= food["price"] <= max_budget
        ]


        if recommendations:
            message =f"{len(recommendations)} food options(s) found!"
        else:
            message = "No matching food. Try different options!"
    
    return render_template(
         "main page.html",
         recommendations="recommendations",
         message=message
    )

if __name__ == "__main__":
    app.run(debug=True)

        

        