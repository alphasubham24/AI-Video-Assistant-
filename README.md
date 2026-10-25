# 🎬 AI Video Assistant (RAG & GenAI)

An intelligent multimodal AI assistant that extracts, transcribes, summarizes, and enables interactive Retrieval-Augmented Generation (RAG) conversational Q&A over YouTube videos and local audio/video media.

---

## 🌟 Features

- **Multimodal Video Ingestion:** Seamlessly download and extract audio from YouTube URLs (including Shorts) via `yt-dlp` or process local media files (`.mp4`, `.mkv`, `.avi`, `.mov`, `.mp3`, `.wav`).
- **Hybrid Speech-to-Text Pipeline:**
  - **English:** High-accuracy local transcription using OpenAI Whisper (`small` model) with thread-safe inference.
  - **Hinglish & Indic Languages:** Integrated with Sarvam AI's Speech-to-Text API (`saaras:v2.5`).
- **Intelligent Long-Form Summarization:** Recursive Map-Reduce summarization using Mistral AI (`open-mistral-7b`) to condense long multi-hour videos into executive summaries, key takeaways, and action items.
- **RAG-Powered Q&A:** Vector storage powered by **ChromaDB** and Hugging Face sentence embeddings (`all-MiniLM-L6-v2`), enabling low-latency, context-grounded Q&A over video transcripts with citations.
- **Dual Interfaces:**
  - **Streamlit Web Application (`app.py`):** Interactive UI with side-by-side video playback, summary cards, and real-time chat.
  - **CLI Terminal (`main.py`):** Headless, lightweight execution for scripting, automation, and quick terminal queries.

---

## 🛠️ Architecture

```
[YouTube URL / Local Video]
            │
            ▼
[Audio Processing & 16kHz Mono Conversion] (FFmpeg & pydub)
            │
    ┌───────┴───────┐
    ▼               ▼
[OpenAI Whisper] [Sarvam AI API]
(English)        (Hinglish/Indic)
    └───────┬───────┘
            ▼
[Full Video Transcript]
            │
    ┌───────┴───────────────────────┐
    ▼                               ▼
[Map-Reduce Summarizer]     [Text Splitter & Chunking]
    │                               │
    ▼                               ▼
[Executive Summary]         [HuggingFace Embeddings]
                                    │
                                    ▼
                            [ChromaDB Vector Store]
                                    │
                                    ▼
                            [RAG Q&A Engine (Mistral LLM)]
```

---

## 💻 Tech Stack

- **Large Language Models:** Mistral AI (`open-mistral-7b`) via `langchain-mistralai`
- **Vector Database:** ChromaDB (`langchain-chroma`)
- **Embeddings:** Hugging Face Sentence Transformers (`all-MiniLM-L6-v2`)
- **Speech-to-Text:** OpenAI Whisper, Sarvam AI (`saaras:v2.5`)
- **Media Ingestion:** `yt-dlp`, FFmpeg, `pydub`
- **Orchestration:** LangChain Core, Community, and Text Splitters
- **Frontend:** Streamlit

---

## 📋 Prerequisites

- Python 3.10+ (Recommended: Python 3.11)
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to your system `PATH`
- API Keys:
  - [Mistral AI API Key](https://console.mistral.ai/)
  - [Sarvam AI API Key](https://www.sarvam.ai/) (optional, required for Hinglish transcription)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/alphasubham24/AI-Video-Assistant-.git
cd AI-Video-Assistant-
```

### 2. Set Up Virtual Environment

```bash
# Using standard venv
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate on Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r Requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (or copy `.env.example`):

```bash
cp .env.example .env
```

Add your API credentials inside `.env`:

```ini
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=open-mistral-7b
WHISPER_MODEL=small
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_STT_MODEL=saaras:v2.5
```

---

## 🖥️ Running the Application

### Option A: Streamlit Web UI

Launch the modern web dashboard:

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

### Option B: Command Line Interface (CLI)

Run interactively:

```bash
python main.py
```

Or run directly with CLI arguments:

```bash
python main.py "https://youtube.com/shorts/bSSgzbnGba8" english
```

---

## 📂 Project Structure

```
AI-Video-Assistant-/
├── app.py                  # Streamlit Web UI application
├── main.py                 # CLI terminal entrypoint
├── Requirements.txt        # Python package dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Ignored files (venv, keys, vector db, cache)
├── core/
│   ├── extractor.py        # Information extraction & key concept identification
│   ├── rag_engine.py       # Conversational RAG pipeline & retriever
│   ├── summarizer.py       # Map-Reduce transcript summarizer
│   ├── transcriber.py      # Whisper and Sarvam STT transcription
│   └── vector_store.py     # ChromaDB and HuggingFace embeddings setup
└── utils/
    ├── audio_processor.py  # YouTube/Local video audio extraction & FFmpeg converter
    └── helper.py           # Helper utilities
```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👤 Author

Developed by **Subham Kumar** ([@alphasubham24](https://github.com/alphasubham24))
