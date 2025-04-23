FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code and certs
COPY app/ .
COPY cert.pem /app/cert.pem
COPY key.pem /app/key.pem

# Start the application
CMD ["python", "app.py"]
