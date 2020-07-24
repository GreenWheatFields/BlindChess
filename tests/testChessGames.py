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
            player2.get("game/")
            print(player1.post("game/?move=move").status_code)
            print(player2.post("/game/?move=move").status_code)

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
