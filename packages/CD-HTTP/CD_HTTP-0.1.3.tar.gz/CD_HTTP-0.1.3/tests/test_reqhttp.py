import unittest
from HTTP import reqhttp  # Adjust the import based on where your HTTP class is located


class TestHTTP(unittest.TestCase):

    def setUp(self):
        self.client = reqhttp.HTTP()

    def test_get_request(self):
        # Test a basic GET request
        response = self.client.get("https://httpbin.org/get")
        self.assertIn("args", response.json())

    def test_post_request(self):
        # Test a basic POST request
        data = {"key": "value"}
        response = self.client.post("https://httpbin.org/post", json=data)
        self.assertEqual(response.json()["json"], data)

    def test_user_agent(self):
        # Test custom user agent
        user_agent = "CustomUserAgent/1.0"
        response = self.client.get("https://httpbin.org/user-agent", user_agent=user_agent)
        self.assertEqual(response.json()["user-agent"], user_agent)

    def test_session(self):
        # Test session persistence
        self.client.start_session()
        response1 = self.client.get("https://httpbin.org/cookies/set/sessioncookie/123456")
        response2 = self.client.get("https://httpbin.org/cookies")
        self.client.close_session()
        self.assertEqual(response2.json()["cookies"]["sessioncookie"], "123456")

    # Add more tests as needed...


if __name__ == '__main__':
    unittest.main()
