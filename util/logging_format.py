import logging


class LoggingFormat:

    @staticmethod
    def format(message, color):
        if not message:
            logging.info('\033[33m' + "Messangem não enviada para o logging" + "\033[0;0m")
        if not color:
            logging.info("\033[37m" + message + "\033[0;0m")
        if "Error" in color:
            # Cor Vermelha
            logging.warning("\033[1;31m" + message + "\033[0;0m")
        elif "Info" in color:
            # Cor branca
            logging.info("\033[97m" + message + "\033[0;0m")
        elif "Success" in color:
            # Cor verde
            logging.info("\033[1;32m" + message + "\033[0;0m")
        elif "Alert" in color:
            # Cor Amarela
            logging.info("\033[33m" + message + "\033[0;0m")
