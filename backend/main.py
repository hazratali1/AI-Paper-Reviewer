"""
FastAPI Application Entry Point
AI Research Paper Reviewer Backend
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from api.routes import router

app = FastAPI(
    title="AI Research Paper Reviewer",
    description="Automated academic paper analysis using multi-agent AI with RAG",
    version="1.0.0",
)

# CORS: allow Next.js frontend (localhost:3000) and any origin for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
async def health_check():
    return {
        "status": "running",
        "service": "AI Research Paper Reviewer",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
