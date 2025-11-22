@echo off
REM PetRescue Test Runner Script for Windows

echo Starting PetRescue Test Suite...

REM Run Django tests
echo Running unit and integration tests...
python manage.py test

REM Check for syntax errors
echo Checking for syntax errors...
python -m py_compile main/models.py main/views.py main/forms.py main/tests.py

REM Run system checks
echo Running Django system checks...
python manage.py check

echo Test suite completed!