import os
from flask import render_template, request
from app import app, mails
import traceback
from werkzeug.exceptions import HTTPException
from flask_login import current_user
from flask import request

@app.errorhandler(Exception)
def handle_exception(e):

    notifyAdmin = True

    if notifyAdmin is True:    
        if current_user.is_authenticated:
            loggedInAs = current_user.email
        else:
            loggedInAs = 'Not Logged In'

    if isinstance(e, HTTPException):
        e_type = "HTTPException"
        if str(str(e.code)+'.svg') in os.listdir("app/static/assets/errors_svg"):
            fname = "assets/errors_svg/"+str(e.code)+".svg"
        else:
            fname = "assets/errors_svg/gen.svg"
        if e.code != 500:
            notifyAdmin = False
            
            mails.notifyError(e=str(e.code), 
            tr=traceback.format_exc(), 
            loggedInAs=loggedInAs, 
            ip=request.remote_addr, 
            ua=request.user_agent.string)

        return render_template("error.html", e=e, fname=fname, e_type=e_type, notifyAdmin=notifyAdmin), e.code
    else:
        e_type = "Exception"
        fname = "assets/errors_svg/gen.svg"

        mails.notifyError(e=str(500), 
        tr=traceback.format_exc(), 
        loggedInAs=loggedInAs, 
        ip=request.remote_addr, 
        ua=request.user_agent.string)

        return render_template("error.html", e=e, fname=fname, e_type=e_type, notifyAdmin=notifyAdmin), 500
    
