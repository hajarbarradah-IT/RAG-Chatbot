# RAG-Chatbot
📋 Copy README (Ollama Version)
# RAG-Chatbot with Ollama 🤖

A Retrieval-Augmented Generation (RAG) chatbot powered by **Ollama** for local LLM inference. This project combines document retrieval with locally-hosted language models to provide intelligent, context-aware responses without API costs.

**Status:** In Development | **Author:** Hajar Barradah | **LLM:** Ollama (Local)

---

## 🚀 Why Ollama + RAG?

- 🏠 **Run Locally:** No API calls, no cloud dependencies
- 💰 **Cost-Free:** Zero LLM API costs
- 🔒 **Privacy:** All data stays on your machine
- ⚡ **Fast:** Optimized inference with Ollama
- 🧠 **Grounded Responses:** RAG prevents hallucinations using real documents

---

## 📋 Overview

RAG-Chatbot leverages:
1. **Retrieval:** FAISS/ChromaDB to find relevant documents
2. **Augmentation:** Add context to the prompt
3. **Generation:** Ollama runs open-source LLMs locally (Llama 2, Mistral, etc.)

Perfect for:
- 📚 Knowledge-base QA systems
- 💬 Document-aware chatbots
- 🔍 Research assistants
- 🏢 Enterprise AI without API vendor lock-in

---

## 🛠️ Tech Stack

**Core:**
- **Ollama** — Local LLM inference engine
- **Python 3.x** — Main programming language
- **LangChain** — RAG pipeline orchestration
- **FAISS** — Vector similarity search

**NLP & Embeddings:**
- **Sentence-Transformers** — Document embeddings
- **Hugging Face** — Tokenizers & utilities
- **ChromaDB** (optional) — Vector database alternative

**Tools:**
- Git & GitHub
- Jupyter Notebooks
- Docker (optional)

---

## 📂 Project Structure

```
RAG-Chatbot/
├── data/
│   ├── documents/          # Your knowledge base (PDFs, TXTs)
│   └── embeddings/         # Pre-computed embeddings cache
├── src/
│   ├── retriever.py        # Document retrieval (FAISS/ChromaDB)
│   ├── ollama_handler.py   # Ollama API wrapper
│   ├── pipeline.py         # RAG pipeline (retrieve + generate)
│   └── utils.py            # Text processing & helpers
├── notebooks/
│   └── rag_demo.ipynb      # Jupyter demo
├── config.yaml             # Ollama & RAG settings
├── requirements.txt        # Python dependencies
├── main.py                 # Entry point
└── README.md
```

---

## ⚙️ Prerequisites

Before starting, install:

