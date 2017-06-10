import os, sys
from shotgun_api3 import Shotgun 
import os.path
import time

sg = Shotgun('http://upgdl.shotgunstudio.com', 'AP_Script', '5a652f41b496c46d6b968206a5cc6f91e617157020c73c8ca87e5d4b71775051')

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
	shotgun_File = sg.find_one(inputType, [["id", "is", validatedID]], ["id", "code"])
	while (shotgunVal == False):



user_action = raw_input("Type what you want to upload?\n-> Asset\n-> Shot\n").lower()
inputType = validateType(user_action)
ID = raw_input("Type in the %s's ID:\n" %inputType)
validateID(ID)

print 'Data correct'
time.sleep(5)

