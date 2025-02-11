# Use a smaller base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to optimize caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "serve_model:app", "--host", "0.0.0.0", "--port", "8000"]
