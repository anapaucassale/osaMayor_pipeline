import os, sys
from shotgun_api3 import Shotgun 
import os.path
import time
from pprint import pprint

#sg = Shotgun('http://upgdl.shotgunstudio.com', 'AP_Script', '5a652f41b496c46d6b968206a5cc6f91e617157020c73c8ca87e5d4b71775051')
sg = Shotgun('http://upgdl.shotgunstudio.com', login = 'anapaucassale', password = 'APcassale.13')
#global inputType, goodID, projectID, goodProjectID, savedVersions
#codeToUpload = None

class shotgunTool():

	# Initialize global variables
	def __init__(self):
		#self.inputType = None
		#self.validatedID = None
		#self.projectID = None
		#self.validatedProjectID = None
		self.savedVersions = None
		self.codeToUpload = None
	
	# Validate the type the user typed in
	# It can be an ASSET or a SHOT
	def validateType(self, user_type):
		isTypeValidated = False
		while (isTypeValidated == False):
			if (user_type == 'asset' or user_type == 'a'):
				return 'Asset'
				#self.inputType = 'Asset'
				#isTypeValidated = True
			elif (user_type == 'shot' or user_type == 's'):
				return 'Shot'
				#self.inputType = 'Shot'
				#isTypeValidated = True
			else:
				user_type= raw_input("\nERROR - Invalid input. Try again\nWhat do you want to upload?\n-> Asset\n-> Shot\n").lower()

	# Validate the ID the user input
	def validateID(self, user_ID):
		isIDvalidated = False
		while (isIDvalidated == False):
			try:
				user_ID = int(user_ID)
				return user_ID
				#self.validatedID = user_ID
				#isIDvalidated = True
			except:
				user_ID = raw_input("ERROR - ID must be a number.\nType in the correct ID:\n")

	# Determine if the user's ID is an existing ID in shotgun
	def validateID_inShotgun(self, inputType, sg_ID):
		isValidated = False
		while (isValidated == False):
			shotgunFile = sg.find_one(inputType, [["id", "is", sg_ID]], ["id", "code", "sg_status_list"])
			if (shotgunFile == None):
				newID = raw_input("ERROR - No %s with ID %s found on the project.\nType in the correct ID:\n" % (inputType, sg_ID))
				sg_ID = self.validateID(newID)
			else:
				print "The founded %s's name is: %s" %(inputType, shotgunFile['code'])
				isValidated = True
				return shotgunFile

	# Check and return the given Type's (Shot or asset) versions in shotgun
	def checkVersionsSG(self, inputType, validatedID):
		#global savedVersions, codeToUpload
		fields = ['id', 'code']
		filters = [['entity', 'is', {'type': inputType, 'id':validatedID}]]
		versions = sg.find("Version", filters, fields)
		self.savedVersions = versions
		print "The versions in this %s are:" %inputType
		for v in versions:
			print 'VERSION: %s | ID: %d' % (v['code'], v['id'])

	# Asign name to content
	def asignName(self):
		#global savedVersions
		#global codeToUpload
		user_action = raw_input("Type what you want to upload?\n-> Asset\n-> Shot\n").lower()
		inputType = validateType(user_action)
		ID = raw_input("Type in %s's ID:\n" %projectName)
		validatedID = self.validateID(ID)
		shotgunInfo = validateIDShotgun(validatedID)
		  
		checkVersionsSG(inputType, validatedID)
		#asignName(raw_input("\nType de NAME to asign to your %s \n" %inputType))
		user_newName = raw_input("\nType de new name to asign to your %s: \n" %inputType)
		for v in self.savedVersions:
			if(user_newName.lower() in v['code'].lower()):
				self.codeToUpload = v['code']
		if (self.codeToUpload == None):
			self.codeToUpload = user_newName + "_v001"
			updateContent(validatedID, self.codeToUpload, inputType)
		else:
			self.codeToUpload = self.codeToUpload[:len(self.codeToUpload) - 4] + ('_v%03d' %(int(self.codeToUpload[len(self.codeToUpload) - 3:])+ 1))
			updateContent(validatedID, self.codeToUpload, inputType)

		print self.codeToUpload

	#Create a shot or an asset whithin a project in shotgun
	def createContent(self):
		projectName = raw_input('Type in the name of the project you want to create a shot in:\n')
		projectID = raw_input("Type in %s's ID:\n" %projectName)
		#self.validatedProjectID = validateID(projectID)
		validatedProjectID = self.validateID(projectID)
		user_action = raw_input("Type what you want to create?\n-> Asset\n-> Shot\n").lower()
		#self.inputType = validateType(user_action)
		inputType = self.validateType(user_action)
		type_name = raw_input("Type in %s's name:\n" %inputType)
		type_description = raw_input("Write a description for the %s:\n" %inputType)
		
		data = {
			'project': {"type": "Project","id": validatedProjectID},
			'code': type_name,
			'description': type_description,
			'sg_status_list': 'ip'
		}
		result = sg.create(inputType, data)
		print "The id of the %s is %d." % (result['type'], result['id'])
		#result = sg.create(inputType, data)
		#pprint(result)
		

	# Create a new version within an asset or a shot
	def createVersion(self):

		projectName = raw_input('Type in the name of the project you want to create a shot in:\n')
		projectID = raw_input("Type in %s's ID:\n" %projectName)
		#self.goodProjectID = validateID(projectID)
		validatedProjectID = self.validateID(projectID)
		#validateID(projectID)
		user_action = raw_input("Where do you wanna create a new version?\n-> Asset\n-> Shot\n").lower()
		inputType = self.validateType(user_action)
		#alidateType(user_action)
		ID = raw_input("Type in the %s's ID:\n" %inputType)
		validatedID = self.validateID(ID)
		#validateID(ID)
		version_name = raw_input("Type in %s's version name:\n" %inputType)
		version_description = raw_input("Type in %s's description:\n" %inputType)

		data = { 'project': {'type': 'Project','id': validatedProjectID},
			 'code': version_name,
			 'description': version_description,
			 #'sg_path_to_movie': mediaPath,
			 'sg_status_list': 'rev',
			 'entity': {'type': inputType, 'id': validatedID}
			 #'sg_task': {'type': 'Task', 'id': task['id']},
			 #'user': {'type': 'HumanUser', 'id': 165} 
			 }
		result = sg.create('Version', data)
		isMediaDefined = False
		uploadMedia = raw_input("Do you want to upload a video? (Y/N):\n").lower()
		while (isMediaDefined == False):
			if(uploadMedia == 'yes' or uploadMedia == 'y'):
				mediaFile = raw_input("Type in the path of the media to upload:\n")
				print 'Be patient, it can take a while...'
				self.uploadContent(result['id'], mediaFile)
				isMediaDefined = True
			elif(uploadMedia == 'no' or uploadMedia == 'n'):
				print '%s created without a video upload.' %version_name
				isMediaDefined = True
			else:
				uploadMedia = raw_input("ERROR - Invalid Input.\n Do you want to upload a video? (Y/N):\n" %inputType).lower()
		#'/Users/anapau/Desktop/Leak.mov'
	
	# Delete content from shotgun
	def deleteContent(self):
		user_action = raw_input("What do you want to delete?\n-> Asset\n-> Shot\n").lower()
		inputType = self.validateType(user_action)
		ID = raw_input("Type in the %s's ID:\n" %inputType)
		validatedID = self.validateID(ID)
		result = sg.delete(inputType, validatedID)
		print 'The %s has been deleted succesfully' %inputType

	# Update name from existing content
	def updateContent(self):
		user_action = raw_input("What you want to update?\n-> Asset\n-> Shot\n").lower()
		inputType = self.validateType(user_action)
		ID = raw_input("Type in %s's ID:\n" %inputType)
		validatedID = self.validateID(ID)
		shotgunInfo = self.validateID_inShotgun(inputType, validatedID)
		  
		#self.checkVersionsSG(inputType, validatedID)
		user_newName = raw_input("\nType de new name to asign to your %s: \n" %inputType)
		new_name = None
		for v in self.savedVersions:
			if(user_newName.lower() in v['code'].lower()):
				new_name = v['code']
		
		if (new_name == None):
			new_name = user_newName + "_v001"
		else:
			new_name = new_name[:len(new_name) - 4] + ('_v%03d' %(int(new_name[len(new_name) - 3:])+ 1))	
		data = {
			'code': new_name,
			#'description': ' ',
			'sg_status_list': 'ip'
		}
		result = sg.update(inputType, validatedID, data)
		print new_name

	# Upload media to existing content
	def uploadContent(self, ID, mediaPath):
		user_action = raw_input("Where do you want to upload your video?\n-> Asset\n-> Shot\n").lower()
		inputType = self.validateType(user_action)
		ID = raw_input("Type in the %s's VERSION ID:\n" %inputType)
		validatedID = self.validateID(ID)
		mediaFile = '/Users/anapau/Desktop/Leak.mov'
		self.checkVersionsSG(inputType, validatedID)
		versionID = raw_input("Type in the ID of the version where you want to upload your video:\n")
		validatedVersionID = self.validateID(versionID)
		#uploadContent(validatedVersionID, mediaFile)
		#sg.upload('Version', ID, mediaPath, display_name = mediaName)
		result = sg.upload("Version", validatedVersionID, mediaFile, field_name = "sg_uploaded_movie", display_name="Latest QT")
		print 'Uploaded succesfully'
		
