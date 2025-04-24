FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the model directory exists
RUN mkdir -p app/model

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--chdir", "app", "--bind", "0.0.0.0:8080", "flask_app:app"] 