from flask import Flask
from auth_module import auth_bp
from editor_module import editor_bp

app = Flask(__name__)
app.secret_key = "secret_key" 

app.register_blueprint(auth_bp)
app.register_blueprint(editor_bp)

if __name__ == "__main__":
    app.run(debug=True)
