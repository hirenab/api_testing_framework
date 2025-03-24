# API Testing Framework

## Overview

A comprehensive API testing framework for testing RESTful APIs. Supports GET, POST, PUT, DELETE requests with schema validation, authentication, and logging.

## Key Features
- Supports GET, POST, PUT, DELETE requests for Comprehensive API Testing
- Dynamic user creation with Unique email addresses and Automatic ID handling 
- Secure token management via Environment variables
- Setup and Teardown fixtures for Automated resource management before and after tests
- Robust authentication handling with Dynamic token usage
- JSON schema validation for response bodies to ensure Data integrity
- Detailed logging for Request, Response, and Error information during API calls
- HTML Report Generation for test results with live logs
- Modular and Reusable test functions for Efficient testing workflows
- Easily extensible framework with New test cases or API endpoints, Including error handling for invalid inputs

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/hirenab/api-testing-framework.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables (e.g., API tokens, base URL):
   ```
   export BASE_URL="https://gorest.co.in"
   export TIMEOUT=30
   ```

4. Set up the API token (replace with your actual token):
   ```
   export API_TOKEN=your_api_token_here
   ```

5. Run the tests:
   ```
   pytest --html=reports/report.html --self-contained-html
   ```

## API Endpoints

1. **Get User**
- **Endpoint**: /public/v2/users/{id}
- **Method**: GET
- **Description**: Retrieves a user by their ID.
- **Parameters**:
  - `id` (required): The ID of the user to retrieve.
- **Expected Response**:
  - Status Code: 200 OK
  - Response Body: JSON object with user details (ID, name, email, gender, status).

2. **Create User**
- **Endpoint**: /public/v2/users
- **Method**: POST
- **Description**: Creates a new user.
- **Request Body**:
   ```json
   {
     "name": "John Doe",
     "email": "johndoe_{timestamp}@example.com",
     "gender": "male",
     "status": "active"
   }
   ```
- **Expected Response**:
  - Status Code: 201 Created
  - Response Body: JSON object with the created user details.

3. **Update User**
- **Endpoint**: /public/v2/users/{id}
- **Method**: PUT
- **Description**: Updates a user by their ID.
- **Parameters**:
  - `id` (required): The ID of the user to update.
- **Request Body**:
   ```json
   {
     "name": "Jane Doe",
     "email": "janedoe_{timestamp}@example.com"
   }
   ```
- **Expected Response**:
  - Status Code: 200 OK
  - Response Body: JSON object with the updated user details (ID, name, email).

4. **Delete User**
- **Endpoint**: /public/v2/users/{id}
- **Method**: DELETE
- **Description**: Deletes a user by their ID.
- **Parameters**:
  - `id` (required): The ID of the user to delete.
- **Expected Response**:
  - Status Code: 204 No Content
  - Response Body: Empty response indicating successful deletion.

## Run Test Cases

To run all tests, use:
```
pytest --html=reports/report.html --self-contained-html
```

To run a specific test file, use:
```
pytest tests/test_api.py
```

To run a specific test case, use:
```
pytest -k "test_get_user"
```
