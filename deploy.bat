@echo off
REM PetRescue Deployment Script for Windows

echo Starting PetRescue Deployment...

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run database migrations
echo Running database migrations...
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Run tests
echo Running tests...
python manage.py test

REM Check system health
echo Running system checks...
python manage.py check

REM Restart application server (example with Gunicorn)
echo Restarting application server...
REM gunicorn petrescue.wsgi:application --bind 0.0.0.0:8000 --workers 3

echo Deployment completed successfully!