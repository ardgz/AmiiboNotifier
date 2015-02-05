from bs4 import BeautifulSoup
import urllib
import urllib2
import sys
import re
import os

def connectAndRetrieveData(zipStr, dcpiStr):
	url = 'http://brickseek.com/target-inventory-checker'
	data = {
		'zip': zipStr,
		'dcpi': dcpiStr
	}
	req = urllib2.Request(url, 
						  data = urllib.urlencode(data)
						  )	
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.code
	except urllib2.URLError, e:
		print e.args	
	else:
		html = response.read()
		soup = BeautifulSoup(html)
		table_code = soup.table
		
		tags_list = []
		
		for item in table_code:
			if len(item.contents) != 1:
				tags_list.append(str(item))
				
		strings_list = []
		
		for tag in tags_list:
			aString = re.sub(r'<tr><td style=""><b>', "", tag) #checked
			aString = re.sub(r'\s<a.*?></a>', "", aString)
			aString = re.sub(r'</a><a class.*?></a>', "", aString)
			aString = re.sub(r'</b><br/>', " | ", aString) 
			aString = re.sub(r'<br>', " | ", aString)
			aString = re.sub(r'<br/>', " | ", aString)
			aString = re.sub(r'</br></td><td><b>', " | ", aString)
			aString = re.sub(r'</b><a style="color:red">|</b><a style="color:green">', "", aString)
			aString = re.sub(r'<b>', "", aString)
			aString = re.sub(r'<b>', "", aString)
			aString = re.sub(r'</b>', "", aString)
			aString = re.sub(r'</b>', "", aString)
			aString = re.sub(r'</td></tr>', "", aString)
			strings_list.append(aString)
		
		targetStoreList = []
		
		for string in strings_list:
			storeDataList = string.split(' | ')
			targetStoreList.append(storeDataList)
			
		email_body = analyzeStoreStock(targetStoreList, dcpiStr)
		return email_body
		
def analyzeStoreStock(targetStoreList, dcpiStr):
	email_body = ""
	for storeData in targetStoreList:
		if "Yes" in storeData[4]:
			amiibo_name = getAmiiboName(dcpiStr)
			email_body = prepareEmailStoreData(storeData, amiibo_name, email_body)
	return email_body

def getAmiiboName(dcpiStr):
	if dcpiStr == '207-00-5001':
		return 'Mario'
	elif dcpiStr == '207-00-5002':
		return 'Pikachu'
	elif dcpiStr == '207-00-5003':
		return 'Link'
	elif dcpiStr == '207-00-5004':
		return 'Peach'
	elif dcpiStr == '207-00-5005':
		return 'Yoshi'
	elif dcpiStr == '207-00-5006':
		return 'Donkey Kong'
	elif dcpiStr == '207-00-5007':
		return 'Kirby'
	elif dcpiStr == '207-00-5008':
		return 'Villager'
	elif dcpiStr == '207-00-5009':
		return 'Fox'
	elif dcpiStr == '207-00-5010':
		return 'Samus'
	elif dcpiStr == '207-00-5011':
		return 'Marth'
	elif dcpiStr == '207-00-5012':
		return 'Wii Fit Trainer'
	elif dcpiStr == '207-00-5013':
		return 'Luigi'
	elif dcpiStr == '207-00-5014':
		return 'Zelda'
	elif dcpiStr == '207-00-5015':
		return 'Little Mac'
	elif dcpiStr == '207-00-5016':
		return 'Diddy Kong'
	elif dcpiStr == '207-00-5017':
		return 'Pit'
	elif dcpiStr == '207-00-5018':
		return 'Captain Falcon'
	elif dcpiStr == '207-00-5019':
		return 'Toon Link'
	elif dcpiStr == '207-00-5020':
		return 'Bowser'
	elif dcpiStr == '207-00-5021':
		return 'Rosalina & Luma'
	elif dcpiStr == '207-00-5022':
		return 'Mega Man'
	elif dcpiStr == '207-00-5023':
		return 'Sonic'
	elif dcpiStr == '207-00-5024':
		return 'Sheik'
	elif dcpiStr == '207-00-5025':
		return 'King Dedede'
	elif dcpiStr == '207-00-5026':
		return 'Ike'

def getAmiiboDCPI(amiiboName):
	if amiiboName == 'Mario':
		return '207-00-5001'
	if amiiboName == 'Pikachu':
		return '207-00-5002'
	if amiiboName == 'Link':
		return '207-00-5003'
	if amiiboName == 'Peach':
		return '207-00-5004'
	if amiiboName == 'Yoshi':
		return '207-00-5005'
	if amiiboName == 'Donkey Kong':
		return '207-00-5006'
	if amiiboName == 'Kirby':
		return '207-00-5007'
	if amiiboName == 'Villager':
		return '207-00-5008'
	if amiiboName == 'Fox':
		return '207-00-5009'
	if amiiboName == 'Samus':
		return '207-00-5010'
	if amiiboName == 'Marth':
		return '207-00-5011'
	if amiiboName == 'Wii Fit Trainer':
		return '207-00-5012'
	if amiiboName == 'Luigi':
		return '207-00-5013'
	if amiiboName == 'Zelda':
		return '207-00-5014'
	if amiiboName == 'Little Mac':
		return '207-00-5015'
	if amiiboName == 'Diddy Kong':
		return '207-00-5016'
	if amiiboName == 'Pit':
		return '207-00-5017'
	if amiiboName == 'Captain Falcon':
		return '207-00-5018'
	if amiiboName == 'Toon Link':
		return '207-00-5019'
	if amiiboName == 'Bowser':
		return '207-00-5020'
	if amiiboName == 'Rosalina & Luma':
		return '207-00-5021'
	if amiiboName == 'Mega Man':
		return '207-00-5022'
	if amiiboName == 'Sonic':
		return '207-00-5023'
	if amiiboName == 'Sheik':
		return '207-00-5024'
	if amiiboName == 'King Dedede':
		return '207-00-5025'
	if amiiboName == 'Ike':
		return '207-00-5026'

def prepareEmailStoreData(targetStore, amiibo_name, email_body):
	email_body += "AMIIBO: " + amiibo_name + '\n'
	email_body +=  "Store Name: " + targetStore[0] + '\n'
	email_body +=  "Address: " + targetStore[1] + '\n'
	email_body += "Phone Number: " + targetStore[2] + '\n'
	email_body += "Distance: " + targetStore[3] + '\n'
	email_body += targetStore[4] + '\n'
	email_body += targetStore[5] + '\n'
	email_body += targetStore[6] + '\n'
	email_body += "==================================\n"
	return email_body

reload(sys)
sys.setdefaultencoding("utf-8")

# ======================================================
# ======================================================

def targetInventory(amiiboNameList, ZIP_CODE):
	dcpi_list = []
	for amiiboName in amiiboNameList:
		amiibo_dcpi = getAmiiboDCPI(amiiboName)
		dcpi_list.append(amiibo_dcpi)
	
	email_body = ''
	for dcpi in dcpi_list:
		email_body += connectAndRetrieveData(ZIP_CODE, dcpi)
	
	return email_body