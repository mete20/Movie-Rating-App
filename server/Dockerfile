# Use an official Python image
FROM python:3.8

# Set the working directory
WORKDIR /app

COPY requirements.txt /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential

# Copy the local app folder to the container
COPY ./app /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Define the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

