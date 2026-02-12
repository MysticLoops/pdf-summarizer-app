# 🚀 Complete Setup Guide for PDF Summarizer & Note-Taking Tool

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Step-by-Step Installation](#step-by-step-installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Optional Enhancements](#optional-enhancements)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Required
- **Python**: Version 3.8 or higher
  - Check: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/

- **pip**: Python package installer (usually comes with Python)
  - Check: `pip --version`

### Optional
- **MongoDB**: For persistent database storage
  - Download: https://www.mongodb.com/try/download/community
  - Alternative: Use MongoDB Atlas (cloud-based, free tier)

---

## Step-by-Step Installation

### Step 1: Get the Project Files

Download or clone the project to your computer:

```bash
# If using git
git clone <repository-url>
cd pdf_summarizer_app

# Or download and extract the ZIP file, then:
cd pdf_summarizer_app
```

### Step 2: Create a Virtual Environment (Recommended)

This keeps your project dependencies isolated from other Python projects.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command line.

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- PyPDF2 (PDF processing)
- LangChain (AI integration)
- OpenAI (AI models)
- PyMongo (MongoDB)
- gTTS (text-to-speech)
- pyttsx3 (offline text-to-speech)
- python-dotenv (environment variables)

**Installation time:** 2-5 minutes depending on your internet connection.

---

## Configuration

### Basic Setup (No API Keys Needed)

The app works out of the box with basic features:
- PDF text extraction ✅
- Extractive summarization ✅
- Google TTS (requires internet) ✅
- Local file storage ✅

**You can skip to "Running the Application" if you want to start immediately!**

### Advanced Setup (Optional)

For enhanced features, configure API keys:

#### 1. Create Environment File

```bash
# Copy the example file
cp .env.example .env

# On Windows, use:
copy .env.example .env
```

#### 2. OpenAI API Key (Optional)

**Benefits:** AI-powered summaries using GPT models

**How to get:**
1. Go to https://platform.openai.com/signup
2. Create an account
3. Navigate to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key

**Add to .env:**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Cost:** Pay-as-you-go (very cheap for summaries, ~$0.01 per page)

#### 3. MongoDB Setup (Optional)

**Benefits:** Persistent storage, search, backups

**Option A: Local MongoDB**
1. Download from https://www.mongodb.com/try/download/community
2. Install and start MongoDB
3. Default connection: `mongodb://localhost:27017/`

**Option B: MongoDB Atlas (Cloud - Free Tier)**
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create free cluster
3. Get connection string
4. Add to .env:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

**Without MongoDB:** App uses local JSON files (works perfectly fine!)

---

## Running the Application

### Start the Application

```bash
streamlit run app.py
```

### What Happens Next

1. Streamlit starts the server
2. Your default browser opens automatically
3. Application loads at `http://localhost:8501`
4. You see the main interface

### If Browser Doesn't Open

Manually open: http://localhost:8501

---

## Optional Enhancements

### 1. Install MongoDB (For Persistent Storage)

**Windows:**
1. Download installer from MongoDB website
2. Run installer (choose "Complete" setup)
3. Install MongoDB Compass (GUI tool)
4. Start MongoDB service

**macOS:**
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mongodb
sudo systemctl start mongodb
```

**Verify MongoDB is running:**
```bash
mongod --version
```

### 2. Text-to-Speech Enhancements

**Google TTS (Default - Free)**
- Requires internet connection
- Good quality
- Multiple languages

**pyttsx3 (Offline)**
- Works offline
- Lower quality
- Faster processing

**Both are already included in requirements.txt!**

---

## Troubleshooting

### Problem: "pip: command not found"

**Solution:**
```bash
# Try python -m pip instead
python -m pip install -r requirements.txt

# Or use python3
python3 -m pip install -r requirements.txt
```

### Problem: "Python not found"

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt

### Problem: "streamlit: command not found"

**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall streamlit
pip install streamlit
```

### Problem: "Module not found" errors

**Solution:**
```bash
# Reinstall all requirements
pip install -r requirements.txt --upgrade
```

### Problem: PDF not loading

**Possible causes:**
- PDF is password-protected → Remove password first
- PDF is corrupted → Try different PDF
- PDF is scanned image → Use OCR tool first

### Problem: MongoDB connection failed

**Solution:**
- Check if MongoDB is running
- Verify connection string in settings
- **Don't worry!** App works without MongoDB (uses local files)

### Problem: Audio not generating

**Solution:**
```bash
# Reinstall audio libraries
pip install gTTS pyttsx3 --upgrade

# Check internet connection (for Google TTS)
# Or use offline mode with pyttsx3
```

### Problem: "Port 8501 already in use"

**Solution:**
```bash
# Kill existing Streamlit process
# Or run on different port
streamlit run app.py --server.port 8502
```

---

## Usage Workflow

### Typical Session

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **Upload a PDF**
   - Click "Browse files"
   - Select your PDF
   - Wait for text extraction

3. **Generate summary**
   - Choose summary type and length
   - Click "Generate Summary"
   - Review the summary

4. **Optional: Listen to audio**
   - Click "Play Audio"
   - Adjust speed if needed

5. **Save as note**
   - Click "Save Summary as Note"
   - Access from Notes Manager

6. **Export notes**
   - Go to Notes Manager
   - Export individual or all notes

---

## Quick Reference Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Deactivate virtual environment
deactivate

# Check Python version
python --version

# Check installed packages
pip list

# Update a specific package
pip install streamlit --upgrade
```

---

## Performance Tips

### For Large PDFs
- Use page range summarization instead of full document
- Break into smaller chunks
- Consider upgrading to OpenAI API for better handling

### For Slow Performance
- Close other browser tabs
- Check system resources (RAM, CPU)
- Restart the application
- Clear browser cache

### For Better Summaries
- Use OpenAI API key for best results
- Choose appropriate summary length
- Review and refine prompts if needed

---

## Next Steps After Installation

1. **Test with sample PDF**: Use a small PDF first
2. **Explore features**: Try different summary types
3. **Create notes**: Test note-taking functionality
4. **Configure APIs**: Add OpenAI key for better summaries
5. **Set up MongoDB**: For persistent storage
6. **Customize**: Modify code to fit your needs

---

## Getting Help

### Resources
- **Streamlit Docs**: https://docs.streamlit.io
- **LangChain Docs**: https://python.langchain.com
- **OpenAI API**: https://platform.openai.com/docs

### Common Questions

**Q: Do I need to pay for anything?**
A: Basic features are free. OpenAI API is pay-as-you-go (very cheap).

**Q: Can I use this offline?**
A: Yes, with extractive summarization and pyttsx3 audio.

**Q: How do I stop the app?**
A: Press Ctrl+C in the terminal.

**Q: Where is my data stored?**
A: In `data/` folder (local) or MongoDB (if configured).

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Application runs successfully
- [ ] Can upload and process PDF
- [ ] Summary generation works
- [ ] Notes can be created and saved
- [ ] (Optional) OpenAI API configured
- [ ] (Optional) MongoDB connected

---

**🎉 Congratulations! You're all set up!**

Start exploring the features and building your PDF summarization workflow!
