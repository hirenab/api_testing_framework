
# API Testing Framework

## Overview

A comprehensive API testing framework for testing RESTful APIs. Supports GET, POST, PUT, DELETE requests with schema validation, authentication, and logging.

## Key Features
- Supports GET, POST, PUT, DELETE requests
- Dynamic user creation with unique email addresses
- Authentication handling
- Schema validation for response bodies
- Detailed logging with request and response data
- HTML report generation for test results
- Modular and reusable test functions
- Easy to extend with new tests or API endpoints
- Setup and teardown fixture for resource management

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/api-testing-framework.git
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

4. Run the tests:
   ```
   pytest --html=reports/report.html --self-contained-html
   ```
## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/api-testing-framework.git
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

4. Run the tests:
   ```
   pytest --html=reports/report.html --self-contained-html
   ```

## API Endpoints

1. Get Post
- **Endpoint**: /posts/{id}
- **Method**: GET
- **Description**: Retrieves a post by its ID.
- **Parameters**: 
  - id (required): The ID of the post to retrieve.
- **Expected Response**: 
  - Status Code: 200 OK
  - Response Body: JSON object with post details.

2. Create Post
- **Endpoint**: /posts
- **Method**: POST
- **Description**: Creates a new post.
- **Request Body**:
json
  {
    "title": "foo",
    "body": "bar",
    "userId": 1
  }

- **Expected Response**: 
  - Status Code: 201 Created
  - Response Body: JSON object with the created post.

## Running the Tests

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
pytest -k "test_get_post"
```

## License

Licensed under the MIT License.
