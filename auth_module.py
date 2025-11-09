from flask import Blueprint, render_template_string, request, redirect, session, flash
import json, os

auth_bp = Blueprint("auth", __name__)

def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

USERS_FILE = "users.json"

def load_users():
    try:
        if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except json.JSONDecodeError:
        pass
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        f.write("{}")
    return {}

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# --- Routes ---
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    html = load_html("login.html")
    users = load_users()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            flash(f"Welcome, {username}!", "success")
            return redirect("/editor")
        flash("Invalid username or password.", "error")
    return render_template_string(html)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    html = load_html("register.html")
    users = load_users()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please fill all fields.", "error")
            return redirect("/register")
        if username in users:
            flash("Username already exists!", "error")
            return redirect("/register")
        users[username] = password
        save_users(users)
        flash("Registration successful!", "success")
        return redirect("/login")
    return render_template_string(html)

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect("/login")
