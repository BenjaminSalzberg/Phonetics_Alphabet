#!/usr/bin/env python3

from json import dump
from json import load
from tkinter import Canvas
from tkinter import Tk
root = Tk()
root.title("Phonetic Alphabet")
root.config(bg="#FFFFFF")
canvas = Canvas(root)
x0 = 0
y0 = 0
current_green_box = None
state = "START"
used_letter = {}
with open("Settings.json", 'r', encoding='utf-8') as f:
	Current_Settings = load(f)
basic_bool = Current_Settings["basic_bool"]
yellow_bool = Current_Settings["yellow_bool"]
green_bool = Current_Settings["green_bool"]
red_bool = Current_Settings["red_bool"]
PIXEL_OFFSET = Current_Settings["PIXEL_OFFSET"]
font_size = int(PIXEL_OFFSET/4)
new_offset = PIXEL_OFFSET
y_toggle_count = Current_Settings["y_toggle_count"]  # 0 for both, 1 for vowel, 2 for consonant


def get_letter(grid_x, grid_y):
	for key in Phonetic_cards:
		if Phonetic_cards[key]["Starting_Column"] == grid_x and Phonetic_cards[key]["Starting_Row"] == grid_y:
			return Phonetic_cards[key]
	return None


def get_location(multiplier=None):
	global state
	i = 0
	if multiplier is None:
		multiplier = 1
		if state == "ALPHABET_DECIDE":
			multiplier = 4
	while i <= x0:
		i += PIXEL_OFFSET * multiplier
	i -= PIXEL_OFFSET * multiplier
	q = 0
	while q <= y0:
		q += PIXEL_OFFSET * multiplier
	q -= PIXEL_OFFSET * multiplier
	return [i, q]


def get_alphabet(basic_boolean, yellow_boolean, green_boolean, red_boolean, y_toggle):
	check = True
	used = False
	dictionary = {}
	if basic_boolean and yellow_boolean and green_boolean and red_boolean and y_toggle == 0:
		with open("Phonetics.json") as file:
			dictionary = load(file)
		check = False
	if basic_boolean and check and y_toggle == 0:
		used = True
		with open("Alphabet_Y_Both.json") as file:
			dictionary = load(file)
	elif basic_boolean and check and y_toggle == 1:
		used = True
		with open("Alphabet_Y_Vowel.json") as file:
			dictionary = load(file)
	elif basic_boolean and check and y_toggle == 2:
		used = True
		with open("Alphabet_Y_Consonant.json") as file:
			dictionary = load(file)
	if yellow_boolean and check:
		if used:
			with open("Consonants.json") as file:
				dictionary = {**dictionary, **load(file)}
		else:
			with open("Consonants.json") as file:
				dictionary = load(file)
			used = True
	if green_boolean and check:
		if used:
			with open("Endings.json") as file:
				dictionary = {**dictionary, **load(file)}
		else:
			with open("Endings.json") as file:
				dictionary = load(file)
			used = True
	if red_boolean and check:
		if used:
			with open("Vowels.json") as file:
				dictionary = {**dictionary, **load(file)}
		else:
			with open("Vowels.json") as file:
				dictionary = load(file)
	return dictionary


Phonetic_cards = get_alphabet(basic_bool, yellow_bool, green_bool, red_bool, y_toggle_count)


