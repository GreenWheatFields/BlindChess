from tests.testChessGames import testChessGames
import unittest


class testPolling(testChessGames):
    def test_simpleHold(self):
        print(self.player1.get("hold/"))
        # todo, query post and get at the same time and see how server responds


if __name__ == '__main__':
    unittest.main()
