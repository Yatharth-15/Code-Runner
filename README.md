Code Runner -
        Multi-Language Web Compiler

A lightweight, web-based code execution engine built with Python (Flask). This application allows users to write, compile, and run code in multiple programming languages (Python, C, C++, and Java) directly from their browser.
Features
Multi-Language Support: Run Python, C, C++, and Java code.

User Authentication: Secure Login/ Logout system to manage user sessions.

Dynamic Input: Support for program inputs (stdin) via comma-separated values.

Clean UI: Minimalist, responsive design with a dedicated output console.

Sticky Forms: Retains your code and language selection after execution for a better workflow.

Technologies Used

Frontend: HTML5, CSS3, Jinja2 Templates.

Backend: Python, Flask Framework.

Execution: Subprocess module (for running system compilers like gcc, g++, and javac

Getting Started

Prerequisites

Ensure you have the following installed on your system:

1. Python 3.x

2. Flask: pip install flask

3. Compilers: * gcc (for C)

g++ (for C++)

jdk (for Java)

Installation & Setup

1. Clone the repository:

bash

git clone https://github.com /Yatharth-15/Code-Runner.git cd Code-Runner

2. Run the application:

   bash

python app.py

3.

Access the web app: Open your browser and go to http://127.0.0.1:5000

How It Works

1. Input: The user writes code in the textarea and selects a language.

2. Processing: The Flask backend receives the code via a POST request.

3. Execution:

The code is saved to a temporary file.

The server uses the subprocess module to call the respective compiler/interpreter.

User inputs are passed into the standard input (stdin) of the running process.

4. Output: The result (or error message) is captured and displayed back on the webpage.
