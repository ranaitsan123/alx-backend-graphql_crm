# GraphQL Concepts & Django Integration

## Table of Contents
1. What is GraphQL?
2. Why Use GraphQL?
3. GraphQL vs REST
4. Core GraphQL Concepts
   - Schema
   - Types
   - Fields
   - Queries
   - Mutations
   - Resolvers
   - Arguments
   - Input Types
   - Enums
   - Interfaces & Unions
5. GraphQL Execution Flow
6. Using GraphQL in Django
   - Choosing a Library
   - Installation
   - Basic Setup
7. Defining GraphQL Types from Django Models
8. Queries in Django GraphQL
9. Mutations in Django GraphQL
10. Authentication & Authorization
11. Pagination & Filtering
12. Error Handling
13. Performance Considerations
14. GraphQL Best Practices

---

## 1. What is GraphQL?

GraphQL is a **query language for APIs** and a **runtime** for executing those queries.  
It allows clients to request **exactly the data they need**, no more and no less.

Instead of multiple endpoints (as in REST), GraphQL typically exposes **a single endpoint**.

---

## 2. Why Use GraphQL?

✔ Fetch only required data  
✔ Avoid over-fetching and under-fetching  
✔ Strongly typed schema  
✔ Self-documenting API  
✔ Ideal for frontend-heavy applications (React, Vue, Mobile apps)

---

## 3. GraphQL vs REST

| Feature | REST | GraphQL |
|------|------|--------|
| Endpoints | Multiple | Single |
| Data Shape | Fixed | Client-defined |
| Over-fetching | Common | Avoided |
| Versioning | Required | Rare |
| Typing | Weak | Strong |

---

## 4. Core GraphQL Concepts

### Schema
The **schema** defines what data can be queried or modified.

```graphql
type Query {
  users: [User]
}
````

---

### Types

Types define the structure of data.

```graphql
type User {
  id: ID!
  username: String!
  email: String
}
```

---

### Fields

Fields are properties of a type.

```graphql
user {
  id
  username
}
```

---

### Queries

Queries are used to **read data**.

```graphql
query {
  users {
    username
    email
  }
}
```

---

### Mutations

Mutations are used to **create, update, or delete data**.

```graphql
mutation {
  createUser(username: "john", email: "john@example.com") {
    user {
      id
      username
    }
  }
}
```

---

### Resolvers

Resolvers are **functions that return data** for a field.

In Django, resolvers usually interact with models.

---

### Arguments

Arguments allow passing parameters to queries or mutations.

```graphql
user(id: 1) {
  username
}
```

---

### Input Types

Used to pass complex data to mutations.

```graphql
input UserInput {
  username: String!
  email: String!
}
```

---

### Enums

Enums restrict values to a fixed set.

```graphql
enum UserRole {
  ADMIN
  USER
}
```

---

### Interfaces & Unions

Used for polymorphism.

* **Interface**: Shared fields
* **Union**: Multiple possible types

---

## 5. GraphQL Execution Flow

1. Client sends a query
2. GraphQL validates it against the schema
3. Resolvers fetch data
4. Response is returned as JSON

---

## 6. Using GraphQL in Django

### Choosing a Library

Popular Django GraphQL libraries:

* **Graphene-Django** (most common)
* Strawberry GraphQL
* Ariadne

This document uses **Graphene-Django**.

---

### Installation

```bash
pip install graphene-django
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "graphene_django",
]
```

---

### Basic Setup

Create `schema.py`:

```python
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

schema = graphene.Schema(query=Query)
```

In `urls.py`:

```python
from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]
```

---

## 7. Defining GraphQL Types from Django Models

### Django Model

```python
from django.contrib.auth.models import User
```

### GraphQL Type

```python
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")
```

---

## 8. Queries in Django GraphQL

```python
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)
```

### Example Query

```graphql
query {
  users {
    username
    email
  }
}
```

---

## 9. Mutations in Django GraphQL

### Create User Mutation

```python
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, email):
        user = User.objects.create(username=username, email=email)
        return CreateUser(user=user)
```

Register mutation:

```python
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
```

Update schema:

```python
schema = graphene.Schema(query=Query, mutation=Mutation)
```

---

## 10. Authentication & Authorization

Graphene integrates with Django authentication:

```python
user = info.context.user
if not user.is_authenticated:
    raise Exception("Authentication required")
```

You can use:

* Django permissions
* Custom decorators
* JWT authentication (`django-graphql-jwt`)

---

## 11. Pagination & Filtering

Graphene-Django supports Django filters:

```python
from graphene_django.filter import DjangoFilterConnectionField
```

```python
users = DjangoFilterConnectionField(UserType)
```

---

## 12. Error Handling

GraphQL returns structured errors:

```json
{
  "errors": [
    {
      "message": "User not found"
    }
  ]
}
```

Raise errors in resolvers:

```python
raise Exception("Invalid input")
```

---

## 13. Performance Considerations

* Avoid N+1 queries
* Use `select_related` / `prefetch_related`
* Use DataLoader pattern
* Limit query depth

---

## 14. GraphQL Best Practices

✔ Keep schemas simple
✔ Use descriptive field names
✔ Validate inputs
✔ Secure mutations
✔ Document your schema
✔ Avoid heavy logic in resolvers

---

## Conclusion

GraphQL provides a **powerful and flexible API layer** for Django applications.
With Graphene-Django, you can quickly expose Django models while maintaining strong typing, performance, and security.

---

**Recommended Next Steps**

* Add JWT authentication
* Introduce pagination
* Implement subscriptions (WebSockets)
* Add query depth limiting

```

