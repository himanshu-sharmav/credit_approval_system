from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer, Loan
from datetime import datetime, timedelta

class CustomerTests(APITestCase):
    def setUp(self):
        """
        Create a sample customer for testing.
        """
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=28,
            phone_number="0987654321",
            monthly_salary=40000,
            approved_limit=1440000,
            current_debt=0
        )

    def test_create_customer(self):
        """
        Test creating a new customer.
        """
        url = reverse('register')
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "age": 30,
            "phone_number": "1234567890",
            "monthly_income": 50000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "Jane")
        self.assertEqual(response.data['last_name'], "Doe")
        self.assertEqual(response.data['age'], 30)
        self.assertEqual(response.data['phone_number'], "1234567890")
        self.assertEqual(response.data['monthly_salary'], 50000)
        self.assertEqual(response.data['approved_limit'], 1800000)

    def test_create_loan(self):
        """
        Test creating a new loan for an existing customer.
        """
        url = reverse('create_loan')
        data = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 200000,
            "interest_rate": 12,
            "tenure": 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('loan_id', response.data)
        self.assertTrue(response.data['monthly_repayment'] > 0)

class LoanViewTests(APITestCase):
    def setUp(self):
        """
        Create a sample customer and loan for testing.
        """
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=28,
            phone_number="0987654321",
            monthly_salary=40000,
            approved_limit=1440000,
            current_debt=0
        )
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_id=101,
            loan_amount=200000,
            tenure=12,
            interest_rate=12,
            monthly_repayment=17769.76,
            emis_paid_on_time=0,
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=12 * 30)).date()
        )

    def test_view_loan(self):
        """
        Test viewing a loan.
        """
        url = reverse('view-loan', args=[self.loan.loan_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan_id'], self.loan.loan_id)
        self.assertEqual(response.data['loan_amount'], self.loan.loan_amount)
        self.assertEqual(response.data['monthly_repayment'], self.loan.monthly_repayment)