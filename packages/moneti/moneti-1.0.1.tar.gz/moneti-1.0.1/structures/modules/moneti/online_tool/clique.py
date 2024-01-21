



import moneti.offline_tool.flask.start_dev as flask_start_dev

def clique ():
	import click
	@click.group ("online_tool")
	def group ():
		pass

	'''
		./moneti online_tool start --port 60000
	'''
	import click
	@group.command ("start")
	@click.option ('--port', '-p', default = '55500')
	def search (port):		
		flask_start_dev.start (
			port = int (port)
		)
	
		return;

	return group




#



