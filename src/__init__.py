import os
import cv2
import time
import matplotlib
import numpy as np

from src.app import CNICDetection, OneLenResult, OneMoreLenResult, OpticalCharacterRecognition

from pathlib import Path
from itertools import chain
from .utils import logging, draw_rectangle, datetime_format, sending_file
from config import ID_DEVICE, GATE, ISO_CODE

from .preproces import resize
from .proces import *

class MainProcess:
	'''
		Main process seal detection
	'''
	def __init__(self):
		self.cnic_detection = CNICDetection('container_number_iso_code')

	def __detection(self, image, size, threshold):
		'''
		Detection container number and iso code
		and filter clasess, confidence
		'''
		result_detection = self.cnic_detection.detection(image)
		container_number, iso_code = self.cnic_detection.filter_and_crop(
			img=image, results=result_detection, min_confidence=threshold
		)
		if len(container_number[0]) >=1 and container_number[1] > 0 and len(container_number[2]) == 4:
			logging.info(f'Got container number detection confidence : {round(container_number[1], 2)} %')

		if len(iso_code[0]) >=1 and iso_code[1] > 0 and len(iso_code[2]) == 4:
			logging.info(f'Got iso code detection confidence : {round(iso_code[1], 2)} %')
		return container_number, iso_code
	
	def save_and_sending_file(self, file, id_file):
		'''
			Send image to server
			Args:
				file_path(str): path of image
			Return:
				
		'''
		# Save File
		year, month, day, hour, _, _,_ = datetime_format()
		save_path = f'results/{year}/{month}/{day}/{hour}'
		Path(save_path).mkdir(parents=True, exist_ok=True)
		
		file_name   = f'{id_file}.jpg'
		path_image  = f'{save_path}/{file_name}'
		cv2.imwrite(f'{path_image}', file)
		
		# Send file to FTP server
		server_path = f'{GATE}/{ID_DEVICE}/{year}-{month}-{day}_{hour}'
		sender = sending_file(file_name=file_name, server_path=server_path)
		if sender:
			os.remove(path_image)
			
		pass
	
	def main(self, image, id=None):
		image_ori = image.copy()
		if not id: id = int(time.time())
		# Container Number Iso Code Detection
		draw_list = list()
		try:
			container_number, iso_code = self.__detection(image, size=0.1, threshold=0.1)
		except:
			container_number 	= (np.array([], dtype=np.uint8), 0, list())
			iso_code         	= (np.array([], dtype=np.uint8), 0, list())
			image_drawed		= image_ori
			logging.info('Not found object detection')

		
		# Get image crop (container number, iso code) and get bbox (container number and iso code)
		if len(container_number[0]) >=1 and container_number[1] > 0 and len(container_number[2]) == 4:
			image_container_number, confidence_container_number, bbox_container_number = \
			container_number[0], container_number[1], container_number[2]
			x_min_c, y_min_c, x_max_c, y_max_c = bbox_container_number
			draw_list.append([[x_min_c, y_min_c, x_max_c, y_max_c], 'container_number', confidence_container_number])
		else:
			x_min_c, y_min_c, x_max_c, y_max_c = None, None, None, None
			image_container_number,confidence_container_number, bbox_container_number = resize(image, 50, 50), 0, None
		
		if ISO_CODE:
			if len(iso_code[0]) >=1 and iso_code[1] > 0 and len(iso_code[2]) == 4:
				image_iso_code, confidence_iso_code, bbox_iso_code = iso_code[0], iso_code[1], iso_code[2]
				x_min_i, y_min_i, x_max_i, y_max_i = bbox_iso_code
				draw_list.append([[x_min_i, y_min_i, x_max_i, y_max_i], 'iso_code', confidence_container_number])
			else:
				x_min_i, y_min_i, x_max_i, y_max_i = None, None, None, None
				image_iso_code, confidence_iso_code, bbox_iso_code = resize(image, 100, 200), 0, None
		else: x_min_i, y_min_i, x_max_i, y_max_i = None, None, None, None
		# Thread Container Number and ISO Code

		container_number_result, container_number_avg_confidence = process_container_number(
			image, image_container_number, bbox_container_number
		)

		if ISO_CODE:
			iso_code_result, iso_code_avg_confidence = process_iso_code(
				image, image_iso_code, bbox_iso_code
			)
		else: iso_code_result, iso_code_avg_confidence = None, None

		end_time = int(time.time()-id)
  
		result_json = {
			'container_number': {
				'result_ocr': container_number_result,
				'confidence': container_number_avg_confidence,
				'box' : {
					"x_min": x_min_c,
					"y_min": y_min_c,
					"x_max": x_max_c,
					"y_max": y_max_c
				}
			},
			'iso_code': {
				'result_ocr': iso_code_result,
				'confidence': iso_code_avg_confidence,
				'box' : {
					"x_min": x_min_i,
					"y_min": y_min_i,
					"x_max": x_max_i,
					"y_max": y_max_i
				}
			},
			'processing_time': end_time,
			'id_device': ID_DEVICE,
			'id': id
		}

		# Draw image and extract result
		new_draw_list = [
			[[x_min_c, y_min_c, x_max_c, y_max_c], container_number_result, container_number_avg_confidence],
			[[x_min_i, y_min_i, x_max_i, y_max_i], iso_code_result, iso_code_avg_confidence]
		]
		print(result_json)
		for i in new_draw_list:
			image_drawed = draw_rectangle(image_ori, i)
			
		# Save and sending file FTP
		self.save_and_sending_file(image_drawed, id)
		return image_drawed