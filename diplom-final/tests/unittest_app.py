import unittest
import app


class Test_app(unittest.TestCase):
    def test_mutual_friends(self):
        self.assertTrue(app.mutual_friends())

    def test_mutual_groups(self):
        self.assertIs(type(app.mutual_groups()), list)

    def test_get_user_interests_music_books(self):
        self.assertTrue(app.get_user_interests_music_books(app.user.user_id))

    def test_get_res_interests_music_books(self):
        self.assertTrue(app.get_res_interests_music_books())

    def test_mutual_interests(self):
        self.assertIs(type(app.mutual_interests()), list)

    def test_mutual_info(self):
        self.assertTrue(app.mutual_info())

    def test_run(self):
        self.assertIs(type(app.run()), list)
