from xbmcswift2 import Plugin, xbmc
from camlistore import Search

plugin = Plugin()

camli = Search('plugin.video.camlistore')

@plugin.route('/')
def main_menu():
	items = [
			{ 'label': 'Videos', 'path': plugin.url_for('video')  },
			{ 'label': 'Search', 'path': plugin.url_for('search')  }
	]
	return items

@plugin.route('/videos/')
def video():
	v = camli.query('-is:image')
	return plugin.finish(v)

@plugin.route('/search/')
def search():
	kb = xbmc.Keyboard('', 'Search Camlistore ' , False)
	kb.doModal()
	if (kb.isConfirmed()):                   
		search_text = kb.getText()
	return plugin.finish(camli.query(search_text))

if __name__ == '__main__':
    plugin.run()
