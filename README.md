# TICKET TICKET

Helps you find event tickets & more...

## Getting Started

1. Create a virtual python environment
2. Install requirements.txt
3. Make migrations
4. Migrate
5. Create superuser
6. Start Django server
7. Start Redis server
8. Run Celery worker
9. Run Celery Beat scheduler

### Prerequisites

How to run the application for the first time

```bash
# Install requirements
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations
# Migrate
python manage.py migrate
# Create superuser
python manage.py createsuperuser
# Run server
python manage.py runserver
# Run Celery worker
celery -A ticketicket worker -l INFO -P solo
# Run Celery Beat scheduler
celery -A ticketicket beat -l info -S django