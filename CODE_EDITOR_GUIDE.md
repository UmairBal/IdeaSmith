# 💻 Code Editor Guide

## Features Added

### 1. **File Explorer** (Left Sidebar)
- **File Management**: Create, view, and delete files
- **Language Detection**: Automatically detects language from file extension
- **Quick Navigation**: Click files to open them
- **Right-Click Delete**: Delete files with confirmation
- **File Icons**: Visual indicators for different file types (🐍 Python, 📜 JavaScript, 🌐 HTML, { } JSON)

### 2. **Code Editor** (Center)
- **Multi-File Support**: Edit multiple files, easily switch between them
- **Syntax Highlighting**: Ready for extensions (using textarea with monospace font)
- **Tab System**: Each open file gets its own tab
- **Character Counter**: Real-time character count display
- **Language Selector**: Switch between Python, JavaScript, HTML, and JSON
- **Auto-Save**: Content saves when switching files or running code

### 3. **Code Runner** (▶ Run Button)
- **Python Execution**: Run Python scripts with full output
- **JavaScript Execution**: Execute Node.js code (requires Node.js installed)
- **JSON Validation**: Validate JSON syntax
- **HTML Preview**: Check HTML validity
- **5-Second Timeout**: Prevents infinite loops
- **Error Handling**: Clear error messages for debugging

### 4. **Output Panel** (Right Side)
- **Real-Time Display**: Shows code execution results
- **Error Messages**: Red text for errors
- **Success Messages**: Green text for successful execution
- **Auto-Clear**: Clear button to reset output
- **Scrollable**: Long outputs are scrollable

---

## How to Use

### Running Python Code
```python
# example.py
print("Hello, World!")
for i in range(5):
    print(f"Count: {i}")
```
1. Click the **Code Editor** tab in navigation
2. Create a new file or edit existing `index.py`
3. Paste your Python code
4. Click **▶ Run**
5. See output in the right panel

### Running JavaScript
```javascript
// script.js
console.log("Hello, World!");
for (let i = 0; i < 5; i++) {
  console.log(`Count: ${i}`);
}
```
1. Select `JavaScript` from language dropdown
2. Paste your code
3. Click **▶ Run**
4. Output appears in real-time

### Creating New Files
1. Click the **➕ New File** button
2. Enter filename with extension (e.g., `test.py`, `app.js`)
3. File appears in explorer
4. Start coding!

### File Management
- **Create**: Click ➕ New File
- **Switch**: Click any file in left sidebar
- **Delete**: Right-click file → Confirm deletion
- **Languages**: Auto-detected from extension

---

## Supported Languages

| Language   | File Extension | Support Level |
|-----------|-----------------|----------------|
| Python    | `.py`          | ✅ Full (via Python 3) |
| JavaScript| `.js`          | ✅ Full (via Node.js) |
| HTML      | `.html`        | ⚠️ Validation only |
| JSON      | `.json`        | ✅ Validation |

---

## Requirements

- **Python 3**: For Python code execution
- **Node.js**: For JavaScript code execution (optional)

Install on Windows (if needed):
```bash
# Python (usually pre-installed)
python --version

# Node.js (from https://nodejs.org/)
npm --version
```

---

## Technical Details

### Backend Endpoint
```
POST /execute-code
Body: { "code": "...", "language": "python|javascript|html|json" }
Response: { "output": "..." } or { "error": "..." }
```

### File Storage
- Files are stored in browser localStorage
- Persists between sessions
- Maximum size: ~5-10MB per browser

### Security
- 5-second execution timeout
- Sandboxed subprocess execution
- No direct filesystem access

---

## Tips & Tricks

1. **Quick Testing**: Use the editor for rapid prototyping
2. **Debugging**: Use print/console.log to debug code
3. **Multiple Files**: Create multiple files and organize your project
4. **Copy Output**: Click in output area to select and copy
5. **Language Switching**: Change language dropdown to format code differently

---

## Troubleshooting

### "Python interpreter not found"
- Install Python from python.org
- Ensure it's in your system PATH

### "Node.js not found"
- Install Node.js from nodejs.org
- Restart your browser

### Code doesn't run
- Check for syntax errors
- Ensure correct language is selected
- Check timeout (max 5 seconds)

### Files disappearing
- Files are stored locally in your browser
- Clearing cache will delete them
- Export important code elsewhere

---

## Future Enhancements

Potential features to add:
- [ ] Syntax highlighting with CodeMirror
- [ ] More languages (Java, C++, etc.)
- [ ] File import/export (zip download)
- [ ] Collaborative editing
- [ ] Code formatting/linting
- [ ] Debug mode with breakpoints
- [ ] Package manager integration (pip, npm)
