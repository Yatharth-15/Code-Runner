from flask import Blueprint, render_template_string, request, redirect, session, flash, url_for
import subprocess, uuid, os

editor_bp = Blueprint("editor", __name__)

def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

@editor_bp.route("/")
def home():
    if "user" in session:
        return redirect(url_for("editor.editor"))
    return redirect(url_for("auth.login"))

@editor_bp.route("/editor", methods=["GET", "POST"])
def editor():
    if "user" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.login"))

    html = load_html("editor.html")
    output = ""

    if request.method == "POST":
        code = request.form.get("code", "")
        user_input = request.form.get("user_input", "")
        filename = f"temp_{uuid.uuid4()}.py"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(code)

        try:
            result = subprocess.run(
                ["python", filename],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
        except subprocess.TimeoutExpired:
            output = "Error: Code execution took too long."
        except Exception as e:
            output = f"Error: {str(e)}"
        finally:
            try:
                os.remove(filename)
            except:
                pass

    return render_template_string(html, username=session["user"], output=output)
