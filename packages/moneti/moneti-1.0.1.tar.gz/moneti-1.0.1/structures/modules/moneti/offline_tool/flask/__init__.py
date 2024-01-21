
from flask import Flask, request
import json
from os.path import dirname, join, normpath
import os

import moneti.offline_tool.options as options

import rich

def build (
	records = 1
):
	app = Flask (__name__)

	'''
import json
from os.path import dirname, join, normpath
import os
import requests
r = requests.patch (
	'http://127.0.0.1:50000', 
	data = json.dumps ({
		"track": "form proposal keys",
		"fields": {
			"seed": "5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
			"directory_path": os.getcwd ()
		}
	})
)
print (r.text)
	'''
	@app.route ("/", methods = [ 'PATCH' ])
	def route ():
		data = ""
		
		try:
			data = request.get_data ();
			
			UTF8 = data.decode ('utf-8')
			if (records >= 1): print ("UTF8 ::", UTF8)
			
			JSON = json.loads (UTF8)
			if (records >= 1): print ("JSON ::", json.dumps (UTF8))
			
			data = options.play (JSON = JSON)
			if (records >= 1): rich.print_json (data = data)
			
			response = app.response_class (
				response = json.dumps (data),
				status = 200,
				mimetype = 'application/json'
			)

			return response
			
		except Exception as E:
			print ("exception:", E)
	
		return json.dumps ({
			"obstacle": ""
		})
	
	return app;