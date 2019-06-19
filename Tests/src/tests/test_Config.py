import unittest
from src.helpers.config import Config
from src.app import App
import sys
import logging


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.levels = (
            ('critical', logging.CRITICAL, False),
            ('error', logging.ERROR, False),
            ('warning', logging.WARNING, False),
            ('info', logging.INFO, True),
            ('debug', logging.DEBUG, False),
        )
        self.config_file = 'testapp.yaml'

    def test_Config(self):
        test = Config()
        self.assertEqual(test.config_file, self.config_file)

    def test_app_init(self):
        app = Config(self.levels)
        self.assertTrue((app.get_verbosity_level(self.levels)) == 20)

    def test_init_env_config_disk(self):
        app = Config.init_env_config_path()
        self.assertTrue(len(app) == 5)

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_wrong_arg(self):
        self.assertRaises(Exception, Config.get_windows_system_disk())


    def test_run(self):
        result = None
        self.assertEqual(App().run(), result)




if __name__ == '__main__':
    unittest.main()

