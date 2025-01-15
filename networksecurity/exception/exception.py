import sys
from networksecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self, message, erro_detials:sys):
        self.message = message
        _, _, exc_tb = erro_detials.exc_info()
        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        super().__init__(self.message)
        
    def __str__(self):
        return f"Error occured in python script name {self.file_name} at line number {self.line_number} with error message {self.message}"
    
    
if __name__=="__main__":
    try:
        logging.info("This is a test log and enter the try block")
        a = 1 /0
        print("This will print if there is no exception")
    except Exception as e:
        logging.error(f"Error: {e}")
        raise NetworkSecurityException("This is a test exception", sys.exc_info())