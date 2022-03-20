import cv2
from .utils import logging

def resize(image, height_percent=180, width_percent=180):
	'''
	resize image by percent
	'''
	height = int(image.shape[0] * height_percent / 100)
	width = int(image.shape[1] * width_percent / 100)
	dim = (width, height)
	new_img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	
	return new_img

def get_position_text(image):
	'''
	Vertical or Horizontal text in image
	'''
	height, width = image.shape[0], image.shape[1]
	position = 'horizontal' if height < width else 'vertical'
	logging.info(f'Text position : {position}')
	return position

def filter_text_conf(text_conf):
	'''
	Remove space in list text_conf and add create new list
	'''
	new_text_conf = list()
	for text, conf in text_conf:
		remove_space = text.split(' ')
		for word in remove_space:
			if word.isalnum():
				new_text_conf.append([word, conf])
	return new_text_conf