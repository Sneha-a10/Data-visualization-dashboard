# Use official Python slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads folder
RUN mkdir -p /app/uploads

# Expose port 5000
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]