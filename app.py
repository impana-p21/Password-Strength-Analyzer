from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    strength = ""
    message = ""

    if request.method == "POST":
        password = request.form["password"]
        score = 0
        suggestions = []

        if len(password) >= 8:
            score += 1
        else:
            suggestions.append("Use at least 8 characters.")

        if re.search(r"[A-Z]", password):
            score += 1
        else:
            suggestions.append("Add an uppercase letter.")

        if re.search(r"[a-z]", password):
            score += 1
        else:
            suggestions.append("Add a lowercase letter.")

        if re.search(r"\d", password):
            score += 1
        else:
            suggestions.append("Add a number.")

        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        else:
            suggestions.append("Add a special character.")

        if score <= 2:
            strength = "Weak Password"
        elif score <= 4:
            strength = "Medium Password"
        else:
            strength = "Strong Password"

        message = " ".join(suggestions) if suggestions else "Excellent password!"

    return render_template("index.html", strength=strength, message=message)

if __name__ == "__main__":
    app.run(debug=True)
