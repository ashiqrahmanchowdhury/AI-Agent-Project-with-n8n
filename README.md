# 🤖 AI Agent Project with n8n
### Ashiq Rahman Chowdhury |

A full-stack AI workflow system where a Streamlit frontend and FastAPI backend connect to **n8n**. The system takes an article URL and user email, scrapes the article using AI, generates summaries and key insights, logs data to Google Sheets, and emails the results directly to the user.

---

## 🎥 Demo Video
👉 **[Watch the End-to-End Demo Video](YOUR_VIDEO_LINK_HERE)**

---

## 🚀 Data Flow Architecture

```
User (Streamlit) → FastAPI Backend → n8n Webhook
                                          ↓
                                   AI Agent (Gemini)
                                          ↓
                              ┌─────────────────────┐
                              │  Scrape Article      │
                              │  Summarize (3-5 sen) │
                              │  Extract Insights    │
                              │  Save to Sheets      │
                              │  Send Email          │
                              └─────────────────────┘
```

1. **Frontend (Streamlit)** — User enters email + article URL
2. **Backend (FastAPI)** — Generates `session_id`, forwards to n8n webhook
3. **n8n AI Agent** — Scrapes article, summarizes, extracts insights, logs to Google Sheets, sends email

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (Python) |
| Backend | FastAPI + HTTPX |
| Workflow | n8n (Self-hosted) |
| AI Model | Google Gemini 2.0 Flash |
| Storage | Google Sheets |
| Email | Gmail (OAuth2) |

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git https://github.com/ashiqrahmanchowdhury/AI-Agent-Project-with-n8n
cd article-analyzer-n8n
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn httpx python-dotenv pydantic[email] streamlit requests
```

### 3. Configure Environment
Create a `.env` file in the `backend/` folder:
```env
N8N_WEBHOOK_URL=http://localhost:5678/webhook/article-analyzer
```

### 4. Run Backend
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 5. Run Frontend
```bash
cd frontend
python -m streamlit run app.py
```

---

## ⚙️ n8n Workflow Setup

1. Import `n8n_workflow.json` into your n8n instance
2. Connect credentials:
   - **Google Gemini API Key**
   - **Google Sheets** (OAuth2)
   - **Gmail** (OAuth2)
3. Update Google Sheet ID in the Google Sheets node
4. Publish the workflow

---

## 📊 Google Sheets Output

| Session ID | Article URL | Email | Summary | Insights | Timestamp |
|------------|-------------|-------|---------|----------|-----------|
| uuid | https://... | user@email.com | 3-5 sentence summary | 1. insight... | 2026-... |

---

## 📁 Project Structure

```
article-analyzer-n8n/
├── backend/
│   ├── main.py          # FastAPI backend
│   └── requirements.txt
├── frontend/
│   └── app.py           # Streamlit frontend
├── n8n_workflow.json    # n8n workflow export
└── README.md
```

---

## ✨ Features

- ✅ End-to-end AI workflow automation
- ✅ Real-time article scraping
- ✅ AI-powered summarization (3-5 sentences)
- ✅ Key insights extraction (3-5 points)
- ✅ Automatic Google Sheets logging
- ✅ Email delivery with formatted results
- ✅ Session-based tracking

---

*AI AGENT PROJECT WITH N8N - ASHIQ RAHMAN CHOWDHURY*