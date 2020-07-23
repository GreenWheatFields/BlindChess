from server import app
import unittest


class TestGeneral(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.player1 = app.test_client()
        self.player2 = app.test_client()

    def init2PlayerGame(self):
        self.player1.get("game/")
        self.player2.get("game/")

    @unittest.skip
    def test_lobbyFullError(self):
        self.init2PlayerGame()
        self.assertEqual(self.client.get("game/").status_code, 404)

    @unittest.skip
    def test_SimpleClientTest(self):
        for i in range(3):
            print(i)
            print(app.test_client().get("game/"))

    # @unittest.skip
    def test_simpleChessMove(self):
        with app.test_client() as player1, app.test_client() as player2:
            player1.get("game/")
            player2.get("game/")
            print(player1.post("game/?move=move").status_code)
            print(player2.post("/game/?move=move").status_code)



if __name__ == '__main__':
    unittest.main()
