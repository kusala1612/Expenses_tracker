from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ombabuji@16",
    database="expense_tracker",
    port=3306
)
cursor = conn.cursor(dictionary=True)

# ----------------- User Registration -----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data['username']
    password = generate_password_hash(data['password'])
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return jsonify({"message": "User registered!"})
    except:
        return jsonify({"message": "Username already exists."}), 400

# ----------------- User Login -----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful!", "user_id": user['id']})
    return jsonify({"message": "Invalid credentials."}), 401

# ----------------- Add Expense -----------------
@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.json
    try:
        date_obj = datetime.strptime(data['date'], "%d-%m-%Y")
        amount = float(data['amount'])
        sql = "INSERT INTO expenses (user_id, date, description, amount, category) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (data['user_id'], date_obj, data['description'], amount, data.get('category', 'General')))
        conn.commit()
        return jsonify({"message": "Expense added!"})
    except:
        return jsonify({"message": "Error adding expense"}), 400

# ----------------- View Expenses -----------------
@app.route("/expenses/<int:user_id>", methods=["GET"])
def view_expenses(user_id):
    cursor.execute("SELECT * FROM expenses WHERE user_id=%s ORDER BY date DESC", (user_id,))
    return jsonify(cursor.fetchall())

# ----------------- Delete Expense -----------------
@app.route("/expenses/<int:user_id>/<int:id>", methods=["DELETE"])
def delete_expense(user_id, id):
    cursor.execute("DELETE FROM expenses WHERE id=%s AND user_id=%s", (id, user_id))
    conn.commit()
    return jsonify({"message": "Deleted!"})

# ----------------- Total Expenses -----------------
@app.route("/expenses/total/<int:user_id>", methods=["GET"])
def total_expenses(user_id):
    cursor.execute("SELECT SUM(amount) AS total FROM expenses WHERE user_id=%s", (user_id,))
    total = cursor.fetchone()['total'] or 0
    return jsonify({"total": total})

# ----------------- Total Between Dates -----------------
@app.route("/expenses/total_between/<int:user_id>", methods=["POST"])
def total_between_dates(user_id):
    data = request.json
    start = datetime.strptime(data['start'], "%d-%m-%Y")
    end = datetime.strptime(data['end'], "%d-%m-%Y")
    cursor.execute("SELECT SUM(amount) AS total FROM expenses WHERE user_id=%s AND date BETWEEN %s AND %s", (user_id, start, end))
    total = cursor.fetchone()['total'] or 0
    return jsonify({"total": total})

if __name__ == "__main__":
    app.run(debug=True)
