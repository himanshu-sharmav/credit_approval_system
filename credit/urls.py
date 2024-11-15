from django.urls import path
from .views import RegisterView, CheckEligibilityView, CreateLoanView, ViewLoanView, ViewLoansView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('check-eligibility/', CheckEligibilityView.as_view(), name='check_eligibility'),
    path('create-loan/', CreateLoanView.as_view(), name='create_loan'),
    path('view-loan/<int:loan_id>/', ViewLoanView.as_view(), name='view_loan'),
    path('view-loans/<int:customer_id>/', ViewLoansView.as_view(), name='view_loans'),
]
