#!/usr/bin/env python


import json

Types = ["CONSONANT", "VOWEL", "ENDING", "CONSONANT_SOUND", "VOWEL_SOUND"]

# a piece is made up of a value, a piece_type, a starting row, a starting column, a current row and a current column.
# rows and columns are pixel offsets. piece_types are the colors and use

# This should never need to be run again.
Phonetic_Cards = {}
lst = ["A", "B", "C", "D", "E", "F", "F", "G", "H", "I", "J", "K", "L", "L", "M", "N", "O", "P", "Qu", "R", "S", "S",
       "T", "U", "V", "W", "X", "Y", "Y", "Z"]
Letter_List = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Qu", "R", "S", "T", "U",
               "V", "W", "X", "Y", "Z"]
lst.sort()
Vowel_Sound_lst = ["AI", "AY", "EA", "EE", "EY", "OA", "OE", "UE", "OI", "OY", "AU", "AW", "OU", "OW", "EW", "EU",
                   "OO", "UI", "EI", "IE", "EIGH", "IGH", "AR", "ER", "IR", "OR", "UR"]
Ending_List = ["TU", "TION", "TURE", "STLE", "SION", "IVE", "ILD", "IND", "OLD", "OLT", "OST", "AN", "AM", "ALL",
               "ANK", "INK", "ONK", "UNK", "ANG", "UNG", "ING", "ONG"]
Consonant_sound_list = ["WH", "TH", "SH", "CH", "CK", "TCH", "CI", "DGE", "TI", "QUE", "PH"]
ALPHABET = {}
VOWEL_SOUND = {}
ENDING = {}
CONSONANT_SOUND = {}


# lst = lst+non_letter_lst


def define_alphabet():
	col_counter = 0
	row_counter = 0
	row_count = 0
	for letter in lst:
		if letter == "A" or letter == "E" or letter == "I" or letter == "O" or letter == "U":
			card_type = 1
		elif letter in Letter_List:
			card_type = 0
		else:
			card_type = 2
		curr_letter = letter
		if letter in ALPHABET:
			curr_letter = letter + "_REPEAT"
		if curr_letter == "Y_REPEAT":
			card_type = 1
		ALPHABET[curr_letter] = dict(Letter=letter, Type=Types[card_type], Starting_Row=row_counter,
		                             Starting_Column=col_counter, Default=True)
		if col_counter == 6 and row_count < 2:
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 7 and row_count > 1:
			col_counter = 0
			row_counter += 1
			row_count += 1
		else:
			col_counter += 1


def define_vowel_sounds():
	col_counter = 0
	row_counter = 0
	row_count = 1
	for sound in Vowel_Sound_lst:
		card_type = 3
		VOWEL_SOUND[sound] = dict(Letter=sound, Type=Types[card_type], Starting_Row=row_counter, Starting_Column=col_counter,
									Default=True)
		if col_counter == 1 and (row_count == 1 or (4 <= row_count <= 6) or (9 <= row_count <= 10)):
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 2 and (row_count == 2 or (3 <= row_count <= 7)):
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 0 and (row_count == 8 or 11 <= row_count):
			col_counter = 0
			row_counter += 1
			row_count += 1
		else:
			col_counter += 1


def define_ending():
	col_counter = 0
	row_counter = 0
	row_count = 1
	for end in Ending_List:
		card_type = 2
		ENDING[end] = dict(Letter=end, Type=Types[card_type], Starting_Row=row_counter,
		                   Starting_Column=col_counter, Default=True)
		if col_counter == 2 and ((1 <= row_count <= 2) or (4 <= row_count <= 5)):
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 1 and row_count == 3:
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 3 and 6 <= row_count:
			col_counter = 0
			row_counter += 1
			row_count += 1
		else:
			col_counter += 1


