# CRM Task Automation with Celery

This project implements automated weekly reporting using Celery, Celery Beat, and Redis.

## Prerequisites
- Redis Server installed and running.
- Python dependencies installed from `requirements.txt`.

## Setup and Installation

1. **Install Redis and dependencies**:
   ```bash
   sudo apt update
   sudo apt install redis-server -y
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   Create the necessary tables for `django-celery-beat`:
   ```bash
   python manage.py migrate
   ```

3. **Start Celery Worker**:
   Open a new terminal and run:
   ```bash
   celery -A crm worker -l info
   ```

4. **Start Celery Beat**:
   Open another terminal and run:
   ```bash
   celery -A crm beat -l info
   ```

## Verification
To verify that the weekly report task is running or to check the output of the logs:
- Check the log file: `cat /tmp/crm_report_log.txt`
- The report is scheduled to run every Monday at 6:00 AM.

## Best Practices
- Ensure Redis is running before starting Celery.
- Use absolute paths in production environments.
