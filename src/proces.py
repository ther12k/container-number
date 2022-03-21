from .schemas import ConfigOcr
from .utils import logging
from .preproces import resize, get_position_text, filter_text_conf
from src.app import (
    OneLenResult, 
    OneMoreLenResult,
    ExtractIsoCode,
    OpticalCharacterRecognition
)

ocr   = OpticalCharacterRecognition()

def detect_char(image):
	detected_char = ocr.detect_char(image)
	logging.info(detected_char)
	if detected_char[0]:
		logging.info(f'Found text in image : {" ".join([str(i) for i in detected_char[0]])}')
		return True
	else:
		logging.info(f'Not found text in image')
		return None

def read_text(image, position_text='horizontal', clasess_name='container_number'):
	'''
	Set methods and value config ocr
	methods view schema/config_ocr.py
	'''
	if position_text == 'horizontal':
		config = ConfigOcr(
			beam_width      = 20,
			batch_size      = 8,
			text_threshold  = 0.4,
			link_threshold  = 0.7,
			low_text        = 0.4,
			slope_ths       = 0.9,
			add_margin 		= 0.3
		)
	elif position_text == 'vertical':
		config = ConfigOcr(
			batch_size  	= 10,
			text_threshold 	= 0.2,
			link_threshold 	= 0.9,
			low_text 		= 0.4,
			add_margin		= 0
		)

	results = ocr.ocr_image(image=image, config=config, clasess_name=clasess_name)
	if position_text == 'horizontal': results.sort(reverse=False)
	else : results = results
	logging.info(f'Ocr {clasess_name} : {" ".join([i[1] for i in results])}')
	return results

def result_container_number_processing(results_ocr):
	'''
	Processing results ocr 
	retrun text, conf in func filter text
	and extract text to get conf, container_number
	'''
	if len(results_ocr) >= 1:
		text_conf_list  = [[i[1], i[2]] for i in results_ocr]
		filtered_text 	= filter_text_conf(text_conf_list)
		# Get len mode text
		len_char_list 	= [len(i[0]) for i in filtered_text]
		if not 4 in len_char_list and not 6 in len_char_list:
			mode_len_char = max(len_char_list, key = len_char_list.count)
		else : mode_len_char = 0

		if mode_len_char == 1:
			text = ''.join([i[0] for i in filtered_text])
			confidence = sum([i[1] for i in filtered_text])/len(filtered_text)
			filtered_text = [[text, confidence]]
		logging.info(f'List for text processing : {filtered_text}')
		
		try:
			if len(filtered_text) == 1:
				text_procesiing = OneLenResult(filtered_text)
			else: 
				text_procesiing = OneMoreLenResult(filtered_text)

			container_number_dict = text_procesiing.container_number_dict
			confidence_level = text_procesiing.confidence_level

			container_number = container_number_dict['unique_owner']+container_number_dict['serial_number']+container_number_dict['container_digit']
			avg_confidence = round(confidence_level, 2)
		except KeyError:
			container_number 	= ''.join([i[0] for i in filtered_text])
			avg_confidence 		= round((sum([i[1] for i in filtered_text])/len(filtered_text)), 2)
	else:
		try:
			container_number	= ''.join([i[1] for i in results_ocr])
			avg_confidence		= round((sum([i[2] for i in results_ocr])/len(results_ocr)), 2)
		except ZeroDivisionError:
			container_number 	= ''
			avg_confidence		= 0

	logging.info(f'Container Number : {container_number}')
	logging.info(f'Confidence Level : {avg_confidence*100} %')
	return container_number, avg_confidence

def result_iso_code_processing(results_ocr):
	if len(results_ocr) >= 1:
		text_conf_list  = [[i[1], i[2]] for i in results_ocr]
		filtered_text 	= filter_text_conf(text_conf_list)
		# Get len mode text
		len_char_list 	= [len(i[0]) for i in filtered_text]
		if not 4 in len_char_list:
			mode_len_char = max(len_char_list, key = len_char_list.count)
		else : mode_len_char = 0

		if mode_len_char == 1:
			text = ''.join([i[0] for i in filtered_text])
			confidence = sum([i[1] for i in filtered_text])/len(filtered_text)
			filtered_text = [[text, confidence]]
		logging.info(f'List for text processing : {filtered_text}')
		try:
			text_processing = ExtractIsoCode(filtered_text)
			iso_code_dict = text_processing.iso_code_dict
			confidence_level = text_processing.confidence_level
			iso_code = iso_code_dict['iso_code']
			avg_confidence = round(confidence_level, 2)
		except KeyError:
			iso_code = ''
			avg_confidence = 0
	else:
		iso_code = None
		avg_confidence = 0
	logging.info(f'Iso Code : {iso_code}') 
	logging.info(f'Confidence Level : {avg_confidence*100} %')
	return iso_code, avg_confidence

def process_container_number(image, image_detection, bbox):
	'''
	Preprocessing image (resize image, detect char and get position text)
	for ocr container number, return container_number and avg_confidence 
	in results ocr processing
	'''
	#global CONTAINER_NUMBER_ISO_CODE_DICT

	if bbox:
		# resize image
		image_crop = resize(image_detection) if image_detection.shape[1] <= 175 else image_detection
		# detect char
		detected_char = detect_char(image_crop)
		# retrun image for ocr
		image_crop = image_crop if detected_char else resize(image, 50, 50)
	else :
		image_crop = resize(image, 70, 70)
	
	# get position text
	position_text = get_position_text(image_crop)
	
	# resize image position vertical and get diffrence value
	if position_text == 'vertical':
		# get difference h, w
		difference = abs((image_crop.shape[0])-image_crop.shape[1])
		if difference > 100:
			if bbox: image_crop =resize(image_crop, 120, 150) #resize(image_crop, 150, 180)
			else : image_crop = resize(image_crop, 100, 127)
		elif difference < 100:
			image_crop = resize(image, 50, 50)
	
	# read text in image
	results_ocr = read_text(image_crop, position_text, 'container_number')
	# Extract container number
	container_number, avg_confidence = result_container_number_processing(results_ocr)
	return container_number, avg_confidence
 
def process_iso_code(image, image_detection, bbox):
	'''
	Preprocessing image (resize image, detect char and get position text)
	for ocr container number, return container_number and avg_confidence 
	in results ocr processing
	'''

	if bbox:
		# resize image
		image_crop = resize(image_detection, 150, 200)
		# detect char
		detected_char = detect_char(image_crop)
		# retrun image for ocr
		image_crop = image_crop if detected_char else resize(image, 50, 50)
	else :
		image_crop = resize(image, 50, 50)
	
	# get position text
	position_text = get_position_text(image_crop)
	
	# resize image position vertical and get diffrence value
	if position_text == 'vertical':
		# get difference h, w
		difference = abs((image_crop.shape[0])-image_crop.shape[1])
		logging.info(difference)
		if difference > 10:
			if bbox: image_crop = resize(image_crop, 100, 100)
			else : image_crop = resize(image_crop, 100, 127)
		elif difference < 10:
			image_crop = resize(image, 50, 100)

	# read text in image
	results_ocr = read_text(image_crop, position_text, 'iso_code')
	iso_code, avg_confidence = result_iso_code_processing(results_ocr)
	return iso_code, avg_confidence
