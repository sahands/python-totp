import os
import pyotp
import qrcode
import pickle
from flask import Flask


# I use a simple flat file to save the user information This is a terrible idea
# for any real work application But this is merely a demo of how TOTP can be
# used in Python, so I am keeping it very minimalistic
USER_FILE_NAME = 'users.data'

app = Flask(__name__)


class User(object):
    def __init__(self, name, key=None):
        self.name = name
        self.key = key
        if key is None:
            key = pyotp.random_base32()

    def save(self):
        users = pickle.load(USER_FILE_NAME)
        if self.name in users:
            return False
        else:
            users[self.name] = key
            pickle.dump(USER_FILE_NAME)
            return True

    @classmethod
    def get_user(cls, name):
        users = pickle.load(USER_FILE_NAME)
        if name in users:
            return users[name]
        else:
            return None

@app.route('/new')
def new():
    return '!'

@app.route('/')
def main():
    return 'Hello!'
