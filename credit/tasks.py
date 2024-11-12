from celery import shared_task
import pandas as pd
from .models import Customer, Loan

@shared_task
def ingest_customer_data():
    df = pd.read_excel('customer_data.xlsx')
    for _, row in df.iterrows():
         Customer.objects.create(
            customer_id=row['Customer ID'],  # Adjusted column name
            first_name=row['First Name'],  # Adjusted column name
            last_name=row['Last Name'],  # Adjusted column name
            phone_number=row['Phone Number'],  # Adjusted column name
            monthly_salary=row['Monthly Salary'],  # Adjusted column name
            approved_limit=row['Approved Limit'],  # Adjusted column name
            age=row['Age'],  # Adjusted column name
        )    
        #         'first_name': row['First Name'],  # Adjusted column name
        #         'last_name': row['Last Name'],  # Adjusted column name
        #         'phone_number': row['Phone Number'],  # Adjusted column name
        #         'monthly_salary': row['Monthly Salary'],  # Adjusted column name
        #         'approved_limit': row['Approved Limit'],  # Adjusted column name
        #         'current_debt': row['Current Debt']  # Adjusted column name
        #     }
        # )

@shared_task
def ingest_loan_data():
    df = pd.read_excel('loan_data.xlsx')
    for _,row in df.iterrows():
        customer = Customer.objects.get(customer_id=row['Customer ID'])     
        Loan.objects.create(
                customer=customer,
                loan_id=row['Loan ID'],  # Adjusted column name
                loan_amount=row['Loan Amount'],  # Adjusted column name
                tenure=row['Tenure'],  # Adjusted column name
                interest_rate=row['Interest Rate'],  # Adjusted column name
                monthly_repayment=row['Monthly payment'],  # Adjusted column name
                emis_paid_on_time=row['EMIs paid on Time'],  # Adjusted column name
                start_date=pd.to_datetime(row['Date of Approval']),  # Adjusted column name
                end_date=pd.to_datetime(row['End Date'])  # Adjusted column name
            )