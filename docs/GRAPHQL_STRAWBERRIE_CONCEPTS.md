# GraphQL Concepts with Django (Strawberry GraphQL)

## Table of Contents
1. What is GraphQL?
2. Why GraphQL with Django?
3. GraphQL vs REST
4. Core GraphQL Concepts
5. Strawberry GraphQL Overview
6. Real-World Django + GraphQL Project Structure
7. Installing & Setting Up Strawberry
8. Defining GraphQL Types
9. Queries in Strawberry
10. Mutations in Strawberry
11. Authentication & Authorization (JWT)
12. Context & Request Lifecycle
13. Pagination & Filtering
14. Error Handling
15. Performance Optimization
16. Best Practices

---

## 1. What is GraphQL?

GraphQL is a **strongly typed API query language** that allows clients to request **exactly the data they need** using a single endpoint.

Instead of many endpoints returning fixed responses (REST), GraphQL exposes a **schema** describing all available data and operations.

---

## 2. Why GraphQL with Django?

Django excels at:
- ORM & database modeling
- Authentication & permissions
- Admin & security

GraphQL adds:
- Flexible data fetching
- Frontend-friendly APIs
- Strong typing & validation
- Reduced API churn

---

## 3. GraphQL vs REST

| Feature | REST | GraphQL |
|------|------|--------|
| Endpoints | Multiple | Single |
| Data Shape | Server-defined | Client-defined |
| Over-fetching | Common | Avoided |
| Versioning | Required | Rare |
| Schema | Optional | Mandatory |

---

## 4. Core GraphQL Concepts

### Schema
Defines **what clients can do**.

```graphql
type Query {
  users: [User!]!
}
````

---

### Types

Define the shape of data.

```graphql
type User {
  id: ID!
  username: String!
}
```

---

### Queries

Used to **fetch data**.

```graphql
query {
  users {
    username
  }
}
```

---

### Mutations

Used to **modify data**.

```graphql
mutation {
  createUser(username: "john") {
    id
  }
}
```

---

### Resolvers

Python functions that return data for fields.

---

### Context

Carries request-specific data (request, user, headers).

---

## 5. Strawberry GraphQL Overview

**Strawberry** is a modern Python GraphQL library that:

* Uses Python type hints
* Feels like writing normal Python
* Integrates cleanly with Django
* Is async-ready

---

## 6. Real-World Django + GraphQL Project Structure

```text
project/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── graphql/
│   │   │   ├── types.py
│   │   │   ├── queries.py
│   │   │   ├── mutations.py
│   │   │   └── permissions.py
│   │   └── apps.py
│
├── graphql/
│   ├── schema.py
│   ├── context.py
│   └── permissions.py
│
└── manage.py
```

✔ Keeps GraphQL logic modular
✔ Separates domain logic from API
✔ Scales cleanly

---

## 7. Installing & Setting Up Strawberry

### Installation

```bash
pip install strawberry-graphql strawberry-graphql-django djangorestframework-simplejwt
```

---

### URL Configuration

```python
# config/urls.py
from django.urls import path
from strawberry.django.views import GraphQLView
from graphql.schema import schema

urlpatterns = [
    path("graphql/", GraphQLView.as_view(schema=schema)),
]
```

---

## 8. Defining GraphQL Types

### Django Model

```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

---

### GraphQL Type

```python
# apps/users/graphql/types.py
import strawberry

@strawberry.type
class UserType:
    id: int
    username: str
    email: str | None
```

---

## 9. Queries in Strawberry

```python
# apps/users/graphql/queries.py
import strawberry
from .types import UserType
from apps.users.models import User

@strawberry.type
class UserQuery:
    @strawberry.field
    def users(self) -> list[UserType]:
        return User.objects.all()

    @strawberry.field
    def user(self, id: int) -> UserType | None:
        return User.objects.filter(id=id).first()
```

---

## 10. Mutations in Strawberry

```python
# apps/users/graphql/mutations.py
import strawberry
from .types import UserType
from apps.users.models import User

@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, username: str, password: str) -> UserType:
        user = User.objects.create_user(
            username=username,
            password=password
        )
        return user
```

---

## 11. Authentication & Authorization (JWT)

### JWT Setup (SimpleJWT)

```python
# settings.py
INSTALLED_APPS += ["rest_framework"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
```

---

### GraphQL Context

```python
# graphql/context.py
def get_context(request):
    return {
        "request": request,
        "user": request.user,
    }
```

Attach context:

```python
GraphQLView.as_view(schema=schema, get_context=get_context)
```

---

### Authenticated Resolver Example

```python
import strawberry
from strawberry.exceptions import GraphQLError

@strawberry.type
class SecureQuery:
    @strawberry.field
    def me(self, info) -> UserType:
        user = info.context["user"]
        if not user.is_authenticated:
            raise GraphQLError("Authentication required")
        return user
```

