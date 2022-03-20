# import cv2
# import time
# import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# from threading import Thread, Event
# from matplotlib.gridspec import GridSpec

# from .utils.config_log import logging
# from .utils.draw_rectangle import draw_rectangle_list
# from .schema.config_ocr import ConfigOcr
# from config.config import SAVE_RESULT, ISO_CODE

# if ISO_CODE: from .app.extract_iso_code import ExtractIsoCode
# from .app.extract_container_number import OneLenResult, OneMoreLenResult
# from .app.container_number_iso_code_ocr import OpticalCharacterRecognition
# from .app.container_number_iso_code_detection import ContainerNumberIsoCodeDetection


# matplotlib.use('agg')

# model = ContainerNumberIsoCodeDetection()
# ocr   = OpticalCharacterRecognition()

# CONTAINER_NUMBER_ISO_CODE_DICT = dict()
# THREADS_LIST = list()

# def detection(image):
# 	'''
# 	Detection container number and iso code
# 	and filter clasess, confidence
# 	'''
# 	result_detection = model.prediction(image)
# 	container_number, iso_code = model.filter_and_crop(
# 		img=image, results=result_detection, min_confidence=0.1
# 	)
# 	if len(container_number[0]) >=1 and container_number[1] > 0 and len(container_number[2]) == 4:
# 		logging.info(f'Got container number detection confidence : {round(container_number[1], 2)} %')

# 	if len(iso_code[0]) >=1 and iso_code[1] > 0 and len(iso_code[2]) == 4:
# 		logging.info(f'Got iso code detection confidence : {round(iso_code[1], 2)} %')
# 	return container_number, iso_code

# def resize(image, height_percent=180, width_percent=180):
# 	'''
# 	resize image by percent
# 	'''
# 	height = int(image.shape[0] * height_percent / 100)
# 	width = int(image.shape[1] * width_percent / 100)
# 	dim = (width, height)
# 	new_img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
# 	logging.info(f'Resize image to : {image.shape}')
# 	return new_img

# def detect_char(image):
# 	detected_char = ocr.detect_char(image)
# 	logging.info(detected_char)
# 	if detected_char[0]:
# 		logging.info(f'Found text in image : {" ".join([str(i) for i in detected_char[0]])}')
# 		return True
# 	else:
# 		logging.info(f'Not found text in image')
# 		return None

# def get_position_text(image):
# 	'''
# 	Vertical or Horizontal text in image
# 	'''
# 	height, width = image.shape[0], image.shape[1]
# 	position = 'horizontal' if height < width else 'vertical'
# 	logging.info(f'Text position : {position}')
# 	return position

# def read_text(image, position_text='horizontal', clasess_name='container_number'):
# 	'''
# 	Set methods and value config ocr
# 	methods view schema/config_ocr.py
# 	'''
# 	if position_text == 'horizontal':
# 		config = ConfigOcr(
# 			beam_width      = 20,
# 			batch_size      = 8,
# 			text_threshold  = 0.4,
# 			link_threshold  = 0.7,
# 			low_text        = 0.4,
# 			slope_ths       = 0.9,
# 			add_margin 		= 0.3
# 		)
# 	elif position_text == 'vertical':
# 		config = ConfigOcr(
# 			batch_size  	= 10,
# 			text_threshold 	= 0.2,
# 			link_threshold 	= 0.9,
# 			low_text 		= 0.4,
# 			add_margin		= 0
# 		)

# 	results = ocr.ocr_image(image=image, config=config, clasess_name=clasess_name)
# 	if position_text == 'horizontal': results.sort(reverse=False)
# 	else : results = results
# 	logging.info(f'Ocr {clasess_name} : {" ".join([i[1] for i in results])}')
# 	return results

# def filter_text_conf(text_conf):
# 	'''
# 	Remove space in list text_conf and add create new list
# 	'''
# 	new_text_conf = list()
# 	for text, conf in text_conf:
# 		remove_space = text.split(' ')
# 		for word in remove_space:
# 			if word.isalnum():
# 				new_text_conf.append([word, conf])
# 	return new_text_conf

