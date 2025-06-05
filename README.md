# 🚀 FastAPI Ingestion Service

This is a FastAPI-based microservice that handles asynchronous ingestion of integer IDs in batches, with priority handling and real-time status tracking.

---

## 🧠 Features

- Accepts a list of IDs with a priority level (HIGH, MEDIUM, LOW)
- Processes IDs in batches of 3 asynchronously
- Supports batch-level status (`yet_to_start`, `triggered`, `completed`)
- Real-time status tracking of ingestion requests
- Asynchronous background processing using `asyncio`

---

## 📦 Requirements

- Python 3.7+
- FastAPI
- Uvicorn

Install dependencies:

```bash
pip install -r requirements.txt
