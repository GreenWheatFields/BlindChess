import unittest
import chess
import random
from server.createApp import create_app

foolsMate = ["f2f3", "e7e5", "g2g4", "d8h4"]


class testChessGames(unittest.TestCase):

    def setUp(self):
        self.board = chess.Board()
        self.app = create_app()
        self.player1 = self.generateClient()
        self.player2 = self.generateClient()
        self.response = None
        self.initGame()
        self.player2First = self.response["turn"] == self.response["yourTurn"]

    def initGame(self):
        self.player1.get("game/")
        self.response = self.player2.get("game/").json
        if self.response is None:
            self.fail("inital response was null")

    def randomMove(self):
        return random.choice(list(self.board.generate_legal_moves()))

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
        return self.player1.get("game/") if not json else self.player1.get("game/").json

    @unittest.skip
    def test_simpleChessMove(self):
        self.initGame()
        if self.response is None:
            self.fail("null json response")
        self.assertEqual(self.postMove("e2e3").status_code, 200)
        self.assertEqual(self.postMove("e7e6").status_code, 200)

    # @unittest.skip
    def test_randomChessMoves(self):
        self.initGame()
        self.board.turn = self.response["turn"]
        gameAlive = self.response["gameAlive"]
        if not gameAlive or gameAlive is None:
            self.fail("gameAlive false or None. game never started")
        while gameAlive:
            move = self.randomMove()
            self.board.push(move)
            self.postMove(move)
            gameAlive = self.queryGame(json=True)
            print(self.board)


    @unittest.skip
    def test_queryIsGameOver(self):
        self.initGame()
        for move in foolsMate:
            self.postMove(move)
        self.assertFalse(self.player1.get("game/").json["gameAlive"])


if __name__ == '__main__':
    unittest.main()
