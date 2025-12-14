## 🧪 GraphQL Mutation & Query Examples

This section shows **how to interact with the GraphQL API** using real examples.
All examples can be tested in **GraphiQL** at:

```
http://localhost:8000/graphql
```

---

## 🔹 Basic Query Example

### Hello World Query

This confirms that the GraphQL endpoint is working.

```graphql
{
  hello
}
```

### Response

```json
{
  "data": {
    "hello": "Hello, GraphQL!"
  }
}
```

✅ What we learned:

* How GraphQL queries work
* How resolvers return data
* How to test APIs using GraphiQL

---

## 🔹 Customer Mutations

### 1️⃣ Create a Single Customer

Creates one customer with validation.

```graphql
mutation {
  createCustomer(
    name: "Alice",
    email: "alice@example.com",
    phone: "+1234567890"
  ) {
    customer {
      id
      name
      email
      phone
    }
    message
  }
}
```

#### What this does:

* Saves a customer to the database
* Validates email uniqueness
* Validates phone number format

✅ Concepts learned:

* GraphQL mutations
* Input validation
* Custom success messages

---

### 2️⃣ Bulk Create Customers (Partial Success)

Creates multiple customers in one request.

```graphql
mutation {
  bulkCreateCustomers(input: [
    { name: "Bob", email: "bob@example.com", phone: "123-456-7890" },
    { name: "Carol", email: "carol@example.com" }
  ]) {
    customers {
      id
      name
      email
    }
    errors
  }
}
```

#### What this does:

* Creates valid customers
* Skips invalid ones
* Returns errors without stopping the whole operation

✅ Concepts learned:

* GraphQL `InputObjectType`
* Bulk operations
* Partial success handling

---

## 🔹 Product Mutations

### 3️⃣ Create a Product

```graphql
mutation {
  createProduct(
    name: "Laptop",
    price: 999.99,
    stock: 10
  ) {
    product {
      id
      name
      price
      stock
    }
  }
}
```

#### What this does:

* Creates a product
* Ensures price is positive
* Ensures stock is non-negative

✅ Concepts learned:

* Business logic validation
* Decimal fields in GraphQL
* Data integrity rules

---

## 🔹 Order Mutations

### 4️⃣ Create an Order with Products

```graphql
mutation {
  createOrder(
    customerId: "1",
    productIds: ["1", "2"]
  ) {
    order {
      id
      customer {
        name
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
  }
}
```

#### What this does:

* Links a customer to products
* Automatically calculates total amount
* Returns nested related data

✅ Concepts learned:

* Many-to-many relationships
* Nested GraphQL responses
* Server-side calculations

---

## 🔹 Filtering Queries

### 5️⃣ Filter Customers by Name and Date

```graphql
query {
  allCustomers(filter: {
    nameIcontains: "Ali"
  }) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

#### What this does:

* Searches customers by partial name match
* Returns paginated results

✅ Concepts learned:

* Filtering with `django-filter`
* Case-insensitive searches
* Relay connections (`edges`, `node`)

---

### 6️⃣ Filter Products by Price Range and Sort by Stock

```graphql
query {
  allProducts(
    filter: { priceGte: 100, priceLte: 1000 }
  ) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

✅ Concepts learned:

* Range filtering
* Efficient database queries
* Product inventory analysis

---

### 7️⃣ Filter Orders by Customer and Product

```graphql
query {
  allOrders(filter: {
    customerName: "Alice",
    productName: "Laptop",
    totalAmountGte: 500
  }) {
    edges {
      node {
        id
        customer {
          name
        }
        products {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

#### What this does:

* Finds orders by customer name
* Filters by product name
* Filters by total amount

✅ Concepts learned:

* Filtering related models
* Complex queries
* Real-world reporting use cases

---

## 🧠 Summary of What These Examples Teach

| Concept               | Learned Through                |
| --------------------- | ------------------------------ |
| Queries vs Mutations  | Hello query & CRUD operations  |
| Input validation      | CreateCustomer & CreateProduct |
| Bulk operations       | BulkCreateCustomers            |
| Relationships         | CreateOrder                    |
| Nested data           | Order → Customer → Products    |
| Filtering & search    | allCustomers, allOrders        |
| Real-world API design | CRM use case                   |

