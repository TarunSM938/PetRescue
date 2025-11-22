@echo off
REM PetRescue Setup Script for Windows

echo Setting up PetRescue development environment...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run database migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser (optional)
echo Creating superuser account...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Run tests
echo Running tests...
python manage.py test

echo Setup completed successfully!
echo To start the development server, run: python manage.py runserver