FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
