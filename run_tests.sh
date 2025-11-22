#!/bin/bash

# PetRescue Test Runner Script

echo "Starting PetRescue Test Suite..."

# Run Django tests
echo "Running unit and integration tests..."
python manage.py test

# Check for syntax errors
echo "Checking for syntax errors..."
python -m py_compile main/models.py main/views.py main/forms.py main/tests.py

# Run system checks
echo "Running Django system checks..."
python manage.py check

echo "Test suite completed!"