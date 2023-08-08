FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the local app folder to the container
COPY ./app /app


# Install the requests library
RUN pip install requests

# Command to run the script
CMD ["python", "client.py"]
