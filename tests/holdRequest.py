from flask import Blueprint, request, jsonify
import time

HoldRequest = Blueprint("HoldRequest", __name__)

testVar = False
escapeClause = 1


@HoldRequest.route("/hold/", methods=["GET", "POST"])
def holdRequest():
    global testVar
    if request.method == "GET":

        return jsonify({"testVar": testVar})
    elif request.method == "POST":
        testVar = True
        time.sleep(5)
        return jsonify({"testVar": testVar})


@HoldRequest.route("/hold/me", methods=["GET", "POST"])
def holdAndUpdate():
    global escapeClause
    if "HOLDME" in request.headers:
        if request.headers["HOLDME"]:
            start = time.time()
            while escapeClause == 1 and time.time() - start < 5:
                pass
            return jsonify({"comeBack!": True})
    elif "ESCAPE" in request.headers:
        escapeClause += 1
        print(escapeClause)
        return "", 204
    return "", 204
