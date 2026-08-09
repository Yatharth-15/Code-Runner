import json
import os
import shutil
import subprocess
import uuid
from flask import Blueprint, Response, jsonify, redirect, render_template_string, request, session

editor_bp = Blueprint("editor", __name__)
TEMP_RUNS_DIR = "temp_runs"
active_runs = {}


def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()


@editor_bp.route("/")
def home():
    if "user" not in session:
        session["user"] = "Guest"
    return redirect("/editor")


@editor_bp.route("/editor", methods=["GET"])
def editor():
    if "user" not in session:
        session["user"] = "Guest"

    return render_template_string(
        load_html("editor.html"),
        username=session["user"],
        output=""
    )


@editor_bp.route("/editor/run", methods=["POST"])
def run_code():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    code = request.form.get("code", "")
    lang = request.form.get("language", "python")

    run_id = str(uuid.uuid4())
    run_dir = os.path.join(TEMP_RUNS_DIR, f"run_{run_id}")
    os.makedirs(run_dir, exist_ok=True)

    if lang == "python":
        file_name = "program.py"
        run_cmd = ["python", "-u", file_name]
    elif lang == "c":
        file_name = "program.c"
        exe_file = os.path.abspath(os.path.join(run_dir, "program.exe" if os.name == "nt" else "program"))
        run_cmd = [exe_file]
    elif lang == "cpp":
        file_name = "program.cpp"
        exe_file = os.path.abspath(os.path.join(run_dir, "program.exe" if os.name == "nt" else "program"))
        run_cmd = [exe_file]
    elif lang == "java":
        file_name = "Main.java"
        run_cmd = ["java", "-cp", ".", "Main"]
    else:
        return jsonify({"error": "Unsupported language"}), 400

    # Write file first
    with open(os.path.join(run_dir, file_name), "w", encoding="utf-8") as f:
        f.write(code)

    # Compile if needed
    compile_cmd = None
    if lang == "c":
        compile_cmd = ["gcc", os.path.join(run_dir, "program.c"), "-o", exe_file]
    elif lang == "cpp":
        compile_cmd = ["g++", os.path.join(run_dir, "program.cpp"), "-o", exe_file]
    elif lang == "java":
        compile_cmd = ["javac", "-d", run_dir, os.path.join(run_dir, "Main.java")]

    if compile_cmd:
        comp = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
        if comp.returncode != 0:
            shutil.rmtree(run_dir, ignore_errors=True)
            return jsonify({"compiled": False, "error": comp.stderr})

    try:
        proc = subprocess.Popen(
            run_cmd,
            cwd=run_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0
        )
        active_runs[run_id] = (proc, run_dir)
    except Exception as e:
        shutil.rmtree(run_dir, ignore_errors=True)
        return jsonify({"compiled": False, "error": f"Failed to start process: {e}"})

    return jsonify({
        "run_id": run_id,
        "compiled": True
    })


@editor_bp.route("/editor/stream/<run_id>")
def stream_output(run_id):
    if run_id not in active_runs:
        return "Process not found", 404

    proc, run_dir = active_runs[run_id]

    def event_stream():
        while True:
            char = proc.stdout.read(1)
            if not char:
                break
            yield f"data: {json.dumps({'stream': 'stdout', 'data': char})}\n\n"

        exit_code = proc.wait()
        yield f"data: {json.dumps({'stream': 'status', 'data': 'finished', 'exit_code': exit_code})}\n\n"

        try:
            proc.stdin.close()
        except:
            pass
        if os.path.exists(run_dir):
            shutil.rmtree(run_dir, ignore_errors=True)
        if run_id in active_runs:
            del active_runs[run_id]

    return Response(event_stream(), mimetype="text/event-stream")


@editor_bp.route("/editor/input/<run_id>", methods=["POST"])
def send_input(run_id):
    if run_id not in active_runs:
        return jsonify({"success": False, "error": "Process is not running"}), 400

    proc, _ = active_runs[run_id]
    data = request.json or {}
    text = data.get("text", "")
    try:
        proc.stdin.write(text)
        proc.stdin.flush()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