def use_board():
	global PIXEL_OFFSET
	global new_offset
	global Phonetic_cards
	global current_green_box
	global state
	global basic_bool
	global yellow_bool
	global green_bool
	global red_bool
	global y_toggle_count
	if state == "SET_PIECE_LOCATION" or state == "SELECT_PIECE" or state == "START":
		if x0 > PIXEL_OFFSET*14:
			if current_green_box is not None:
				canvas.delete(current_green_box)
			state = "SELECT_PIECE"
			location = get_location()
			x = location[0]
			y = location[1]
			current_green_box = canvas.create_rectangle(x, y, x + PIXEL_OFFSET, y + PIXEL_OFFSET, outline="#000000",
			                                            fill="#00FF00")
		else:
			if state == "SELECT_PIECE":
				location = get_location()
				x = location[0]
				y = location[1]
				grid_x = x / PIXEL_OFFSET
				grid_y = y / PIXEL_OFFSET
				value = get_letter(grid_x, grid_y)
				if value is not None:
					if value["Type"] == "VOWEL" or value["Type"] == "VOWEL_SOUND":
						color = "#FF0000"
					elif value["Type"] == "CONSONANT" or value["Type"] == "CONSONANT_SOUND":
						color = "#FFFF00"
					else:
						color = "#00FF00"
					state = "SET_PIECE_LOCATION"
					coordinates = canvas.coords(current_green_box)
					coord_string = ''.join(str(coordinates))
					if coord_string in used_letter.keys():
						lst = used_letter[coord_string]
						canvas.delete(lst[0])
						canvas.delete(lst[1])
					used_letter[coord_string] = ([
						canvas.create_rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3],
						                        outline="#000000", fill=color),
						canvas.create_text(coordinates[0] + (PIXEL_OFFSET / 2), coordinates[1] + (PIXEL_OFFSET / 2),
						                   font=("Purisa", font_size), text=value["Letter"])
					])
					canvas.delete(current_green_box)
				elif 0 <= x <= PIXEL_OFFSET * 15 and PIXEL_OFFSET * 14 <= y <= PIXEL_OFFSET * 16:
					state = "ALPHABET_DECIDE"
					use_board()
				else:
					state = "SET_PIECE_LOCATION"
					coordinates = canvas.coords(current_green_box)
					coord_string = ''.join(str(coordinates))
					if coord_string in used_letter.keys():
						lst = used_letter[coord_string]
						canvas.delete(lst[0])
						canvas.delete(lst[1])
					canvas.delete(current_green_box)
			elif state != "ALPHABET_DECIDE":
				location = get_location()
				x = location[0]
				y = location[1]
				if 0 <= x <= PIXEL_OFFSET * 15 and PIXEL_OFFSET * 14 <= y <= PIXEL_OFFSET * 16:
					state = "ALPHABET_DECIDE"
					use_board()
	elif state == "ALPHABET_DECIDE":
		state = "ALPHABET_DECIDE"
		canvas.delete("all")
		show_board()
		location = get_location()
		x = location[0]
		y = location[1]
		if x == 0 and y == 0:
			basic_bool = True
			yellow_bool = True
			green_bool = True
			red_bool = True
			y_toggle_count = 0
			Current_Settings["basic_bool"] = basic_bool
			Current_Settings["yellow_bool"] = yellow_bool
			Current_Settings["green_bool"] = green_bool
			Current_Settings["red_bool"] = red_bool
			Current_Settings["y_toggle_count"] = y_toggle_count
			with open("Settings.json", 'w', encoding='utf-8') as file:
				dump(Current_Settings, file, ensure_ascii=False, indent=4)
			show_board()
		# print("Default")
		elif x == PIXEL_OFFSET*4 and y == 0:
			basic_bool = not basic_bool
			Current_Settings["basic_bool"] = basic_bool
			with open("Settings.json", 'w', encoding='utf-8') as file:
				dump(Current_Settings, file, ensure_ascii=False, indent=4)
			show_board()
		# print("ALPHABET")
		elif x == PIXEL_OFFSET*4*2 and y == 0:
			yellow_bool = not yellow_bool
			Current_Settings["yellow_bool"] = yellow_bool
			with open("Settings.json", 'w', encoding='utf-8') as file:
				dump(Current_Settings, file, ensure_ascii=False, indent=4)
			show_board()
		# print("consonant combinations")
		elif x == PIXEL_OFFSET*4*3 and y == 0:
			green_bool = not green_bool
			Current_Settings["green_bool"] = green_bool
			with open("Settings.json", 'w', encoding='utf-8') as file:
				dump(Current_Settings, file, ensure_ascii=False, indent=4)
			show_board()
		# print("word endings")
		elif x == 0 and y == PIXEL_OFFSET*4:
			red_bool = not red_bool
			Current_Settings["red_bool"] = red_bool
			with open("Settings.json", 'w', encoding='utf-8') as file:
				dump(Current_Settings, file, ensure_ascii=False, indent=4)
			show_board()
		# print("Vowel Sounds")
		elif x == PIXEL_OFFSET*4 and y == PIXEL_OFFSET*4:
			y_toggle_count = (y_toggle_count + 1) % 3
			Current_Settings["y_toggle_count"] = y_toggle_count
			with open("Settings.json", 'w', encoding='utf-8') as file:
				dump(Current_Settings, file, ensure_ascii=False, indent=4)
			show_board()
		# print("Toggle Y")
		elif x == PIXEL_OFFSET*4*2 and y == PIXEL_OFFSET*4:
			new_offset = (new_offset + 10)
			if new_offset > 60:
				new_offset = 40
			else:
				if new_offset < 40:
					new_offset = 40
			Current_Settings["PIXEL_OFFSET"] = new_offset
			# PIXEL_OFFSET = new_offset
			with open("Settings.json", 'w', encoding='utf-8') as file:
				dump(Current_Settings, file, ensure_ascii=False, indent=4)
			show_board()
		# print("pixel_offset")
		elif 0 <= x <= PIXEL_OFFSET * 16 and PIXEL_OFFSET * 8 <= y < PIXEL_OFFSET * 12:
			canvas.delete("all")
			Phonetic_cards = get_alphabet(basic_bool, yellow_bool, green_bool, red_bool, y_toggle_count)
			state = "SET_PIECE_LOCATION"
			canvas.delete("all")
			show_board()


