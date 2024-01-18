#!/bin/bash

# Specify the values for your environment variables
PROJECT_NAME="your_project_name"
host="your_host"
port="your_port"
POSTGRES_SERVER="your_postgres_server"
POSTGRES_USER="your_postgres_user"
POSTGRES_PASSWORD="your_postgres_password"
POSTGRES_DB="your_postgres_db"
EMAIL_SMTP_USER="your_email_smtp_user"
EMAIL_SMTP_PASSWORD="your_email_smtp_password"
EMAILS_FROM_EMAIL="example@gmail.com"

# Create or overwrite the .env file
cat <<EOF > .env
# project
PROJECT_NAME=${PROJECT_NAME}

# application
host=${host}
port=${port}

# postgres
POSTGRES_SERVER=${POSTGRES_SERVER}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}

# email Configuration
EMAIL_SMTP_TLS=True
EMAIL_SMTP_PORT=465
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_USER=${EMAIL_SMTP_USER}
EMAIL_SMTP_PASSWORD=${EMAIL_SMTP_PASSWORD}
EMAILS_FROM_EMAIL=${EMAILS_FROM_EMAIL}
EOF

echo ".env file created successfully."
