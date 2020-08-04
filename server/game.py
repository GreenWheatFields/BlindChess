import random
import uuid
import chess
from flask import Blueprint, abort, request, jsonify, session

game = Blueprint("game", __name__)
approvedPlayers = {}
approvedUser = None
setupReady = False
board = chess.Board()
boardTurn = None
gameAlive = False
move = None


@game.route("/game/", methods=["GET", "POST"])
def handleRequest():
    global setupReady, approvedUser, approvedPlayers, gameAlive
    checkSession()
    approvedUser = session['userID'] in approvedPlayers
    if not setupReady:
        return createGame()
    elif not approvedUser:
        abort(404, "lobby full")
    else:
        if request.method == "GET":
            return jsonify({"gameAlive": gameAlive, "boardTurn": boardTurn, "yourTurn": approvedPlayers[session["userID"]]})
        elif request.method == "POST":
            parseArguments()
            return playChess(request.args.get("move"))


def parseArguments():
    # moves shouldbe validated client side
    args = request.args
    if "move" in args:
        move = request.args.get("move")
        if move == "resign":
            endGame()
            return gameStatus()
        else:
            return move

    else:
        # todo, post but no move
        pass


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
            return gameStatus() if len(approvedPlayers) < 2 else gameReady()
        elif approvedUser:
            return gameStatus()
        else:
            # may be uneccesary
            gameReady()
    if approvedUser:
        return gameStatus()


def setupGame():
    global boardTurn, gameAlive, board
    approvedPlayers[list(approvedPlayers.keys())[0]] = chess.BLACK if random.randrange(2) + 1 == 2 else chess.WHITE
    approvedPlayers[list(approvedPlayers.keys())[1]] = not approvedPlayers[list(approvedPlayers.keys())[0]]
    boardTurn = chess.WHITE
    gameAlive = True
    return gameStatus()


def playChess(move: str):
    # todo, move used as parameter and global variable
    global board, boardTurn, gameAlive
    move = chess.Move.from_uci(move)
    if approvedPlayers.get(session["userID"]) is not board.turn:
        print("wrong turn")
        abort(404)
    elif board.is_legal(move):
        board.push(move)
        boardTurn = not boardTurn
        if board.is_game_over(claim_draw=True):
            endGame()
        return gameStatus()
    elif move == "resign":
        gameAlive = False
        return gameStatus()
    else:
        print("bad move")
        return abort(404)

    return "placeholder"


def checkSession():
    try:
        if session['userID'] is None:
            session['userID'] = uuid.uuid4().__str__()
    except KeyError:
        session['userID'] = uuid.uuid4().__str__()


def gameStatus():
    global gameAlive, boardTurn, setupReady, move, approvedUser
    # todo, approvedUser always false
    temp = {"gameAlive": gameAlive,
            "boardTurn": boardTurn,
            }
    if setupReady:
        if request.method == "POST":
            temp["lastMove"] = move.__str__()

    elif not setupReady:
        temp["waiting"] = False
        temp["userID"] = session['userID']
    if isApproved():
        temp["yourTurn"] = approvedPlayers[session['userID']]
    return jsonify(temp)


def isApproved():
    return session['userID'] in approvedPlayers


def endGame():
    global board, gameAlive
    gameAlive = False
