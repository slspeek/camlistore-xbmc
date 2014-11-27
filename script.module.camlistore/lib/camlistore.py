'''
    camlistore
    ~~~~~~~~~~

    This module contains the search class which is a simplified calistore search client
'''
import requests
from xbmcswift2 import xbmcaddon


class Config:

    def __init__(self, https, address, username, password):
        self._https = https
        self._address = address
        self._username = username
        self._password = password

    @property
    def https(self):
        """docstring for https"""
        return self._https

    @property
    def address(self):
        return self._address

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    def protocol(self):
        return "https://" if self.https else  "http://"

def xbmcConfig(name):
    addon = xbmcaddon.Addon(name)
    return Config(
            addon.getSetting('https'),
            addon.getSetting('address'),
            addon.getSetting('username'),
            addon.getSetting('password'))

class Search:

    def __init__(self, config):
        self.config = config
        self.conf = self._conf_discovery()

    def _conf_discovery(self):
        """ Perform a discovery to gather server configuration. """
        r = requests.get(self.config.protocol() + self.config.address,
                auth=self.auth(),
                headers={'Accept': 'text/x-camli-configuration'},
                verify=False)
        r.raise_for_status()
        return r.json()


    def auth(self):
        return (self.config.username, self.config.password)

    def _url(self,path):
        '''Returns a full url for the given path'''            
        return self.config.protocol() + self.config.address +  path

    def _get(self, url, data=None):
        resp = requests.post(url, data=data,auth=self.auth(), verify=False)
        resp.raise_for_status()
        return resp.json()

    def query(self, expression):
        ''' Returns a list of playable permanodes '''
        data = '{"expression": "%s", "describe":{ "depth": 2}}' % expression
        searchRoot = self.conf['searchRoot']
        url = self._url(searchRoot + 'camli/search/query')
        j = self._get(url, data=data)
        if not j.has_key("blobs"):
            return []

        blobs = j["blobs"]
        meta = j["description"]["meta"]
        items = []
        if not blobs or not meta:
            return []

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
                    'path': self.config.protocol() + self.config.username + ':'+ self.config.password + '@' + self.config.address + '/ui/download/' + fileref,
                    'is_playable': True,
                    #'info_type': 'pictures',
                    })
        return items

