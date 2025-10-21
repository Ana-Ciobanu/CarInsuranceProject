# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set environment variables
ENV FLASK_APP=app/main.py
ENV FLASK_ENV=development

# Expose port
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
