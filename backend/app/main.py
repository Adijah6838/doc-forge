from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import docs

app = FastAPI(title="DocForge API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(docs.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok"}