# def result_container_number_processing(results_ocr):
# 	'''
# 	Processing results ocr 
# 	retrun text, conf in func filter text
# 	and extract text to get conf, container_number
# 	'''
# 	if len(results_ocr) >= 1:
# 		text_conf_list  = [[i[1], i[2]] for i in results_ocr]
# 		filtered_text 	= filter_text_conf(text_conf_list)
# 		# Get len mode text
# 		len_char_list 	= [len(i[0]) for i in filtered_text]
# 		if not 4 in len_char_list and not 6 in len_char_list:
# 			mode_len_char = max(len_char_list, key = len_char_list.count)
# 		else : mode_len_char = 0

# 		if mode_len_char == 1:
# 			text = ''.join([i[0] for i in filtered_text])
# 			confidence = sum([i[1] for i in filtered_text])/len(filtered_text)
# 			filtered_text = [[text, confidence]]
# 		logging.info(f'List for text processing : {filtered_text}')
		
# 		try:
# 			if len(filtered_text) == 1:
# 				text_procesiing = OneLenResult(filtered_text)
# 			else: 
# 				text_procesiing = OneMoreLenResult(filtered_text)

# 			container_number_dict = text_procesiing.container_number_dict
# 			confidence_level = text_procesiing.confidence_level

# 			container_number = container_number_dict['unique_owner']+container_number_dict['serial_number']+container_number_dict['container_digit']
# 			avg_confidence = round(confidence_level, 2)
# 		except KeyError:
# 			container_number 	= ''.join([i[0] for i in filtered_text])
# 			avg_confidence 		= round((sum([i[1] for i in filtered_text])/len(filtered_text)), 2)
# 	else:
# 		try:
# 			container_number	= ''.join([i[1] for i in results_ocr])
# 			avg_confidence		= round((sum([i[2] for i in results_ocr])/len(results_ocr)), 2)
# 		except ZeroDivisionError:
# 			container_number 	= ''
# 			avg_confidence		= 0

# 	logging.info(f'Container Number : {container_number}')
# 	logging.info(f'Confidence Level : {avg_confidence*100} %')
# 	return container_number, avg_confidence

# def result_iso_code_processing(results_ocr):
# 	if len(results_ocr) >= 1:
# 		text_conf_list  = [[i[1], i[2]] for i in results_ocr]
# 		filtered_text 	= filter_text_conf(text_conf_list)
# 		# Get len mode text
# 		len_char_list 	= [len(i[0]) for i in filtered_text]
# 		if not 4 in len_char_list:
# 			mode_len_char = max(len_char_list, key = len_char_list.count)
# 		else : mode_len_char = 0

# 		if mode_len_char == 1:
# 			text = ''.join([i[0] for i in filtered_text])
# 			confidence = sum([i[1] for i in filtered_text])/len(filtered_text)
# 			filtered_text = [[text, confidence]]
# 		logging.info(f'List for text processing : {filtered_text}')
# 		try:
# 			text_processing = ExtractIsoCode(filtered_text)
# 			iso_code_dict = text_processing.iso_code_dict
# 			confidence_level = text_processing.confidence_level
# 			iso_code = iso_code_dict['iso_code']
# 			avg_confidence = round(confidence_level, 2)
# 		except KeyError:
# 			iso_code = None
# 			avg_confidence = 0
# 	else:
# 		iso_code = None
# 		avg_confidence = 0
# 	logging.info(f'Iso Code : {iso_code}') 
# 	logging.info(f'Confidence Level : {avg_confidence*100} %')
# 	return iso_code, avg_confidence

# def process_container_number(image, image_detection, bbox):
# 	'''
# 	Preprocessing image (resize image, detect char and get position text)
# 	for ocr container number, return container_number and avg_confidence 
# 	in results ocr processing
# 	'''
# 	global CONTAINER_NUMBER_ISO_CODE_DICT

# 	if bbox:
# 		# resize image
# 		image_crop = resize(image_detection) if image_detection.shape[1] <= 175 else image_detection
# 		# detect char
# 		detected_char = detect_char(image_crop)
# 		# retrun image for ocr
# 		image_crop = image_crop if detected_char else resize(image, 50, 50)
# 	else :
# 		image_crop = resize(image, 70, 70)
	
