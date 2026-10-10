
from flask import Flask, request, jsonify
import sqlite3
import re
from pathlib import Path

app = Flask(__name__)
DATABASE = Path(__file__).with_name("students.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age BETWEEN 1 AND 120)
            )
        """)


def validate_student(data):
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    for field in ("name", "email", "course", "age"):
        if field not in data:
            return f"Missing required field: {field}"

    for field in ("name", "email", "course"):
        if not isinstance(data[field], str) or not data[field].strip():
            return f"{field} must be a non-empty string."

    if not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", data["email"].strip()
    ):
        return "Please provide a valid email address."

    if type(data["age"]) is not int or not 1 <= data["age"] <= 120:
        return "Age must be an integer between 1 and 120."

    return None


def row_to_dict(row):
    return dict(row)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Student Management REST API",
        "endpoints": [
            "POST /api/students",
            "GET /api/students",
            "GET /api/students/<student_id>",
            "PUT /api/students/<student_id>",
            "DELETE /api/students/<student_id>"
        ]
    }), 200


# CREATE
@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)
    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO students (name, email, course, age)
                   VALUES (?, ?, ?, ?)""",
                (
                    data["name"].strip(),
                    data["email"].strip().lower(),
                    data["course"].strip(),
                    data["age"]
                )
            )
            row = conn.execute(
                "SELECT * FROM students WHERE id = ?",
                (cursor.lastrowid,)
            ).fetchone()

        return jsonify(row_to_dict(row)), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists."}), 409


# READ ALL
@app.route("/api/students", methods=["GET"])
def get_students():
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

    return jsonify([row_to_dict(row) for row in rows]), 200


# READ ONE
@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

    if row is None:
        return jsonify({"error": "Student not found."}), 404

    return jsonify(row_to_dict(row)), 200


# UPDATE
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True)
    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    try:
        with get_db_connection() as conn:
            existing = conn.execute(
                "SELECT id FROM students WHERE id = ?",
                (student_id,)
            ).fetchone()

            if existing is None:
                return jsonify({"error": "Student not found."}), 404

            conn.execute(
                """UPDATE students
                   SET name = ?, email = ?, course = ?, age = ?
                   WHERE id = ?""",
                (
                    data["name"].strip(),
                    data["email"].strip().lower(),
                    data["course"].strip(),
                    data["age"],
                    student_id
                )
            )

            row = conn.execute(
                "SELECT * FROM students WHERE id = ?",
                (student_id,)
            ).fetchone()

        return jsonify(row_to_dict(row)), 200

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists."}), 409


# DELETE
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    with get_db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found."}), 404

    return jsonify({
        "message": "Student deleted successfully.",
        "id": student_id
    }), 200


@app.errorhandler(404)
def route_not_found(error):
    return jsonify({"error": "Route not found."}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "HTTP method not allowed."}), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=False)