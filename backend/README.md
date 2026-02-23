# FastAPI Backend

## Setup

```bash
cd backend
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API will run at `http://127.0.0.1:8000`.

If port `8000` is already in use, start on another port:

```bash
uvicorn app.main:app --reload --port 8030
```

## Endpoints

- `GET /health`
- `POST /upload` (`multipart/form-data` with `file` as a CSV)
- `POST /audit` (`multipart/form-data` with `file` as a CSV)

### Example curl

```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@sample.csv"
```

```bash
curl -X POST "http://127.0.0.1:8000/audit" -F "file=@sample.csv"
```
