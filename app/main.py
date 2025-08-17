from fastapi import FastAPI
from pydantic import BaseModel

from .rag import LocalRAG

app = FastAPI(title="legal-ai")

rag = LocalRAG()


class QueryRequest(BaseModel):
    query: str


@app.post("/legal/summarize")
def summarize(req: QueryRequest):
    """Return top legal fragments and a naive summary."""
    return rag.summarize(req.query)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