sg_info = shotgunTool()

#sg_info.createContent()
#sg_info.createVersion()
#sg_info.deleteContent()
sg_info.updateContent()


'''def validateType(userInputType):
	validationType = False
	while (validationType == False):
		if (userInputType == 'asset' or userInputType == 'a'):
			#validationType = True
			return 'Asset'
		elif (userInputType == 'shot' or userInputType == 's'):
			#validationType = True
			return 'Shot'
		else:
			userInputType = raw_input("ERROR - Invalid input. Try again\nWhat do you want to upload?\n-> Asset\n-> Shot\n").lower()'''

'''def validateID(userInputID):
	validationNum = False
	while (validationNum == False):
		try:
			userInputID = int(userInputID)
			#validationNum = True
			return userInputID
		except:
			userInputID = raw_input("ERROR - ID must be a number.\nType in the correct ID:\n")'''

'''def validateIDShotgun(validatedID):
	shotgunVal = False
	while (shotgunVal == False):
		shotgunFile = sg.find_one(inputType, [["id", "is", validatedID]], ["id", "code", "sg_status_list"])
		if (shotgunFile == None):
			newID = raw_input("ERROR - No %s with ID %s found on the project.\nType in the correct ID:\n" % (inputType, validatedID))
			validatedID = validateID(newID)
		else:
			print "The founded %s's name is: %s" %(inputType, shotgunFile['code'])
			shotgunVal = True
			return shotgunFile'''

