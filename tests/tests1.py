from server import app
import unittest


class TestGeneralRequests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_lobbyFullError(self):
        users = []
        for i in range(3):
            users.append(app.test_client().get("/game"))
        self.assertEqual(users[2].status_code, 404)


if __name__ == '__main__':
    unittest.main()
