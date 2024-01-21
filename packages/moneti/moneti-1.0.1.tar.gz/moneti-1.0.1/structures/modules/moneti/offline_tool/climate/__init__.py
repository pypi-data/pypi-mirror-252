
'''
	import moneti.offline_tool.climate as offline_tool_climate
	offline_climate = offline_tool_climate.retrieve ()
'''

import os
from os.path import dirname, join, normpath
import pathlib
import sys

climate = {
	"elected wallet": {},
	
	"paths": {}
}

def build (
	CWD = None
):
	offline_goods = str (normpath (join (CWD, "offline_goods")))
	wallets = str (normpath (join (offline_goods, "wallets")))

	if (os.path.isdir (offline_goods) != True):
		os.mkdir (offline_goods)
		
	if (os.path.isdir (wallets) != True):
		os.mkdir (wallets)

	climate ["paths"] ["offline_good"] = offline_goods
	climate ["paths"] ["wallets"] = wallets
	

	return;


def retrieve ():
	return climate