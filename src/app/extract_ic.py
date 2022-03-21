from similarity.weighted_levenshtein import (CharacterSubstitutionInterface,
											 WeightedLevenshtein)
from config import  ISO_CODE_LIST, COMPNAMES

'''
Add cost substituting word in compnames and result ocr
'''
class CharacterSubstitution(CharacterSubstitutionInterface):
	def cost(self, c0, c1):
		# print('df',c0)
		if c0 == 'G' and c1 == '6': return 0.5
		if c0 == 'G' and c1 == '5': return 0.5
		if c0 == '4' and c1 == 'A': return 0.5
		if c0 == '1' and c1 == 'I': return 0.5
		if c0 == 'T' and c1 == '1': return 0.4
		return 1.0

'''
Text processing to get iso_code_dict
with algoritm WeightedLevenshtein for correction iso code
'''
class ExtractIsoCode:
	def __init__(self, filtered_text):
		self.weighted_levenshtein = WeightedLevenshtein(CharacterSubstitution())
		self.filtered_text = filtered_text
		self.iso_code_dict = dict()
		self.confidence_list = list()
		self.get_iso_code()
		self.confidence_level = self.calculate_confidence()

	def get_iso_code(self):
		'''
		Filtered len(text) == 4 and
		Get unique owner with algoritm weighted_levenshtein
		and update confidence (conf+1)/2
		'''
		text_list = [text for text,_ in self.filtered_text]
		conf_list = [conf for _,conf in self.filtered_text]
		index = [i for i,x in enumerate(text_list) if len(x) == 4]
		if index:
			min_ratio = 10
			temp = str()
			conf_i = float()
			for i in index:
				for iso_code in ISO_CODE_LIST:
					ratio = self.weighted_levenshtein.distance(iso_code, text_list[i])
					if ratio < min_ratio:
						min_ratio = ratio
						temp = iso_code
						conf_i = (conf_list[i]+1)/2
					else:
						min_ratio = min_ratio
						temp = temp
						conf_i = conf_i

			if int(min_ratio) < 2 and temp in ISO_CODE_LIST:
				self.iso_code_dict.update({'iso_code': temp})
				self.confidence_list.append(conf_i)
			else: self.get_more_iso_code()
		else: self.get_more_iso_code()
		pass
	
	def get_more_iso_code(self):
		'''
		filtered text with minimum pattren iso code
		Get unique owner with algoritm weighted_levenshtein
		and update confidence (conf+1)/2
		'''
		min_ratio = 10
		temp = str()
		conf_i = float()
		for text, conf in self.filtered_text:
			if text.isalnum() and len(text) in range(3, 5) and not text in COMPNAMES:
				for iso_code in ISO_CODE_LIST:
					ratio = self.weighted_levenshtein.distance(iso_code, text)
					if ratio < min_ratio:
						min_ratio = ratio
						temp = iso_code
						conf_i = (conf+1)/2
					else:
						min_ratio = min_ratio
						temp = temp
						conf_i = conf_i
		if int(min_ratio) <= 4 and temp in ISO_CODE_LIST:
			self.iso_code_dict.update({'iso_code': temp})
			self.confidence_list.append(conf_i)
		else:
			self.iso_code_dict.update({'iso_code': None})
			self.confidence_list.append(0)
		pass
	
	def calculate_confidence(self):
		'''
		Calculate avg confidence in confidence_list
		'''
		confidence_avg = round((sum(self.confidence_list)/len(self.confidence_list)),2)
		return confidence_avg