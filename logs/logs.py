import logging
import os


class Logs:
    LOG_FOLDER = 'logs'
    LOG_FILE = os.path.join(LOG_FOLDER, 'app.log')

    @staticmethod
    def setup_logging():
        if not os.path.exists(Logs.LOG_FOLDER):
            os.makedirs(Logs.LOG_FOLDER)

        # Configurar el nombre del archivo de log
        logging.basicConfig(filename=Logs.LOG_FILE, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def debug(message):
        logging.debug(message)

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def warning(message):
        logging.warning(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def critical(message):
        logging.critical(message)
