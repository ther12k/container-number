from stdnum import iso6346
from config import WORD_FOR_REPLACE, COMPNAMES, REMOVE_WORD
from similarity.weighted_levenshtein import (
    CharacterSubstitutionInterface,
	WeightedLevenshtein)

'''
Add cost substituting word in compnames and result ocr
'''
class CharacterSubstitution(CharacterSubstitutionInterface):
	def cost(self, c0, c1):
		# print(c0)
		if c0 == 'N' and c1 == 'M': return 0.5
		if c0 == 'A' and c1 == '2': return 0.5
		if c0 == 'G' and c1 == '6': return 0.5
		if c0 == 'U' and c1 == '0': return 0.5
		if c0 == 'U' and c1 == '8': return 0.5
		if c0 == 'U' and c1 == 'W': return 0.5
		if c0 == 'S' and c1 == '5': return 0.5
		if c0 == 'I' and c1 == '1': return 0.5
		return 1.0

'''
Text processing to get container_number_dict
with algoritm WeightedLevenshtein for correction unique_owner
'''
class OneLenResult:
	def __init__(self, filtered_text):
		self.weighted_levenshtein   = WeightedLevenshtein(CharacterSubstitution())
		self.replace_word           = WORD_FOR_REPLACE
		self.filtered_text          = filtered_text
		self.container_number_dict  = dict()
		self.confidence_list        = list()
		self.temporary_text         = str()
		self.temporary_text_r       = str()
		self.get_unique_owner(), self.get_serial_number_digit()
		self.confidence_level       = self.calculate_confidence()

	def replace_word_serial_number(self, text, conf):
		'''
		Replace alpha to number
		'''
		serial_number = text
		confidence = conf
		for i in range(len(serial_number)):
			if not serial_number[i].isnumeric() and serial_number[i] in self.replace_word:
				replaced = self.replace_word[str(serial_number[i])]
				serial_number = serial_number.replace(serial_number[i], replaced)
				confidence = (conf+1)/2
		return serial_number, confidence

	def replace_number_serial_number(self, text, conf):
		'''
		Replace number to alpha
		'''
		serial_number = text
		confidence = conf
		for i in range(len(serial_number)):
			if serial_number[i].isnumeric() and serial_number[i] in self.replace_word:
				replaced = self.replace_word[str(serial_number[i])]
				if replaced.isalpha():
					serial_number = serial_number.replace(serial_number[i], replaced)
					confidence = (conf+1)/2
		return serial_number, confidence

	def get_unique_owner(self):
		'''
		Get unique owner with algoritm weighted_levenshtein
		and update confidence (conf+1)/2
		'''
		min_ratio = 10
		unique_owner = str()
		for text, conf in self.filtered_text:
			text_uo = text[:4]
			if text_uo.isalpha() and not text_uo.isnumeric():
				text_r, conf_r = self.replace_number_serial_number(text_uo, conf)
			for compname in COMPNAMES:
				ratio = self.weighted_levenshtein.distance(compname, text_uo)
				if min_ratio > ratio:
					min_ratio = ratio
					unique_owner = compname
					conf_i = (conf+1)/2
					self.temporary_text	= text_uo
					self.temporary_text_r = unique_owner
				else: 
					min_ratio = min_ratio
		if unique_owner in COMPNAMES:
			self.confidence_list.append(conf_i)
			self.container_number_dict.update({'unique_owner': unique_owner})
			pass

	def get_serial_number_digit(self):
		'''
		Get serial number and digit
		'''
		text = ''.join([i[0] for i in self.filtered_text])
		conf = [i[1] for i in self.filtered_text][0]
		# if list(text).index(self.temporary_text[-1]) >=4 and list(text).index(self.container_number_dict["unique_owner"][-1]):
		# 	index = list(text).index(self.container_number_dict["unique_owner"][-1])
		# else:
		# 	index = list(text).index(self.temporary_text[-1])
		try: index = list(text).index(self.temporary_text_r[-1])
		except: index = list(text).index(self.temporary_text[-1])
		new_text = text[index+1:]

		new_text_r, new_conf_r = self.replace_word_serial_number(new_text, conf)
		new_text_r = new_text_r.replace(' ', '')
		serial_number_digit = new_text_r[:7]
		text_m = (f'{self.container_number_dict["unique_owner"]}{serial_number_digit}')
		text_val = iso6346.is_valid(text_m)
		if text_val:
			self.confidence_list.append(new_conf_r)
			self.container_number_dict.update({
				'serial_number' : serial_number_digit[:6], 
				'container_digit' : serial_number_digit[-1] })
		else:
			self.confidence_list.append(new_conf_r)
			digit = iso6346.calc_check_digit(text_m[:10])
			self.container_number_dict.update({
				'serial_number' : serial_number_digit[:6], 
				'container_digit' : digit })
		pass

	def calculate_confidence(self):
		'''
		Calculate avg confidence in confidence_list
		'''
		confidence_avg = round((sum(self.confidence_list)/len(self.confidence_list)),2)
		return confidence_avg


