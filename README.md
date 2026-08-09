# Code Runner - Multi-Language Web IDE

Code Runner is a simple yet powerful Web IDE built with **Python (Flask)**. It allows you to write, compile, and run code in **Python, C, C++, and Java** directly in your browser.

---

## Features

*   **Interactive Terminal:** Stream compilation and program outputs in real-time, with full standard input (stdin) support.
*   **Dracula Syntax Highlighter:** Beautiful syntax coloring for code editing powered by CodeMirror.
*   **Split Layout:** Clean side-by-side split layout (Code Editor on the left, Terminal on the right).
*   **Save File:** Download code files locally with custom filenames and automatic extensions.
*   **SQLite Auth:** Safe user authentication using SQLite database and secure password hashing. Bypasses to a guest account for direct links.

---

## Project Structure

*   `app.py` - Flask server launcher.
*   `auth_module.py` - Authentication logic and database tables.
*   `editor_module.py` - Non-blocking process execution engine and SSE outputs.
*   `editor.html` - The frontend workspace template.
*   `database.db` - SQLite database storing user hashes.

---

## 🚀 Setup & Execution

### 1. Prerequisites (Compiler Command Setup)

Open your terminal or command prompt and run the commands for your operating system:

#### **Windows (CMD/PowerShell):**
```powershell
# Install Python & Java JDK
winget install Python.Python.3
winget install Eclipse.Temurin.17.JDK

# Install C/C++ compiler (Install MSYS2 and run this inside MSYS2 terminal)
winget install MSYS2.MSYS2
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-g++
```
*(Make sure to add Python, Java, and MinGW `bin` directories to your System Environment variables PATH).*

#### **macOS:**
```bash
# Install Python & Java JDK
brew install python
brew install openjdk

# Install C/C++ compiler tools
xcode-select --install
```

#### **Linux (Ubuntu/Debian):**
```bash
# Install Python, C/C++, and Java JDK
sudo apt update
sudo apt install python3 python3-pip build-essential default-jdk -y
```

---

### 2. Run the Application

Navigate to the project folder and execute:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Now, open your browser and navigate to:
**`http://localhost:5000`**
