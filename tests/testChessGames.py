import unittest
import chess
import random
from server.createApp import create_app


class testChessGames(unittest.TestCase):

    def setUp(self):
        self.board = chess.Board()
        self.randomMove = lambda: random.choice(list(self.board.generate_legal_moves()))
        self.app = create_app()
        self.player1 = self.generateClient()
        self.player2 = self.generateClient()

    def generateClient(self):
        with self.app.test_client() as client:
            return client

    # @unittest.skip
    def test_simpleChessMove(self):
        self.player2.get("game/")
        print(self.player1.get("game/").status_code)
        # self.player1.get("game/")
        # json = self.player2.get("game/").json
        # # todo rename yourTurn varibale
        # if json is None:
        #     self.fail("null json response")
        # if json["turn"] == json["yourTurn"]:
        #     self.assertEqual(self.player2.post("game/?move=e2e3").status_code, 200)
        #     self.assertEqual(self.player1.post("game/?move=e3e4").status_code, 200)
        # else:
        #     self.assertEqual(self.player1.post("game/?move=e2e3").status_code, 200)
        #     self.assertEqual(self.player2.post("game/?move=e3e4").status_code, 200)

    # @unittest.skip
    def test_randomChessMoves(self):
        self.player2.get("game/")
        print(self.player1.get("game/").status_code)
        # player1ID = self.player1.get("game/").json
        # player2ID = self.player2.get("game/").json
        # turn = 1 if player2ID['turn'] == player2ID["yourTurn"] else 0
        #
        # for _ in range(20):
        #     print(turn)
        #     self.player2.post("game/?move={}".format(self.randomMove())) if turn == 1 else self.player1.post("game/?move={}".format(self.randomMove()))
        #     turn = int(not turn)


if __name__ == '__main__':
    unittest.main()
