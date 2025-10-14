# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential gcc gfortran python3-dev libpq-dev

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run database migrations and start the server
CMD ["bash", "-c", "python manage.py migrate && gunicorn eth_prediction_project.wsgi:application --bind 0.0.0.0:8000"]