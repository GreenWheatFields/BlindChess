from flask import Blueprint, request
import time

HoldRequest = Blueprint("HoldRequest", __name__)


@HoldRequest.route("/hold/", methods=["GET", "POST"])
def holdRequest():
    if request.method == "GET":
        print("here")
        return "", 204
    elif request.method == "POST":
        time.sleep(5)
        return "", 204
