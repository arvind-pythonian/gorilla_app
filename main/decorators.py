import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def request_handler(fn):
    def processor(*args):
        start = time.time()
        self, request = args[0], args[1]
        logger.info(f"Request Received::Method::{request.method}")
        response = fn(self, request)
        logger.info(f"Request Processed::Total Processing time::{time.time()-start} seconds")
        return response
    return processor