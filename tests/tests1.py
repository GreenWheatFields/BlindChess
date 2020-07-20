from server import app
import unittest


class TestGeneral(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @unittest.skip
    def test_lobbyFullError(self):
        users = []
        for i in range(3):
            users.append(app.test_client().get("/game"))
        self.assertEqual(users[2].status_code, 404)

    # @unittest.skip
    def test_SimpleClientTest(self):
        for i in range(3):
            print(app.test_client().post("game/?move=e4e5"))


if __name__ == '__main__':
    unittest.main()
