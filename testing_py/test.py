# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, template_id, substitution, TemplateId, Substitution, From

message = Mail(
    to_emails='rishabh@curabit.in')

message.from_email = From(email='tech-support@curabit.in', name='Console by Curabit')

message.dynamic_template_data = {
    'th_name':"Rishabh N."
    }

message.template_id = 'd-af9cefb855bd425ba3a1e41cdf220a44'

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)