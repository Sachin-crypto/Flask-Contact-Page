# Importing required libs
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
import datetime

app = Flask(__name__)

# Configuring DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/contact"

db = SQLAlchemy(app)

# Creating entry points
class Queries(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(35), nullable=False)
    sub = db.Column(db.String(50), nullable=False)
    msg = db.Column(db.String(1200), nullable=False)
    date = db.Column(db.String(12), nullable=True)

# Getting environment variables
gmail_user = os.getenv('GMAIL_USERNAME')
gmail_pass = os.getenv('GMAIL_PASSWORD')

# Configuring values
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = gmail_user,
    MAIL_PASSWORD = gmail_pass,
)

# Instantiate Mail
mail = Mail(app)

# App route
@app.route("/", methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Getting data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Adding entries to the DB and committing
        entry = Queries(name=name, email=email, sub=subject, msg=message, date=datetime.datetime.now())
        db.session.add(entry)
        db.session.commit()

        # Sending message to gmail
        mail.send_message("Message from " + name + " at " + email,
                          sender = email,
                          recipients = [gmail_user],
                          body = subject + "\n\n" + message
                          )
    # Rendering template
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)