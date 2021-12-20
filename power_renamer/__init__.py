from fman import DirectoryPaneCommand, DirectoryPane, ApplicationCommand, show_alert, FMAN_VERSION, DirectoryPaneListener, load_json, save_json, show_prompt, YES, NO, ABORT
from fman.fs import copy, move, exists
from fman.url import as_human_readable, basename
from subprocess import Popen
import os.path
import re

class PowerRename(DirectoryPaneCommand):
	def __call__(self):		
		url = self.pane.get_path() 
		paths = self.pane.get_selected_files()

		if len(paths) < 1:
			show_alert("Please select at least 1 file.")
			return

		basefilename, ok = show_prompt('Please enter the bease name like "filename_####"')
		if not basefilename and not ok:
			return
		

		# how many times does text contain #
		digitLength = basefilename.count('#')
		if(digitLength < 1):
			show_alert('Please enter a valid base name with at least 1 #')
			return

		# digitlength power of 10
		maxNumber = pow(10, digitLength)
		#show_alert('Max number is ' + str(maxNumber))


		name_split = basefilename.split("#")
		baseFilename = name_split[0]

		if(len(paths) > maxNumber):
			show_alert('You added ' + str(digitLength) + ' #s. With that you can rename ' + str(maxNumber) + ' files. But you selected ' + str(len(paths)) + ' files.')
			return

		#show_alert('You entered ' + str(count) + ' #')
		preview = iteateFiles(paths, baseFilename, digitLength, url, False)
		
		choice = show_alert(
			preview,
			buttons=YES | ABORT,
			)
		if choice == ABORT:
			return

		iteateFiles(paths, baseFilename, digitLength, url, True)
		self.pane.clear_selection() 
			

def iteateFiles(paths, baseFilename, digitLength, url, rename):	
	preview = ''
	index = 1
	for path in paths:	
		name, ext = os.path.splitext(path)
		name = os.path.basename(path)	
		
		indexString = str(index)
		newFilename = baseFilename + indexString.zfill(digitLength) + ext		
		newPath = url + "/" + newFilename

		preview += name  + ' > ' + newFilename + '\n'
		if exists(newPath):
			preview += "File already exists, will be skipped.\n"
			continue			

		
		if(rename):
			move(path, newPath)

		index += 1

	return preview

