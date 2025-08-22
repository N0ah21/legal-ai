# legal-ai

A minimal FastAPI application demonstrating retrieval-augmented generation (RAG) over local legal documents.

## Local Demo Steps

1. `make install`
2. `make run`
3. Send a request:

```bash
curl -X POST "http://localhost:8000/legal/summarize" \
  -H "Content-Type: application/json" \
  -d '{"query": "confidentiality"}'
```

## Docker 本地啟動

1. `make up`
2. 服務啟動後可透過 `http://localhost:8000` 存取。
3. 健康檢查：`curl http://localhost:8000/health`
4. 停止並移除容器：`make down`

容器啟動時若索引不存在會自動建立。
