import sys
from app_logging.logger import logger


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    return f"Error in [{file_name}] at line [{exc_tb.tb_lineno}]: {str(error)}"


class CustomException(Exception):
    def __init__(self, error, error_detail: sys):
        self.error_message = error_message_detail(error, error_detail)
        logger.error(self.error_message)
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message
