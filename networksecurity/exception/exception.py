import sys
from networksecurity.logging import create_logger
logger = create_logger()

class NetworkSecurityException(Exception):
    def __init__(self, message, error_details:sys):
        self.message = message
        _, _, exc_tb = error_details.exc_info()
        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        super().__init__(self.message)

    def __str__(self):
        return f"Error occured in python script name [{self.file_name}] at line number [{self.line_number}] with error message [{self.message}]"


if __name__=="__main__":
    try:
        logger.info("This is a test log and enter the try block")
        a = 1 /0
        logger.info("This will print if there is no exception")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise NetworkSecurityException("This is a test exception", sys.exc_info())