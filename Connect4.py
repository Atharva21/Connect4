from tkinter import *
from Grid import *

def main():

	root = Tk()
	root.title("Connect 4")
	root.geometry("600x600+430+90")
	root.resizable(False, False)
	root.wm_attributes("-topmost", 1)

	canvas = Canvas(root, width = 600, height = 600, bg = 'black', bd = 0, highlightthickness = 0)
	canvas.pack()

	grid = Grid(canvas, root)

	root.mainloop()
	

if __name__ == '__main__':
	main()