



import moneti.offline_tool.flask.start_dev as flask_start_dev
import moneti.offline_tool.sockets as offline_tool_sockets

import os
from os.path import dirname, join, normpath
import pathlib
import sys
		
def clique ():
	import click
	@click.group ("offline_tool")
	def group ():
		pass

	'''
		./moneti offline_tool sockets --port 65000
	'''
	import click
	@group.command ("sockets")
	@click.option ('--port', '-np', default = '65000')
	def search (port):	
		CWD = os.getcwd ();
		
		import moneti.offline_tool.climate as offline_tool_climate
		offline_tool_climate.build (
			CWD
		)
	
		offline_tool_sockets.open (
			port = port
		)
	
		return;


	'''
		./moneti offline_tool start --port 50000
	'''
	import click
	@group.command ("start")
	@click.option ('--port', '-np', default = '50000')
	def search (port):	
		CWD = os.getcwd ();
		
		import moneti.offline_tool.climate as offline_tool_climate
		offline_tool_climate.build (
			CWD
		)
	
		flask_start_dev.start (
			port = int (port)
		)
	
		return;
		
	return group




#



