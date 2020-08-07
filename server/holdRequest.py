from flask import Blueprint, request, jsonify
import time

HoldRequest = Blueprint("HoldRequest", __name__)

testVar = False


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
    escapeClause = 1
    if "HOLDME" in request.headers:
        start = time.time()
        # while escapeClause == 1
    return jsonify({1:2})