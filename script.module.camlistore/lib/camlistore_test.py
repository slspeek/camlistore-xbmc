import unittest
import logging
import os
import time
import subprocess

from lib import camlistore 


class QueryEmptyServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = camlistore.Config(False, 'localhost:3179', 'camli', 'pass3179')
        cwd = os.getcwd()
        os.chdir(os.environ['CAMLI_SRC'])
        cls.devcam_server = subprocess.Popen(['bin/devcam', 'server'])
        os.chdir(cwd)
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.devcam_server.kill()

    def test_query(self):
        scraper = camlistore.Search(self.config)
        resp  = scraper.query("-is:image")
        self.assertEqual(len(resp), 0)

class Secure(QueryEmptyServer):

    @classmethod
    def setUpClass(cls):
        cls.config = camlistore.Config(True, 'localhost:3179', 'camli', 'pass3179')
        cwd = os.getcwd()
        os.chdir(os.environ['CAMLI_SRC'])
        cls.devcam_server = subprocess.Popen(['bin/devcam', 'server', "-tls"])
        os.chdir(cwd)
        time.sleep(3)