# 	# get position text
# 	position_text = get_position_text(image_crop)
	
# 	# resize image position vertical and get diffrence value
# 	if position_text == 'vertical':
# 		# get difference h, w
# 		difference = abs((image_crop.shape[0])-image_crop.shape[1])
# 		if difference > 100:
# 			if bbox: image_crop =resize(image_crop, 120, 150) #resize(image_crop, 150, 180)
# 			else : image_crop = resize(image_crop, 100, 127)
# 		elif difference < 100:
# 			image_crop = resize(image, 50, 50)
	
# 	# read text in image
# 	results_ocr = read_text(image_crop, position_text, 'container_number')
# 	container_number, avg_confidence = result_container_number_processing(results_ocr)
# 	CONTAINER_NUMBER_ISO_CODE_DICT.update({
# 		'container_number' : {
# 			'result_ocr': container_number,
# 			'confidence': avg_confidence
# 		}
# 	})
# 	# return container_number, avg_confidence

# def process_iso_code(image, image_detection, bbox):
# 	'''
# 	Preprocessing image (resize image, detect char and get position text)
# 	for ocr container number, return container_number and avg_confidence 
# 	in results ocr processing
# 	'''
# 	global CONTAINER_NUMBER_ISO_CODE_DICT

# 	if bbox:
# 		# resize image
# 		image_crop = resize(image_detection, 150, 200)
# 		# detect char
# 		detected_char = detect_char(image_crop)
# 		# retrun image for ocr
# 		image_crop = image_crop if detected_char else resize(image, 50, 50)
# 	else :
# 		image_crop = resize(image, 50, 50)
	
# 	# get position text
# 	position_text = get_position_text(image_crop)
	
# 	# resize image position vertical and get diffrence value
# 	if position_text == 'vertical':
# 		# get difference h, w
# 		difference = abs((image_crop.shape[0])-image_crop.shape[1])
# 		logging.info(difference)
# 		if difference > 10:
# 			if bbox: image_crop = resize(image_crop, 100, 100)
# 			else : image_crop = resize(image_crop, 100, 127)
# 		elif difference < 10:
# 			image_crop = resize(image, 50, 100)
	
# 	# read text in image
# 	results_ocr = read_text(image_crop, position_text, 'iso_code')
# 	iso_code, avg_confidence = result_iso_code_processing(results_ocr)
# 	CONTAINER_NUMBER_ISO_CODE_DICT.update({
# 		'iso_code' : {
# 			'result_ocr': iso_code,
# 			'confidence': avg_confidence
# 		}
# 	})
# 	# return iso_code, avg_confidence
	
# def visualisasi_process(img_prediction, img_crop, img_ocr, container_number, avg_confidence, preocess_time):
# 	def format_axes(fig):
# 		for i, ax in enumerate(fig.axes):
# 			# ax.xlabel(0.5, 0.5, "ax%d" % (i+1), va="center_baseline")
# 			ax.tick_params(labelbottom=False, labelleft=False)

# 	fig = plt.figure(constrained_layout=True, dpi=140)

# 	gs = GridSpec(23, 16, figure=fig)
# 	ax1 = fig.add_subplot(gs[2:15, :])
# 	ax2 = fig.add_subplot(gs[15:19, 3:8])
# 	ax3 = fig.add_subplot(gs[15:19, 8:-3])
# 	ax4 = fig.add_subplot(gs[20:23, :])

# 	fig.suptitle('PT. Halotec Indonesia \n Realtime OCR Container Number', fontsize=10)

# 	format_axes(fig)
# 	ax1.imshow(img_prediction)
# 	ax2.imshow(img_crop)
# 	ax3.imshow(img_ocr)

# 	ax1.set_title('Input Image', fontsize=8)
# 	ax2.set_title('Container Number Detection', fontsize=8)
# 	ax3.set_title('OCR Container Number', fontsize=8)
# 	ax4.set_title('Result', fontsize=8)

