#!/bin/bash

# PetRescue Deployment Script

echo "Starting PetRescue Deployment..."

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run tests
echo "Running tests..."
python manage.py test

# Check system health
echo "Running system checks..."
python manage.py check

# Restart application server (example with Gunicorn)
echo "Restarting application server..."
# gunicorn petrescue.wsgi:application --bind 0.0.0.0:8000 --workers 3

echo "Deployment completed successfully!"