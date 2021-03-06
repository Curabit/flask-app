from datetime import datetime
from sendgrid.helpers.mail import Mail, From
from app import sg
from flask import url_for, request

def resetPass(email, th_name, token):
    message = Mail(to_emails=email)
    message.from_email = From('console-support@curabit.in', 'Console by Curabit')
    message.dynamic_template_data = {
        'th_name': th_name,
        'reset_link': url_for('resetPassword', token=token, _external=True)
    }
    message.template_id = 'd-8b4bb145b12c40c99b37f8e951934faa'
    sg.send(message)

from app.models import User

admins = list()
for user in User.objects(user_type='admin'):
    admins.append(user.email)

def ackSignUp(email, th_name):
    message = Mail(to_emails=email)
    message.from_email = From('console-support@curabit.in', 'Console by Curabit')
    message.dynamic_template_data = {
        'th_name': th_name
    }
    message.template_id = 'd-af9cefb855bd425ba3a1e41cdf220a44'
    sg.send(message)

def approvedSignUp(email, th_name):
    message = Mail(to_emails=email)
    message.from_email = From('console-support@curabit.in', 'Console by Curabit')
    message.dynamic_template_data = {
        'th_name': th_name
    }
    message.template_id = 'd-2df5d0a4a7c44ce18bb44b6211d12dfb'
    sg.send(message)

def notifyError(e, tr, loggedInAs, ip, ua):
    if not admins:
        pass
    else:
        message = Mail(to_emails=admins)
        message.from_email = From('console-support@curabit.in', 'Console by Curabit')
        message.dynamic_template_data = {
            'e': e,
            'tr': tr,
            'from_url': request.url,
            'utc_date': str(datetime.utcnow()),
            'headers': str(request.headers),
            'loggedInAs': loggedInAs,
            'ip_add': ip,
            'user_agent': ua
        }
        message.template_id = 'd-192e156c80fa470a873ff577ef991cb6'
        sg.send(message)

def notifySignUp(name, email, cl_name, cl_add):
    if not admins:
        pass
    else:
        message = Mail(to_emails=admins)
        message.from_email = From('console-support@curabit.in', 'Console by Curabit')
        message.dynamic_template_data = {
            'th_name': name,
            'th_email': email,
            'clinic_name': cl_name,
            'clinic_add': cl_add
        }
        message.template_id = 'd-375351e478c346faabab1dfac3180b20'
        sg.send(message)
