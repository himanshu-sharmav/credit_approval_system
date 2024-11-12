from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'customer_id',
            'first_name',
            'last_name',
            'phone_number',
            'monthly_salary',
            'approved_limit',
            'current_debt',
            'age'
        ]


class LoanSerializer(serializers.ModelSerializer):
    # Including customer details using a nested serializer
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Loan
        fields = [
            'id',                  # Primary key field (auto-incremented)
            'loan_id',             # Loan ID (unique per customer, not globally)
            'customer',            # Foreign key to Customer
            'loan_amount',
            'tenure',
            'interest_rate',
            'monthly_repayment',
            'emis_paid_on_time',
            'start_date',
            'end_date'
        ]
