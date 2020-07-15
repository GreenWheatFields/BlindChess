from server import app
from flask import session
import uuid

@app.route("/")
def getIP():
    if session['userID'] is None:
        session['userID'] = uuid.uuid4().__str__()
    print(session)
    return "true"


if __name__ == '__main__':
    app.run()
