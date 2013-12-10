import os
import pyotp
import qrcode
import pickle
import logging
from StringIO import StringIO
from flask import Flask, render_template, redirect, request, flash, send_file


# I use a simple flat file to save the user information This is a terrible idea
# for any real work application But this is merely a demo of how TOTP can be
# used in Python, so I am keeping it very minimalistic
USER_FILE_NAME = 'users.data'

app = Flask(__name__)

app.config.update(SECRET_KEY = 'fB04LfYc0Nfjneu47wYwPGyWYcEVeWbaxdA')
app.config.update(DEBUG = True)

logging.basicConfig(level=logging.DEBUG)


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
            pass
        t = pyotp.TOTP(self.key)
        return t.verify(p)


    @classmethod
    def get_user(cls, email):
        users = pickle.load(open(USER_FILE_NAME, 'rb'))
        if email in users:
            return User(email, users[email])
        else:
            return None


@app.route('/qr/<email>')
def qr(email):
    u = User.get_user(email)
    if u is None:
        return ''
    t = pyotp.TOTP(u.key)
    # q = qrcode.make(t.provisioning_uri("python-totp.herokuapp.com:" + email))
    q = qrcode.make(t.provisioning_uri(email))
    img = StringIO()
    q.save(img)
    img.seek(0)
    return send_file(img, mimetype="image/png")



@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        u = User(request.form['email'])
        if u.save():
            return render_template('/created.html', user=u)
        else:
            flash('Invalid email or user already exists.', 'danger')
            return render_template('new.html')
    else:
        return render_template('new.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.get_user(request.form['email'])
        if u is None:
            flash('Invalid email address.', 'danger')
            return render_template('login.html')
        else:
            otp = request.form['otp']
            if u.authenticate(otp):
                flash('Authentication successful!', 'success')
                return render_template('login.html')
            else:
                flash('Invalid one-time password!', 'danger')
                return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/')
def main():
    return render_template('index.html')
