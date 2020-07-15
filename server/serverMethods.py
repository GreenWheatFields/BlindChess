from flask import session
import uuid

@staticmethod
def checkSession():
    if session['userId'] is None:
        session['userID'] = uuid.uuid4().__str__()
