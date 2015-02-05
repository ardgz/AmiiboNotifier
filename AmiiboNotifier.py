from Tkinter import *
import os
import sys
import mandrill
import Queue
import threading
import time
import targetInventory

class Amiibo:
	def __init__(self, name):
		self.name = name
		self.var = IntVar()
	def getName(self):
		return self.name
	def getVar(self):
		return self.var
	def getVarValue(self):
		return self.var.get()
		
class TextRedirector(object):
	def __init__(self, widget, tag="stdout"):
		self.widget = widget
		self.tag = tag
	def write(self, str):
		self.widget.configure(state="normal")
		self.widget.insert("end", str, (self.tag,))
		self.widget.configure(state="disabled")
	
class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.master.title("Amiibo Notifier")
		self.buildInterface(self.master)
		sys.stdout = TextRedirector(self.outputBox, "stdout")
		sys.stderr = TextRedirector(self.outputBox, "stderr")
		self.processRunning = False
	
	def buildInterface(self, master):
		self.amiiboList = self.setVariables()
		self.buildLabelFrames(master)
		self.buildInput(master)
		self.buildOutput(master)
		
	def buildLabelFrames(self, master):
		i = 0
		currentRow = 0
		currentColumn = 0
		
		waveOneLabelFrame = LabelFrame(master, text='Wave 1', padx=5, pady=5)
		waveOneLabelFrame.grid(sticky=W+E, padx=5)
		self.populateFrame(waveOneLabelFrame, i, self.numWaveOne)
		i += self.numWaveOne
		
		waveTwoLabelFrame = LabelFrame(master, text='Wave 2', padx=5, pady=5)
		waveTwoLabelFrame.grid(sticky=W+E, padx=5)
		self.populateFrame(waveTwoLabelFrame, i, self.numWaveTwo)
		i += self.numWaveTwo
		
		waveThreeLabelFrame = LabelFrame(master, text='Wave 3', padx=5, pady=5)
		waveThreeLabelFrame.grid(sticky=W+E, padx=5)
		self.populateFrame(waveThreeLabelFrame, i, self.numWaveThree)
		
	def populateFrame(self, labelFrame, i, waveSize):
		currentColumn = 0
		currentRow = 0
		for index in range(waveSize):
			if currentColumn >= 3:
				currentColumn = 0
				currentRow += 1
			
			c = Checkbutton(labelFrame, text=self.amiiboList[i].getName(), var=self.amiiboList[i].getVar())
			c.grid(row=currentRow, column=currentColumn, sticky=W)
			currentColumn += 1
			i += 1
			
	def setVariables(self):
		waveOneAmiibos = ['Mario', 'Link', 'Samus', 'Kirby',
					'Fox', 'Donkey Kong', 'Pikachu', 'Peach',
					'Marth', 'Yoshi', 'Villager', 'Wii Fit Trainer']
		waveTwoAmiibos = ['Diddy Kong', 'Zelda', 'Luigi', 'Captain Falcon',
							'Pit', 'Little Mac']
		waveThreeAmiibos = ['Bowser', 'Toon Link', 'Sheik', 'Sonic',
							'Mega Man', 'King Dedede', 'Ike', 'Rosalina & Luma']
		
		allAmiibos = []
		for i in range(len(waveOneAmiibos)):
			allAmiibos.append(Amiibo(waveOneAmiibos[i]))
		for i in range(len(waveTwoAmiibos)):
			allAmiibos.append(Amiibo(waveTwoAmiibos[i]))
		for i in range(len(waveThreeAmiibos)):
			allAmiibos.append(Amiibo(waveThreeAmiibos[i]))
			
		self.numWaveOne = len(waveOneAmiibos)
		self.numWaveTwo = len(waveTwoAmiibos)
		self.numWaveThree = len(waveThreeAmiibos)
		
		return allAmiibos
	
	def buildInput(self, master):
		# Create Input Label Frame
		inputLabelFrame = LabelFrame(master, text='Email notification', padx=5, pady=5)
		inputLabelFrame.grid(sticky=W+E, padx=5)
		
		# Create Email Label
		emailLabel = Label(inputLabelFrame, text='Email:', justify=LEFT, anchor=W, padx=5)
		emailLabel.grid(row=0, column=0, sticky=W)
		
		# Create Email Field
		self.email = Entry(inputLabelFrame, width='33')
		self.email.grid(row=0, column=1)
		
		# Create Zip Code Frame
		zipCodeFrame = LabelFrame(master, text='Area Search', padx=5, pady=5)
		zipCodeFrame.grid(sticky=W+E, padx=5)
		
		# Create Zip Code Label
		zipLabel = Label(zipCodeFrame, text='Zip Code:', justify=LEFT, anchor=W, padx=5)
		zipLabel.grid(row=0, column=0, sticky=W)
		
		# Create Zip Code Field
		self.zip = Entry(zipCodeFrame, width='6')
		self.zip.grid(row=0, column=1)
		
		# Create Button Frame
		buttonFrame = Frame(master, padx=5, pady=5)
		buttonFrame.grid(sticky=W+E)
		
		# Create Buttons
		self.amiiboButton = Button(buttonFrame, text='Run Amiibo Notifier', width=25, command=self.amiiboNotifierFunction) #command = self.testFunction
		self.amiiboButton.grid(row=0, padx=10)
		self.stopButton = Button(buttonFrame, text='Stop', width=6, command=self.stopFunction)
		self.stopButton.grid(row=0, column=1, padx=20)
		
	def buildOutput(self, master):
		self.outputBox = Text(master, wrap='word', state='disabled', width=40)
		self.outputBox.grid(row=1, column=1, rowspan=5, pady=10, padx=10)
		
	def emailTask(self, stop_event):
		while(not stop_event.is_set()):
			# Make outputBox editable and clear contents
			self.outputBox.config(state='normal')
			self.outputBox.delete("1.0", END)
			
			# Disable button for now
			self.amiiboButton.config(state='disabled')
			
			# Check if required correct data is given
			completeDataFlag = self.validateData()
			if not completeDataFlag:
				self.amiiboButton.config(state='normal')
				self.processRunning = False
				return
			
			# Process data
			toEmailAddress = self.email.get()
			fromEmailAddress = 'amiiboalert@gmail.com'
			fromName = 'Amiibo Alert'
			emailSubject = 'Amiibo Notification'
			username = toEmailAddress.partition('@')[0]
			zip_code = self.zip.get()
			email_body = ''
			selectedAmiiboNameList = []
			for amiibo in self.amiiboList:
				if amiibo.getVarValue() == 1:
					selectedAmiiboNameList.append(amiibo.getName())		
			print 'Checking Inventory...'
			
			# Initialize message data and add found Amiibo data if any were found in specified area
			email_body = ''		
			email_body += targetInventory.targetInventory(selectedAmiiboNameList, zip_code)	
			
			# open config file to fetch Mandrill API KEY
			config_file = open('config', 'r')  
			API_KEY = config_file.readline().rstrip()
			
			# Send email if message data was successfully generated
			if email_body != '':
				print 'Sending email...'
				try:
					mandrill_client = mandrill.Mandrill(API_KEY)
					message = { 
								'from_name': fromName,
								'from_email': fromEmailAddress,
								'to':[{'email': toEmailAddress}],
								'subject': emailSubject,
								'text': email_body,
								'important': True,
								'track_opens': True,
								'track_clicks': True
							}
					result = mandrill_client.messages.send(message=message)
					
					recipientEmail = result[0]['email']
					# the sending status of the recipient - either "sent", "queued", "scheduled", "rejected", or "invalid"
					status = result[0]['status']
					rejectReason = result[0]['reject_reason']
					
					if status == 'sent':
						print 'Successfully sent email to', recipientEmail
					elif status == 'rejected':
						print 'Email rejected, please try another email address'
					elif status == 'invalid':
						print 'Email is invalid, please provide correct email'
				
				except mandrill.Error, e:
					print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
					# A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
					raise
			else:
				print 'Selected amiibos not found in your area.'
			
			MINUTES = 15  	# Can be changed to a lower amount, but not recommended
							# to avoid overwhelming websites
			SECONDS_IN_MINUTES = 60 # Constant, DO NOT CHANGE
			timeInterval = SECONDS_IN_MINUTES * MINUTES # DO NOT CHANGE
			
			print 'Searching again in', MINUTES, 'minutes.'
			stop_event.wait(timeInterval)
		
		# Mark process as finished
		self.processRunning = False
		
		# Enable button
		self.amiiboButton.config(state='normal')
			
		# Make outputBox noneditable
		self.outputBox.config(state='disabled')
	
	def validateData(self):
		completeDataFlag = True
		
		# Check if required data is given
		selectionCount = 0
		for amiibo in self.amiiboList:
			if amiibo.getVarValue() == 1:
				selectionCount += 1
		
		# Check if any amiibos were selected before proceeding
		if selectionCount == 0:
			print 'No amiibos selected'
			completeDataFlag = False
			
		# Check if email was entered and valid
		if len(self.email.get()) == 0:
			print 'Email not specified'
			completeDataFlag = False
		elif '@' not in self.email.get():
			print 'Email is not valid'
			completeDataFlag = False
		elif '.' not in self.email.get():
			print 'Email is not valid'
			completeDataFlag = False
		
		# Check if zip code is valid
		if len(self.zip.get()) == 0:
			print 'Zipcode not provided'
			completeDataFlag = False
		elif len(self.zip.get().strip()) != 5:
			print 'Zipcode must have only five digits'
			completeDataFlag = False
		elif not self.zip.get().strip().isdigit():
			print 'Zipcode must consist of only digits'
			completeDataFlag = False
			
		return completeDataFlag
		
	def amiiboNotifierFunction(self):
		self.processRunning = True
		self.process_stop = threading.Event()
		self.process = threading.Thread(target=self.emailTask, args=(self.process_stop,))
		self.process.start()
		
	def stopFunction(self):
		if self.processRunning:
			self.process_stop.set()
			print 'Program stopped'
			self.amiiboButton.config(state='normal')
			self.outputBox.config(state='disabled')
		
if __name__ == '__main__':
	root = Tk()
	app = Application(root)
	app.mainloop()