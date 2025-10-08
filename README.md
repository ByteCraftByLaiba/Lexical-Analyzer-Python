# 🧩 Lexical Analyzer (Python)

A feature-rich **Lexical Analyzer** written in Python that performs tokenization and lexical analysis of source code.  
It supports **interactive CLI menus**, **colorized output**, **token type testing**, and **error reporting**, making it perfect for compiler design students and enthusiasts.

---

## 🚀 Features

- 🧠 **Classifies tokens** into:
  - Keywords
  - Identifiers
  - Operators
  - Literals
  - Punctuations
  - Special Characters
  - Constants
- 🌈 **Color-coded output** using `colorama`
- 📊 **Tabular token display** using `tabulate`
- 📁 **Export results** to `Token.txt` and `Error.txt`
- ⚙️ **Interactive CLI menu** for loading, analyzing, and viewing results
- 🧪 **Test token types** manually
- 🧼 **Error detection and reporting**

---

## 🧰 Requirements

Make sure you have **Python 3.7+** installed.

Install required libraries:
```bash
pip install colorama tabulate
````

---

## 💻 Usage

### 1️⃣ Run the Analyzer

```bash
python lexical_analyzer.py
```

### 2️⃣ Main Menu Options

| Option | Description                              |
| ------ | ---------------------------------------- |
| 1      | Load Source Code (manually or from file) |
| 2      | Analyze Code                             |
| 3      | View Token Types                         |
| 4      | Show Errors                              |
| 5      | Export Files                             |
| 6      | Test Token Type                          |
| 7      | Exit                                     |

---

## 🧪 Example

**Input:**

```cpp
int main() {
    float x = 3.14;
    if (x > 0) {
        cout << "Positive";
    }
}
```

**Output (terminal view):**

```
Keyword: int (Line 1)
Identifier: main (Line 1)
Punctuation: ( (Line 1)
Punctuation: ) (Line 1)
...
Operator: = (Line 2)
Literal: 3.14 (Line 2)
...
```

**Token.txt (exported file):**

```
TOKEN COUNTS:
Keyword: 2
Identifier: 3
Operator: 4
Literal: 1
Total: 15

ALL TOKENS:
Keyword: int (Line 1)
Identifier: main (Line 1)
...
```

---

## 📂 Project Structure

```
Lexical-Analyzer-Python/
│
├── lexical_analyzer.py     # Main program file
├── Token.txt               # Generated tokens file (after analysis)
├── Error.txt               # Generated errors file (after analysis)
└── README.md               # Project documentation
```

---

## 🧑‍💻 Author

**Laiba Shahab**

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify it.

---

## ⭐ Acknowledgements

Special thanks to compiler design concepts and tools that inspired this educational project.

---

Would you like me to make the README **include images (e.g., terminal screenshots)** or **GitHub badges** (like Python version, MIT license, etc.) for a more polished look?
```
