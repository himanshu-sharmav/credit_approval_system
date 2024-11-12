from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_debt = self.loan_set.aggregate(
            total_debt=Sum(
                ExpressionWrapper(
                    F('loan_amount') - (F('monthly_repayment') * (F('tenure') - F('emis_paid_on_time'))),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )
        )['total_debt'] or 0
        self.current_debt = total_debt
        super().save(update_fields=['current_debt'])

        
class Loan(models.Model):
    loan_id = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('customer', 'loan_id') 

    def __str__(self):
        return f"Loan {self.loan_id} for Customer {self.customer.customer_id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.customer.save()
