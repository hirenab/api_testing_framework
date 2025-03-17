
import logging

logger = logging.getLogger('api_testing')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('api_test.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
