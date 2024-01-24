
'''
	import moneti.treasury.climate as treasury_climate
	offline_climate = treasury_climate.retrieve ()
'''

import os
from os.path import dirname, join, normpath
import pathlib
import sys

climate = {
	"elected treasury": {},
	
	"paths": {}
}

def build (
	CWD = None
):
	offline_goods = str (normpath (join (CWD, "offline_goods")))
	treasurys = str (normpath (join (offline_goods, "treasurys")))

	if (os.path.isdir (offline_goods) != True):
		os.mkdir (offline_goods)
		
	if (os.path.isdir (treasurys) != True):
		os.mkdir (treasurys)

	climate ["paths"] ["offline_good"] = offline_goods
	climate ["paths"] ["treasurys"] = treasurys
	

	return;


def retrieve ():
	return climate