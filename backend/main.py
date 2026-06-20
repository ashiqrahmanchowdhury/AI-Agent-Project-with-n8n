from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import httpx
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Article Analyzer API", version="1.0.0")

# CORS — allow frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Config ──────────────────────────────────────────────────
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")  # Paste your n8n webhook URL here


# ── Schemas ─────────────────────────────────────────────────
class ArticleRequest(BaseModel):
    email: str
    article_url: str


class ArticleResponse(BaseModel):
    session_id: str
    message: str
    status: str


# ── Routes ──────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Article Analyzer API is running ✅"}


@app.post("/analyze", response_model=ArticleResponse)
async def analyze_article(request: ArticleRequest):
    """
    1. Generate a unique session_id
    2. Forward { email, article_url, session_id } to n8n webhook
    3. Return session_id + status to frontend
    """
    if not N8N_WEBHOOK_URL:
        raise HTTPException(
            status_code=500,
            detail="N8N_WEBHOOK_URL is not configured. Set it in .env file."
        )

    session_id = str(uuid.uuid4())

    payload = {
        "email": request.email,
        "article_url": request.article_url,
        "session_id": session_id,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(N8N_WEBHOOK_URL, json=payload)
            response.raise_for_status()
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="n8n webhook timed out. The workflow may still be running."
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"n8n webhook returned error: {e.response.status_code}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reach n8n webhook: {str(e)}"
        )

    return ArticleResponse(
        session_id=session_id,
        message="Article is being processed! Check your email shortly. 📧",
        status="processing"
    )


@app.get("/health")
def health():
    return {"status": "ok", "webhook_configured": bool(N8N_WEBHOOK_URL)}