'''
Text processing to get container_number_dict
with algoritm WeightedLevenshtein for correction unique_owner
'''
class OneMoreLenResult:
	def __init__(self, filtered_text):
		self.weighted_levenshtein 	= WeightedLevenshtein(CharacterSubstitution())
		self.replace_word 			= WORD_FOR_REPLACE
		self.filtered_text 			= filtered_text
		self.container_number_dict 	= dict()
		self.confidence_list 		= list()
		self.temporary_list 		= list()

		self.get_unique_owner(), self.get_serial_number()
		try: self.container_number_dict['container_digit']
		except KeyError: self.get_digit_code()
		self.confidence_level = self.calculate_confidence()

	def replace_word_serial_number(self, text, conf):
		serial_number = text
		confidence = conf
		for i in range(len(serial_number)):
			if not serial_number[i].isnumeric() and serial_number[i] in self.replace_word:
				replaced = self.replace_word[str(serial_number[i])]
				serial_number = serial_number.replace(serial_number[i], replaced)
				confidence = (conf+1)/2
		return serial_number, confidence

	def replace_number_serial_number(self, text, conf):
		serial_number = text
		confidence = conf
		for i in range(len(serial_number)):
			if serial_number[i] in self.replace_word and serial_number[i].isnumeric():
				replaced = self.replace_word[str(serial_number[i])]
				if replaced.isnumeric():
					serial_number = serial_number.replace(serial_number[i], replaced)
					confidence = (conf+1)/2
					break
		return serial_number, confidence

	def get_unique_owner(self):
		'''
		Get unique owner with algoritm weighted_levenshtein,
		update confidence (conf+1)/2,
		and append new [text, conf] if text > temp merge with index text+1
		'''
		text_list = [text for text, _ in self.filtered_text]
		conf_list = [conf for _,conf in self.filtered_text]
		index = [i for i,x in enumerate(text_list) if x[-1] == 'U' and len(x) > 2]
		if index:
			min_ratio = 10
			temp = str()
			conf_i = float()
			text = text_list[index[0]]
			conf = conf_list[index[0]]
			for compname in COMPNAMES:
				ratio = self.weighted_levenshtein.distance(compname, text)
				if ratio < min_ratio:
					min_ratio = ratio
					temp = compname
					conf_i = (conf+1)/2
				else:
					min_ratio = min_ratio
			if int(min_ratio) < 2 and temp in COMPNAMES:
				self.container_number_dict.update({'unique_owner': temp})
				self.temporary_list.append([text, conf])
				self.confidence_list.append(conf)

		else:
			for text, conf in self.filtered_text:
				min_ratio = 10
				temp = str()
				conf_i = float()
				if text.isalnum() and not text.isnumeric() and \
					len(text) >= 3 and not text in ['TARE', 'MAX'] and \
					(text[-1] == 'U' or len(text)==4) or (len(text) <=6 or len(text)>=3):
					for compname in COMPNAMES:
						ratio = self.weighted_levenshtein.distance(compname, text)
						if ratio < min_ratio:
							min_ratio = ratio
							temp = compname
							conf_i = (conf+1)/2
						else:
							min_ratio = min_ratio
				if temp in COMPNAMES:
					if len(text) > len(temp) and not text.isalpha():
						next_index = self.filtered_text.index([text, conf])+1
						new_text, new_conf = (text[-1] + self.filtered_text[next_index][0]), (conf+self.filtered_text[next_index][1])/2
						self.filtered_text.pop(next_index)
						self.filtered_text.insert(0, [new_text, new_conf])
					self.container_number_dict.update({'unique_owner': temp})
					self.temporary_list.append([text, conf])
					self.confidence_list.append(conf_i)
					break
		pass
	
	def get_serial_number(self):
		'''
		Get serial number  and replace result ocr
		if len text > 7 getting container digit
		'''
		new_text_conf = [elem for elem in self.filtered_text if elem not in self.temporary_list]
		text_minim = list()
		for text, conf in new_text_conf:
			if text.isalnum() and not text.isalpha() and len(text) in range(2, 9):
				if len(text) == 6:
					text_r, conf_r  = self.replace_word_serial_number(text, conf)
					if text_r.isnumeric():
						self.container_number_dict.update({'serial_number': text_r})
						self.confidence_list.append(conf_r)
						self.temporary_list.append([text, conf])
						break
					else: continue
				elif len(text) >= 7:
					text_r, conf_r  = self.replace_word_serial_number(text, conf)
					if text[0] == '1':
						text_m = (f'{self.container_number_dict["unique_owner"]}{text_r[:7]}')
						text_val = iso6346.is_valid(text_m)
						if text_val: text_r[1:]
						else: text_r = text_r[1:]

					number  = text_r[:6]
					digit   = text_r[-1]
					text_m = (f'{self.container_number_dict["unique_owner"]}{number}{digit}')
					text_val = iso6346.is_valid(text_m)
					if text_val:
						self.container_number_dict.update({'serial_number': number, 'container_digit' : digit})
						self.confidence_list.append(conf_r)
						self.temporary_list.append([text, conf])
						break
					else:
						self.container_number_dict.update({'serial_number': number})
						self.confidence_list.append(conf_r)
						self.temporary_list.append([text, conf])
						break
				elif len(text) <= 5 and not text in REMOVE_WORD:
					text_minim.append([text, conf])

		if len(text_minim) >= 2:
			for i in range(len(text_minim)):
				try:
					if text_minim[i][1] <= 0.25:
						text_1, conf_1 = self.replace_number_serial_number(text_minim[i][0], text_minim[i][1])
						text_2, conf_2 = self.replace_number_serial_number(text_minim[i+1][0], text_minim[i+1][1])
					else:
						text_1, conf_1 = text_minim[i][0], text_minim[i][1]
						text_2, conf_2 = text_minim[i+1][0], text_minim[i+1][1]
				except IndexError:
					continue
				text = text_1+text_2
				conf = (conf_1+conf_2)/2
				text_m = (f'{self.container_number_dict["unique_owner"]}{text}')
				text_val = iso6346.is_valid(text_m)
				if text_val:
					self.container_number_dict.update({'serial_number': text[0:6]})
					self.confidence_list.append(conf)
					break
				else:
					if len(text_minim)==2:
						text_r, conf_r = self.replace_word_serial_number(text, conf)
						if len(text_r) == 7:
							text_m = (f'{self.container_number_dict["unique_owner"]}{text}')
							text_val = iso6346.is_valid(text_m)
						elif len(text_r) == 6:
							text_m = (f'{self.container_number_dict["unique_owner"]}{text}')
							digit = iso6346.calc_check_digit(text_m)
							text_val = iso6346.is_valid(text_m+digit)
						else:
							text_m = (f'{self.container_number_dict["unique_owner"]}{text[:7]}')
							text_val = iso6346.is_valid(text_m)

						self.container_number_dict.update({'serial_number': text[0:6]})
						self.confidence_list.append(conf)
						break
					else:
						if len(text_m) == 10:
							digit = iso6346.calc_check_digit(text_m)
							self.container_number_dict.update({'serial_number': text_m[4:], 'container_digit': digit})
							break
		pass
	
	def get_digit_code(self):
		'''
		Get digit code
		'''
		new_text_conf = [elem for elem in self.filtered_text if elem not in self.temporary_list]
		digit = str()
		for text, conf in new_text_conf:
			text_r, conf_r  = self.replace_word_serial_number(text, conf)
			for text_i in text:
				text_m = (f'{self.container_number_dict["unique_owner"]}{self.container_number_dict["serial_number"]}{text_i}')
				text_val = iso6346.is_valid(text_m)
				if text_val:
					# digit = True
					self.container_number_dict.update({'container_digit': text_r})
					self.confidence_list.append(conf_r)
					break

		if not digit:
			text_m = (f'{self.container_number_dict["unique_owner"]}{self.container_number_dict["serial_number"]}')
			digit = iso6346.calc_check_digit(text_m)
			self.container_number_dict.update({'container_digit': digit})
			self.confidence_list.append(0.5)
		pass

	def calculate_confidence(self):
		'''
		Calculate avg confidence in confidence_list
		'''
		confidence_avg = round((sum(self.confidence_list)/len(self.confidence_list)),2)
		return confidence_avg
