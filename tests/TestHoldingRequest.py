from tests.testChessGames import testChessGames
import unittest
import time
import threading

postResponse = {}
responses = []


class testPolling(testChessGames):

    @unittest.skip
    def test_simpleHold(self):
        endpoint = "hold/"
        post = threading.Thread(target=self.post, args=endpoint)
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

    @unittest.skip
    def test_headers(self):
        headers = {"HOLDME": True}
        get1 = threading.Thread(target=self.get, args=("hold/me", headers))
        headers = {"ESCAPE": 0}
        get2 = threading.Thread(target=self.get, args=("hold/me", headers))
        get1.start()
        get2.start()
        get2.join()
        if get1.is_alive():
            get1.join(0)
            self.fail("escape clause not met")

    @unittest.skip
    def test_reconnect(self):
        # todo, see if gamestatus is updated when a user doesnt reconnect after a specific timeout
        pass




if __name__ == '__main__':
    unittest.main()