---

## 12. Context & Request Lifecycle

1. HTTP request hits `/graphql/`
2. Django middleware authenticates user
3. Strawberry builds context
4. Resolvers access `info.context`
5. Response returned as JSON

---

## 13. Pagination & Filtering

### Simple Pagination

```python
@strawberry.field
def users(self, limit: int = 10, offset: int = 0) -> list[UserType]:
    return User.objects.all()[offset:offset + limit]
```

---

## 14. Error Handling

Raise GraphQL-safe errors:

```python
from strawberry.exceptions import GraphQLError

raise GraphQLError("Invalid credentials")
```

Returned as:

```json
{
  "errors": [{ "message": "Invalid credentials" }]
}
```

---

## 15. Performance Optimization

✔ Use `select_related` & `prefetch_related`
✔ Avoid heavy business logic in resolvers
✔ Batch queries when possible
✔ Limit query depth
✔ Cache expensive fields

---

## 16. Best Practices

✔ Use service layers for business logic
✔ Keep resolvers thin
✔ Group GraphQL by domain
✔ Protect mutations
✔ Document schema descriptions
✔ Validate inputs

---

## Conclusion

Using **Strawberry GraphQL with Django** provides:

* Clean Pythonic APIs
* Strong typing
* Seamless Django integration
* Scalable architecture

This setup is **production-ready**, secure, and frontend-friendly.

---

### Recommended Next Steps

* Add role-based permissions
* Implement refresh tokens
* Add subscriptions (WebSockets)
* Add query depth limiting
* Introduce DataLoaders

```

---

## 17. Role-Based Permissions

Role-based permissions control **who can access which fields, queries, or mutations** based on user roles (e.g. ADMIN, STAFF, USER).

---

### 17.1 Defining Roles

Roles can be:
- Django Groups
- Boolean flags (`is_staff`, `is_superuser`)
- A custom model field (`role`)

#### Example: Role Field

```python
# apps/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN"
        STAFF = "STAFF"
        USER = "USER"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
````

---

### 17.2 Permission Helpers

Centralize permission logic.

```python
# graphql/permissions.py
from strawberry.exceptions import GraphQLError

def require_auth(user):
    if not user or not user.is_authenticated:
        raise GraphQLError("Authentication required")

def require_role(user, roles: list[str]):
    require_auth(user)
    if user.role not in roles:
        raise GraphQLError("You do not have permission")
```

---

### 17.3 Protecting Queries

```python
# apps/users/graphql/queries.py
import strawberry
from graphql.permissions import require_role
from .types import UserType
from apps.users.models import User

@strawberry.type
class AdminQuery:
    @strawberry.field
    def all_users(self, info) -> list[UserType]:
        user = info.context["user"]
        require_role(user, ["ADMIN"])
        return User.objects.all()
```

---

### 17.4 Protecting Mutations

```python
# apps/users/graphql/mutations.py
import strawberry
from graphql.permissions import require_role
from apps.users.models import User
from .types import UserType

@strawberry.type
class AdminMutation:
    @strawberry.mutation
    def promote_user(self, info, user_id: int) -> UserType:
        current_user = info.context["user"]
        require_role(current_user, ["ADMIN"])

        user = User.objects.get(id=user_id)
        user.role = "STAFF"
        user.save()
        return user
```

---

### 17.5 Field-Level Permissions

```python
@strawberry.type
class UserType:
    id: int
    username: str

    @strawberry.field
    def email(self, info) -> str | None:
        user = info.context["user"]
        if user.id != self.id and user.role != "ADMIN":
            return None
        return self.email
```

---

### Best Practices for Permissions

✔ Centralize permission checks
✔ Never trust client input
✔ Protect mutations first
✔ Prefer deny-by-default
✔ Log permission failures

---

## 18. GraphQL Subscriptions (Real-Time Updates)

Subscriptions enable **real-time communication** over **WebSockets**.

Typical use cases:

* Notifications
* Live chat
* Status updates
* Dashboards

---

## 18.1 Requirements

```bash
pip install strawberry-graphql[channels] channels channels-redis
```

---

## 18.2 Django Channels Setup

### settings.py

```python
INSTALLED_APPS += ["channels"]

ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

---

### asgi.py

```python
# config/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from strawberry.channels import GraphQLWSConsumer
from graphql.schema import schema

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("graphql/", GraphQLWSConsumer.as_asgi(schema=schema)),
    ]),
})
```

---

## 18.3 Defining Subscriptions

```python
# graphql/subscriptions.py
import strawberry

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def notifications(self, info) -> str:
        for i in range(1, 6):
            yield f"Notification {i}"
