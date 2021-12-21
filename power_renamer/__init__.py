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

		basefilename, ok = show_prompt('Please enter the base name like "filename_####"')
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

		showPreview = shouldShowPreview(basefilename)
		if(showPreview):			
			basefilename = basefilename[1:]			

		name_split = basefilename.split("#")
		baseFilename = name_split[0]

		if(len(paths) > maxNumber):
			show_alert('You added ' + str(digitLength) + ' #s. With that you can rename ' + str(maxNumber) + ' files. But you selected ' + str(len(paths)) + ' files.')
			return

		#show_alert('You entered ' + str(count) + ' #')
		if(showPreview):
			preview = iteateFilesForRename(paths, baseFilename, digitLength, url, False)
		
			choice = show_alert(
				preview,
				buttons=YES | ABORT,
				)
			if choice == ABORT:
				return

		iteateFilesForRename(paths, baseFilename, digitLength, url, True)
		self.pane.clear_selection() 
			
class PowerReplace(DirectoryPaneCommand):
	def __call__(self):		
		url = self.pane.get_path() 
		paths = self.pane.get_selected_files()

		if len(paths) < 1:
			show_alert("Please select at least 1 file.")
			return
		
		name = os.path.basename(paths[0])	
		name, ext = os.path.splitext(name)
		replaceString, ok = show_prompt('Please enter the string you want to replace', name)
		if not replaceString and not ok:
			return

		newString, ok = show_prompt('Please enter the new string you want replace ' + replaceString + ' with')
		if not newString and not ok:
			return			

		showPreview = shouldShowPreview(replaceString)
		if(showPreview):			
			replaceString = replaceString[1:]			

		if(showPreview):
			preview = iteateFilesForReplace(paths, replaceString, newString, url, False)
		
			choice = show_alert(
				preview,
				buttons=YES | ABORT,
				)
			if choice == ABORT:
				return

		iteateFilesForReplace(paths, replaceString, newString, url, True)	

		self.pane.clear_selection() 
			

def shouldShowPreview(basefilename):
	if(basefilename[0] == '$'):
		return True
	return False


def iteateFilesForReplace(paths, replaceString, newString, url, replace):	
	preview = ''
	for path in paths:	
		name, ext = os.path.splitext(path)
		name = os.path.basename(path)	

		if(name.find(replaceString) > -1):
			newFilename = name.replace(replaceString, newString)
			
			newPath = url + "/" + newFilename
			preview += name  + ' > ' + newFilename + '\n'
			if exists(newPath):
				preview += "File already exists, will be skipped.\n"
				continue	
			
			if(replace):
				move(path, newPath)

	return preview


def iteateFilesForRename(paths, baseFilename, digitLength, url, rename):	
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

