FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (better Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application (with PORT env variable support)
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port \"