```

---

## 18.4 Publishing Events

```python
from strawberry.channels import broadcast

async def send_notification(message: str):
    await broadcast.publish(
        channel="notifications",
        message=message,
    )
```

---

## 18.5 Securing Subscriptions

```python
@strawberry.subscription
async def secure_notifications(self, info) -> str:
    user = info.context["user"]
    if not user.is_authenticated:
        raise Exception("Authentication required")

    async for message in info.context["pubsub"].subscribe("notifications"):
        yield message
```

---

## 18.6 Subscription Example (Client)

```graphql
subscription {
  notifications
}
```

---

## Best Practices for Subscriptions

✔ Authenticate WebSocket connections
✔ Avoid heavy logic in subscriptions
✔ Use Redis for scaling
✔ Clean up unused connections
✔ Apply rate limiting

---

## Summary

You now have:
✔ Role-based access control
✔ Secure admin-only operations
✔ Real-time GraphQL subscriptions
✔ WebSocket support via Django Channels

This completes a **production-grade GraphQL stack with Django**.

---

### Recommended Next Enhancements

* Field-level permission decorators
* Subscription authorization middleware
* Query complexity limiting
* Audit logging

---

## 19. Unit Testing GraphQL Permissions

Testing permissions is critical because **GraphQL has a single endpoint**.  
You must ensure unauthorized users **cannot access protected fields or mutations**.

---

### 19.1 Testing Strategy

We test:
- Unauthenticated access → ❌ denied
- Authenticated user without role → ❌ denied
- Authorized role → ✅ allowed

We use:
- Django `TestCase`
- Strawberry test client
- JWT authentication headers

---

### 19.2 GraphQL Test Utilities

```python
# tests/utils.py
from strawberry.test import GraphQLTestClient
from graphql.schema import schema

def gql_client():
    return GraphQLTestClient(schema)
````

---

### 19.3 Permission Test Example

#### Protected Query

```python
@strawberry.field
def all_users(self, info) -> list[UserType]:
    require_role(info.context["user"], ["ADMIN"])
    return User.objects.all()
```

---

#### Test Case

```python
# apps/users/tests/test_permissions.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from tests.utils import gql_client

User = get_user_model()

class AdminQueryPermissionTest(TestCase):

    def setUp(self):
        self.client = gql_client()
        self.user = User.objects.create_user(
            username="user",
            password="pass",
            role="USER",
        )

    def test_denies_non_admin(self):
        response = self.client.query(
            """
            query {
              allUsers {
                id
              }
            }
            """,
            context_value={"user": self.user},
        )

        assert response.errors is not None
        assert "permission" in response.errors[0].message.lower()
```

---

### 19.4 Testing Admin Access

```python
def test_allows_admin(self):
    admin = User.objects.create_user(
        username="admin",
        password="pass",
        role="ADMIN",
    )

    response = self.client.query(
        """
        query {
          allUsers {
            id
          }
        }
        """,
        context_value={"user": admin},
    )

    assert response.errors is None
    assert len(response.data["allUsers"]) >= 1
```

---

### Testing Best Practices

✔ Test unauthorized access first
✔ Test allowed roles explicitly
✔ Assert error messages
✔ Avoid hitting database unnecessarily
✔ Keep permission logic centralized

---

## 20. JWT Refresh Token Rotation

Refresh token rotation improves security by:

* Issuing a **new refresh token on every refresh**
* Invalidating old tokens
* Preventing token replay attacks

---

### 20.1 Enable Refresh Token Rotation

```python
# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

---

### 20.2 Install Blacklist App

```python
INSTALLED_APPS += [
    "rest_framework_simplejwt.token_blacklist",
]
```

```bash
python manage.py migrate
```

---

### 20.3 Token Flow

1. User logs in → access + refresh token
2. Access token expires
3. Client sends refresh token
4. Server:

   * Issues new access token
   * Issues new refresh token
   * Blacklists old refresh token

---

### 20.4 GraphQL Login Mutation

```python
@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def login(self, username: str, password: str) -> dict:
        user = authenticate(username=username, password=password)
        if not user:
            raise GraphQLError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
```

---

### 20.5 Refresh Token Mutation

```python
@strawberry.mutation
def refresh_token(self, refresh: str) -> dict:
    token = RefreshToken(refresh)
    return {
        "access": str(token.access_token),
        "refresh": str(token),
    }
