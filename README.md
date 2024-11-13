# Credit Approval System

This is a Django-based Credit Approval System designed to evaluate customer loan eligibility, manage customer data, and process loans. The application is fully dockerized, using PostgreSQL as the database, Redis as the message broker for background tasks with Celery, and Django Rest Framework for building APIs.

## Table of Contents

- [Features](#features)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
- [API Endpoints](#api-endpoints)
- [Running Celery Tasks](#running-celery-tasks)
- [Testing](#testing)
- [Usage](#usage)
- [Stopping the Application](#stopping-the-application)
- [License](#license)

## Features

- **Customer Management**: Register new customers and store their details.
- **Loan Processing**: Create and manage loans with automatic eligibility checks.
- **Credit Limit and Debt Tracking**: Track approved limits, current debt, and loan repayments.
- **Background Task Processing**: Celery tasks for data ingestion and other background tasks.
- **API Documentation**: REST API endpoints using Django Rest Framework.

## Setup and Installation

### Prerequisites

- Docker: Install Docker and Docker Compose ([Docker installation guide](https://docs.docker.com/get-docker/)).
- Basic knowledge of Python, Django, and REST APIs is recommended.

### Environment Variables

Configure the following environment variables in `docker-compose.yml`:

- `POSTGRES_DB`: The name of the PostgreSQL database (e.g., `credit_db`).
- `POSTGRES_USER`: The database username.
- `POSTGRES_PASSWORD`: The database password.
- `CELERY_BROKER_URL`: URL for the Celery broker (set to `redis://redis:6379/0` by default).
- `CELERY_RESULT_BACKEND`: URL for the Celery result backend (set to `redis://redis:6379/0` by default).

### Docker Setup

1. Clone the repository and navigate to the project directory.

   ```bash
   git clone https://github.com/himanshu-sharmav/credit_approval_system.git
   cd credit-approval-system
   ```

2. Run the below command  for Python dependencies.

    ```bash
    pip install requirements.txt
    ```

3. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

4. Run database migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Create a superuser for accessing the Django admin (optional):

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Create a .env File
Create a .env file in the root of the project directory with the following content:

    # Database configuration
    POSTGRES_DB=credit_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password

    # Celery configuration
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Register a New Customer

- **URL**: `/register/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "first_name": "Alice",
    "last_name": "Smith",
    "age": 32,
    "monthly_income": 60000,
    "phone_number": "1122334455"
  }
  ```
- **Description**: Registers a new customer and calculates their approved credit limit.

### 2. Check Loan Eligibility

- **URL**: `/check-eligibility/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "customer_id": 1,
    "loan_amount": 300000,
    "interest_rate": 10,
    "tenure": 24
  }
  ```
- **Description**: Checks if a customer is eligible for a loan based on credit score and existing debt.

### 3. Create a Loan

- **URL**: `/create-loan/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "customer_id": 1,
    "loan_id": 101,
    "loan_amount": 200000,
    "interest_rate": 12,
    "tenure": 12
  }
  ```
- **Description**: Creates a new loan for a customer and calculates the monthly repayment amount.

### 4. View Loan Details

- **URL**: `/view-loan/<id>/`
- **Method**: `GET`
- **Description**: Retrieves details of a specific loan by its primary key (`id`).

### 5. View All Loans for a Customer

- **URL**: `/view-loans/<customer_id>/`
- **Method**: `GET`
- **Description**: Retrieves all loans associated with a specific customer.

## Running Celery Tasks

This project uses Celery for background task processing with Redis as the broker.

To start a Celery worker:

```bash
docker-compose exec web celery -A credit_approval_system worker -l info
```

To run a scheduled job, use Celery Beat:

```bash
docker-compose exec web celery -A credit_approval_system beat -l info
```

## Testing

To test the API endpoints, you can use tools like Postman or cURL with the following sample requests:

### Sample Customer Registration

```json
{
  "first_name": "Alice",
  "last_name": "Smith",
  "age": 32,
  "monthly_income": 60000,
  "phone_number": "1122334455"
}
```

### Sample Loan Eligibility Check

```json
{
  "customer_id": 1,
  "loan_amount": 300000,
  "interest_rate": 10,
  "tenure": 24
}
```

### Running Django Tests

To run Django’s built-in test suite:

```bash
docker-compose exec web python manage.py test
```

## Usage

1. **Start Application**: Run `docker-compose up --build` to start the application.
2. **API Testing**: Use Postman or any REST client to test the API endpoints as described.
3. **Admin Access**: Access the Django admin at `http://127.0.0.1:8000/admin` (after creating a superuser).

## Stopping the Application

To stop and remove the Docker containers, use:

```bash
docker-compose down
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

    