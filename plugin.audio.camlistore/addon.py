from xbmcswift2 import Plugin, xbmc
import camlistore

plugin = Plugin()

camli = camlistore.Search(camlistore.xbmcConfig('plugin.audio.camlistore'))

@plugin.route('/')
def main_menu():
	items = [
			{ 'label': 'Music', 'path': plugin.url_for('music')  },
			{ 'label': 'Search', 'path': plugin.url_for('search')  }
	]
	return items

@plugin.route('/music/')
def music():
	v = camli.query('-is:image')
	return plugin.finish(v)

@plugin.route('/search/')
def search():
	kb = xbmc.Keyboard('', 'Search Camlistore ' , False)
	kb.doModal()
	if (kb.isConfirmed()):                   
		search_text = kb.getText()
	return camli.query(search_text)

if __name__ == '__main__':
    plugin.run()
