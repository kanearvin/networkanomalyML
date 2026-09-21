# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ /app/src/
COPY models/ /app/models/

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI when the container launches
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
