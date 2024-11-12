from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from datetime import datetime,timedelta
import random

# Utility function to calculate monthly installment using compound interest
def calculate_monthly_installment(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure) / (((1 + monthly_rate) ** tenure) - 1)
    return round(emi, 2)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        monthly_salary = data.get("monthly_income")
        approved_limit = round(36 * int(monthly_salary) / 1_00_000) * 1_00_000  # Rounded to nearest lakh

        # Create and save the customer instance
        customer = Customer(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            age=data.get("age"),
            monthly_salary=monthly_salary,
            approved_limit=approved_limit,
            phone_number=data.get("phone_number"),
            current_debt=0
        )
        customer.save()  # Save the instance to assign a primary key

        # Serialize and return the saved customer instance
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckEligibilityView(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get("customer_id")
        loan_amount = data.get("loan_amount")
        requested_rate = data.get("interest_rate")
        tenure = data.get("tenure")

        customer = get_object_or_404(Customer, customer_id=customer_id)
        credit_score = 0
        customer_loans = Loan.objects.filter(customer=customer)

        # Calculate active loans and determine eligibility based on start and end dates
        active_loans = customer_loans.filter(end_date__gte=datetime.now().date())
        if sum(loan.loan_amount for loan in active_loans) > customer.approved_limit:
            credit_score = 0
        else:
            credit_score += sum(loan.emis_paid_on_time for loan in customer_loans)
            credit_score -= len(customer_loans)  # Deduct for multiple loans

            credit_score += sum(1 for loan in customer_loans if loan.start_date.year == datetime.now().year)
            credit_score += sum(loan.loan_amount for loan in customer_loans) // 1_00_000

        # Determine loan approval based on credit score
        if credit_score > 50:
            approval = True
        elif 50 >= credit_score > 30 and requested_rate < 12:
            requested_rate = 12
            approval = True
        elif 30 >= credit_score > 10 and requested_rate < 16:
            requested_rate = 16
            approval = True
        else:
            approval = False

        if approval:
            monthly_installment = calculate_monthly_installment(loan_amount, requested_rate, tenure)
            response = {
                "customer_id": customer.customer_id,
                "approval": approval,
                "interest_rate": requested_rate,
                "corrected_interest_rate": requested_rate,
                "tenure": tenure,
                "monthly_installment": monthly_installment
            }
        else:
            response = {
                "customer_id": customer.customer_id,
                "approval": approval,
                "interest_rate": requested_rate,
                "corrected_interest_rate": requested_rate,
                "tenure": tenure,
                "monthly_installment": None
            }
        
        return Response(response, status=status.HTTP_200_OK)

class CreateLoanView(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get("customer_id")
        loan_amount = data.get("loan_amount")
        interest_rate = data.get("interest_rate")
        tenure = data.get("tenure")

        # Check eligibility using CheckEligibilityView logic
        eligibility_response = CheckEligibilityView().post(request)
        eligibility_data = eligibility_response.data

        if eligibility_data["approval"]:
            monthly_installment = eligibility_data["monthly_installment"]

            while True:
                loan_id = random.randint(1000, 9999)
                if not Loan.objects.filter(customer_id=customer_id, loan_id=loan_id).exists():
                    break

             # Ensure start_date and end_date are date objects
            start_date = datetime.now().date()
            end_date = (datetime.now() + timedelta(days=tenure * 30)).date()    

            loan = Loan.objects.create(
                customer_id=customer_id,
                loan_id=loan_id,
                loan_amount=loan_amount,
                tenure=tenure,
                interest_rate=interest_rate,
                monthly_repayment=monthly_installment,
                emis_paid_on_time=0,
                start_date=start_date,
                end_date=end_date
            )

            loan_serializer = LoanSerializer(loan)
            return Response(loan_serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            response = {
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "Loan not approved due to eligibility criteria.",
                "monthly_installment": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ViewLoanView(APIView):
    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, loan_id=loan_id)  
        loan_serializer = LoanSerializer(loan)
        return Response(loan_serializer.data, status=status.HTTP_200_OK)

class ViewLoansView(APIView):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, customer_id=customer_id)
        loans = Loan.objects.filter(customer=customer)
        loan_serializer = LoanSerializer(loans, many=True)
        return Response(loan_serializer.data, status=status.HTTP_200_OK)
