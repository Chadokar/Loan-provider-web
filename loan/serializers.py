# serializers.py
from rest_framework import serializers
from .models import Loans


class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ['id', 'customer_id', 'loan_amount', 'interest_rate', 'tenure', 'monthly_installment',
                  'emis_paid_on_time', 'repayments_left', 'date_of_approval', 'end_date']
