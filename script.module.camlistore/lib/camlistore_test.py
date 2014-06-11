import unittest
import logging

from lib import camlistore as scraper

class TestNoseCases(unittest.TestCase):

	def test_get_videos(self):
		scraper.address = lambda: "localhost:3179/"
		scraper.username = lambda: "steven"
		scraper.password = lambda: "gnu"
		resp  = scraper.get_videos()
		import json
		logging.info(json.dumps(resp, indent=4))
		self.assertIsNotNone(resp)
		logging.info("HELLO")
		self.fail()
		
	def test_query(self):
		scraper.address = lambda: "localhost:3179/"
		scraper.username = lambda: "steven"
		scraper.password = lambda: "gnu"
		resp  = scraper.query("is:pano")
		import json
		logging.info(json.dumps(resp, indent=4))
		self.assertIsNotNone(resp)
		logging.info("HELLO")
		self.fail()
		
