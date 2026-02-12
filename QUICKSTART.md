# ⚡ Quick Start Guide - Get Running in 5 Minutes

## For Complete Beginners

### Step 1: Install Python (if you don't have it)
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. **Important**: Check "Add Python to PATH" during installation
4. Click Install

### Step 2: Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac**: Press `Cmd + Space`, type `terminal`, press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 3: Navigate to Project Folder
```bash
# Replace with your actual path
cd path/to/pdf_summarizer_app

# Example Windows:
cd C:\Users\YourName\Downloads\pdf_summarizer_app

# Example Mac/Linux:
cd ~/Downloads/pdf_summarizer_app
```

### Step 4: Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your command line.

### Step 5: Install Everything
```bash
pip install -r requirements.txt
```

Wait 2-5 minutes for installation to complete.

### Step 6: Run the Application
```bash
streamlit run app.py
```

### Step 7: Use the App
- Your browser will open automatically
- If not, go to: http://localhost:8501
- Upload a PDF and start summarizing!

---

## Stopping the App

Press `Ctrl + C` in the terminal

---

## Common First-Time Issues

### "pip: command not found"
**Solution:**
```bash
python -m pip install -r requirements.txt
```

### "streamlit: command not found"
**Solution:**
Make sure virtual environment is activated (you should see `(venv)`)

### Still Having Issues?
See SETUP_GUIDE.md for detailed troubleshooting

---

## First Time Using the App?

### Try This:
1. **Upload a PDF**: Click "Browse files" on the main page
2. **Generate Summary**: Choose "Full Document" and "Moderate"
3. **Play Audio**: Scroll down and click "Play Audio"
4. **Save Note**: Click "Save Summary as Note"
5. **View Notes**: Go to "Notes Manager" page

---

## No API Keys Needed!

The app works immediately with:
- ✅ PDF text extraction
- ✅ Basic summarization
- ✅ Note-taking
- ✅ Text-to-speech (requires internet)
- ✅ Local storage

Add API keys later for enhanced features!

---

## What's Next?

### Want Better Summaries?
1. Get free OpenAI API key: https://platform.openai.com
2. Create `.env` file in project folder
3. Add: `OPENAI_API_KEY=your-key-here`
4. Restart app

### Want Permanent Storage?
1. Install MongoDB (optional)
2. Configure in Settings page
3. All notes will be saved to database

---

## Quick Commands Reference

```bash
# Activate environment (do this every time)
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run app
streamlit run app.py

# Stop app
Ctrl + C

# Deactivate environment when done
deactivate
```

---

## Need Help?

1. Check SETUP_GUIDE.md for detailed instructions
2. Check README.md for feature documentation
3. Run `python test_components.py` to test setup

---

**That's it! You're ready to go! 🎉**

Start the app and upload your first PDF!
