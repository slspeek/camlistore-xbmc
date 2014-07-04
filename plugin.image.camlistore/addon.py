from xbmcswift2 import Plugin, xbmc
import camlistore

plugin = Plugin()


camli = camlistore.Search(camlistore.xbmcConfig('plugin.image.camlistore'))

@plugin.route('/')
def main_menu():
	items = [
			{ 'label': 'Images', 'path': plugin.url_for('images')  },
			{ 'label': 'Search', 'path': plugin.url_for('search')  }
	]
	return items

@plugin.route('/images/')
def images():
	v = camli.query('is:image')
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
