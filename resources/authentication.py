import os

from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth

load_dotenv(verbose=True)

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')

auth = HTTPBasicAuth()


USER_DATA = {
    f"{API_USER}": f"{API_PASSWORD}"
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password
