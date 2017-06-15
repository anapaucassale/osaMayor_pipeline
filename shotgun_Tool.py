import os, sys
from shotgun_api3 import Shotgun 
import os.path
import time
from pprint import pprint

sg = Shotgun('http://upgdl.shotgunstudio.com', 'AP_Script', '5a652f41b496c46d6b968206a5cc6f91e617157020c73c8ca87e5d4b71775051')
#sg = Shotgun('http://upgdl.shotgunstudio.com', login = "anapaucassale", password = "APcassale.13")
global inputType, goodID, savedVersions
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
			userInputID = raw_input("ERROR - ID must be a number.\nType in the %s's ID:\n" %inputType)

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
		print v['code']

def asignName(inputName):
	global savedVersions
	global codeToUpload
	for v in savedVersions:
		if(inputName.lower() in v['code'].lower()):
			codeToUpload = v['code']
	if (codeToUpload == None):
		codeToUpload = inputName + "_v001"
	else:
		codeToUpload = codeToUpload[:len(codeToUpload) - 4] + ('_v%03d' %(int(codeToUpload[len(codeToUpload) - 3:])+ 1))


def createShot(id, code, taskType):
    data = {
        'project': {"type": "Project","id": id},
        'code': code,
        'description': 'Open on a beautiful field with fuzzy bunnies',
        'sg_status_list': 'ip'
    }
    result = sg.create(taskType, data)
    pprint(result)
    print "The id of the %s is %d." % (result['type'], result['id'])

def uploadContent(mediaPath, mediaName):
	print goodID
	sg.upload('Version', goodID, mediaPath, display_name = mediaName)

'''
user_action = raw_input("Type what you want to upload?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's ID:\n" %inputType)
goodID = validateID(ID)
shotgunInfo = validateIDShotgun(goodID)'''

projectName = raw_input('Type in the name of the project you want to create a shot in:\n')
projectID = raw_input("Type in %s's ID:\n" %projectName)
goodID = validateID(projectID)
user_action = raw_input("Type what you want to create?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
code = raw_input("Type in %s's name:\n" %inputType)


createShot(goodID, code, inputType)


'''
mediaFile = '/Users/anapau/Desktop/IMG_7327.JPG'
#mediaFile = raw_input("Type in the PATH of media to upload:\n")
uploadContent(mediaFile, 'AP_v001')'''

'''checkVersionsSG()
asignName(raw_input("\nType de NAME to asign to your %s \n" %inputType))
print codeToUpload'''

print 'Data correct'
time.sleep(5)

