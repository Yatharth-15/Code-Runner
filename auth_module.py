import sqlite3
from flask import Blueprint, flash, redirect, render_template_string, request, session
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)
DB_FILE = "database.db"


def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.commit()


init_db()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    html = load_html("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            user = conn.execute(
                "SELECT password FROM users WHERE username = ?", (username,)
            ).fetchone()

        if user:
            stored_password = user["password"]
            if check_password_hash(stored_password, password):
                session["user"] = username
                flash(f"Welcome, {username}!", "success")
                return redirect("/editor")

        flash("Invalid username or password.", "error")
    return render_template_string(html)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    html = load_html("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please fill all fields.", "error")
            return redirect("/register")

        hashed_password = generate_password_hash(password)
        try:
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password)
                )
                conn.commit()
            flash("Registration successful!", "success")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Username already exists!", "error")
            return redirect("/register")
            
    return render_template_string(html)


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect("/login")
