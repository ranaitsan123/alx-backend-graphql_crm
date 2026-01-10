from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
        verify=False,
            retries=3,
            )

            client = Client(transport=transport, fetch_schema_from_transport=True)

            query = gql("""
            query OrdersLastWeek($since: DateTime!) {
              orders(orderDate_Gte: $since) {
                  id
                      customer {
                            email
                                }
                                  }
                                  }
                                  """)

                                  since = (datetime.now() - timedelta(days=7)).isoformat()
                                  result = client.execute(query, variable_values={"since": since})

                                  with open("/tmp/order_reminders_log.txt", "a") as f:
                                      for order in result.get("orders", []):
                                              ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                      f.write(
                                                                  f"{ts} - Order {order['id']} "
                                                                              f"Customer {order['customer']['email']}\n"
                                                                                      )

                                                                                      print("Order reminders processed!")