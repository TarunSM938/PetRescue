# PetRescue

PetRescue is a Django web application designed to help connect lost pets with their owners and facilitate pet adoptions. The platform provides a comprehensive solution for reporting lost/found pets, searching for missing animals, and supporting animal welfare through community engagement.

## Features

- **Pet Reporting**: Users can report lost or found pets with detailed information and photos
- **Search & Filter**: Advanced search functionality to find pets by various criteria
- **Admin Dashboard**: Comprehensive admin panel for managing reports and user submissions
- **Notification System**: Real-time notifications for admins and users
- **User Profiles**: Personalized user accounts with profile management
- **Activity Tracking**: Complete history of all actions and changes
- **Responsive Design**: Mobile-friendly interface that works on all devices

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- MySQL 5.7 or higher (or compatible database)
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

### Quick Setup (Recommended)

For Windows:
```bash
setup.bat
```

For macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Production Deployment

For production deployment, use Gunicorn:
```bash
gunicorn petrescue.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## Environment Variables

The following environment variables should be set in production:

```bash
# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=petrescue_production
DB_USER=petrescue_user
DB_PASSWORD=your_secure_password
DB_HOST=your_database_host
DB_PORT=3306

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your_smtp_host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Database Setup

1. Create a MySQL database:
   ```sql
   CREATE DATABASE petrescue_db;
   CREATE USER 'petrescue_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON petrescue_db.* TO 'petrescue_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. Update `petrescue/settings.py` with your database credentials

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test suite
python manage.py test main.tests.AdminDashboardTestCase

# Run syntax check
python -m py_compile main/models.py main/views.py main/forms.py

# Run system checks
python manage.py check
```

### Test Coverage

The project includes:
- Unit tests for models and views
- Integration tests for user flows
- Admin functionality tests
- Cross-browser compatibility tests
- Mobile responsiveness tests
- Security tests
- Performance tests

## Documentation

- [User Guide](docs/user_guide.md) - How to use the platform
- [Admin Guide](docs/admin_guide.md) - How to manage the platform
- [Deployment Checklist](docs/deployment_checklist.md) - Steps for deployment
- [Test Matrix](docs/test_matrix.md) - Detailed testing documentation
- [UI Components Guide](docs/ui_components.md) - UI component documentation
- [QA Report](docs/qa_report.md) - Quality assurance report

## Project Structure

```
PetRescue/
├── main/                 # Main application
│   ├── models.py         # Data models
│   ├── views.py          # View functions
│   ├── forms.py          # Form definitions
│   ├── urls.py           # URL routing
│   ├── tests.py          # Test cases
│   └── templates/        # HTML templates
├── petrescue/            # Django project settings
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded files
├── docs/                 # Documentation files
├── requirements.txt      # Python dependencies
├── manage.py             # Django management script
└── README.md             # This file
```

## Health Check Endpoint

A health check endpoint is available at `/health/` for deployment verification:
```bash
curl http://127.0.0.1:8000/health/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact the development team or refer to the documentation.