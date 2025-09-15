# # from app import lwphone

# # def test_lwphone():
# #         assert lwphone() == "9309982768"


# import unittest
# from app import app

# class TestApp(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()

#     def test_name_route(self):
#         response = self.client.get('/name')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"ruturaj gidde", response.data)

#     def test_phone_route(self):
#         response = self.client.get('/phone')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"9309982768", response.data)

# if __name__ == '__main__':
#     unittest.main()

import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Flask provides a test client for simulating requests
        self.client = app.test_client()
        self.client.testing = True

    def test_root_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome to Ruturaj's Flask App".encode(), response.data)

    def test_name_route(self):
        response = self.client.get('/name')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ruturaj gidde", response.data)

    def test_phone_route(self):
        response = self.client.get('/phone')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"9309982768", response.data)

if __name__ == '__main__':
    unittest.main()
