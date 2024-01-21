



import moneti.offline_tool.flask.start_dev as flask_start_dev

import os
from os.path import dirname, join, normpath
import pathlib
import sys
		
def clique ():
	import click
	@click.group ("offline_tool_tracks")
	def group ():
		pass

	'''
		moneti_local offline_tool_tracks create_wallet --label wallet-1
	'''
	import click
	@group.command ("create_wallet")
	@click.option ('--label', required = True)
	@click.option ('--port', '-np', default = '50000')
	def search (label, port):	
		address = f"http://127.0.0.1:{ port }"
	
		import json
		from os.path import dirname, join, normpath
		import os
		import requests
		r = requests.patch (
			address, 
			data = json.dumps ({
				"label": "create wallet",
				"fields": {
					"label": label
				}
			})
		)
		print (r.text)
		
		return;
		
	return group




#



