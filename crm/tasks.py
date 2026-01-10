from celery import shared_task
from datetime import datetime
from django.db.models import Sum
# Import your models - assuming Customer and Order names
from .models import Customer, Order 

@shared_task
def generate_crm_report():
    # 1. Fetch Data (Aggregating like a GraphQL resolver)
        total_customers = Customer.objects.count()
            total_orders = Order.objects.count()
                total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

                    # 2. Format Timestamp and Message
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            report_msg = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

                                # 3. Log to file
                                    with open('/tmp/crm_report_log.txt', 'a') as f:
                                            f.write(report_msg)
                                                
                                                    return "Report Generated Successfully"
                                                    