from datetime import datetime
from logs.logs import Logs


class StringUtils:
    @staticmethod
    def string_to_insertion(input_string, datatype):
        if input_string.is_displayed():
            if datatype == 'str':
                return input_string.text
            if datatype == 'int':
                try:
                    return int(input_string.text)
                except ValueError:
                    Logs.critical("StringUtils - string_to_insertion: ", input_string.text)
                    return None
            if datatype == 'date':
                try:
                    return datetime.strptime(input_string.text, '%b %d, %Y')
                except ValueError:
                    Logs.critical("StringUtils - string_to_insertion: ", input_string.text)
                    return None
            if datatype == 'streams':
                try:
                    return input_string.text.replace(',', '')
                except ValueError:
                    Logs.critical("StringUtils - string_to_insertion: ", input_string.text)
                    return None
        else:
            return None
