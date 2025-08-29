from fastapi import FastAPI, HTTPException
from concurrent.futures import ThreadPoolExecutor
import uuid

# Import from app folder
from app.models import SummarizeRequest
from app.tasks import run_task, tasks

app = FastAPI(title="Text Summarizer API", version="1.0")

executor = ThreadPoolExecutor(max_workers=4)

# For summarization
@app.post("/summarize")
def create_task(req: SummarizeRequest):
    if len(req.text.split()) < 10:
        raise HTTPException(status_code=400, detail="Text too short to summarize")

    if len(req.text) > 2000:
        raise HTTPException(status_code=400, detail="Text too long, max 2000 chars")

    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending", "result": None}

    executor.submit(run_task, task_id, req.text)

    return {
        "task_id": task_id,
        "status_url": f"/status/{task_id}",
        "result_url": f"/result/{task_id}"
    }

# Checking the status of tasks
@app.get("/status/{task_id}")
def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": tasks[task_id]["status"]}

# Getting the result
@app.get("/result/{task_id}")
def get_result(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    if tasks[task_id]["status"].startswith("pending"):
        raise HTTPException(status_code=202, detail="Task still processing")
    return {"task_id": task_id, "result": tasks[task_id]["result"]}
