from flask import session
import uuid


def checkSession():
    try:
        if session['userID'] is None:
            session['userID'] = uuid.uuid4().__str__()
    except KeyError:
        session['userID'] = uuid.uuid4().__str__()