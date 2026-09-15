
from flask import Flask, render_template, request
import pickle
import math

app = Flask(__name__)

model = pickle.load(open("model/risk_model.pkl", "rb"))

def calculate_emi(P, annual_rate, years):
    R = annual_rate / (12 * 100)
    N = years * 12
    emi = (P * R * (1 + R)**N) / ((1 + R)**N - 1)
    return round(emi, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        salary = float(request.form["salary"])
        expenses = float(request.form["expenses"])
        credit_score = float(request.form["credit_score"])
        loan_amount = float(request.form["loan_amount"])
        interest = float(request.form["interest"])
        tenure = int(request.form["tenure"])

        emi = calculate_emi(loan_amount, interest, tenure)

        prediction = model.predict([[salary, expenses, credit_score, loan_amount]])[0]

        risk_label = ["Low Risk ✅", "Medium Risk ⚠", "High Risk ❌"][prediction]

        total_payment = round(emi * tenure * 12, 2)
        total_interest = round(total_payment - loan_amount, 2)

        return render_template("result.html", emi=emi,
                               total_payment=total_payment,
                               total_interest=total_interest,
                               risk=risk_label)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
