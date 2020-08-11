import random
import uuid
import chess
import time
from flask import Blueprint, abort, request, jsonify, session

game = Blueprint("game", __name__)
approvedPlayers = {}
approvedUser = None
setupReady = False
board = chess.Board()
boardTurn = None
gameAlive = False
lastMove = ""
currentHold = None


# todo, dynamically genreate urls with this blueprint


@game.route("/game/", methods=["GET", "POST"])
def handleRequest():
    global setupReady, approvedPlayers, gameAlive, currentHold
    checkSession()
    currentHold = HoldRequest()
    if not setupReady:
        return createGame()
    elif not isApproved():
        abort(404, "lobby full")
    else:
        if request.method == "GET":
            return gameStatus()
        elif request.method == "POST":
            return playChess(parseArguments())


def createGame():
    global setupReady, approvedUser, approvedPlayers
    lobbySize = len(approvedPlayers)
    if not setupReady and lobbySize < 2:
        if not approvedUser:
            approvedPlayers[session['userID']] = None
            return gameStatus() if len(approvedPlayers) < 2 else setupGame()
        elif approvedUser:
            return gameStatus()
    if approvedUser:
        return gameStatus()


def setupGame():
    global boardTurn, gameAlive, board, setupReady
    setupReady = True
    approvedPlayers[list(approvedPlayers.keys())[0]] = chess.BLACK if random.randrange(2) + 1 == 2 else chess.WHITE
    approvedPlayers[list(approvedPlayers.keys())[1]] = not approvedPlayers[list(approvedPlayers.keys())[0]]
    boardTurn = chess.WHITE
    gameAlive = True
    return gameStatus()


def playChess(move: str):
    global board, boardTurn, gameAlive, lastMove, currentHold
    if move == "resign":
        endGame()
        return gameStatus()
    move = chess.Move.from_uci(move)
    if approvedPlayers.get(session["userID"]) is not board.turn:
        print("wrong turn")
        abort(404)

    elif board.is_legal(move):
        board.push(move)
        lastMove = move.__str__()
        boardTurn = not boardTurn
        if board.is_game_over(claim_draw=True):
            endGame()
        return gameStatus()
    else:
        print("bad move")
        return abort(404)


def endGame():
    global board, gameAlive
    gameAlive = False


def checkSession():
    try:
        if session['userID'] is None:
            session['userID'] = uuid.uuid4().__str__()
    except KeyError:
        session['userID'] = uuid.uuid4().__str__()


def gameStatus():
    global gameAlive, boardTurn, setupReady, lastMove, approvedUser
    # todo, approvedUser always false
    temp = {"gameAlive": gameAlive,
            "boardTurn": boardTurn,
            }
    if setupReady:
        if request.method == "POST":
            temp["lastMove"] = lastMove.__str__()

    elif not setupReady:
        temp["waiting"] = False
        temp["userID"] = session['userID']
    if isApproved():
        temp["yourTurn"] = approvedPlayers[session['userID']]
    return jsonify(temp)


def isApproved():
    return session['userID'] in approvedPlayers


def parseArguments():
    # moves shouldbe validated client side
    if "move" in request.args:
        if request.args.get("move") is not None:
            return request.args.get("move")
        else:
            # todo, posted empty move will cause error as this fucntion has to return a string
            pass
    else:
        # todo, emppty move parameters
        pass


# def validToHold():
#     if "HOLDME" in request.headers:
#         if request.headers["HOLDME"]:
#             return True
#         else:
#             # error
#             pass
#     else:
#         return False


class HoldRequest:
    def __init__(self):
        self.releaseClause = False
        self.startTime = None

    def hold(self):
        self.startTime = time.time()
        while not self.releaseClause and time.time() - self.startTime < 3:
            print("holding")
        # todo, find out what condition was met

    def notify(self):
        self.releaseClause = True
        return gameStatus()