1. **Ollama** (Download from https://ollama.ai)
   ```bash
   # After installing, verify:
   ollama --version
   ```

2. **Python 3.8+**
   ```bash
   python --version
   ```

3. **Git**
   ```bash
   git --version
   ```

---

## 🔧 Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/hajarbarradah-IT/RAG-Chatbot.git
cd RAG-Chatbot
```

### Step 2: Setup Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
langchain>=0.0.200
ollama>=0.1.0
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0
python-dotenv>=1.0.0
pyyaml>=6.0
requests>=2.31.0
```

### Step 4: Start Ollama Service
```bash
# Start Ollama daemon (runs in background)
ollama serve

# In another terminal, pull a model:
ollama pull llama2          # Llama 2 (7B) - Recommended
ollama pull mistral         # Mistral 7B
ollama pull neural-chat     # Neural Chat (faster)
```

**Recommended Models:**
- `llama2` — Best quality, ~4GB
- `mistral` — Fast & capable, ~5GB
- `neural-chat` — Fastest, ~4GB
- `orca-mini` — Lightweight, ~3GB

### Step 5: Configure Project
Create/edit `config.yaml`:
```yaml
ollama:
  base_url: "http://localhost:11434"
  model: "llama2"              # or mistral, neural-chat, etc.
  temperature: 0.7
  top_p: 0.9
  max_tokens: 512

retrieval:
  vector_db: "faiss"           # or "chromadb"
  embedding_model: "all-MiniLM-L6-v2"
  top_k: 5                      # Return top 5 documents

data:
  documents_path: "./data/documents"
  embeddings_cache: "./data/embeddings"
```

### Step 6: Prepare Documents
Place your documents in `data/documents/`:
```bash
data/documents/
├── file1.txt
├── file2.pdf
└── guide.md
```

---

## 🚀 Usage

### Basic Usage (Python)

```python
from src.pipeline import RAGPipeline
from src.ollama_handler import OllamaClient
import yaml

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Initialize RAG pipeline
rag = RAGPipeline(config)

# Ask a question
query = "What is machine learning?"
response = rag.answer(query)

print(f"📌 Query: {query}")
print(f"💬 Response: {response}")
```

### Command Line
```bash
python main.py --query "What is RAG?"
python main.py --interactive  # Chat mode
```

### Jupyter Notebook
```bash
jupyter notebook notebooks/rag_demo.ipynb
```

---

## 📝 Code Example: Custom Implementation

```python
from langchain.llms import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader

# 1. Load documents
loader = DirectoryLoader("./data/documents")
docs = loader.load()

# 2. Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. Build vector store
vectorstore = FAISS.from_documents(docs, embeddings)

# 4. Initialize Ollama LLM
llm = Ollama(
    base_url="http://localhost:11434",
    model="llama2",
    temperature=0.7
)

# 5. Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 6. Answer questions
result = qa_chain.run("What is the main topic?")
print(result)
```

---

## 🎯 Performance Tips

**Optimize Ollama:**
```bash
# Use GPU acceleration (if available)
export CUDA_VISIBLE_DEVICES=0  # Use your GPU

# Reduce model size for faster inference
ollama pull orca-mini  # Smaller, faster model
```

**Optimize Retrieval:**
```python
# Reduce top_k for faster retrieval
config["retrieval"]["top_k"] = 3  # Instead of 5

# Use faster embeddings
"embedding_model": "distiluse-base-multilingual-cased-v2"
```

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Make sure `ollama serve` is running |
| Model too slow | Try smaller model (orca-mini, neural-chat) |
| Out of memory | Reduce `max_tokens`, use smaller embedding model |
| Poor answers | Increase `top_k` docs, improve document chunking |

---

## 📊 Supported Ollama Models

```bash
ollama pull llama2              # 7B, 13B, 70B
ollama pull mistral             # Mistral 7B
ollama pull neural-chat         # Neural Chat 7B
ollama pull orca-mini           # Lightweight, fast
ollama pull dolphin-mixtral     # Powerful, 8x7B MoE
ollama pull openchat            # OpenChat 3.5
```

Check all models: https://ollama.ai/library

---

## 📚 Learning Resources

- [Ollama Documentation](https://ollama.ai)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/qa_structured_data)
- [FAISS Tutorial](https://github.com/facebookresearch/faiss)
- [RAG Paper (Lewis et al.)](https://arxiv.org/abs/2005.11401)

---

## 🎓 Project Goals

Explore:
- ✅ Local LLM inference with Ollama
- ✅ Document retrieval & ranking
- ✅ RAG pipeline design
- ✅ Embedding models & vector search
- ✅ Production-ready AI systems

---

## 🤝 Connect & Collaborate

💌 **Email:** hajarbarradah55@gmail.com

📱 **Phone:** +212 698 854 711

💼 **LinkedIn:** [Hajar Barradah](https://linkedin.com/in/hajar-barradah)

🐙 **GitHub:** [@hajarbarradah-IT](https://github.com/hajarbarradah-IT)

*Open to internship discussions, collaborations, and AI/NLP projects!* 🚀

---

## 📄 License

MIT License — See LICENSE file for details.

---

**Built with curiosity, executed with precision. Local LLMs, unlimited possibilities.** ⚡
