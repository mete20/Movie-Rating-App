FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the local app folder to the container
COPY ./app /app

COPY wait_for_it.sh /wait_for_it.sh
RUN chmod +x /wait_for_it.sh

# Install the requests library
RUN pip install requests

# Command to run the script
CMD ["/wait_for_it.sh", "web:8000", "--", "python", "client.py"]
