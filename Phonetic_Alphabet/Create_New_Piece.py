#!/usr/bin/env python3


import json
from tkinter import messagebox
from tkinter import *
PIXEL_OFFSET = 60
with open('Phonetics.json') as f:
	Phonetic_cards = json.load(f)
root = Tk()
root.config(bg="#FFFFFF")
label1 = Label(root, text="Please write what the piece contains.")
E1 = Entry(root, bd=5)


def show_board():
	root.deiconify()
	canvas = Canvas(root)
	canvas.config(bg="#FFFFFF")
	canvas.pack_propagate(0)
	root.geometry("1500x1000+0+0")
	canvas_txt = {}
	for key in Phonetic_cards.keys():
		text = Phonetic_cards[key]["Letter"]
		if Phonetic_cards[key]["Type"] == "VOWEL" or Phonetic_cards[key]["Type"] == "VOWEL_SOUND":
			color = "#FF0000"
		elif Phonetic_cards[key]["Type"] == "CONSONANT" or Phonetic_cards[key]["Type"] == "CONSONANT_SOUND":
			color = "#FFFF00"
		else:
			color = "#00FF00"
		canvas.create_rectangle(Phonetic_cards[key]["Starting_Column"]*PIXEL_OFFSET, Phonetic_cards[key]["Starting_Row"]
								* PIXEL_OFFSET,
								(Phonetic_cards[key]["Starting_Column"] + 1) * PIXEL_OFFSET,
								(Phonetic_cards[key]["Starting_Row"]+1)*PIXEL_OFFSET, outline="#000000", fill=color)
		canvas_txt[key] = canvas.create_text(((Phonetic_cards[key]["Starting_Column"])*PIXEL_OFFSET+(PIXEL_OFFSET/2)),
									((Phonetic_cards[key]["Starting_Row"])*PIXEL_OFFSET+(PIXEL_OFFSET/2)), font=("Purisa", 15), text=text)
	canvas.create_line(800, 0, 800, 2000, fill="red")
	canvas.pack(fill='both', expand=True)
	canvas.update()


def get_piece(_event=None):
	root.withdraw()
	new_piece = E1.get().upper()
	if new_piece in Phonetic_cards:
		cont = messagebox.askquestion("ERROR", "This piece already exists! Try Again? ")
		if cont == "yes":
			root.deiconify()
			E1.delete(0, 'end')
		else:
			root.destroy()
	else:
		messagebox.showinfo("Success", "Piece Added!")
		label1.destroy()
		E1.destroy()
		submit.destroy()
		# show_board()


def ask_for_piece():
	submit = Button(root, text="Submit", command=get_piece)
	root.bind("<Return>", get_piece)
	label1.pack()
	E1.pack()
	submit.pack(side=BOTTOM)
	global submit
	root.mainloop()


ask_for_piece()
