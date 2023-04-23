# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=app/api.py

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host", "0.0.0.0"]
