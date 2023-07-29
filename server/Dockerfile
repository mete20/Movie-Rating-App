# Pull base image
FROM python:3.9

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install mariadb

# Copy project
COPY . .
