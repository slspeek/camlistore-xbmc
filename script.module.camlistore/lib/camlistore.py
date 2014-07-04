'''
    camlistore
    ~~~~~~~~~~

    This module contains the search class which is a simplified calistore search client
'''
import requests
from xbmcswift2 import xbmcaddon

def xbmcConfig(name):
	addon = xbmcaddon.Addon(name)
	return Config(
			addon.getSetting('address'),
			addon.getSetting('username'),
			addon.getSetting('password'))

class Config:

	def __init__(self, address, username, password):
		self._address = address
		self._username = username
		self._password = password

	@property
	def address(self):
		return self._address

	@property
	def username(self):
		return self._username

	@property
	def password(self):
		return self._password


class Search:

	def __init__(self, config):
		self.config = config
		self.conf = self._conf_discovery()

	def _conf_discovery(self):
		""" Perform a discovery to gather server configuration. """
		r = requests.get('http://' + self.config.address,
				auth=self.auth(),
				headers={'Accept': 'text/x-camli-configuration'})
		r.raise_for_status()
		return r.json()


	def auth(self):
		return (self.config.username, self.config.password)

	def _url(self,path):
		'''Returns a full url for the given path'''            
		return 'http://' + self.config.address +  path

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
					'path': 'http://' + self.config.username + ':'+ self.config.password + '@' + self.config.address + '/ui/download/' + fileref,
					'is_playable': True,
					#'info_type': 'pictures',
					})
		return items

