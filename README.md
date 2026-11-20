# DocForge - AI-Powered Technical Documentation Generator
Parses Python code with AST, documents only real functions/classes, detects missing docs, scores quality, exports Markdown.
## Run Backend
cd backend; venv\Scripts\activate; uvicorn app.main:app --port 8001
## Run Frontend
cd frontend; npm run dev
## Test
cd backend; pytest tests/ -v
## Endpoints
POST /api/parse, POST /api/upload, POST /api/export, GET /api/health
