import os
from datetime import datetime, date as date_type
from decimal import Decimal
from dotenv import load_dotenv
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2 import errors
import psycopg2.extras

# ----------------- LOAD ENV VARIABLES -----------------
load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="dpg-d3412cjuibrs73b0m3t0-a.singapore-postgres.render.com",
            database="expense_tracker_db_i6nk",
            user="expense_tracker_db_i6nk_user",
            password="SWoddph65axD4fgQrLUpGtY0nYA35K7F",
            port=5432
        )
        return conn
    except Exception as e:
        print("DB connect error:", e)
        return None

@app.teardown_appcontext
def close_db_conn(exc):
    conn = getattr(g, "_db_conn", None)
    if conn:
        try:
            conn.close()
        except Exception:
            pass

# ---------- HELPER FUNCTION ----------
def serialize_rows(rows):
    """Convert datetimes/Decimals to JSON-friendly types."""
    out = []
    for r in rows:
        new = {}
        for k, v in r.items():
            if isinstance(v, (datetime, date_type)):
                new[k] = v.strftime("%d-%m-%Y")
            elif isinstance(v, Decimal):
                new[k] = float(v)
            else:
                new[k] = v
        out.append(new)
    return out

# ---------- HOME ROUTE ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Expense Tracker API is running with PostgreSQL!"}), 200

# ----------------- User Registration -----------------
@app.route("/register", methods=["POST"])
def register():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503

    data = request.json or {}
    username = data.get("username")
    password_plain = data.get("password")
    if not username or not password_plain:
        return jsonify({"error": "username and password required"}), 400

    hashed = generate_password_hash(password_plain)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed),
        )
        conn.commit()
        return jsonify({"message": "User registered!"}), 201
    except errors.UniqueViolation:
        conn.rollback()
        return jsonify({"message": "Username already exists."}), 400
    except Exception as e:
        conn.rollback()
        app.logger.error("Register error: %s", e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        cursor.close()

# ----------------- User Login -----------------
@app.route("/login", methods=["POST"])
def login():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503

    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user["password"], password):
            return jsonify(
                {"message": "Login successful!", "user_id": user["id"]}
            ), 200
        return jsonify({"message": "Invalid credentials."}), 401
    except Exception as e:
        app.logger.error("Login error: %s", e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        cursor.close()

# ----------------- Add Expense -----------------
@app.route("/expenses", methods=["POST"])
def add_expense():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503

    data = request.json or {}
    required = ("user_id", "date", "description", "amount")
    if not all(k in data for k in required):
        return jsonify(
            {"error": "user_id, date, description and amount required"}), 400

    try:
        date_obj = datetime.strptime(data["date"], "%d-%m-%Y").date()
        amount = float(data["amount"])
        category = data.get("category", "General")

        cursor = conn.cursor()
        sql = """
            INSERT INTO expenses (user_id, date, description, amount, category)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (data["user_id"], date_obj, data["description"], amount, category),
        )
        conn.commit()
        return jsonify({"message": "Expense added!"}), 201
    except ValueError:
        return jsonify({"message": "Invalid date or amount format"}), 400
    except Exception as e:
        conn.rollback()
        app.logger.error("Add expense error: %s", e)
        return jsonify({"message": "Error adding expense"}), 500
    finally:
        cursor.close()

# ----------------- View Expenses -----------------
@app.route("/expenses/<int:user_id>", methods=["GET"])
def view_expenses(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute(
            "SELECT * FROM expenses WHERE user_id=%s ORDER BY date DESC",
            (user_id,),
        )
        rows = cursor.fetchall()
        return jsonify(serialize_rows(rows)), 200
    except Exception as e:
        app.logger.error("View expenses error: %s", e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        cursor.close()

# ----------------- Delete Expense -----------------
@app.route("/expenses/<int:user_id>/<int:expense_id>", methods=["DELETE"])
def delete_expense(user_id, expense_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503

    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM expenses WHERE id=%s AND user_id=%s",
            (expense_id, user_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Not found"}), 404
        return jsonify({"message": "Deleted!"}), 200
    except Exception as e:
        conn.rollback()
        app.logger.error("Delete error: %s", e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        cursor.close()

# ----------------- Total Expenses -----------------
@app.route("/expenses/total/<int:user_id>", methods=["GET"])
def total_expenses(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute(
            "SELECT SUM(amount) AS total FROM expenses WHERE user_id=%s",
            (user_id,),
        )
        total = cursor.fetchone()
        total_val = (
            float(total["total"]) if total and total["total"] is not None else 0.0
        )
        return jsonify({"total": total_val}), 200
    except Exception as e:
        app.logger.error("Total error: %s", e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        cursor.close()

# ----------------- Total Between Dates -----------------
@app.route("/expenses/total_between/<int:user_id>", methods=["POST"])
def total_between_dates(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503

    data = request.json or {}
    if not data.get("start") or not data.get("end"):
        return jsonify({"error": "start and end required (dd-mm-YYYY)"}), 400

    try:
        start = datetime.strptime(data["start"], "%d-%m-%Y").date()
        end = datetime.strptime(data["end"], "%d-%m-%Y").date()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
            SELECT SUM(amount) AS total
            FROM expenses
            WHERE user_id=%s AND date BETWEEN %s AND %s
            """,
            (user_id, start, end),
        )
        total = cursor.fetchone()
        total_val = (
            float(total["total"]) if total and total["total"] is not None else 0.0
        )
        return jsonify({"total": total_val}), 200
    except ValueError:
        return jsonify({"error": "Invalid date format; use dd-mm-YYYY"}), 400
    except Exception as e:
        app.logger.error("Total between dates error: %s", e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        cursor.close()