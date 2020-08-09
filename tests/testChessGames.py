import unittest
import chess
import random
from server.createApp import create_app
import threading

foolsMate = ["f2f3", "e7e5", "g2g4", "d8h4"]


class testChessGames(unittest.TestCase):

    def setUp(self):
        if __name__ != "main":
            unittest.skip("NotMain")
        self.board = chess.Board()
        self.app = create_app()
        self.player1 = self.generateClient()
        self.player2 = self.generateClient()
        self.response = None
        self.initGame()

    def initGame(self):
        self.player1.get("game/")
        self.response = self.player2.get("game/").json
        if self.response is None:
            self.fail("inital response was null")
        self.player2First = self.response["boardTurn"] == self.response["yourTurn"]

    def randomMove(self, localGame=True):
        move = random.choice(list(self.board.generate_legal_moves()))
        if localGame:
            self.board.push(move)
        return move

    def generateClient(self):
        with self.app.test_client() as client:
            return client

    def postMove(self, move):
        if self.player2First:
            response = self.player2.post("game/?move={}".format(move))
        else:
            response = self.player1.post("game/?move={}".format(move))
        self.player2First = not self.player2First
        return response

    def queryGame(self, json=False):
        if not json:
            return self.player1.get("game/")
        else:
            return self.player1.get("game/").json

    def get(self, endpoint, headers=None):
        # todo, post and get methods should belong to the super class
        return self.player1.get(endpoint, headers=headers if headers is not None else headers)

    def post(self, *endpoint, **other):
        endpoint = "".join(endpoint)
        r = self.player2.post(endpoint).json
        global postResponse
        postResponse = r

    @unittest.skip
    def test_simpleChessMove(self):
        self.initGame()
        if self.response is None:
            self.fail("null json response")
        self.assertEqual(self.postMove(self.randomMove()).status_code, 200)
        self.assertEqual(self.postMove(self.randomMove()).status_code, 200)

    @unittest.skip
    def test_randomChessMoves(self):
        self.initGame()
        self.board.turn = self.response["boardTurn"]
        gameAlive = self.response["gameAlive"]
        if not gameAlive or gameAlive is None:
            self.fail("gameAlive false or None. game never started")
        while self.queryGame(json=True)["gameAlive"]:
            self.assertEqual(self.postMove(self.randomMove()).status_code, 200)

    @unittest.skip
    def test_queryIsGameOver(self):
        self.initGame()
        for move in foolsMate:
            self.postMove(move)
        self.assertFalse(self.player1.get("game/").json["gameAlive"])

    @unittest.skip
    def test_resign(self):
        self.initGame()
        self.postMove(self.randomMove())
        response = self.postMove("resign")
        self.assertEqual(response.status_code, 200)

    # @unittest.skip
    def test_headers(self):
        self.initGame()
        print(self.player2First)
        one = threading.Thread(target=self.get, args=("game/", {"HOLDME": True}))
        one.start()
        # self.player2.ge

if __name__ == '__main__':
    unittest.main()
