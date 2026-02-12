# 📚 PDF Summarizer & Note-Taking Tool

A comprehensive Streamlit-based application that supports PDF summarization, note-taking, and audio playback using AI and LLM APIs.

## 🌟 Features

### PDF Processing
- ✅ Upload and extract text from PDF documents
- ✅ Single page, multi-page, and page range summarization
- ✅ Automatic text extraction with page tracking
- ✅ PDF metadata extraction

### AI-Powered Summarization
- ✅ Multiple summary lengths (Brief, Moderate, Detailed)
- ✅ Full document summarization
- ✅ Single page summarization
- ✅ Page range summarization
- ✅ Key points extraction
- ✅ Integration with OpenAI/LangChain for advanced summaries
- ✅ Fallback extractive summarization (no API required)

### Note Management
- ✅ Create custom notes manually
- ✅ Save summaries as notes automatically
- ✅ Search and filter notes
- ✅ Export notes (TXT, MD, JSON formats)
- ✅ Batch export all notes
- ✅ Note statistics and analytics

### Text-to-Speech
- ✅ Convert summaries to audio
- ✅ Multiple voice types (Male, Female, Neutral)
- ✅ Adjustable playback speed
- ✅ Google TTS and pyttsx3 support
- ✅ Audio file management

### Database Integration
- ✅ MongoDB integration for persistent storage
- ✅ Automatic backup and restore
- ✅ Local file storage fallback
- ✅ Database statistics and monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Optional: MongoDB (for database features)

### Installation

1. **Clone or download the project**
```bash
cd pdf_summarizer_app
```

2. **Create a virtual environment (recommended)**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional)**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
# For basic functionality, this is optional
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload a PDF

1. Navigate to **"📄 PDF Upload & Summary"** page
2. Click **"Browse files"** and select a PDF
3. The app will automatically extract text and display document info

### 2. Generate Summaries

1. Choose your summary type:
   - **Full Document**: Summarize entire PDF
   - **Single Page**: Summarize one specific page
   - **Page Range**: Summarize a range of pages
   - **Key Points**: Extract main bullet points

2. Select summary length:
   - **Brief**: 2-3 sentences
   - **Moderate**: Comprehensive overview
   - **Detailed**: In-depth summary with details

3. Click **"🚀 Generate Summary"**

### 3. Text-to-Speech

1. After generating a summary, scroll to the **"🔊 Text-to-Speech"** section
2. Select voice type and speed
3. Click **"🎵 Play Audio"**
4. Audio player will appear with the generated speech

### 4. Manage Notes

1. Navigate to **"📝 Notes Manager"** page
2. **Create new notes**: Use the "Create New Note" expander
3. **Search notes**: Use the search bar to filter
4. **Export notes**: Click export on individual notes or export all
5. **Delete notes**: Remove unwanted notes

### 5. Configure Settings

1. Navigate to **"⚙️ Settings"** page
2. **API Configuration**: Add OpenAI API key for advanced features
3. **Database Settings**: Configure MongoDB connection
4. **Data Management**: Export or backup your data

## 🔧 Configuration

### API Keys (Optional)

For enhanced functionality, you can configure API keys:

#### OpenAI (for advanced summarization)
1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env` file: `OPENAI_API_KEY=your_key_here`

#### MongoDB (for persistent storage)
1. Install MongoDB locally or use MongoDB Atlas
2. Update `.env`: `MONGODB_URI=your_connection_string`

### Without API Keys

The application works without any API keys using:
- Extractive summarization (built-in algorithm)
- Google TTS (free, no key required)
- Local file storage for notes

## 📁 Project Structure

```
pdf_summarizer_app/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── pdf_processor.py       # PDF text extraction
│   ├── summarizer.py          # AI summarization
│   ├── note_manager.py        # Note management
│   ├── audio_player.py        # Text-to-speech
│   └── database.py            # MongoDB integration
│
├── data/                      # Data storage
│   ├── notes/                 # Saved notes (JSON)
│   └── audio/                 # Generated audio files
│
└── exports/                   # Exported files
```

## 🎯 Key Features Explained

### LangChain Pipeline

When OpenAI API key is configured:
- Uses LangChain's `load_summarize_chain`
- Implements map-reduce for long documents
- Splits text intelligently for processing
- Generates coherent, AI-powered summaries

### MongoDB Storage

When MongoDB is connected:
- Persistent note storage
- Full-text search capabilities
- Automatic backup and restore
- Statistics and analytics

### Extractive Summarization (Fallback)

When no API key is provided:
- Scores sentences based on importance
- Considers word frequency and position
- Selects top-ranked sentences
- Maintains original order

## 🛠️ Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### MongoDB connection failed
- Check if MongoDB is running: `mongod --version`
- Verify connection string in settings
- App works fine without MongoDB (uses local storage)

### Audio not generating
- Install required packages: `pip install gTTS pyttsx3`
- Check internet connection for Google TTS
- Use pyttsx3 for offline audio generation

### PDF extraction issues
- Ensure PDF is not password-protected
- Try with a different PDF file
- Check PDF file size (large files may take longer)

## 📊 System Requirements

### Minimum
- Python 3.8+
- 2GB RAM
- 500MB disk space

### Recommended
- Python 3.10+
- 4GB RAM
- 1GB disk space
- MongoDB installed
- OpenAI API key

## 🔐 Privacy & Security

- All processing happens locally
- API keys stored in environment variables
- Notes stored locally or in your MongoDB instance
- No data sent to third parties (except API providers when keys are used)

## 🚀 Advanced Features

### Batch Processing
- Process multiple PDFs in sequence
- Bulk export notes
- Automated summarization workflows

### Custom Prompts
- Modify summarization prompts in `summarizer.py`
- Adjust extractive algorithm parameters
- Customize audio voice settings

### Integration
- MongoDB for enterprise storage
- REST API endpoints (can be added)
- CI/CD pipeline integration

## 📝 Development

### Adding New Features

1. **New utility module**: Add to `utils/` directory
2. **New page**: Add to main `app.py`
3. **New dependency**: Update `requirements.txt`

### Code Structure

- **app.py**: Main UI and navigation
- **utils/**: Business logic and processing
- **data/**: Runtime data storage

## 🤝 Contributing

This is a portfolio project. Feel free to:
- Fork and modify for your needs
- Report issues or bugs
- Suggest improvements

## 📄 License

This project is open source and available for educational purposes.

## 🎓 Learning Resources

### Streamlit
- Official docs: https://docs.streamlit.io
- Tutorial: Build data apps quickly

### LangChain
- Documentation: https://python.langchain.com
- Learn about chains and agents

### MongoDB
- Getting started: https://docs.mongodb.com
- Python integration guide

## 💡 Tips for Best Results

1. **PDF Quality**: Use text-based PDFs (not scanned images)
2. **Summary Length**: Start with "Moderate" and adjust
3. **Page Range**: For long documents, summarize in chunks
4. **Notes**: Add context to your notes for better organization
5. **Backup**: Regularly export notes to avoid data loss

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review requirements and installation steps
3. Ensure all dependencies are installed
4. Try without API keys first (basic functionality)

---

**Built with ❤️ using Streamlit, LangChain, and Python**

*April-May 2025 Portfolio Project*
