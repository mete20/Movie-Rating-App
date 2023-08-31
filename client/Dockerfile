FROM python:3.9

# Set the working directory
WORKDIR /app

COPY requirements.txt /app/

COPY wait_for_it.sh /wait_for_it.sh
RUN chmod +x /wait_for_it.sh


# Copy the local app folder to the container
COPY ./app /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Define the command to run the application
# CMD ["/bin/sh", "-c", "/wait_for_it.sh db:3306 -- && uvicorn client:app --host 0.0.0.0 --port 8001"]
CMD ["/bin/sh", "-c", "/wait_for_it.sh web:8000 -- && python testing/test.py && uvicorn client:app --host 0.0.0.0 --port 8001"]

