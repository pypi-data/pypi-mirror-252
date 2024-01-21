
'''
	create_wallet
	
	fields {
		"label": ""
	}
'''

'''
	(mo)net
	monay
	monayuh
	monaym
'''

import moneti.offline_tool.climate as offline_tool_climate

import os
from os.path import dirname, join, normpath
import pathlib
import sys

def play (
	JSON
):
	print ('create wallet', JSON)
	offline_climate = offline_tool_climate.retrieve ()

	wallets_paths = offline_climate ["paths"] ["wallets"]
	fields = JSON ["fields"]
	
	if ("label" not in fields):
		return {
			"obstacle": f'Please choose a "label" for the wallet.'
		}
	
	wallet_label = fields ["label"]
	wallet_path = str (normpath (join (wallets_paths, wallet_label)))

	if (os.path.isdir (wallet_path) != True):
		os.mkdir (wallet_path)
		offline_tool_climate.climate ["elected wallet"] ["path"] = wallet_path
		return {
			"victory": "wallet created"
		}
		
	else:
		offline_tool_climate.climate ["elected wallet"] ["path"] = wallet_path
		return {
			"obstacle": "There is already a directory at that path"
		}
