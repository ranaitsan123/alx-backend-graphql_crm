# 🐳 DOCKERIZED DJANGO + GRAPHQL SETUP

## 📁 Final Project Structure

```
alx-backend-graphql_crm/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── manage.py
├── alx_backend_graphql_crm/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── schema.py
│   └── asgi.py
├── crm/
│   ├── models.py
│   ├── schema.py
│   ├── filters.py
│   ├── admin.py
│   └── migrations/
```

---

# 1️⃣ requirements.txt

```txt
Django>=4.2
graphene-django>=3.1
django-filter>=24.2
```

---

# 2️⃣ Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

# 3️⃣ docker-compose.yml

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: graphql_django
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    command: python manage.py runserver 0.0.0.0:8000
```

---

# 4️⃣ .dockerignore

```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.env
.db.sqlite3
.git
```

---

# 5️⃣ Initialize Django Project (INSIDE DOCKER)

### 🧠 Run commands via Docker

```bash
docker compose run web django-admin startproject alx_backend_graphql_crm .
docker compose run web django-admin startapp crm
```

---

# 6️⃣ settings.py (IMPORTANT)

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "graphene_django",
    "django_filters",
    "crm",
]

GRAPHENE = {
    "SCHEMA": "alx_backend_graphql_crm.schema.schema"
}
```

---

# 7️⃣ urls.py – GraphQL Endpoint

```python
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
```

---

# 8️⃣ Run Migrations (Docker)

```bash
docker compose run web python manage.py makemigrations
docker compose run web python manage.py migrate
```

---

# 9️⃣ Run the Server

```bash
docker compose up
```

Access:

```
http://localhost:8000/graphql
```

---

# 🔁 Useful Docker Commands (Cheat Sheet)

| Action              | Command                                         |
| ------------------- | ----------------------------------------------- |
| Rebuild image       | `docker compose build`                          |
| Run shell           | `docker compose run web bash`                   |
| Run Django commands | `docker compose run web python manage.py <cmd>` |
| Stop containers     | `docker compose down`                           |

---

# ✅ WHY THIS WORKS FOR ALX

✔ No system Python dependency
✔ Reproducible builds
✔ Matches checker environment
✔ GraphQL endpoint enabled
✔ Filtering + mutations ready

