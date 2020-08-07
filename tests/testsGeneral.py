import unittest
from tests.testChessGames import testChessGames


class TestGeneral(testChessGames):

    # @unittest.skip
    def test_lobbyFullError(self):
        self.initGame()
        self.assertEqual(self.generateClient().get("game/").status_code, 404)


if __name__ == '__main__':
    unittest.main()
