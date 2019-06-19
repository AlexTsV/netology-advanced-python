import vk_api
import unittest


class Test_vk_api(unittest.TestCase):
    def test_get_user_info(self):
        self.assertTrue(vk_api.usr.get_user_info(vk_api.usr.user_id))

    def test_get_user_groups(self):
        self.assertIsNotNone(vk_api.usr.get_user_groups(vk_api.usr.user_id))

    def test_get_age_user(self):
        self.assertIs(type(vk_api.usr.get_age_user()), int)

    def test_search(self):
        self.assertIs(type(vk_api.usr.search()), list)

    def test_get_photo(self):
        self.assertRaises(TypeError, vk_api.usr.get_photo(vk_api.usr.user_id), {'fsa', 'fds'})


if __name__ == '__main__':
    unittest.main()
