
# HudumaAI - Government Services RAG Chatbot

HudumaAI is a multilingual AI-powered chatbot designed to provide Kenyan citizens with 
instant, conversational access to government services and information. The system leverages 
a **Retrieval-Augmented Generation (RAG)** pipeline trained on Kenyan government websites 
and public documents to ensure accurate, up-to-date responses.

## 🚀 Features
- **RAG-powered Conversational AI** – Combines document retrieval with generative AI.
- **Multilingual Support** – English, Kiswahili, and local dialects.
- **Government Data Sources** – Trained on official `.go.ke` sites and public service documents.
- **Multi-Channel Access** – Works via WhatsApp, SMS, Telegram, and Web.

---

## 📂 Project Structure
```
huduma-ai/
│
├── data/                  # Raw and processed documents
├── notebooks/             # Jupyter notebooks for experimentation
├── src/                   # Source code for RAG pipeline
│   ├── scraping/           # Web scraping scripts
│   ├── processing/         # Text cleaning and chunking
│   ├── embeddings/         # Embedding generation
│   ├── retrieval/          # Vector store search
│   ├── chatbot/            # Conversational interface logic
│   └── api/                # API endpoints (FastAPI/Django)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/huduma-ai.git
cd huduma-ai
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate   # For Windows
pip install -r requirements.txt
```

### 3. Scrape & Load Government Data
```bash
python src/scraping/scrape_websites.py
python src/processing/clean_and_chunk.py
```

### 4. Generate Embeddings & Store in Vector DB
```bash
python src/embeddings/generate_embeddings.py
```

### 5. Run the RAG Chatbot API
```bash
uvicorn src.api.main:app --reload
```

---

## 📡 Deployment Options
- **Local Testing** – Run API locally and connect via Postman or Web UI.
- **Cloud Deployment** – Host API and vector database on AWS, GCP, or Azure.
- **Messaging Integration** – Connect to WhatsApp via Twilio, Telegram Bot API, or Africa's Talking SMS.

---

## 📌 Data Sources
- [eCitizen](https://www.ecitizen.go.ke/)
- [Kenya Revenue Authority (KRA)](https://www.kra.go.ke/)
- [Ministry of Health](https://www.health.go.ke/)
- [Council of Governors](https://www.cog.go.ke/)
- Public service manuals, gazettes, and legal documents.

---

## ⚠️ Disclaimer
HudumaAI retrieves and processes information from **official government sources** only. 
While the system aims for accuracy, it should not replace direct verification from 
official agencies.

---

## 📜 License
This project is licensed under the MIT License.
