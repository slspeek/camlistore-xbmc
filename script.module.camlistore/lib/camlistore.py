'''
    camlistore
    ~~~~~~~~~~

    This module contains the search class which is a simplified calistore search client
'''
import requests
from xbmcswift2 import xbmcaddon


class Search:

	def __init__(self, name):
		self.name = name
		self.conf = self._conf_discovery()

	def _conf_discovery(self):
		""" Perform a discovery to gather server configuration. """
		r = requests.get('http://' + self.address(),
				auth=self.auth(),
				headers={'Accept': 'text/x-camli-configuration'})
		r.raise_for_status()
		return r.json()

	def address(self):
		addon = xbmcaddon.Addon(self.name)
		return addon.getSetting('address')

	def username(self):
		addon = xbmcaddon.Addon(self.name)
		return addon.getSetting('username')

	def password(self):
		addon = xbmcaddon.Addon(self.name)
		return addon.getSetting('password')

	def auth(self):
		return (self.username(), self.password())

	def _url(self,path):
		'''Returns a full url for the given path'''            
		return 'http://' + self.address() +  path

	def _get(self, url, data=None):
		resp = requests.post(url, data=data,auth=self.auth())
		#print "Resp:", resp.text
		return resp.json()

	def query(self, expression):
		''' Returns a list of playable permanodes '''
		data = '{"expression": "%s", "describe":{ "depth": 2}}' % expression
		searchRoot = self.conf['searchRoot']
		print 'searchRoot', searchRoot
		url = self._url(searchRoot + 'camli/search/query')
		print url
		j = self._get(url, data=data)
		if not j.has_key("blobs"):
			return []

		blobs = j["blobs"]
		meta = j["description"]["meta"]
		items = []
		if not blobs or not meta:
			return []

		print blobs, meta
		for k in blobs:
			k = k["blob"]
			attrs = meta[k]["permanode"]["attr"]
			filename = k
			fileref = None
			title = None
			if attrs.has_key("camliContent"):
				fileref = attrs["camliContent"][0]
				filename = meta[fileref]["file"]["fileName"]
			if attrs.has_key('title'):
				title = attrs["title"][0]
			if title:
				label = title
			else:
				label = filename
			if fileref:
				items.append({
					'label': label,
					'path': 'http://' + self.username() + ':'+ self.password() + '@' + self.address() + '/ui/download/' + fileref,
					'is_playable': True,
					#'info_type': 'pictures',
					})
		return items

