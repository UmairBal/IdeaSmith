# 🔨 Developer AI File Generation & Visualization

## Overview

IdeaSmith now automatically generates and visualizes code files created by Developer AI. When you forge a project, the AI creates actual project files with proper folder structure, and you can preview and download them.

---

## How It Works

### 1. **Code Generation**
When Developer AI creates code for a task, it formats it like this:

```
Here's the complete Python chess game:

```main.py
# Main chess game file
import chess

def play_game():
    board = chess.Board()
    ...
```

```app.py
# Game interface
def start_app():
    ...
```
```

### 2. **Automatic File Creation**
- Developer AI extracts code blocks with filenames
- Files are created in `generated_projects/` folder
- Project folder structure is preserved
- Nested folders (e.g., `src/main.py`) are created automatically

### 3. **File Visualization**
In the output cards, generated files appear as clickable tiles:

```
📁 Generated Files
┌─────────┬─────────┬─────────┐
│  🐍     │  📜     │  🌐     │
│ main.py │ app.js  │ index   │
└─────────┴─────────┴─────────┘
```

---

## Using Generated Files

### **View Code**
1. Click any file preview tile
2. A modal opens showing the full code
3. Options to:
   - 📋 **Copy Code** - Copy to clipboard
   - ⬇️ **Download** - Save file to computer

### **File Organization**
- Files are automatically organized in folders
- Project structure matches the task requirements
- Nested files are supported (e.g., `src/components/Button.jsx`)

### **File Icons**
```
🐍 .py      - Python files
📜 .js      - JavaScript files
🌐 .html    - HTML files
{ }  .json  - JSON files
⚛️  .jsx    - React JSX
🎨 .css    - Stylesheets
☕ .java   - Java files
⚙️  .cpp    - C++ files
📝 .md     - Markdown
```

---

## Example Workflow

### **Scenario**: Create a Python Web App

**You Input:**
> "Create a simple Flask web app with a chat interface"

**Developer AI Creates:**
```
app.py - Main Flask application
templates/index.html - Chat interface
static/style.css - Styling
requirements.txt - Dependencies
```

**Result:**
- Folder: `generated_projects/create_a_simple_flask_web_app/`
- Files automatically saved
- Preview tiles show all files
- Click to view, copy, or download

---

## File Structure

Generated files are stored at:
```
IdeaSmith/
├── generated_projects/
│   ├── chess_game/
│   │   ├── main.py
│   │   └── config.py
│   ├── web_app/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── templates/
│   │   │   └── index.html
│   │   └── static/
│   │       └── style.css
```

---

## Code Block Format (for Developers)

When prompting Developer AI to create code, use this format:

### **Single File:**
````
```filename.ext
code content
```
````

### **Multiple Files:**
````
```main.py
# Python code
print("Hello")
```

```app.py
# More code
def hello():
    ...
```
````

### **Nested Folders:**
````
```src/main.py
code here
```

```src/components/Card.jsx
react code
```
````

---

## Features

✅ **Automatic File Generation** - Files created during forge process  
✅ **Folder Structure** - Nested folders preserved  
✅ **File Preview** - Click to view code in modal  
✅ **Copy to Clipboard** - Easy code copying  
✅ **Download Files** - Save individual files  
✅ **File Icons** - Visual language indicators  
✅ **Code Display** - Full syntax preserved  
✅ **Escape HTML** - Safe HTML rendering  

---

## Technical Details

### **Backend Extraction**
- Regex pattern extracts code blocks: ` ```filename\ncontent``` `
- Supports nested paths: `src/components/main.py`
- Creates directories as needed
- Files saved with UTF-8 encoding

### **Frontend Display**
- Files stored in `ps.files` object
- Modal overlay for code viewing
- Clipboard API for copying
- Download via data URLs

### **Security**
- Safe HTML escaping
- No arbitrary file execution
- Files readonly in preview

---

## Example Output

```
OUTPUT:
  📁 Generated Files
  
  🐍 main.py        Click to view Python code
  📜 app.js        Click to view JavaScript code
  🌐 index.html    Click to view HTML structure
  
  Generated Code Output:
  [Full text of the output with code blocks highlighted]
```

---

## Troubleshooting

### **Files not appearing?**
- Check Developer AI status
- Ensure code blocks have filenames
- Check browser console for errors

### **Can't download files?**
- Use "Copy Code" instead
- Save the clipboard text locally
- Browser might block downloads

### **Folder structure not created?**
- Verify filenames include paths (e.g., `src/main.py`)
- Check `generated_projects/` folder on disk

---

## Future Enhancements

- [ ] Zip download for entire project
- [ ] Edit generated files in browser
- [ ] Syntax highlighting with CodeMirror
- [ ] Run Python/Node.js files directly
- [ ] Git repository initialization
- [ ] Live preview for HTML/CSS
- [ ] Code formatting (Prettier, Black)
- [ ] Dependency auto-install

---

## Tips & Tricks

1. **Well-Structured Prompts**: Give clear file structure instructions
   > "Create a React app with:  
   > - src/components/App.jsx  
   > - src/index.js  
   > - src/styles/main.css"

2. **Download All**: Download each file individually, then combine locally

3. **Import to IDE**: Copy code and paste into your favorite IDE

4. **Version Control**: Use downloaded files with Git immediately

5. **Iteration**: Run forge again to regenerate with updates

