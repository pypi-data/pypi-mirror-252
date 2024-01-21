




from moneti._clique.group import clique as clique_group

from moneti.offline_tool.clique import clique as offline_tool_clique
from moneti.offline_tool.clique_tracks import clique as offline_tool_clique_tracks
from moneti.offline_tool.clique_socket import clique as offline_tool_clique_socket


from moneti.online_tool.clique import clique as online_tool_clique


#from moneti.modules.vibes.clique import clique as vibes_clique

def clique ():

	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("example")
	def example_command ():	
		print ("example")

	group.add_command (example_command)

	group.add_command (offline_tool_clique ())
	group.add_command (offline_tool_clique_tracks ())
	group.add_command (offline_tool_clique_socket ())
	
	group.add_command (online_tool_clique ())
	
	#group.add_command (vibes_clique ())
	
	
	group ()




#
