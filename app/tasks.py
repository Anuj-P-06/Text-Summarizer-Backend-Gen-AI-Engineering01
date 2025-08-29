import os
import requests

# Load env variables
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/distilbart-cnn-12-6")

# In-memory task & cache store
tasks = {}   # {task_id: {"status": str, "result": str}}
cache = {}   # {input_text: summary}


def summarize_text(text: str) -> str:
    """Run summarization using Hugging Face Inference API"""
    if HF_API_KEY is None:
        raise RuntimeError("❌ HF_API_KEY not set in environment")

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
        headers=headers,
        json={"inputs": text},
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Hugging Face API error: {response.text}")

    data = response.json()
    if not isinstance(data, list) or "summary_text" not in data[0]:
        raise RuntimeError(f"Unexpected API response: {data}")

    return data[0]["summary_text"]


def run_task(task_id: str, text: str):
    """Execute a summarization task (with caching)"""
    try:
        # check cache
        if text in cache:
            tasks[task_id]["result"] = cache[text]
            tasks[task_id]["status"] = "completed (cached)"
            return

        # call API
        summary = summarize_text(text)

        # save to cache
        cache[text] = summary
        tasks[task_id]["result"] = summary
        tasks[task_id]["status"] = "completed"

    except Exception as e:
        tasks[task_id]["status"] = f"failed: {str(e)}"
        tasks[task_id]["result"] = None

