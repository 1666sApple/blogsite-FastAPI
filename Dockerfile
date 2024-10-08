# Use the official Python image with version 3.12 as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Append /app to the existing PYTHONPATH environment variable to ensure the application modules are accessible
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the FastAPI server with live reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
