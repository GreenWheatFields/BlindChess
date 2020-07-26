import unittest
from server import app
import chess
import random


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.board = chess.Board()
        self.randomMove = lambda: random.choice(list(self.board.generate_legal_moves()))

    @unittest.skip
    def test_simpleChessMove(self):
        with app.test_client() as player1, app.test_client() as player2:
            player1.get("game/")
            json = player2.get("game/").json
            # probable could be simplified
            #todo rename yourTurn varibale
            if json["turn"] == json["yourTurn"]:
                self.assertEqual(player2.post("game/?move=e2e3").status_code, 200)
                self.assertEqual(player1.post("game/?move=e3e4").status_code, 200)
            else:
                self.assertEqual(player1.post("game/?move=e2e3").status_code, 200)
                self.assertEqual(player2.post("game/?move=e3e4").status_code, 200)

    @unittest.skip
    def test_randomChessMoves(self):
        with app.test_client() as player1, app.test_client() as player2:
            player1ID = player1.get("game/").json
            player2ID = player2.get("game/").json
            turn = 1 if player2ID['turn'] == player2ID["yourTurn"] else 0

            for _ in range(20):
                print(turn)
                player2.post("game/?move={}".format(self.randomMove())) if turn == 1 else player1.post("game/?move={}".format(self.randomMove()))
                turn = int(not turn)


if __name__ == '__main__':
    unittest.main()
