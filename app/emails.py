# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From

def send_email(message):
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    sg.send(message)

def ack_reg(th_email, th_name):
    message = Mail(
    to_emails=th_email)

    message.from_email = From(email='tech-support@curabit.in', name='Console by Curabit')

    message.dynamic_template_data = {
        'th_name': th_name
        }

    message.template_id = 'd-af9cefb855bd425ba3a1e41cdf220a44'

    send_email(message)

