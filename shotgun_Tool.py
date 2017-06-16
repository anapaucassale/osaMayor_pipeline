import os, sys
from shotgun_api3 import Shotgun 
import os.path
import time
from pprint import pprint

sg = Shotgun('http://upgdl.shotgunstudio.com', 'AP_Script', '5a652f41b496c46d6b968206a5cc6f91e617157020c73c8ca87e5d4b71775051')
#upload_movie: yes
global inputType, goodID, projectID, goodProjectID, savedVersions
codeToUpload = None
#colectedVersions = None

def validateType(userInputType):
	validationType = False
	while (validationType == False):
		if (userInputType == 'asset' or userInputType == 'a'):
			#validationType = True
			return 'Asset'
		elif (userInputType == 'shot' or userInputType == 's'):
			#validationType = True
			return 'Shot'
		else:
			userInputType = raw_input("ERROR - Invalid input. Try again\nWhat do you want to upload?\n-> Asset\n-> Shot\n").lower()

def validateID(userInputID):
	validationNum = False
	while (validationNum == False):
		try:
			userInputID = int(userInputID)
			#validationNum = True
			return userInputID
		except:
			userInputID = raw_input("ERROR - ID must be a number.\nType in the correct ID:\n")

def validateIDShotgun(validatedID):
	shotgunVal = False
	while (shotgunVal == False):
		shotgunFile = sg.find_one(inputType, [["id", "is", validatedID]], ["id", "code", "sg_status_list"])
		if (shotgunFile == None):
			newID = raw_input("ERROR - No %s with ID %s found on the project.\nType in the correct ID:\n" % (inputType, validatedID))
			validatedID = validateID(newID)
		else:
			print "The founded %s's name is: %s" %(inputType, shotgunFile['code'])
			shotgunVal = True
			return shotgunFile

def checkVersionsSG():
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
		print 'VERSION: %s y su ID es: %d' % (v['code'], v['id'])

def asignName(inputName):
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
		updateContent(goodID, codeToUpload, inputType)

def createContent(id, code, taskType):
    data = {
        'project': {"type": "Project","id": id},
        'code': code,
        'description': 'Open on a beautiful field with fuzzy bunnies',
        'sg_status_list': 'ip'
    }
    result = sg.create(taskType, data)
    pprint(result)
    print "The id of the %s is %d." % (result['type'], result['id'])

def createVersion(ID, code, actionID, mediaPath, description):
	data = { 'project': {'type': 'Project','id': ID},
         'code': code,
         'description': description,
         #'sg_path_to_movie': mediaPath,
         'sg_status_list': 'rev',
         'entity': {'type': 'Shot', 'id': actionID}
         #'sg_task': {'type': 'Task', 'id': task['id']},
         #'user': {'type': 'HumanUser', 'id': 165} 
         }
	result = sg.create('Version', data)
	uploadContent(result['id'], mediaPath)

def deleteContent(inpType, inputID):
	result = sg.delete(inpType, inputID)
	print 'The %s has been deleted succesfully' %inpType

def updateContent(contentID, code, inputType):
	data = {
		'code': code,
		'description': 'Updating...',
        'sg_status_list': 'ip'
	}
	result = sg.update(inputType, contentID, data)
    #result = sg.update(taskType, contentID, data)
    #result = sg.update(taskType, contentID, data)
    #pprint(result)

def uploadContent(ID, mediaPath):
	#sg.upload('Version', ID, mediaPath, display_name = mediaName)
	result = sg.upload("Version", ID, mediaPath, field_name = "sg_uploaded_movie", display_name="Latest QT")
	print 'Uploaded succesfully'


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
createVersion(goodProjectID, code, goodID, mediaFile, desc)



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

