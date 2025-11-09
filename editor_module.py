from flask import Blueprint, render_template_string, request, redirect, session, flash
import subprocess, uuid, os, json

editor_bp = Blueprint("editor", __name__)

def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

HISTORY_FILE = "history.json"


def load_history():
    try:
        if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except json.JSONDecodeError:
        pass
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("{}")
    return {}

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@editor_bp.route("/editor", methods=["GET", "POST"])
def editor():
    if "user" not in session:
        return redirect("/login")

    html = load_html("editor.html")
    username = session["user"]
    history = load_history()
    history.setdefault(username, [])
    output = ""

    if request.method == "POST":
        code = request.form.get("code", "")
        user_input = request.form.get("user_input", "")
        lang = request.form.get("language", "python")
        user_input = user_input.strip().replace(",", "\n")
        filename = f"temp_{uuid.uuid4()}"

        if code.strip():
            history[username].append(code.strip())
            history[username] = history[username][-5:]
            save_history(history)

        # --- Setup commands ---
        if lang == "python":
            filename += ".py"
            run_cmd = ["python", filename]
            compile_cmd = None
        elif lang == "c":
            filename += ".c"
            exe_file = f"{filename[:-2]}.exe"
            compile_cmd = ["gcc", filename, "-o", exe_file]
            run_cmd = [exe_file]
        elif lang == "cpp":
            filename += ".cpp"
            exe_file = f"{filename[:-4]}.exe"
            compile_cmd = ["g++", filename, "-o", exe_file]
            run_cmd = [exe_file]
        elif lang == "java":
            filename += ".java"
            compile_cmd = ["javac", filename]
            run_cmd = ["java", filename[:-5]]
        else:
            output = "Unsupported language"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            if compile_cmd:
                comp = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
                if comp.returncode != 0:
                    output = comp.stderr
                else:
                    result = subprocess.run(run_cmd, input=user_input, capture_output=True, text=True, timeout=10)
                    output = result.stdout or result.stderr
            else:
                result = subprocess.run(run_cmd, input=user_input, capture_output=True, text=True, timeout=10)
                output = result.stdout or result.stderr
        except subprocess.TimeoutExpired:
            output = "⏳ Error: Code execution took too long."
        except Exception as e:
            output = f"⚠️ Error: {e}"
        finally:
            for ext in ["", ".exe", ".class", ".py", ".c", ".cpp", ".java"]:
                try:
                    os.remove(filename.replace(".py", ext))
                except:
                    pass

    return render_template_string(html, username=username, output=output, user_history=history[username])

@editor_bp.route("/")
def home():
    if "user" in session:
        return redirect("/editor")
    return redirect("/login")
