from flask import Flask, render_template, request, redirect, session
import subprocess, uuid, os

app = Flask(__name__)
app.secret_key = "secret_key"

# Temporary in-memory user storage (for demo only)
users = {}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check user in dictionary
        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/editor")
        else:
            return render_template("login.html", message="Invalid username or password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_template("register.html", message="User already exists!")
        users[username] = password
        return redirect("/login")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/editor", methods=["GET", "POST"])
def editor():
    if "user" not in session:
        return redirect("/login")

    output = ""
    if request.method == "POST":
        code = request.form["code"]
        user_input = request.form.get("user_input", "")
        filename = f"temp_{uuid.uuid4()}.py"

        with open(filename, "w") as f:
            f.write(code)

        try:
            result = subprocess.run(
                ["python", filename],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout or result.stderr
        except subprocess.TimeoutExpired:
            output = "Error: Code execution timed out."

        os.remove(filename)

    return render_template("editor.html", username=session["user"], output=output)

@app.route("/")
def home():
    if "user" in session:
        return redirect("/editor")
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
