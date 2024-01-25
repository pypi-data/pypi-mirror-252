


'''
	import basal.ganglia.list as basal_ganglia_list
	basal_ganglia_list.start ()
'''


'''
	[{
		"name": "",
		"definitions": []
	}]
'''

import basal.climate as basal_climate
from pathlib import Path

import os
from rich import print_json

def start ():	
	basal_ganglia = basal_climate.find ("basal ganglia")	
	basal_ganglia_path = basal_ganglia ['path']
	
	issues = []
	
	directory_names = []
	for address in Path (basal_ganglia_path).iterdir ():
		address_name = os.path.relpath (address, basal_ganglia_path)
		
		proceeds = {
			"name": address_name,
			"definitions": []
		}
		
		if address.is_dir ():
			for basal_module in Path (address).iterdir ():
				
				if basal_module.is_dir ():
					basal_module_name = os.path.relpath (basal_module, address)
					basal_module_name_split = basal_module_name.split ('.')
					assert (type (int (basal_module_name_split [0])) == int), basal_module
					proceeds ["definitions"].append (basal_module_name)
					
				else:
					issues.append ({
						"exception": "This module address is not a directory.",
						"path": str (basal_module)
					})
				
				
				
		else:
			issues.append ({
				"exception": "This address is not a directory.",
				"path": address
			})
		
			#raise Exception (f'found a path that is not a directory: \n\n\t{ name }\n')
		
	
		'''
		if trail.is_file ():
			print(f"{trail.name}:\n{trail.read_text()}\n")
		'''
	
	if (len (issues) >= 1):
		print_json (data = issues)
		raise Exception (f"Issues were found with the basal directory.")
	
	return proceeds