from flask import Blueprint, render_template_string, request, redirect, session, flash, url_for
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def add_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = generate_password_hash(password)
    save_users(users)
    return True

def verify_user(username, password):
    users = load_users()
    if username in users and check_password_hash(users[username], password):
        return True
    return False

def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    html = load_html("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if verify_user(username, password):
            session["user"] = username
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for("editor.editor"))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("auth.login"))

    return render_template_string(html)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    html = load_html("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill all fields.", "error")
            return redirect(url_for("auth.register"))

        if add_user(username, password):
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Username already exists.", "error")
            return redirect(url_for("auth.register"))

    return render_template_string(html)

@auth_bp.route("/logout")
def logout():
    username = session.get("user", "User")
    session.pop("user", None)
    flash(f"Goodbye, {username}!", "info")
    return redirect(url_for("auth.login"))
