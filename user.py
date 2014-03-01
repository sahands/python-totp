import pyotp
import pickle


__author__ = "Sahand Saba"


# I use a simple flat file to save the user information. This of course would
# be a bad idea for any real world application, but the point of this demo is
# not proper database use, and for the sake of simplicity I am keeping the
# storage mechanism as simple as possible.
USER_FILE_NAME = 'users.data'


class User(object):
    def __init__(self, email, key=None):
        self.email = email
        self.key = key
        if key is None:
            self.key = pyotp.random_base32()

    def save(self):
        if len(self.email) < 1:
            return False

        users = pickle.load(open(USER_FILE_NAME, 'rb'))
        if self.email in users:
            return False
        else:
            users[self.email] = self.key
            pickle.dump(users, open(USER_FILE_NAME, 'wb'))
            return True

    def authenticate(self, otp):
        p = 0
        try:
            p = int(otp)
        except:
            return False
        t = pyotp.TOTP(self.key)
        return t.verify(p)

    @classmethod
    def get_user(cls, email):
        users = pickle.load(open(USER_FILE_NAME, 'rb'))
        if email in users:
            return User(email, users[email])
        else:
            return None
