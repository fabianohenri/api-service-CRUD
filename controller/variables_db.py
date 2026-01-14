from dotenv import load_dotenv
import os

from util.logging_format import LoggingFormat


class VariablesDataBase:

    @staticmethod
    def connect_string():
        env_path = '../.env'
        load_dotenv(dotenv_path=env_path, verbose=False)
        db_string_connection = "postgresql://" + os.getenv("DB_USER") + ":" + os.getenv("DB_PASS") + "@" + os.getenv("DB_HOST") + \
                               ":" + os.getenv("DB_PORT") + "/" + os.getenv("DB_NAME")
        return db_string_connection

    @staticmethod
    def vars_db():
        env_path = '../.env'
        load_dotenv(dotenv_path=env_path, verbose=False)
        variables_env = {"DB_USER": os.getenv("DB_USER"),
                         "DB_PASS": os.getenv("DB_PASS"),
                         "DB_HOST": os.getenv("DB_HOST"),
                         "DB_PORT": os.getenv("DB_PORT"),
                         "DB_NAME": os.getenv("DB_NAME"),
                         "KEY_HASH": os.getenv("KEY_HASH")}
        return variables_env
