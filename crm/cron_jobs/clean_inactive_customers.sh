#!/bin/bash

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

DELETED=$(python manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)

qs = Customer.objects.filter(
    orders__isnull=True,
        created_at__lt=cutoff
        )

        count = qs.count()
        qs.delete()
        print(count)
        EOF
)

echo "$TIMESTAMP - Deleted customers: $DELETED" >> /tmp/customer_cleanup_log.txt