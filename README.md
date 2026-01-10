# ALX Backend: Crons, Scheduling, and Automating Tasks

This project focuses on automating repetitive tasks within a Django-based CRM application. It covers three levels of automation: native System Crontabs, Django-integrated Crons, and Distributed Task Queues (Celery).

## 🚀 Features

### 1. System Cron Jobs (Native Unix)
- **Customer Cleanup**: A shell script (`clean_inactive_customers.sh`) that identifies and deletes customers with no orders in the last year.
- **Order Reminders**: A Python script (`send_order_reminders.py`) that queries the GraphQL API to find recent orders and logs reminders.

### 2. Django-Crontab (Integrated)
- **Heartbeat Logger**: A recurring task that logs the system status every 5 minutes to verify application health.
- **Low Stock रेस्टॉक (Restock)**: A 12-hour cron job that triggers a GraphQL mutation to restock products with less than 10 units.

### 3. Celery & Celery Beat (Distributed)
- **Weekly CRM Report**: A robust, scheduled task that fetches total customers, orders, and revenue via GraphQL and generates a summary log every Monday at 6:00 AM.

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.x
- Redis Server (Required for Celery)
- SQLite (Default Database)

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/alx-backend-graphql_crm.git
   cd alx-backend-graphql_crm
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install & Start Redis**:
   ```bash
   sudo apt update
   sudo apt install redis-server -y
   sudo systemctl start redis-server
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

---

## 📅 Scheduling Tasks

### System Crontab (Tasks 0 & 1)
To install the native cron jobs into your system:
```bash
crontab crm/cron_jobs/customer_cleanup_crontab.txt
crontab crm/cron_jobs/order_reminders_crontab.txt
```

### Django-Crontab (Tasks 2 & 3)
To add the Django-managed jobs:
```bash
python manage.py crontab add
python manage.py crontab show
```

### Celery Beat (Task 4)
To run the asynchronous weekly report:
1. **Start the Worker**:
   ```bash
   celery -A crm worker -l info
   ```
2. **Start the Beat Scheduler**:
   ```bash
   celery -A crm beat -l info
   ```

---

## 📂 Project Structure
- `crm/cron_jobs/`: Contains shell and python scripts for system-level crons.
- `crm/cron.py`: Functions for `django-crontab`.
- `crm/tasks.py`: Periodic tasks for Celery.
- `crm/celery.py`: Celery application configuration.

## 📝 Logs
Task outputs can be monitored in the `/tmp/` directory:
- `/tmp/customer_cleanup_log.txt`
- `/tmp/order_reminders_log.txt`
- `/tmp/crm_heartbeat_log.txt`
- `/tmp/low_stock_updates_log.txt`
- `/tmp/crm_report_log.txt`

