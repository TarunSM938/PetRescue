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
- MySQL 8.0 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/petrescue.git
cd petrescue
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

1. Create a MySQL database:
   ```sql
   CREATE DATABASE petrescue_db;
   CREATE USER 'petrescue_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON petrescue_db.* TO 'petrescue_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. Update database settings in `petrescue/settings.py` with your database credentials

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Production Server

For production deployment, use Gunicorn:

```bash
gunicorn petrescue.wsgi:application --bind 0.0.0.0:8000
```

## Environment Variables

For production deployment, set the following environment variables:

```bash
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=petrescue_production
DB_USER=petrescue_user
DB_PASSWORD=your_secure_password
DB_HOST=your_database_host
DB_PORT=3306
```

## Project Structure

```
petrescue/
├── main/                 # Main application
│   ├── models.py         # Data models
│   ├── views.py          # View functions
│   ├── forms.py          # Form definitions
│   ├── templates/        # HTML templates
│   └── static/           # Static files (CSS, JS, images)
├── petrescue/            # Project settings
│   ├── settings.py       # Configuration settings
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI entry point
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Key Models

- **User**: Custom user model with phone number field
- **Profile**: Extended user profile information
- **Pet**: Pet information (lost, found, or adoptable)
- **Request**: User requests related to pets
- **ActivityLog**: Tracking of all activities
- **Notification**: Admin notifications
- **ContactSubmission**: User contact form submissions

## Testing

### Running Tests

```bash
python manage.py test
```

### Test Coverage

The project includes:
- Unit tests for models and views
- Integration tests for key workflows
- Admin permission tests
- Form validation tests

## Documentation

- [User Guide](docs/user_guide.md) - How to use the platform
- [Admin Guide](docs/admin_guide.md) - How to manage the platform
- [Deployment Checklist](docs/deployment_checklist.md) - Steps for production deployment
- [Test Matrix](docs/test_matrix.md) - Comprehensive testing documentation

## Deployment

See [Deployment Checklist](docs/deployment_checklist.md) for detailed deployment instructions.

### Quick Deployment Steps

1. Set up production database
2. Configure environment variables
3. Run migrations
4. Collect static files
5. Start Gunicorn server
6. Configure Nginx reverse proxy (recommended)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact:
- Email: support@petrescue.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/petrescue/issues)

## Acknowledgements

- Thanks to all contributors who have helped build this platform
- Inspired by the need to help pets find their way home
- Built with Django, Bootstrap, and ❤️