import unittest
import logging
import os
import time
import subprocess

from lib import camlistore 

config = camlistore.Config('localhost:3179', 'camli', 'pass3179')

class TestNoseCases(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cwd = os.getcwd()
		os.chdir(os.environ['CAMLI_SRC'])
		cls.devcam_server = subprocess.Popen(['bin/devcam', 'server'])
		os.chdir(cwd)
		time.sleep(3)

	@classmethod
	def tearDownClass(cls):
		cls.devcam_server.kill()
		
	def test_query(self):
		scraper = camlistore.Search(config)
		resp  = scraper.query("-is:image")
		import json
		logging.info(json.dumps(resp, indent=4))
		self.assertIsNotNone(resp)
		logging.info("HELLO")
		self.fail()
		
