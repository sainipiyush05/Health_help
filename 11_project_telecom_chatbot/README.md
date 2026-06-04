# 📡 Project 11: Telecom Customer Care RAG Chatbot

An advanced, multi-source **Retrieval-Augmented Generation (RAG)** Customer Care Assistant designed to resolve subscriber questions about mobile internet speed, billing anomalies, international roaming, SIM issues, and device setups.

---

## 🌟 Key Features

1. **Multi-Source Retrieval:** Seamlessly queries three distinct knowledge bases:
   - **FAQ Entries:** Direct policy details and structural information.
   - **Resolved Support Tickets:** Real historical client issues and their step-by-step resolutions.
   - **User Guides (PDF):** In-depth technical guides for hardware/network features (e.g., Wi-Fi calling, SIM activation).
2. **Unified Semantic Search:** Combines results from three separate **Chroma DB** vector collections using HuggingFace's `sentence-transformers/all-MiniLM-L6-v2` embeddings.
3. **Contextual Guardrails:** The system prompt instructs the assistant to *only* answer using the retrieved context. If information is insufficient, it safely directs the user to phone support (611) or the MyTelecom mobile app.
4. **Interactive UI with Quick Actions:** Includes clickable preset sample questions (e.g., *"Why is my mobile internet so slow?"*, *"My bill is higher than usual"*) to instantly test chatbot capabilities.
5. **Real-Time Streaming Responses:** Outputs responses word-by-word utilizing Streamlit's `write_stream` and LangChain's `.stream()` API.

---

## 🏗️ Project Architecture

```mermaid
graph TD
    User([User]) <--> App[Streamlit Web App: app.py]
    App <--> Chain[RAG Chain: rag_chain.py]
    
    subgraph Ingestion Pipelines
        IF[injest_faq.py] -->|CSV| FAQ[(Chroma: faq)]
        IT[ingest_tickets.py] -->|SQLite DB| TKT[(Chroma: tickets)]
        IP[ingest_pdf.py] -->|PDF Loader + Splitter| GD[(Chroma: guides)]
    end
    
    subgraph Merged Retriever (retriever.py)
        MR[Merged Retriever] --> FAQ
        MR --> TKT
        MR --> GD
    end
    
    Chain --> MR
    Chain -->|Prompt + Context| LLM[ChatGroq: qwen/qwen3-32b]
```

### File Structure & Roles
- [app.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/app.py): Entry point for the Streamlit UI, displaying chat history and sidebar templates.
- [retriever.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/retriever.py): Loads the embedding model and coordinates querying across `faq`, `tickets`, and `guides` collections.
- [rag_chain.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/rag_chain.py): Combines the merged retriever, system-specific instructions, ChatGroq LLM model (`qwen/qwen3-32b`), and an output parser.
- [injest_faq.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/injest_faq.py): Reads [faq.csv](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/data/faq.csv) and writes embeddings to Chroma.
- [ingest_tickets.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/ingest_tickets.py): Loads resolved tickets from the SQLite DB [tickets.db](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/data/tickets.db) and indexes them.
- [ingest_pdf.py](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/ingest_pdf.py): Uses `PyPDFLoader` to load [telecom_guide.pdf](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/data/telecom_guide.pdf), chunks it using `RecursiveCharacterTextSplitter` (600 characters size, 100 overlap), and stores it.
- **data/**: Directory hosting source knowledge resources:
  - [faq.csv](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/data/faq.csv)
  - [tickets.db](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/data/tickets.db)
  - [telecom_guide.pdf](file:///Users/piyushsaini/Desktop/AI/learn_agentic/11_project_telecom_chatbot/data/telecom_guide.pdf)

---

## 🛠️ Ingestion & Setup

Before running the application, you must populate the Chroma vector store.

### 1. Configure API Credentials
Ensure that your `.env` file in the project or workspace root contains:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Build the Vector Database
Execute the three ingestion scripts in order to parse raw resources and build the embeddings:
```bash
# Ingest FAQs
python injest_faq.py

# Ingest Resolved Support Tickets
python ingest_tickets.py

# Ingest PDF Guides
python ingest_pdf.py
```
This creates or updates the local `chroma_store` folder with search-optimized embeddings.

---

## 🚀 Running the Application

Launch the Streamlit dashboard:
```bash
streamlit run app.py
```
The browser interface will spin up at `http://localhost:8501`.

### Suggested Test Interactions
- Click on *"Why is my mobile internet so slow?"* to see context retrieved from resolved tickets and guides.
- Click on *"How do I enable Wi-Fi calling?"* to retrieve PDF chunk data instructions.
- Try entering a completely off-topic question to test the system guardrails (e.g., *"Who won the world cup in 2022?"*). The agent should reply that it cannot answer based on the context and suggest calling 611.
