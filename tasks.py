import time
from transformers import pipeline

# Load HuggingFace summarizer model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# In-memory task store
tasks = {}   # {task_id: {"status": str, "result": str}}
cache = {}   # {input_text: summary}


def summarize_text(text: str) -> str:
    """Run text summarization"""
    time.sleep(2)
    result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return result[0]["summary_text"]


def run_task(task_id: str, text: str):
    try:
        # for checking cache
        if text in cache:
            tasks[task_id]["result"] = cache[text]
            tasks[task_id]["status"] = "completed (cached)"
            return

        # for summarizing
        summary = summarize_text(text)
        cache[text] = summary
        tasks[task_id]["result"] = summary
        tasks[task_id]["status"] = "completed"
    except Exception as e:
        tasks[task_id]["status"] = f"failed: {str(e)}"
