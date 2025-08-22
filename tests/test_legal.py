import os

from fastapi.testclient import TestClient

os.environ["STUB_EMBEDDINGS"] = "1"

from app.main import app


client = TestClient(app)


def test_summarize_endpoint():
    response = client.post("/legal/summarize", json={"query": "confidentiality"})
    assert response.status_code == 200
    data = response.json()
    assert "fragments" in data and len(data["fragments"]) <= 3
    assert "summary" in data
