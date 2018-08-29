import time

class Grid:

	def __init__(self, canvas, master):
		self.canvas = canvas
		self.master = master
		self.canvas.update()
		self.x = self.y = -100, -100	#init
		self.xIndex = self.yIndex = -1
		self.HEIGHT = self.canvas.winfo_height()
		self.WIDTH = self.canvas.winfo_width()
		self.isP1Playing = True			#p1 is red, p2 is blue & p1 starts the game
		self.gameState = []
		self.markIds = []
		self.roundCount = 0
		self.winningMarks = [0, 0, 0, 0]
		for i in range(1, 7):
			self.gameState.append([0]*6)
			self.markIds.append([-1]*6)
			self.canvas.create_line(i*100, 0, i*100, self.HEIGHT, fill = 'white')
			self.canvas.create_line(0, i*100, self.WIDTH, i*100, fill = 'white')
		self.canvas.bind_all("<Button-1>", self.clickEvent)

	def clickEvent(self, event):
		self.x = int(event.x)
		self.y = int(event.y)
		self.xIndex = self.getXIndex()
		self.placeMark()
		self.isP1Playing = not self.isP1Playing
		
		if(self.checkWin()):
			if(self.isP1Playing):
				self.p2Wins()
			else:
				self.p1Wins()
			self.resetBoard()
		self.roundCount += 1
		if(self.roundCount == 36):
			self.draw()
			self.resetBoard()
		
		self.canvas.update()

		#animate

	def getXIndex(self):
		if(self.x - 100 < 0):
			return 0
		if(self.x - 200 < 0):
			return 1
		if(self.x - 300 < 0):
			return 2
		if(self.x - 400 < 0):
			return 3
		if(self.x - 500 < 0):
			return 4
		if(self.x - 600 < 0):
			return 5

	def placeMark(self):
		#final indices [x, y] of the mark -1 for initial
		self.yIndex = self.calculatePosOfMark()
		if(self.yIndex == -1):
			return
		if(self.isP1Playing):
			#self.gameState[self.yIndex][self.xIndex] = 1
			#tmp = self.canvas.create_oval((self.xIndex*100)+20, (self.yIndex*100) +20, (self.xIndex*100)+80, (self.yIndex*100)+80, fill = 'red')
			#self.markIds[self.yIndex][self.xIndex] = tmp

			self.gameState[self.yIndex][self.xIndex] = 1
			tmp = self.canvas.create_oval((self.xIndex*100)+20, (self.yIndex*100) -680, (self.xIndex*100)+80, (self.yIndex*100)-620, fill = 'red')
			self.dropInAnimation(tmp)
			self.markIds[self.yIndex][self.xIndex] = tmp

		else:
			#self.gameState[self.yIndex][self.xIndex] = 2
			#tmp = self.canvas.create_oval((self.xIndex*100)+20, (self.yIndex*100) +20, (self.xIndex*100)+80, (self.yIndex*100)+80, fill = 'blue')
			#self.markIds[self.yIndex][self.xIndex] = tmp

			self.gameState[self.yIndex][self.xIndex] = 2
			tmp = self.canvas.create_oval((self.xIndex*100)+20, (self.yIndex*100) -680, (self.xIndex*100)+80, (self.yIndex*100)-620, fill = 'blue')
			self.dropInAnimation(tmp)
			self.markIds[self.yIndex][self.xIndex] = tmp

	def calculatePosOfMark(self):
		i = 5
		while(i >= 0):
			if(self.gameState[i][self.xIndex] == 0):
				return i
			i -= 1
		return -1

	def checkWin(self):

		win = 0
		x = y = 0
		
		for i in range(3):
			for j in range(6):
				#vertical
				if(self.gameState[i][j] != 0 and (self.gameState[i][j] == self.gameState[i+1][j] == self.gameState[i+2][j] == self.gameState[i+3][j])):
					win = 1
					x = i
					y = j
					break
				#horizontal
				if(self.gameState[j][i] != 0 and (self.gameState[j][i] == self.gameState[j][i+1] == self.gameState[j][i+2] == self.gameState[j][i+3])):
					win = 2
					x = i
					y = j
					break
			if(win != 0):
				break

		if(win == 0):
			#Diagonals
			for i in range(3):
				for j in range(3):
					if(self.gameState[i][j] != 0):
						if(self.gameState[i][j] == self.gameState[i+1][j+1] == self.gameState[i+2][j+2] == self.gameState[i+3][j+3]):
							win = 3
							x = i
							y = j
							break
					k = j + 3
					if(self.gameState[i][k] != 0):
						if(self.gameState[i][k] == self.gameState[i+1][k-1] == self.gameState[i+2][k-2] == self.gameState[i+3][k-3]):
							win = 4
							x = i
							y = k
							break
				if(win != 0):
					break
		
		if(win == 0):
			return False
		else:
			if(win == 1):
				self.winningMarks = [self.markIds[x][y], self.markIds[x+1][y], self.markIds[x+2][y], self.markIds[x+3][y]]
			elif(win == 2):
				self.winningMarks = [self.markIds[y][x], self.markIds[y][x+1], self.markIds[y][x+2], self.markIds[y][x+3]]
			elif(win == 3):
				self.winningMarks = [self.markIds[x][y], self.markIds[x+1][y+1], self.markIds[x+2][y+2], self.markIds[x+3][y+3]]
			elif(win == 4):
				self.winningMarks = [self.markIds[x][y], self.markIds[x+1][y-1], self.markIds[x+2][y-2], self.markIds[x+3][y-3]]
			return True
	
	def p1Wins(self):
		self.blinkingAnimation()
		txt = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2, text = "Red Wins!!", font = "Consolas 34 bold", fill = "red")
		self.canvas.update()
		time.sleep(1.5)
		self.canvas.delete(txt)
	def p2Wins(self):
		self.blinkingAnimation()
		txt = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2, text = "Blue Wins!!", font = "Consolas 34 bold", fill = "blue")
		self.canvas.update()
		time.sleep(1.5)
		self.canvas.delete(txt)

	def draw(self):
		txt = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2, text = "Draw!", font = "Consolas 34 bold", fill = "white")
		self.canvas.update()
		time.sleep(1.5)
		self.canvas.delete(txt)

	def resetBoard(self):
		for i in self.markIds:
			for j in i:
				if(j > 0):
					self.canvas.delete(j)
		self.isP1Playing = True
		self.winningMarks = [0, 0, 0, 0]
		self.xIndex = self.yIndex = -1
		self.roundCount = 0
		self.gameState = []
		for i in range(6):
			self.gameState.append([0, 0, 0, 0, 0, 0])
			self.markIds.append([-1]*6)
		self.canvas.update()

	def dropInAnimation(self, id):
		#i = 0
		start_y = self.canvas.coords(id)[1]
		while(self.canvas.coords(id)[1] < start_y+700):
			try:
				self.master.update()
				self.master.update_idletasks()
				self.canvas.update()
				self.canvas.move(id, 0, 7)
			except:
				pass
			
			time.sleep(0.000001)
			#i += 1

	def blinkingAnimation(self):
		for i in range(4):
			self.canvas.itemconfigure(self.winningMarks[0], fill = 'white')
			self.canvas.itemconfigure(self.winningMarks[1], fill = 'white')
			self.canvas.itemconfigure(self.winningMarks[2], fill = 'white')
			self.canvas.itemconfigure(self.winningMarks[3], fill = 'white')
			self.canvas.update()
			time.sleep(0.2)
			if(self.isP1Playing):
				self.canvas.itemconfigure(self.winningMarks[0], fill = 'blue')
				self.canvas.itemconfigure(self.winningMarks[1], fill = 'blue')
				self.canvas.itemconfigure(self.winningMarks[2], fill = 'blue')
				self.canvas.itemconfigure(self.winningMarks[3], fill = 'blue')
			else:
				self.canvas.itemconfigure(self.winningMarks[0], fill = 'red')
				self.canvas.itemconfigure(self.winningMarks[1], fill = 'red')
				self.canvas.itemconfigure(self.winningMarks[2], fill = 'red')
				self.canvas.itemconfigure(self.winningMarks[3], fill = 'red')
			self.canvas.update()
			time.sleep(0.2)
