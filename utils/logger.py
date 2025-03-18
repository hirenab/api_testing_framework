import logging

# Create a logger with the name 'api_testing'
logger = logging.getLogger('api_testing')
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG to capture all types of log messages

# Create a file handler to write log messages to a file named 'api_test.log'
handler = logging.FileHandler('api_test.log')
handler.setLevel(logging.DEBUG)  # Set the handler's logging level to DEBUG to capture all messages

# Define the format for log messages (timestamp, logger name, log level, and message)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)  # Attach the formatter to the handler

# Add the handler to the logger
logger.addHandler(handler)
