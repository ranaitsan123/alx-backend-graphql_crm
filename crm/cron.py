from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

        try:
                requests.post(
                            "http://localhost:8000/graphql",
                                        json={"query": "{ hello }"},
                                                    timeout=5,
                                                            )
                                                                    status = "CRM is alive"
                                                                        except Exception:
                                                                                status = "CRM unreachable"

                                                                                    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
                                                                                            f.write(f"{timestamp} {status}\n")

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

def update_low_stock():
    transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
                    verify=False,
                            retries=3,
                                )

                                    client = Client(transport=transport, fetch_schema_from_transport=True)

                                        mutation = gql("""
                                            mutation {
                                                  updateLowStockProducts {
                                                          products {
                                                                    name
                                                                              stock
                                                                                      }
                                                                                            }
                                                                                                }
                                                                                                    """)

                                                                                                        result = client.execute(mutation)

                                                                                                            with open("/tmp/low_stock_updates_log.txt", "a") as f:
                                                                                                                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                                                                                            for p in result["updateLowStockProducts"]["products"]:
                                                                                                                                        f.write(f"{ts} - {p['name']} -> {p['stock']}\n")