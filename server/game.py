import random
import uuid
import chess
from flask import Blueprint, abort, request, jsonify, session

game = Blueprint("game", __name__)

approvedPlayers = {}
approvedUser = None
setupReady = False
board = chess.Board()
turn = None
gameAlive = False


@game.route("/game/", methods=["GET", "POST"])
def handleRequest():
    global setupReady, approvedUser, approvedPlayers
    # parseArguments()
    checkSession()
    approvedUser = session['userID'] in approvedPlayers
    if not setupReady:
        return createGame()
    elif not approvedUser:
        abort(404, "lobby full")
    else:
        return playChess(request.args.get("move"))


# def parseArguments():
#     args = request.args
#     # print(args)
#     if "move" in args:
#         return args.get("move")


def createGame():
    def gameReady():
        global setupReady
        setupReady = True
        # TODO: let users pick colors
        return setupGame()

    global setupReady, approvedUser, approvedPlayers
    lobbySize = len(approvedPlayers)
    if not setupReady and lobbySize < 2:
        if not approvedUser:
            approvedPlayers[session['userID']] = None
            temp = {'userID': session['userID'],
                    "waiting": True}
            return jsonify(temp) if len(approvedPlayers) < 2 else gameReady()
        elif approvedUser:
            temp = {'userID': session['userID'],
                    "waiting": True}
            return jsonify(temp)
        else:
            gameReady()
    if approvedUser:
        return "ready"


def setupGame():
    global turn
    approvedPlayers[list(approvedPlayers.keys())[0]] = chess.BLACK if random.randrange(2) + 1 == 2 else chess.WHITE
    approvedPlayers[list(approvedPlayers.keys())[1]] = not approvedPlayers[list(approvedPlayers.keys())[0]]
    turn = chess.WHITE if random.randrange(2) + 1 == 1 else chess.BLACK
    temp = {"userID": session["userID"],
            "waiting": False,
            "turn": turn,
            "yourTurn": approvedPlayers[session["userID"]]}
    return jsonify(temp)


def playChess(move: str):
    global board, turn
    move = chess.Move.from_uci(move)
    if approvedPlayers.get(session["userID"]) is not turn:
        abort(404)
    elif board.is_legal(move):
        board.push(move)
        turn = not turn
        temp = {"gameAlive": True,
                "turn": turn,
                "lastMove": move.__str__()}
        return jsonify(temp)
    elif move == "resign":
        # todo, end game here
        pass

    return "placeholder"


def checkSession():
    try:
        if session['userID'] is None:
            session['userID'] = uuid.uuid4().__str__()
    except KeyError:
        session['userID'] = uuid.uuid4().__str__()
