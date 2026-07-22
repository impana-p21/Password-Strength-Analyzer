from flask import Flask, render_template, request
import re
import sqlite3
import hashlib

app = Flask(__name__)

# Create database
conn = sqlite3.connect("passwords.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT UNIQUE
)
""")
conn.commit()

common_passwords = [
    "password",
    "123456",
    "123456789",
    "qwerty",
    "admin",
    "welcome",
    "password123"
]

@app.route("/", methods=["GET", "POST"])
def home():

    strength = ""
    message = ""

    if request.method == "POST":

        password = request.form["password"]

        score = 0
        suggestions = []

        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            suggestions.append("Use at least 12 characters.")

        if re.search(r"[A-Z]", password):
            score += 1
        else:
            suggestions.append("Add uppercase letters.")

        if re.search(r"[a-z]", password):
            score += 1
        else:
            suggestions.append("Add lowercase letters.")

        if re.search(r"\d", password):
            score += 1
        else:
            suggestions.append("Add numbers.")

        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        else:
            suggestions.append("Add special characters.")

        if password.lower() in common_passwords:
            suggestions.append("Avoid common passwords.")
            score = max(score - 2, 0)

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM passwords WHERE hash=?", (password_hash,))
        exists = cursor.fetchone()

        if exists:
            suggestions.append("Password has already been used.")
        else:
            cursor.execute(
                "INSERT INTO passwords(hash) VALUES(?)",
                (password_hash,)
            )
            conn.commit()

        if score <= 2:
            strength = "Weak Password"
        elif score <= 5:
            strength = "Medium Password"
        else:
            strength = "Strong Password"

        if suggestions:
            message = "Suggestions: " + " ".join(suggestions)
        else:
            message = "Excellent! This is a strong and unique password."

    return render_template(
        "index.html",
        strength=strength,
        message=message
    )

if __name__ == "__main__":
    app.run(debug=True)
