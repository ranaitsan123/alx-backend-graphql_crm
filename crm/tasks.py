import requests
from datetime import datetime
from celery import shared_task

@shared_task
def generate_crm_report():
    url = "http://localhost:8000/graphql"
    
    # GraphQL Query to get CRM stats
    query = """
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """
    
    try:
        response = requests.post(url, json={'query': query})
        data = response.json().get('data', {})
        
        customers = data.get('totalCustomers', 0)
        orders = data.get('totalOrders', 0)
        revenue = data.get('totalRevenue', 0)
        
        # Format: YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"
        
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(log_entry)
            
    except Exception as e:
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{datetime.now()} - Error generating report: {str(e)}\n")

