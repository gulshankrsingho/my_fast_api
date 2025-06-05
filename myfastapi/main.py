from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
import uuid
from typing import List, Dict
from enum import Enum
from collections import defaultdict

app = FastAPI()

# Enum for priority levels
class PriorityLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

# Model for the ingestion request
class IngestionRequestModel(BaseModel):
    ids: List[int]
    priority: PriorityLevel

# Enum for batch status
class BatchState(str, Enum):
    YET_TO_START = "yet_to_start"
    TRIGGERED = "triggered"
    COMPLETED = "completed"

# Class representing a batch of IDs
class Batch:
    def __init__(self, ids: List[int]):
        self.batch_id = str(uuid.uuid4())
        self.ids = ids
        self.status = BatchState.YET_TO_START

# Class representing an ingestion process
class IngestionProcess:
    def __init__(self):
        self.batches = []
        self.status = BatchState.YET_TO_START

# In-memory storage for ingestions
ingestion_storage: Dict[str, IngestionProcess] = {}

# Asynchronous function to simulate batch processing
async def simulate_batch_processing(batch: Batch):
    batch.status = BatchState.TRIGGERED
    await asyncio.sleep(5)  # Simulate processing delay
    batch.status = BatchState.COMPLETED

# Endpoint to submit a data ingestion request
@app.post("/ingest")
async def submit_ingestion(request: IngestionRequestModel):
    ingestion_id = str(uuid.uuid4())
    ingestion_process = IngestionProcess()
    ingestion_storage[ingestion_id] = ingestion_process

    # Process IDs in batches of 3
    for i in range(0, len(request.ids), 3):
        batch_ids = request.ids[i:i + 3]
        batch = Batch(batch_ids)
        ingestion_process.batches.append(batch)
        asyncio.create_task(simulate_batch_processing(batch))

    ingestion_process.status = BatchState.TRIGGERED
    return {"ingestion_id": ingestion_id}

# Endpoint to check the status of an ingestion request
@app.get("/status/{ingestion_id}")
async def check_status(ingestion_id: str):
    ingestion_process = ingestion_storage.get(ingestion_id)
    if not ingestion_process:
        return {"error": "Ingestion ID not found"}

    # Determine overall status based on batch statuses
    overall_status = BatchState.COMPLETED
    for batch in ingestion_process.batches:
        if batch.status == BatchState.YET_TO_START:
            overall_status = BatchState.YET_TO_START
            break
        elif batch.status == BatchState.TRIGGERED:
            overall_status = BatchState.TRIGGERED

    return {
        "ingestion_id": ingestion_id,
        "status": overall_status,
        "batches": [{"batch_id": batch.batch_id, "ids": batch.ids, "status": batch.status} for batch in ingestion_process.batches]
    }
