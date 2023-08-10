FROM python:3.9

# Set the working directory
WORKDIR /app

COPY requirements.txt /app/

# Copy the local app folder to the container
COPY ./app /app

COPY wait_for_it.sh /wait_for_it.sh
RUN chmod +x /wait_for_it.sh

# Install the requests library
RUN pip install -r requirements.txt

# Command to run the script
CMD ["/wait_for_it.sh", "web:8000", "--", "python", "client.py"]
