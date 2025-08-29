import os
from transformers import pipeline

# Load model name from environment (default = distilbart)
MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/distilbart-cnn-12-6")

# Load HuggingFace summarizer model (initialize once)
try:
    summarizer = pipeline("summarization", model=MODEL_NAME, tokenizer=MODEL_NAME)
except Exception as e:
    summarizer = None
    print(f"❌ Failed to load summarizer: {e}")

# In-memory stores
tasks = {}   # {task_id: {"status": str, "result": str}}
cache = {}   # {input_text: summary}


def summarize_text(text: str) -> str:
    """Run text summarization"""
    if summarizer is None:
        raise RuntimeError("Summarizer model not loaded")

    result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return result[0]["summary_text"]


def run_task(task_id: str, text: str):
    """Execute a summarization task (with caching)"""
    try:
        # return cached result if available
        if text in cache:
            tasks[task_id]["result"] = cache[text]
            tasks[task_id]["status"] = "completed (cached)"
            return

        # otherwise run summarizer
        summary = summarize_text(text)
        cache[text] = summary
        tasks[task_id]["result"] = summary
        tasks[task_id]["status"] = "completed"

    except Exception as e:
        tasks[task_id]["status"] = f"failed: {str(e)}"
        tasks[task_id]["result"] = None
