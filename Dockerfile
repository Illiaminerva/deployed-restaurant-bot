FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the model file first (it's large and changes less frequently)
COPY app/model/best_rl_model.pt app/model/

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--chdir", "app", "--bind", "0.0.0.0:8080", "flask_app:app"] 