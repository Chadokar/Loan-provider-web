# models.py
from django.db import models


class Loans(models.Model):
    customer_id = models.IntegerField()
    loan_amount = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()
    monthly_installment = models.PositiveIntegerField()
    emis_paid_on_time = models.PositiveIntegerField(null=True)
    repayments_left = models.PositiveIntegerField(null=True)
    date_of_approval = models.DateField(null=True)
    end_date = models.DateField(null=True)

    REQUIRED_FIELDS = ['customer_id', 'loan_amount',
                       'interest_rate', 'tenure', 'monthly_installment']
