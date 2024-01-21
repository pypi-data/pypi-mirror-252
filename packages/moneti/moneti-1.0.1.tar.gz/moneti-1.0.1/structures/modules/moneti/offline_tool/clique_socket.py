



import moneti.offline_tool.flask.start_dev as flask_start_dev

import os
from os.path import dirname, join, normpath
import pathlib
import sys
		
import asyncio
from websockets.sync.client import connect

async def async_search (port):
	address = f"ws://localhost:{ port }"
	
	with connect (address) as websocket:
		websocket.send ("Hello world!")
		message = websocket.recv ()
		
		print (f"Received: {message}")

	
		
def clique ():
	import click
	@click.group ("offline_tool_socket")
	def group ():
		pass

	'''
		moneti_local offline_tool_socket create_wallet --label wallet-1
	'''
	import click
	@group.command ("create_wallet")
	@click.option ('--label', required = True)
	@click.option ('--port', '-np', default = '65000')
	def search (label, port):	
		
		asyncio.run (async_search (port))	
		
	return group




#



