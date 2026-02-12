import streamlit as st
import os
from datetime import datetime
from utils.pdf_processor import PDFProcessor
from utils.summarizer import Summarizer
from utils.note_manager import NoteManager
from utils.audio_player import AudioPlayer
from utils.database import Database

# Page configuration
st.set_page_config(
    page_title="PDF Summarizer & Note-Taking Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'current_pdf' not in st.session_state:
    st.session_state.current_pdf = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None

# Initialize utilities
@st.cache_resource
def init_utilities():
    return {
        'pdf_processor': PDFProcessor(),
        'summarizer': Summarizer(),
        'note_manager': NoteManager(),
        'audio_player': AudioPlayer(),
        'database': Database()
    }

utils = init_utilities()

# Custom CSS
st.markdown("""
<style>
    /* ---------- Design tokens (light & dark aware) ---------- */
    :root {
        --primary-color: #2563eb;
        --primary-color-soft: rgba(37, 99, 235, 0.08);
        --background-color: #f3f4f6;
        --surface-color: #ffffff;
        --surface-muted: #f9fafb;
        --border-subtle: #e5e7eb;
        --text-color: #0f172a;
        --text-muted: #6b7280;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #020617;
            --surface-color: #020617;
            --surface-muted: #020617;
            --border-subtle: #1f2937;
            --text-color: #e5e7eb;
            --text-muted: #9ca3af;
            --primary-color-soft: rgba(37, 99, 235, 0.16);
        }
    }

    /* Override Streamlit theme vars to keep consistent palette */
    :root {
        --primaryColor: var(--primary-color);
        --backgroundColor: var(--background-color);
        --secondaryBackgroundColor: var(--surface-color);
        --textColor: var(--text-color);
        --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* ---------- Global layout ---------- */
    .stApp {
        background: radial-gradient(circle at top, rgba(15, 23, 42, 0.08), transparent 55%),
                    radial-gradient(circle at bottom, rgba(37, 99, 235, 0.06), transparent 60%),
                    var(--background-color);
        color: var(--text-color);
    }

    [data-testid="stAppViewContainer"] {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Page shell card */
    .app-shell {
        background-color: var(--surface-color);
        border-radius: 18px;
        padding: 1.75rem 2rem 2.25rem 2rem;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    }

    /* ---------- Typography & headings ---------- */
    body {
        font-family: var(--font);
        color: var(--text-color);
    }

    .main-header {
        font-size: 2.25rem;
        line-height: 1.15;
        font-weight: 700;
        color: var(--text-color);
        text-align: left;
        margin-bottom: 0.35rem;
    }

    .main-subtitle {
        font-size: 0.98rem;
        color: var(--text-muted);
        margin-bottom: 1.75rem;
        max-width: 36rem;
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 0.75rem;
    }

    .section-caption {
        font-size: 0.86rem;
        color: var(--text-muted);
        margin-bottom: 0.25rem;
    }

    /* Remove aggressive blue text selection */
    *::selection {
        background: rgba(148, 163, 184, 0.28);
        color: inherit;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background-color: var(--surface-color);
        border-right: 1px solid var(--border-subtle);
    }

    [data-testid="stSidebar"] .sidebar-content {
        padding-top: 1.5rem;
    }

    /* Navigation labels */
    [data-testid="stSidebar"] h3 {
        font-size: 0.9rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
    }

    /* Radio menu as vertical nav */
    [data-baseweb="radio"] > div {
        gap: 0.35rem;
    }

    [data-baseweb="radio"] label {
        padding: 0.4rem 0.75rem;
        border-radius: 999px;
        transition: background-color 0.15s ease, color 0.15s ease;
    }

    [data-baseweb="radio"] label > div:first-child {
        margin-right: 0.35rem;
    }

    [data-baseweb="radio"] input:checked + label {
        background-color: var(--primary-color-soft);
        color: var(--primary-color);
    }

    /* Sidebar metrics & badges */
    .sidebar-pill {
        border-radius: 10px;
        background-color: var(--surface-muted);
        border: 1px solid var(--border-subtle);
        padding: 0.6rem 0.75rem;
        font-size: 0.9rem;
    }

    /* ---------- Cards & content containers ---------- */
    .section-card {
        background-color: var(--surface-color);
        border-radius: 14px;
        padding: 1.1rem 1.25rem 1.3rem 1.25rem;
        border: 1px solid var(--border-subtle);
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
        margin-bottom: 1rem;
    }

    .section-card + .section-card {
        margin-top: 0.35rem;
    }

    .note-card {
        background-color: var(--surface-muted);
        padding: 0.9rem 1rem;
        border-radius: 10px;
        margin: 0.35rem 0;
        border: 1px solid var(--border-subtle);
    }

    .summary-box {
        background-color: var(--surface-muted);
        padding: 1.25rem 1.4rem;
        border-radius: 12px;
        margin: 0.75rem 0 0.25rem 0;
        border: 1px solid var(--border-subtle);
        font-size: 0.96rem;
        line-height: 1.6;
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploaderDropzone"] {
        background-color: var(--surface-muted);
        border-radius: 14px;
        border: 1px dashed rgba(148, 163, 184, 0.9);
        padding: 1.25rem 1.4rem;
    }

    [data-testid="stFileUploaderDropzone"] > div {
        color: var(--text-muted);
    }

    /* ---------- Buttons ---------- */
    .stButton>button {
        border-radius: 999px;
        padding: 0.42rem 1.35rem;
        font-weight: 600;
        border: 1px solid var(--primary-color);
        background: linear-gradient(135deg, var(--primary-color), #1d4ed8);
        color: #ffffff;
        font-size: 0.9rem;
    }

    .stButton>button:hover {
        border-color: #1d4ed8;
        background: linear-gradient(135deg, #1d4ed8, var(--primary-color));
        color: #ffffff;
    }

    .stButton>button[kind="secondary"] {
        background: transparent;
        color: var(--text-color);
        border-color: rgba(148, 163, 184, 0.9);
    }

    .stButton>button[kind="secondary"]:hover {
        background: rgba(148, 163, 184, 0.12);
    }

    /* ---------- Inputs, selects, sliders ---------- */
    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input {
        border-radius: 9px;
        background-color: var(--surface-muted);
    }

    .stSlider > div > div > div {
        color: var(--primary-color);
    }

    /* Metrics */
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio(
        "Choose a page:",
        ["PDF Upload & Summary", "Notes Manager", "Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Current session")
    if st.session_state.current_pdf:
        st.success(f"Active PDF: {st.session_state.current_pdf}")
    else:
        st.info("No PDF loaded")
    
    st.metric("Notes Created", len(st.session_state.notes))
    
    st.markdown("---")
    st.markdown("### Quick actions")
    if st.button("Clear all data", type="secondary"):
        st.session_state.notes = []
        st.session_state.current_pdf = None
        st.session_state.summary = None
        st.session_state.extracted_text = None
        st.rerun()

# Main content
if page == "PDF Upload & Summary":
    st.markdown(
        """
        <div class="app-shell">
            <div class="main-header">PDF Summarizer &amp; Note‑Taking</div>
            <p class="main-subtitle">
                Upload PDF documents, generate concise AI summaries, and capture structured notes in a single workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown("<div class='app-shell' style='margin-top:1.25rem;'>", unsafe_allow_html=True)

        # PDF Upload Section
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Upload PDF document</div>", unsafe_allow_html=True)
        st.markdown(
            "<p class='section-caption'>Choose a file to extract the full text and generate summaries.</p>",
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF document to extract text and generate summaries"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if uploaded_file:
            st.session_state.current_pdf = uploaded_file.name

            # Save uploaded file temporarily
            temp_path = f"data/{uploaded_file.name}"
            os.makedirs("data", exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract text
            with st.spinner("Extracting text from PDF..."):
                extracted_text = utils['pdf_processor'].extract_text(temp_path)
                st.session_state.extracted_text = extracted_text
                total_pages = utils['pdf_processor'].get_page_count(temp_path)

            st.success(f"Successfully extracted text from {total_pages} pages.")

            # Metrics card
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            cols = st.columns(3)
            with cols[0]:
                st.metric("Total pages", total_pages)
            with cols[1]:
                st.metric("Total words", len(extracted_text.split()))
            with cols[2]:
                st.metric("Characters", len(extracted_text))
            st.markdown("</div>", unsafe_allow_html=True)

            # Summarization options card
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Generate summary</div>", unsafe_allow_html=True)

            col1, col2 = st.columns([2, 1])

            with col1:
                summary_type = st.selectbox(
                    "Summary type",
                    ["Full Document", "Single Page", "Page Range", "Key Points"],
                    help="Choose the type of summary you want to generate"
                )

            with col2:
                summary_length = st.select_slider(
                    "Summary length",
                    options=["Brief", "Moderate", "Detailed"],
                    value="Moderate"
                )

            # Page selection for single page or range
            if summary_type == "Single Page":
                page_num = st.number_input(
                    "Select page number",
                    min_value=1,
                    max_value=total_pages,
                    value=1
                )
            elif summary_type == "Page Range":
                col1, col2 = st.columns(2)
                with col1:
                    start_page = st.number_input("Start page", min_value=1, max_value=total_pages, value=1)
                with col2:
                    end_page = st.number_input(
                        "End page",
                        min_value=start_page,
                        max_value=total_pages,
                        value=min(start_page + 5, total_pages),
                    )

            # Generate summary button
            if st.button("Generate summary", type="primary"):
                with st.spinner("Generating AI summary..."):
                    if summary_type == "Full Document":
                        summary = utils['summarizer'].summarize(extracted_text, summary_length)
                    elif summary_type == "Single Page":
                        page_text = utils['pdf_processor'].extract_page_text(temp_path, page_num - 1)
                        summary = utils['summarizer'].summarize(page_text, summary_length)
                    elif summary_type == "Page Range":
                        range_text = utils['pdf_processor'].extract_page_range(
                            temp_path, start_page - 1, end_page - 1
                        )
                        summary = utils['summarizer'].summarize(range_text, summary_length)
                    else:  # Key Points
                        summary = utils['summarizer'].extract_key_points(extracted_text)

                    st.session_state.summary = summary

                st.success("Summary generated successfully.")

            st.markdown("</div>", unsafe_allow_html=True)

            # Display summary and actions card
            if st.session_state.summary:
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>Summary</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='summary-box'>{st.session_state.summary}</div>",
                    unsafe_allow_html=True,
                )

                # Audio playback
                st.markdown("<div class='section-title' style='margin-top:1.1rem;'>Text-to-speech</div>", unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])

                with col1:
                    voice_type = st.selectbox("Voice type", ["Male", "Female", "Neutral"])

                with col2:
                    speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.1)

                if st.button("Play audio", type="secondary"):
                    with st.spinner("Generating audio..."):
                        audio_file = utils['audio_player'].text_to_speech(
                            st.session_state.summary,
                            voice_type,
                            speed
                        )
                        if audio_file and os.path.exists(audio_file):
                            st.audio(audio_file)
                        else:
                            st.warning("Audio generation is not available (requires API keys).")

                st.markdown("---")
                if st.button("Save summary as note"):
                    note = {
                        'id': len(st.session_state.notes) + 1,
                        'title': f"Summary: {st.session_state.current_pdf}",
                        'content': st.session_state.summary,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'source': st.session_state.current_pdf,
                        'type': summary_type
                    }
                    st.session_state.notes.append(note)
                    utils['database'].save_note(note)
                    st.success("Summary saved to notes.")

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Notes Manager":
    st.markdown(
        """
        <div class="main-header">Notes manager</div>
        <p class="main-subtitle">Browse, search, and export the insights you have captured from your documents.</p>
        """,
        unsafe_allow_html=True,
    )
    
    # Create new note
    with st.expander("Create new note", expanded=False):
        note_title = st.text_input("Note Title", placeholder="Enter note title...")
        note_content = st.text_area(
            "Note Content",
            placeholder="Write your note here...",
            height=200
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Save note", type="primary"):
                if note_title and note_content:
                    note = {
                        'id': len(st.session_state.notes) + 1,
                        'title': note_title,
                        'content': note_content,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'source': 'Manual Entry',
                        'type': 'Custom Note'
                    }
                    st.session_state.notes.append(note)
                    utils['database'].save_note(note)
                    st.success("Note saved.")
                    st.rerun()
                else:
                    st.error("Please fill in both title and content")
    
    st.markdown("---")
    
    # Display notes
    st.markdown("### Your notes")
    
    if st.session_state.notes:
        # Search and filter
        search_term = st.text_input("Search notes", placeholder="Search by title or content...")
        
        filtered_notes = st.session_state.notes
        if search_term:
            filtered_notes = [
                note for note in st.session_state.notes
                if search_term.lower() in note['title'].lower() or
                   search_term.lower() in note['content'].lower()
            ]
        
        st.markdown(f"Showing {len(filtered_notes)} of {len(st.session_state.notes)} notes")
        
        # Display each note
        for note in reversed(filtered_notes):
            with st.container():
                st.markdown(f"""
                <div class="note-card">
                    <h3>{note['title']}</h3>
                    <p><small>{note['timestamp']} &nbsp;|&nbsp; Source: {note['source']}</small></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(note['content'])
                
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("Delete", key=f"delete_{note['id']}"):
                        st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note['id']]
                        utils['database'].delete_note(note['id'])
                        st.rerun()
                
                with col2:
                    if st.button("Export", key=f"export_{note['id']}"):
                        utils['note_manager'].export_note(note, format='txt')
                        st.success("Note exported!")
                
            st.markdown("---")
    else:
        st.info("No notes yet. Upload a PDF and generate summaries, or create a custom note.")
    
else:  # Settings page
    st.markdown(
        """
        <div class="main-header">Settings</div>
        <p class="main-subtitle">Connect APIs, configure text‑to‑speech, and manage data storage for your workspace.</p>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("### API configuration")
    st.info("Configure your API keys for enhanced functionality")
    
    with st.expander("OpenAI configuration", expanded=True):
        openai_key = st.text_input("OpenAI API Key", type="password", help="For advanced summarization")
        if openai_key:
            os.environ['OPENAI_API_KEY'] = openai_key
            st.success("OpenAI key configured.")
    
    with st.expander("Text-to-speech configuration"):
        tts_provider = st.selectbox("TTS Provider", ["Google TTS", "Azure TTS", "ElevenLabs"])
        if tts_provider != "Google TTS":
            tts_key = st.text_input(f"{tts_provider} API Key", type="password")
    
    st.markdown("---")
    
    st.markdown("### Database settings")
    with st.expander("MongoDB configuration"):
        mongo_uri = st.text_input("MongoDB URI", value="mongodb://localhost:27017/", help="Your MongoDB connection string")
        db_name = st.text_input("Database Name", value="pdf_summarizer")
        
        if st.button("Test connection"):
            if utils['database'].test_connection(mongo_uri, db_name):
                st.success("Database connection successful.")
            else:
                st.warning("Could not connect to database. Using local storage instead.")
    
    st.markdown("---")
    
    st.markdown("### Data management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export all notes"):
            export_file = utils['note_manager'].export_all_notes(st.session_state.notes)
            st.success(f"Notes exported to {export_file}.")
    
    with col2:
        if st.button("Back up to database"):
            for note in st.session_state.notes:
                utils['database'].save_note(note)
            st.success("All notes backed up to database.")
            
# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 2rem; font-size: 0.9rem;'>
    <p>PDF Summarizer &amp; Note-Taking Tool · Built with Streamlit, LangChain &amp; AI</p>
</div>
""", unsafe_allow_html=True)
