
# API Testing Framework

## Setup

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest --html=reports/report.html --self-contained-html
   ```

## Features
- Supports GET, POST, PUT, DELETE methods.
- Logger setup for detailed request and response logging.
- Custom configuration through config.py.
- Payload separation in payloads.py for clean test cases.
- Pytest markers for running smoke and regression tests.
- HTML report generation.
