# 📊 ALX Backend GraphQL CRM

## 📌 Project Overview

This project is part of the **ALX ProDev Backend curriculum** and focuses on **understanding GraphQL** and **building a real-world CRM (Customer Relationship Management) API** using:

* **Django**
* **Graphene-Django (GraphQL for Django)**
* **Docker**
* **django-filter**

Instead of using traditional REST APIs with many endpoints, we built a **single GraphQL endpoint** that allows clients to request **exactly the data they need**.

---

## 🎯 Learning Objectives

By completing this project, we learned how to:

* Understand **GraphQL vs REST**
* Design a **GraphQL schema**
* Create **queries and mutations**
* Integrate **Django models** with GraphQL
* Handle **validation and errors**
* Support **bulk operations**
* Add **filtering and searching**
* Use **Docker** for reproducible development environments

---

## 🧠 Key Concepts Explained (Beginner Friendly)

### 1️⃣ What is GraphQL?

GraphQL is a **query language for APIs**.

Instead of:

```
/customers/
/customers/1/
/customers/1/orders/
```

GraphQL uses **one endpoint**:

```
/graphql
```

And the client decides **what data to fetch**.

Example:

```graphql
{
  customer {
    name
    orders {
      totalAmount
    }
  }
}
```

➡️ No over-fetching
➡️ No under-fetching
➡️ One request, precise data

---

### 2️⃣ Why Django + Graphene?

* **Django** gives us:

  * ORM (database models)
  * Migrations
  * Admin panel
* **Graphene-Django**:

  * Converts Django models into GraphQL types
  * Handles queries and mutations cleanly

---

### 3️⃣ Why Docker?

Docker ensures:

* Same environment for everyone
* No “works on my machine” problems
* Easy setup in **GitHub Codespaces**

We used Docker to:

* Install Python dependencies
* Run Django
* Run migrations
* Serve the GraphQL API

---

## 🐳 Docker Setup Summary

### Files Used

| File                 | Purpose                            |
| -------------------- | ---------------------------------- |
| `Dockerfile`         | Builds Python + Django environment |
| `docker-compose.yml` | Runs Django server                 |
| `requirements.txt`   | Python dependencies                |

### Run the Project

```bash
docker compose build
docker compose run web python manage.py migrate
docker compose up
```

Access:

```
http://localhost:8000/graphql
```

---

## 📂 Project Structure

```
alx-backend-graphql_crm/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── alx_backend_graphql_crm/
│   ├── settings.py
│   ├── urls.py
│   ├── schema.py
├── crm/
│   ├── models.py
│   ├── schema.py
│   ├── filters.py
│   └── migrations/
```

---

## ✅ Task Breakdown & What We Learned

---

## 🟢 Task 0: Set Up GraphQL Endpoint

### 🎯 Goal

Create a basic GraphQL endpoint and verify it works.

### What We Did

* Created a GraphQL schema
* Added a simple `hello` query
* Connected `/graphql` endpoint

### Code Example

```graphql
{
  hello
}
```

### What We Learned

* How GraphQL schemas work
* How resolvers return data
* How to use GraphiQL for testing

---

## 🟢 Task 1 & 2: CRM Models + GraphQL Mutations

### 🎯 Goal

Build a real CRM system with:

* Customers
* Products
* Orders

### Models Created

| Model    | Purpose                     |
| -------- | --------------------------- |
| Customer | Stores client info          |
| Product  | Stores items for sale       |
| Order    | Links customers to products |

---

### 🔹 Mutations Implemented

#### 1️⃣ CreateCustomer

Creates one customer with validation.

Validation:

* Email must be unique
* Phone format must be valid

What we learned:

* Input validation
* Custom error messages

---

#### 2️⃣ BulkCreateCustomers

Creates many customers in one request.

Why?

* Efficient for importing data
* Real-world CRM use case

Special feature:

* **Partial success** (valid records are saved even if others fail)

What we learned:

* GraphQL input types
* Transactions and error handling

---

#### 3️⃣ CreateProduct

Creates products with:

* Positive price
* Non-negative stock

What we learned:

* Business logic validation
* Decimal handling

---

#### 4️⃣ CreateOrder

Creates an order with:

* Existing customer
* Multiple products
* Automatic total calculation

What we learned:

* Many-to-many relationships
* Nested GraphQL responses
* Data consistency

---

### Example Mutation

```graphql
mutation {
  createOrder(input: {
    customerId: "1",
    productIds: ["1", "2"]
  }) {
    order {
      customer { name }
      products { name price }
      totalAmount
    }
  }
}
```

---

## 🟢 Task 3: Filtering & Searching

### 🎯 Goal

Allow users to **search and filter data** efficiently.

### Tool Used

**django-filter**

---

### Filters Implemented

#### Customers

* Name (contains)
* Email (contains)
* Phone pattern
* Date range

#### Products

* Name
* Price range
* Stock range
* Low stock detection

#### Orders

* Total amount range
* Date range
* Customer name
* Product name

---

### Example Query

```graphql
query {
  allCustomers(filter: { nameIcontains: "Ali" }) {
    edges {
      node {
        name
        email
      }
    }
  }
}
```

### What We Learned

* Filtering related models
* Efficient querying
* Clean schema design

---

## 🧪 Testing Tools Used

* **GraphiQL** (built-in browser UI)
* **Docker logs** for debugging
* GraphQL introspection

---

## 📚 Key Takeaways

✔ GraphQL gives **flexible data querying**
✔ Django integrates well with GraphQL
✔ Docker simplifies setup and deployment
✔ Validation and errors are critical
✔ Filtering improves performance and usability

---

## 🚀 Future Improvements

* Authentication (JWT)
* Pagination optimization
* PostgreSQL database
* GraphQL subscriptions
* Kubernetes deployment

---

## 🏁 Conclusion

This project helped us move from **theory to practice** by building a **real-world GraphQL API** with Django.
We learned how modern APIs are designed, secured, and optimized — skills essential for backend developers.

---

**© 2025 ALX — ProDev Backend Program**