# 	result_text_vis = (
# 		f'Container Number : {container_number} | ' 
# 		f'Confidence Level : {avg_confidence*100:.2f} % | '
# 		f'Processing Time : {preocess_time} s'
# 	)
# 	ax4.text(0.5, 0.5, result_text_vis, ha='center', va='center', fontsize=8)

# 	plt.savefig(f'assets/test-img/webcam/new_results/{container_number}-new.png')
# 	logging.info(f'Done saved {container_number}.png')
# 	plt.close()
# 	pass

# def main_process(image):
# 	global CONTAINER_NUMBER_ISO_CODE_DICT, THREADS_LIST
# 	start_time = time.time()
# 	draw_list = list()
# 	# detection container number
# 	try:
# 		container_number, iso_code = detection(image)
# 	except:
# 		container_number = (np.array([], dtype=np.uint8), 0, list())
# 		iso_code         = (np.array([], dtype=np.uint8), 0, list())
# 		logging.info('Not found object detection')
	
# 	# Get image crop (container number, iso code) and get bbox (container number and iso code)
# 	if len(container_number[0]) >=1 and container_number[1] > 0 and len(container_number[2]) == 4:
# 		image_container_number, confidence_container_number, bbox_container_number = \
# 		container_number[0], container_number[1], container_number[2]
# 		x_min, y_min, x_max, y_max = bbox_container_number
# 		draw_list.append([x_min, y_min, x_max, y_max, 'container_number', confidence_container_number])
# 	else:
# 		image_container_number,confidence_container_number, bbox_container_number = resize(image, 50, 50), 0, None

# 	if ISO_CODE:
# 		if len(iso_code[0]) >=1 and iso_code[1] > 0 and len(iso_code[2]) == 4:
# 			image_iso_code, confidence_iso_code, bbox_iso_code = iso_code[0], iso_code[1], iso_code[2]
# 			x_min, y_min, x_max, y_max = bbox_iso_code
# 			draw_list.append([x_min, y_min, x_max, y_max, 'iso_code', confidence_container_number])
# 		else:
# 			image_iso_code, confidence_iso_code, bbox_iso_code = resize(image, 100, 200), 0, None
	
# 	# Process thred container number and iso code
# 	processed_container_number = Thread(
# 		target=process_container_number,
# 		args=(image, image_container_number, bbox_container_number, )
# 	)

# 	if ISO_CODE: 
# 		processed_iso_code = Thread(
# 			target=process_iso_code,
# 			args=(image, image_iso_code, bbox_iso_code, )
# 		)
# 	processed_container_number.start()
# 	if ISO_CODE : processed_iso_code.start()
	
# 	processed_container_number.join()
# 	if ISO_CODE: processed_iso_code.join()

# 	end_time = round((time.time()-start_time), 2)
# 	CONTAINER_NUMBER_ISO_CODE_DICT.update({'processing_time': end_time})

# 	# Draw_rectangle
# 	print(draw_list)
# 	image_encoded = draw_rectangle_list(image, draw_list, encoded=True)
# 	CONTAINER_NUMBER_ISO_CODE_DICT.update({'image': image_encoded})
# 	# visualisasi prediction and ocr image
# 	if SAVE_RESULT:
# 		if bbox:
# 			draw_image_prediction = container_number_detection.draw_boxes(image, bbox)
# 		else : draw_image_prediction = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 		if container_number:
# 			draw_image_ocr, _, _ = container_number_ocr.draw_boxes(image_crop, results_ocr)
# 		else: draw_image_ocr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# 		# cv2.imwrite('prediction.jpg', cv2.cvtColor(np.asarray(draw_image_prediction),cv2.COLOR_RGB2BGR))
# 		# cv2.imwrite('ocr.jpg', cv2.cvtColor(np.asarray(draw_image_ocr),cv2.COLOR_RGB2BGR))
		
# 		visualisasi_process(draw_image_prediction, cv2.cvtColor(image_crop, cv2.COLOR_BGR2RGB),
# 			draw_image_ocr, container_number, avg_confidence, end_time)

# 	return CONTAINER_NUMBER_ISO_CODE_DICT