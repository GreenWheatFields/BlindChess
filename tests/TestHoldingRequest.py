from tests.testChessGames import testChessGames
import unittest
import time
import threading

postResponse = {}


class testPolling(testChessGames):

    @unittest.skip
    def test_simpleHold(self):
        endpoint = "hold/"
        post = threading.Thread(target=self.post, args=(endpoint))
        post.start()
        response = self.get(endpoint)
        try:
            if response["testVar"] is True:
                pass
        except KeyError:
            self.fail("invalid response")
        post.join(6)
        if post.is_alive():
            self.fail("thread still alive after timeoue")
        else:
            try:
                global postResponse
                if postResponse["testVar"] is True:
                    pass
            except KeyError:
                self.fail("variables differentiate")

    def test_headers(self):
        headers = {"2" : "4"}
        self.get("hold/me/", headers=headers)

    def get(self, endpoint, headers=None):
        #todo, post and get methods should belong to the super class
        return self.player1.get(endpoint, headers=headers if headers is not None else headers)

    def post(self, *endpoint, **other):
        endpoint = "".join(endpoint)
        r = self.player2.post(endpoint).json
        global postResponse
        postResponse = r


if __name__ == '__main__':
    unittest.main()
