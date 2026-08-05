# Local RAG Chatbot

A local, privacy-friendly RAG (Retrieval-Augmented Generation) chatbot for asking questions about your own PDF documents. Everything runs locally — no data leaves your machine.

Built with:
- **Streamlit** — chat UI
- **LangChain** — orchestration
- **Chroma** — vector store
- **Ollama** — local LLM (`qwen2.5:7b`) and embedding model (`nomic-embed-text`)

## Features

- Upload a PDF and chat with its content
- Answers are grounded only in retrieved document chunks (with source citations)
- Chat history is included in the prompt for follow-up questions
- One-click "Clear Memory" button to wipe the vector database

## Prerequisites

1. **Python 3.10+**
2. **[Ollama](https://ollama.com/)** installed and running locally
3. Pull the required models:
   ```bash
   ollama pull qwen2.5:7b
   ollama pull nomic-embed-text
   ```

## Installation

```bash
git clone https://github.com/NargsAbb/local-rag-chatbot.git
cd local-rag-chatbot
pip install -r requirements.txt
```

## Usage

```bash
streamlit run chatbot.py
```

1. Open the app in your browser (Streamlit will print the local URL).
2. Upload a PDF using the file uploader.
3. Ask questions about the document in the chat box.
4. Use "🗑️ Clear Memory Of Files(DB)" to reset the vector store and start fresh.

## Project Structure

```
.
├── chatbot.py       # Streamlit UI + RAG query logic
├── embeddings.py     # Embedding model configuration
├── setting.py        # PDF loading, chunking, and vector DB management
└── requirements.txt
```

## Choosing a Different Model

The LLM is configured at the top of `chatbot.py`:

```python
MODEL_NAME = "qwen2.5:7b"
MODEL_PROVIDER = "ollama"
```

By default the project uses `qwen2.5:7b`, which needs a decent amount of RAM/VRAM to run smoothly. Depending on your system's resources, feel free to swap this out for a model that better fits your hardware:

- **Lower-end systems** (limited RAM/no dedicated GPU): try a smaller model such as `qwen2.5:3b` or `llama3.2:3b` for faster responses.
- **Higher-end systems** (more RAM/VRAM available): try a larger, more capable model such as `qwen2.5:14b` or `llama3.1:8b` for better answer quality.

To use a different model:
1. Pull it with Ollama: `ollama pull <model-name>`
2. Update `MODEL_NAME` in `chatbot.py` to match.

You can browse available models at [ollama.com/library](https://ollama.com/library).

## Notes

- The vector database is stored locally in a `chroma/` folder (excluded from version control).
- Make sure the Ollama server is running (`ollama serve`) before starting the app.