def get_origin(eventorigin):
	global x0, y0
	x0 = eventorigin.x
	y0 = eventorigin.y
	use_board()


# mouse click event
canvas.bind("<Button 1>", get_origin)


def show_board():
	global Phonetic_cards
	global state
	global basic_bool
	global yellow_bool
	global green_bool
	global red_bool
	global y_toggle_count
	root.deiconify()
	canvas.config(bg="#FFFFFF")
	canvas.pack_propagate(0)
	root.geometry(""+str(int(PIXEL_OFFSET*25))+"x"+str(int(PIXEL_OFFSET*17))+"+0+0")
	canvas_box = {}
	canvas_txt = {}
	if state == "START" or state == "SET_PIECE_LOCATION" or state == "SELECT_PIECE":
		for key in Phonetic_cards.keys():
			text = Phonetic_cards[key]["Letter"]
			if Phonetic_cards[key]["Type"] == "VOWEL" or Phonetic_cards[key]["Type"] == "VOWEL_SOUND":
				color = "#FF0000"
			elif Phonetic_cards[key]["Type"] == "CONSONANT" or Phonetic_cards[key]["Type"] == "CONSONANT_SOUND":
				color = "#FFFF00"
			else:
				color = "#00FF00"
			canvas_box[key] = canvas.create_rectangle(Phonetic_cards[key]["Starting_Column"] * PIXEL_OFFSET,
			                                          Phonetic_cards[key]["Starting_Row"] * PIXEL_OFFSET,
			                                          (Phonetic_cards[key]["Starting_Column"] + 1) * PIXEL_OFFSET,
			                                          (Phonetic_cards[key]["Starting_Row"] + 1) * PIXEL_OFFSET,
			                                          outline="#000000",
			                                          fill=color)
			canvas_txt[key] = canvas.create_text(
				((Phonetic_cards[key]["Starting_Column"]) * PIXEL_OFFSET + (PIXEL_OFFSET / 2)),
				((Phonetic_cards[key]["Starting_Row"]) * PIXEL_OFFSET + (PIXEL_OFFSET / 2)),
				font=("Purisa", font_size), text=text)
			canvas.create_rectangle(0, PIXEL_OFFSET * 15, PIXEL_OFFSET * 14 - 1, PIXEL_OFFSET * 16,
			                        fill="Black")
			canvas.create_text(PIXEL_OFFSET * 7, PIXEL_OFFSET * 15 + (PIXEL_OFFSET / 2),
			                   fill="white", text="OPTIONS")
		canvas.create_line(PIXEL_OFFSET * 14 - 1, 0, PIXEL_OFFSET * 14 - 1, 2000, fill="red")
	elif state == "ALPHABET_DECIDE":
		if basic_bool and yellow_bool and green_bool and red_bool and y_toggle_count == 0:
			default_color = "#00FF00"
		else:
			default_color = "#FF0000"
		if basic_bool:
			basic_color = "#00FF00"
		else:
			basic_color = "#FF0000"
		if yellow_bool:
			yellow_color = "#00FF00"
		else:
			yellow_color = "#FF0000"
		if green_bool:
			green_color = "#00FF00"
		else:
			green_color = "#FF0000"
		if red_bool:
			red_color = "#00FF00"
		else:
			red_color = "#FF0000"
		if y_toggle_count == 0:
			y_toggle_color = "#4444FF"
		elif y_toggle_count == 1:
			y_toggle_color = "#FF0000"
		else:
			y_toggle_color = "#00FF00"
		canvas.create_rectangle(0, 0, PIXEL_OFFSET * 4, PIXEL_OFFSET * 4, outline="#000000",
		                        fill=default_color)
		canvas.create_rectangle(PIXEL_OFFSET * 4, 0, PIXEL_OFFSET * 8, PIXEL_OFFSET * 4, outline="#000000",
		                        fill=basic_color)
		canvas.create_rectangle(PIXEL_OFFSET * 8, 0, PIXEL_OFFSET * 12, PIXEL_OFFSET * 4, outline="#000000",
		                        fill=yellow_color)
		canvas.create_rectangle(PIXEL_OFFSET * 12, 0, PIXEL_OFFSET * 16, PIXEL_OFFSET * 4, outline="#000000",
		                        fill=green_color)
		canvas.create_rectangle(0, PIXEL_OFFSET * 4, PIXEL_OFFSET * 4, PIXEL_OFFSET * 8, outline="#000000",
		                        fill=red_color)
		canvas.create_rectangle(PIXEL_OFFSET * 4, PIXEL_OFFSET * 4, PIXEL_OFFSET * 8, PIXEL_OFFSET * 8,
		                        outline="#000000", fill=y_toggle_color)
		canvas.create_text(PIXEL_OFFSET * 2, PIXEL_OFFSET * 2, font=("Purisa", font_size),
		                   text="Everything (Default)")
		canvas.create_text(PIXEL_OFFSET * 6, PIXEL_OFFSET * 2, font=("Purisa", font_size),
		                   text="Alphabet")
		canvas.create_text(PIXEL_OFFSET * 10, PIXEL_OFFSET * 2, font=("Purisa", font_size),
		                   text="Consonant Combinations")
		canvas.create_text(PIXEL_OFFSET * 14, PIXEL_OFFSET * 2, font=("Purisa", font_size),
		                   text="Word Endings")
		canvas.create_text(PIXEL_OFFSET * 2, PIXEL_OFFSET * 6, font=("Purisa", font_size),
		                   text="Vowel Sounds")
		canvas.create_text(PIXEL_OFFSET * 6, PIXEL_OFFSET * 6, font=("Purisa", font_size),
		                   text="Toggle Y, \nRed = Vowel, \nGreen = Consonant, \nBlue = Both")
		canvas.create_rectangle(PIXEL_OFFSET * 8, PIXEL_OFFSET * 4, PIXEL_OFFSET * 12, PIXEL_OFFSET * 8,
		                        outline="#000000", fill="#00FF00")
		canvas.create_text(PIXEL_OFFSET * 10, PIXEL_OFFSET * 6, font=("Purisa", font_size),
		                   text="Size " + str(int(new_offset)) + "\nDoes not update \nuntil program restart. ")
		canvas.create_rectangle(0, PIXEL_OFFSET * 8, PIXEL_OFFSET * 16, PIXEL_OFFSET * 12,
		                        fill="Black")
		canvas.create_text(PIXEL_OFFSET * 6, PIXEL_OFFSET * 10 + (PIXEL_OFFSET / 2), fill="white",
		                   text="CONFIRM")
	canvas.pack(fill='both', expand=True)
	canvas.update()


show_board()
root.mainloop()
