from Tkinter import *
import os

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
	
class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.master.title("Amiibo Notifier")
		self.buildInterface(self.master)
		
	
	def buildInterface(self, master):
		self.amiiboList = self.setVariables()
		
		self.buildLabelFrames(master)
		self.buildInput(master)
		
	def buildLabelFrames(self, master):
		i = 0
		currentRow = 0
		currentColumn = 0
		
		waveOneLabelFrame = LabelFrame(master, text='Wave 1', padx=5, pady=5)
		waveOneLabelFrame.grid()
		self.populateFrame(waveOneLabelFrame, i, self.numWaveOne)
		i += self.numWaveOne
		
		waveTwoLabelFrame = LabelFrame(master, text='Wave 2', padx=5, pady=5)
		waveTwoLabelFrame.grid()
		self.populateFrame(waveTwoLabelFrame, i, self.numWaveTwo)
		i += self.numWaveTwo
		
		waveThreeLabelFrame = LabelFrame(master, text='Wave 3', padx=5, pady=5)
		waveThreeLabelFrame.grid()
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
							'Mega Man', 'King Dedede', 'Ike']
		
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
		inputLabelFrame = LabelFrame(master, text='Gmail notification', padx=5, pady=5)
		inputLabelFrame.grid()
		
		emailLabel = Label(inputLabelFrame, text='Gmail address:', justify=LEFT, anchor=W, padx=5)
		emailLabel.grid(row=0, column=0, sticky=W)
		Entry(inputLabelFrame).grid(row=0, column=1)
		
		passwordLabel = Label(inputLabelFrame, text='Password:', justify=LEFT, anchor=W, padx=5)
		passwordLabel.grid(row=1, column=0, sticky=W)
		Entry(inputLabelFrame, show='*').grid(row=1, column=1)
		
		b = Button(master, text='Run Amiibo Notifier', width=30, command=self.testFunction)
		b.grid()
		
	def testFunction(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		for amiibo in self.amiiboList:
			print amiibo.getName(), amiibo.getVarValue()
			
if __name__ == '__main__':
	root = Tk()
	app = Application(root)
	app.mainloop()