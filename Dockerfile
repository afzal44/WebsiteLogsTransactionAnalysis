# app/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the entire application directory into the Docker image
COPY app/ .
COPY logs .
COPY reports .


# Change directory to /app
WORKDIR /app

# Expose port 5000 for flask
EXPOSE 5000
# Command to run the Flask application
CMD ["python", "app.py"]
