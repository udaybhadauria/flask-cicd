#!/bin/bash

# Load environment variables
set -o allexport
source /home/pi/flask-cicd/.env
set +o allexport

# Check if SLACK_WEBHOOK_URL is set
if [ -z "$SLACK_WEBHOOK_URL" ]; then
    echo "SLACK_WEBHOOK_URL not set. Skipping Slack notification."
    exit 1
fi

# Path to .env file
ENV_FILE="/home/pi/flask-cicd/.env"

# Generate a secure JWT key
NEW_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Replace or add JWT_SECRET_KEY in .env
if grep -q "^JWT_SECRET_KEY=" "$ENV_FILE"; then
    sed -i "s|^JWT_SECRET_KEY=.*|JWT_SECRET_KEY=$NEW_KEY|" "$ENV_FILE"
else
    echo "JWT_SECRET_KEY=$NEW_KEY" >> "$ENV_FILE"
fi

echo "✅ JWT secret key updated at $(date)"

# Send Slack notification
SLACK_MESSAGE="🔐 *JWT Secret Key was rotated* at $(date +'%Y-%m-%d %H:%M:%S') on *$(hostname)*."
curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\": \"$SLACK_MESSAGE\"}" \
  "$SLACK_WEBHOOK_URL"
