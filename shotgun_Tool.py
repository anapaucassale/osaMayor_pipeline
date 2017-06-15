import os, sys
from shotgun_api3 import Shotgun 
import os.path
import time

sg = Shotgun('http://upgdl.shotgunstudio.com', 'AP_Script', '5a652f41b496c46d6b968206a5cc6f91e617157020c73c8ca87e5d4b71775051')
global inputType, goodID


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
	fields = ['id', 'code']
	filters = [['entity', 'is', {'type': inputType, 'id': goodID}]]
	#versions = sg.find("Version", [["id","is", validatedID]], ['code'])
	versions = sg.find("Version", filters, fields)

	print "The versions in this %s are:\n" %inputType
	for v in versions:
		print v['code']

#def create

user_action = raw_input("Type what you want to upload?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's ID:\n" %inputType)
goodID = validateID(ID)
shotgunInfo = validateIDShotgun(goodID)

checkVersionsSG()


print 'Data correct'
time.sleep(5)

