import sys
from hrchacha.logging.logger import logging


class HRChachaException(Exception):

    def __init__(self, error_message:str, error_details:sys):
        self.error_message = error_message
        self.exc_info = error_details.exc_info()
        _,_,exc_tb = self.exc_info

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        custom_error_message = f"Error occurred in python script name [{self.filename}] line number [{self.lineno}] error message [{self.error_message}]"
        logging.info(custom_error_message)
        return custom_error_message