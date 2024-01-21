

'''
	{
		"label": "",
		"fields": {
			
		}
	}
'''

import json
from os.path import dirname, join, normpath
import os

import moneti.offline_tool.options.labels.create_wallet as create_wallet
import moneti.offline_tool.options.labels.form_proposal_keys as form_proposal_keys

def records (record):
	print (record)

def play (
	JSON = "",
	records = records
):
	print ("JSON:", JSON)

	
	if ("label" not in JSON ):
		records (f'Options need a "label".')
		return;

	label = JSON ["label"]
	
	print ("label:", label)
	
	if (label == "create wallet"):
		return create_wallet.play (JSON)
	elif (label == "form proposal keys"):
		return form_proposal_keys.play (JSON)

	return {
		"obstacle": "That label was not found."
	}
