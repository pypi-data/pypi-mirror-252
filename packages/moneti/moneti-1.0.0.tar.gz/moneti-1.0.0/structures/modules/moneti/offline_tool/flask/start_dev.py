

import moneti.offline_tool.flask as offline_tool_flask

def start (
	port
):
	print ('starting')
	
	app = offline_tool_flask.build ()
	app.run (port = port)

	return;