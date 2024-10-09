# Use the official Python image with version 3.12 as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Define PYTHONPATH to include the /app/src directory
ENV PYTHONPATH="/app/src"

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code from the src directory into the container
COPY src/ /app/src

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the FastAPI server with live reload
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
