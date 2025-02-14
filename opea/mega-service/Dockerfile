FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# Copy in and install Python dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py /app

# Expose port 8000 for external access
EXPOSE 8000

# By default, run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