'''def checkVersionsSG():
	global savedVersions, codeToUpload
	fields = ['id', 'code']
	filters = [['entity', 'is', {'type': inputType, 'id': goodID}]]
	#versions = sg.find("Version", [["id","is", validatedID]], ['code'])
	versions = sg.find("Version", filters, fields)
	savedVersions = versions
	#colectedVersions = sg.find("Version", filters, fields)
	#colectedVersions = versions
	print "The versions in this %s are:" %inputType
	for v in versions:
		#colectedVersions.append(v['code'])
		print 'VERSION: %s y su ID es: %d' % (v['code'], v['id'])'''

'''def asignName(inputName):
	global savedVersions
	global codeToUpload
	for v in savedVersions:
		if(inputName.lower() in v['code'].lower()):
			codeToUpload = v['code']
	if (codeToUpload == None):
		codeToUpload = inputName + "_v001"
		updateContent(goodID, codeToUpload, inputType)
	else:
		codeToUpload = codeToUpload[:len(codeToUpload) - 4] + ('_v%03d' %(int(codeToUpload[len(codeToUpload) - 3:])+ 1))
		updateContent(goodID, codeToUpload, inputType)'''

'''def createContent(id, code, taskType, description):
	data = {
		'project': {"type": "Project","id": id},
		'code': code,
		'description': description,
		'sg_status_list': 'ip'
	}
	result = sg.create(taskType, data)
	pprint(result)
	print "The id of the %s is %d." % (result['type'], result['id'])'''

'''def createVersion(inType, ID, code, actionID, mediaPath, description):
	data = { 'project': {'type': 'Project','id': ID},
		 'code': code,
		 'description': description,
		 #'sg_path_to_movie': mediaPath,
		 'sg_status_list': 'rev',
		 'entity': {'type': inType, 'id': actionID}
		 #'sg_task': {'type': 'Task', 'id': task['id']},
		 #'user': {'type': 'HumanUser', 'id': 165} 
		 }
	result = sg.create('Version', data)
	uploadContent(result['id'], mediaPath)'''

