import os
from flask import render_template, request
from app import app, mails
import traceback
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    notifyAdmin = True

    if isinstance(e, HTTPException):
        e_type = "HTTPException"
        if str(str(e.code)+'.svg') in os.listdir("app/static/assets/errors_svg"):
            fname = "assets/errors_svg/"+str(e.code)+".svg"
        else:
            fname = "assets/errors_svg/gen.svg"
        if e.code != 500:
            notifyAdmin = False
        if notifyAdmin is True:
            
            #TODO: Check if user is authenticated. If yes, send email ID of current user. If no, send notLoggedIn.
            
            mails.notifyError(e=str(e.code), 
            tr=traceback.format_exc(), 
            loggedInAs="dummy", 
            ip=request.remote_addr, 
            ua=request.user_agent.string)

        return render_template("error.html", e=e, fname=fname, e_type=e_type, notifyAdmin=notifyAdmin), e.code
    else:
        e_type = "Exception"
        fname = "assets/errors_svg/gen.svg"
        
        #TODO: Check if user is authenticated. If yes, send email ID of current user. If no, send notLoggedIn.
        mails.notifyError(e="Not HTTP Exception", 
        tr=traceback.format_exc(), 
        loggedInAs="dummy", 
        ip=request.remote_addr, 
        ua=request.user_agent.string)

        return render_template("error.html", e=e, fname=fname, e_type=e_type, notifyAdmin=notifyAdmin), 500
    