def define_consonant_sound():
	col_counter = 0
	row_counter = 0
	row_count = 1
	for sound in Consonant_sound_list:
		card_type = 3
		CONSONANT_SOUND[sound] = dict(Letter=sound, Type=Types[card_type], Starting_Row=row_counter,
		                              Starting_Column=col_counter, Default=True)
		if col_counter == 4 and row_count == 1:
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 2 and row_count != 1:
			col_counter = 0
			row_counter += 1
			row_count += 1
		else:
			col_counter += 1


def define_phonetic_cards():
	col_counter = 0
	row_counter = 0
	row_count = 0
	for letter in lst:
		if letter == "A" or letter == "E" or letter == "I" or letter == "O" or letter == "U":
			card_type = 1
		elif letter in Letter_List:
			card_type = 0
		else:
			card_type = 2
		curr_letter = letter
		if letter in Phonetic_Cards:
			curr_letter = letter + "_REPEAT"
		if curr_letter == "Y_REPEAT":
			card_type = 1
		Phonetic_Cards[curr_letter] = dict(Letter=letter, Type=Types[card_type], Starting_Row=row_counter,
		                                   Starting_Column=col_counter, Default=True)
		if col_counter == 6 and row_count < 2:
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 7 and row_count > 1:
			col_counter = 0
			row_counter += 1
			row_count += 1
		else:
			col_counter += 1
	col_counter = 0
	second_row_counter = 0
	row_count = 1
	for sound in Vowel_Sound_lst:
		card_type = 4
		Phonetic_Cards[sound] = dict(Letter=sound, Type=Types[card_type], Starting_Row=second_row_counter,
		                             Starting_Column=col_counter + 10, Default=True)
		if col_counter == 1 and (row_count == 1 or (4 <= row_count <= 6) or (9 <= row_count <= 10)):
			col_counter = 0
			second_row_counter += 1
			row_count += 1
		elif col_counter == 2 and (row_count == 2 or (3 <= row_count <= 7)):
			col_counter = 0
			second_row_counter += 1
			row_count += 1
		elif col_counter == 0 and (row_count == 8 or 11 <= row_count):
			col_counter = 0
			second_row_counter += 1
			row_count += 1
		else:
			col_counter += 1
	col_counter = 0
	row_count = 1
	for sound in Consonant_sound_list:
		card_type = 3
		Phonetic_Cards[sound] = dict(Letter=sound, Type=Types[card_type], Starting_Row=row_counter,
		                             Starting_Column=col_counter, Default=True)
		if col_counter == 4 and row_count == 1:
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 2 and row_count != 1:
			col_counter = 0
			row_counter += 1
			row_count += 1
		else:
			col_counter += 1
	col_counter = 0
	row_count = 1
	for end in Ending_List:
		card_type = 2
		Phonetic_Cards[end] = dict(Letter=end, Type=Types[card_type], Starting_Row=row_counter,
		                           Starting_Column=col_counter, Default=True)
		if col_counter == 2 and ((1 <= row_count <= 2) or (4 <= row_count <= 5)):
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 1 and row_count == 3:
			col_counter = 0
			row_counter += 1
			row_count += 1
		elif col_counter == 3 and 6 <= row_count:
			col_counter = 0
			row_counter += 1
			row_count += 1
		else:
			col_counter += 1


define_alphabet()
# print(Phonetic_Cards)
# with open('Primary_Alphabet.json', 'w', encoding='utf-8') as f:
# 	json.dump(ALPHABET, f, ensure_ascii=False, indent=4)
# define_vowel_sounds()
# with open("Vowel_sounds.json", 'w', encoding='utf-8') as f:
# 	json.dump(VOWEL_SOUND, f, ensure_ascii=False, indent=4)
# define_ending()
# with open("Ending.json", 'w', encoding='utf-8') as f:
# 	json.dump(ENDING, f, ensure_ascii=False, indent=4)
# define_consonant_sound()
# with open("Consonant_sounds.json", 'w', encoding='utf-8') as f:
# 	json.dump(CONSONANT_SOUND, f, ensure_ascii=False, indent=4)
define_phonetic_cards()
with open("Phonetics.json", 'w', encoding='utf-8') as f:
	json.dump(Phonetic_Cards, f, ensure_ascii=False, indent=4)