'''def deleteContent(inpType, inputID):
	result = sg.delete(inpType, inputID)
	print 'The %s has been deleted succesfully' %inpType'''

'''def updateContent(contentID, code, inputType, description):
	global savedVersions
	global codeToUpload
	for v in savedVersions:
		if(inputName.lower() in v['code'].lower()):
			codeToUpload = v['code']
	if (codeToUpload == None):
		codeToUpload = inputName + "_v001"
		#updateContent(goodID, codeToUpload, inputType)
	else:
		codeToUpload = codeToUpload[:len(codeToUpload) - 4] + ('_v%03d' %(int(codeToUpload[len(codeToUpload) - 3:])+ 1))
	
	data = {
		'code': codeToUpload,
		'description': ' ',
		'sg_status_list': 'ip'
	}
	result = sg.update(inputType, goodID, data)
	#result = sg.update(taskType, contentID, data)
	#result = sg.update(taskType, contentID, data)
	#pprint(result)'''

'''def uploadContent(ID, mediaPath):
	#sg.upload('Version', ID, mediaPath, display_name = mediaName)
	result = sg.upload("Version", ID, mediaPath, field_name = "sg_uploaded_movie", display_name="Latest QT")
	print 'Uploaded succesfully'''


# UPLOAD CONTENT
'''
user_action = raw_input("Where do you want to upload your video?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's VERSION ID:\n" %inputType)
goodID = validateID(ID)
mediaFile = '/Users/anapau/Desktop/Leak.mov'
checkVersionsSG()
versionID = raw_input("Type in the ID of the version where you want to upload your video:\n")
goodVersionID = validateID(versionID)
uploadContent(goodVersionID, mediaFile)
'''

# DELETE CONTENT
'''
user_action = raw_input("What do you want to delete?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's ID:\n" %inputType)
goodID = validateID(ID)

deleteContent(inputType, goodID)
'''

#shotgunInfo = validateIDShotgun(goodID)

# CERATE A NEW VERSION WITHIN A SHOT OR AN ASSET
'''
projectName = raw_input('Type in the name of the project you want to create a shot in:\n')
projectID = raw_input("Type in %s's ID:\n" %projectName)
goodProjectID = validateID(projectID)
user_action = raw_input("Where do you wanna create a new version?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's ID:\n" %inputType)
goodID = validateID(ID)
#shotgunInfo = validateIDShotgun(goodID)
code = raw_input("Type in %s's version name:\n" %inputType)
mediaFile = '/Users/anapau/Desktop/Leak.mov'
desc = raw_input("Type in %s's description:\n" %inputType)
#uploadContent(goodVersionID, mediaFile)
createVersion(inputType, goodProjectID, code, goodID, mediaFile, desc)
'''


# CREATE A SHOT OR AN ASSET
'''
user_action = raw_input("Type what you want to upload?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's ID:\n" %inputType)
goodID = validateID(ID)
shotgunInfo = validateIDShotgun(goodID)
checkVersionsSG()
newName = asignName(raw_input("\nType de NAME to asign to your %s \n" %inputType))
print codeToUpload
'''

'''
user_action = raw_input("Type what you want to upload?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's ID:\n" %inputType)
goodID = validateID(ID)
shotgunInfo = validateIDShotgun(goodID)
'''

# CREATE NEW ASSET OR SHOT 
'''
projectName = raw_input('Type in the name of the project you want to create a shot in:\n')
projectID = raw_input("Type in %s's ID:\n" %projectName)
goodID = validateID(projectID)
user_action = raw_input("Type what you want to create?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
code = raw_input("Type in %s's name:\n" %inputType)

createContent(goodID, code, inputType)
'''

'''
mediaFile = '/Users/anapau/Desktop/IMG_7327.JPG'
#mediaFile = raw_input("Type in the PATH of media to upload:\n")
uploadContent(mediaFile, 'AP_v001')'''

'''checkVersionsSG()
asignName(raw_input("\nType de NAME to asign to your %s \n" %inputType))
print codeToUpload'''

print 'Data correct'
time.sleep(5)

