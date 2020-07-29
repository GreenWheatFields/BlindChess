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

    # @unittest.skip
    def test_simpleChessMove(self):
        self.initGame()
        if self.response is None:
            self.fail("null json response")
        if self.player2First:
            self.assertEqual(self.player2.post("game/?move=e2e3").status_code, 200)
            self.assertEqual(self.player1.post("game/?move=e3e4").status_code, 200)
        else:
            self.assertEqual(self.player1.post("game/?move=e2e3").status_code, 200)
            self.assertEqual(self.player2.post("game/?move=e3e4").status_code, 200)

    @unittest.skip
    def test_randomChessMoves(self):
        self.initGame()
        self.board.turn = self.response["turn"]
        gameAlive = self.response["gameAlive"]
        if not gameAlive or None:
            self.fail("gameAlive false. game never started")
        while gameAlive:
            if self.player2First:
                move = self.randomMove()
                self.player2.post("game/?move={}".format(move))
                self.player2First = not self.player2First
                self.board.push(move)
            else:
                move = self.randomMove()
                self.player1.post("game/?move={}".format(move))
                self.player2First = not self.player2First
                self.board.push(move)
            gameAlive = self.player1.get("game/").json["gameAlive"]

    @unittest.skip
    def test_queryIsGameOver(self):
        # todo replicate on server
        for move in foolsMate:
            move = chess.Move.from_uci(move)
            self.board.push(move)
        print(self.board.is_game_over())


if __name__ == '__main__':
    unittest.main()
