FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /app

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and files
COPY app/ .
COPY run_tests.sh /app/run_tests.sh
COPY cert.pem /app/cert.pem
COPY key.pem /app/key.pem

# Make test script executable
RUN chmod +x /app/run_tests.sh

# Run the Flask app
CMD ["python", "app.py"]
