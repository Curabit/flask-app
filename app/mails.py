import os
import json
from sendgrid.helpers.mail import Mail, From
from app import sg

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

def resetPass(email, th_name, reset_link):
    message = Mail(to_emails=email)
    message.from_email = From('console-support@curabit.in', 'Console by Curabit')
    message.dynamic_template_data = {
        'th_name': th_name,
        'reset_link': reset_link
    }
    message.template_id = 'd-8b4bb145b12c40c99b37f8e951934faa'
    sg.send(message)

    