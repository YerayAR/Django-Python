# Lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Start Django development server
CMD ["python", "memory_project/manage.py", "runserver", "0.0.0.0:8000"]