```

---

### Security Best Practices

✔ Store refresh tokens securely (HTTP-only cookies)
✔ Short access-token lifetime
✔ Always rotate refresh tokens
✔ Enable blacklist
✔ Revoke tokens on logout

---

## 21. JWT Authentication for GraphQL Subscriptions

WebSockets **do not use HTTP headers the same way**, so JWT handling must be explicit.

---

### 21.1 Passing JWT via WebSocket Connection

Client sends token in connection params:

```json
{
  "type": "connection_init",
  "payload": {
    "Authorization": "Bearer <ACCESS_TOKEN>"
  }
}
```

---

### 21.2 Custom Subscription Context

```python
# graphql/context.py
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_ws_context(connection_params):
    auth = connection_params.get("Authorization")
    if not auth:
        return {"user": None}

    token = auth.replace("Bearer ", "")
    jwt_auth = JWTAuthentication()

    validated = jwt_auth.get_validated_token(token)
    user = jwt_auth.get_user(validated)

    return {"user": user}
```

---

### 21.3 Secure Subscription Resolver

```python
@strawberry.subscription
async def notifications(self, info) -> str:
    user = info.context["user"]
    if not user or not user.is_authenticated:
        raise Exception("Authentication required")

    async for message in info.context["pubsub"].subscribe("notifications"):
        yield message
```

---

### 21.4 Wiring WebSocket Auth

```python
GraphQLWSConsumer.as_asgi(
    schema=schema,
    get_context=get_ws_context,
)
```

---

### Subscription Security Checklist

✔ Validate JWT at connection time
✔ Reject unauthenticated sockets
✔ Do not trust client payloads
✔ Close connections on auth failure
✔ Use short-lived access tokens

---

## Final Summary

You now have:

✔ Fully tested permission logic
✔ Secure JWT refresh-token rotation
✔ Authenticated GraphQL subscriptions
✔ Production-ready security patterns

This completes a **robust, enterprise-grade GraphQL setup for Django**.

---

### Final Recommended Enhancements

* Query complexity limits
* Rate limiting per user
* Audit logs for admin actions
* Permission decorators
* CI pipeline for GraphQL tests

---

## 22. Final Recommended Enhancements

Even with a fully functional and secure GraphQL setup, these enhancements help **future-proof and harden** your application:

---

### 22.1 Query Complexity Limits

Prevent malicious or overly expensive queries:

```python
# graphql/schema.py
from strawberry.extensions import Extension

class QueryComplexityLimit(Extension):
    def on_request_start(self):
        self.query_depth = 0

    def on_field_resolve(self, _):
        self.query_depth += 1
        if self.query_depth > 10:  # example depth limit
            raise Exception("Query too complex")
```

Attach to Strawberry view:

```python
GraphQLView.as_view(schema=schema, extensions=[QueryComplexityLimit])
```

✔ Protects against DoS attacks  
✔ Encourages efficient queries

---

### 22.2 Rate Limiting per User

Throttle requests to avoid abuse:

```python
# graphql/context.py
from django.core.cache import cache
from datetime import datetime, timedelta

def rate_limit(user):
    key = f"rate:{user.id}"
    attempts = cache.get(key, 0)
    if attempts >= 100:  # max 100 requests per period
        raise Exception("Rate limit exceeded")
    cache.set(key, attempts + 1, timeout=60)  # 1 minute
```

Call in resolvers or middleware.

---

### 22.3 Audit Logging for Admin Actions

Track sensitive mutations:

```python
import logging

logger = logging.getLogger("audit")

def log_admin_action(user, action, target):
    logger.info(f"{datetime.now()} | {user.username} performed {action} on {target}")
```

Call after every admin mutation, e.g., `promote_user`.

---

### 22.4 Permission Decorators

Simplify field and resolver protection:

```python
from functools import wraps
from graphql.permissions import require_role

def requires_roles(roles: list[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, info, **kwargs):
            user = info.context["user"]
            require_role(user, roles)
            return func(*args, info=info, **kwargs)
        return wrapper
    return decorator
```

Usage:

```python
@strawberry.field
@requires_roles(["ADMIN"])
def all_users(self, info) -> list[UserType]:
    return User.objects.all()
```

✔ Reduces boilerplate  
✔ Centralizes permission logic

---

### 22.5 CI Pipeline for GraphQL Tests

Automate testing and validation:

* Run `pytest` on every pull request
* Include GraphQL test queries and mutation tests
* Fail builds on permission or security regressions

```yaml
# .github/workflows/test.yml
name: Test GraphQL

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python manage.py migrate
      - run: pytest
```

✔ Ensures schema and permissions remain correct  
✔ Prevents regressions in CI/CD

---

### 22.6 Summary

By implementing these **final enhancements**, your Django + Strawberry GraphQL stack becomes:

* **Resilient**: Query complexity and rate limits  
* **Auditable**: Admin actions logged  
* **Secure**: Centralized permissions and decorators  
* **Maintainable**: Automated tests via CI  

You now have a **complete, production-grade, enterprise-ready GraphQL setup** ready for both REST-like flexibility and real-time subscriptions.

---
