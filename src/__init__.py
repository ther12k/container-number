import os
from turtle import end_fill
import cv2
import time
import matplotlib
import numpy as np

from src.app import CNICDetection, OneLenResult, OneMoreLenResult, OpticalCharacterRecognition

from pathlib import Path
from itertools import chain
from .utils import logging, draw_rectangle, datetime_format, sending_file
from config import DEVICE_ID, GATE_ID, ISO_CODE
from config import DATETIME_FORMAT,TIMEID_FORMAT,END_POINT,DELAY_IN_SECONDS,FTP_HOST, USER_NAME, USER_PASSWD
from .preproces import resize
from .proces import *

from io import BytesIO
import ftplib
import requests
from requests.exceptions import HTTPError
from datetime import datetime

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
		result_detection = self.cnic_detection.detection(image, image_size=size)
		container_number, iso_code = self.cnic_detection.filter_and_crop(
			img=image, results=result_detection, min_confidence=threshold
		)
		if len(container_number[0]) >=1 and container_number[1] > 0 and len(container_number[2]) == 4:
			logging.info(f'Got container number detection confidence : {round(container_number[1], 2)} %')

		if len(iso_code[0]) >=1 and iso_code[1] > 0 and len(iso_code[2]) == 4:
			logging.info(f'Got iso code detection confidence : {round(iso_code[1], 2)} %')
		return container_number, iso_code
	
	def chdir(self,ftp_path, ftp_conn):
		dirs = [d for d in ftp_path.split('/') if d != '']
		for p in dirs:
			self.check_dir(p, ftp_conn)


	def check_dir(dir, ftp_conn):
		filelist = []
		ftp_conn.retrlines('LIST', filelist.append)
		found = False

		for f in filelist:
			if f.split()[-1] == dir and f.lower().startswith('d'):
				found = True

		if not found:
			ftp_conn.mkd(dir)
		ftp_conn.cwd(dir)

	def img_upload(self,img,time_id):
		try:
			year, month, day, hour, _, _,_ = datetime_format()
			dest_path = f'/{GATE_ID}/{year}/{month}/{day}/'
			"""Transfer file to FTP."""
			# Connect
			session = ftplib.FTP(FTP_HOST, USER_NAME, USER_PASSWD)

			# Change to target dir
			self.chdir(dest_path,session)

			# Transfer file
			name = time_id.strftime(TIMEID_FORMAT)[:-4]
			file_name  = f'{DEVICE_ID}{name}.jpg'
			logging.info("Transferring %s to %s..." % (file_name,dest_path))
			print("Transferring %s to %s..." % (file_name,dest_path))
			#using memory, can also use file
			retval, buffer = cv2.imencode('.jpg', img)
			flo = BytesIO(buffer)
			session.storbinary('STOR %s' % os.path.basename(dest_path+file_name), flo)
			
			# Close session
			session.quit()
			return dest_path+file_name
		except:
			logging.info('error: upload file error')
			return 'error: upload file error'

	def send_data(file_path,start_time,end_time,
				container_number_result,container_number_avg_confidence,
				x_min_c,y_min_c,x_max_c,y_max_c,
				iso_code_result,iso_code_avg_confidence,
				x_min_i,y_min_i,x_max_i,y_max_i): 
		try:
			url= END_POINT+'container/'
			json_data = {
				'gateId': GATE_ID,
				'deviceId': 'container'+DEVICE_ID,
				'startTime': start_time.strftime(DATETIME_FORMAT),
				'EndTime': end_time.strftime(DATETIME_FORMAT),
				'delayInSeconds' : DELAY_IN_SECONDS,
				'container': {
					'result': container_number_result,
					'confidence': int(container_number_avg_confidence),
					'box' : {
						"x_min": x_min_c,
						"y_min": y_min_c,
						"x_max": x_max_c,
						"y_max": y_max_c
					},
					'filePath': file_path
				},
				'iso_code': {
					'result': iso_code_result,
					'confidence': int(iso_code_avg_confidence),
					'box' : {
						"x_min": x_min_i,
						"y_min": y_min_i,
						"x_max": x_max_i,
						"y_max": y_max_i
					},
					'filePath': file_path
				}
			}
			logging.info(json_data)
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
			
			logging.info(r)
			ret = r.json()
			return ret
		except HTTPError as e:
			logging.info(e.response.text)
		except:

			logging.info('error send')
			return 'send error'

	# def save_and_sending_file(self, file, id_file):
	# 	'''
	# 		Send image to server
	# 		Args:
	# 			file_path(str): path of image
	# 		Return:
				
	# 	'''
	# 	# Save File
	# 	year, month, day, hour, _, _,_ = datetime_format()
	# 	save_path = f'results/{year}/{month}/{day}/{hour}'
	# 	Path(save_path).mkdir(parents=True, exist_ok=True)
		
	# 	file_name   = f'{id_file}.jpg'
	# 	path_image  = f'{save_path}/{file_name}'
	# 	cv2.imwrite(f'{path_image}', file)
		
		# Send file to FTP server
		#server_path = f'{GATE}/{DEVICE_ID}/{year}-{month}-{day}_{hour}'
		#sender = sending_file(file_name=file_name, server_path=server_path)
		#if sender:
		#	os.remove(path_image)
			
		#pass
	
	def main(self, image, id=None):
		image_ori = image.copy()
		if not id: id = datetime.now()
		# Container Number Iso Code Detection
		draw_list = list()
		try:
			container_number, iso_code = self.__detection(image, size=480, threshold=0.1)
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
			x_min_c, y_min_c, x_max_c, y_max_c = 0, 0, 0, 0
			image_container_number,confidence_container_number, bbox_container_number = resize(image, 50, 50), 0, None
		
		if ISO_CODE:
			if len(iso_code[0]) >=1 and iso_code[1] > 0 and len(iso_code[2]) == 4:
				image_iso_code, confidence_iso_code, bbox_iso_code = iso_code[0], iso_code[1], iso_code[2]
				x_min_i, y_min_i, x_max_i, y_max_i = bbox_iso_code
				draw_list.append([[x_min_i, y_min_i, x_max_i, y_max_i], 'iso_code', confidence_container_number])
			else:
				x_min_i, y_min_i, x_max_i, y_max_i = 0, 0, 0, 0
				image_iso_code, confidence_iso_code, bbox_iso_code = resize(image, 100, 200), 0, None
		else: x_min_i, y_min_i, x_max_i, y_max_i = 0, 0, 0, 0
		# Thread Container Number and ISO Code

		container_number_result, container_number_avg_confidence = process_container_number(
			image, image_container_number, bbox_container_number
		)

		if ISO_CODE:
			iso_code_result, iso_code_avg_confidence = process_iso_code(
				image, image_iso_code, bbox_iso_code
			)
		else: iso_code_result, iso_code_avg_confidence = '', ''

		# Draw image and extract result
		new_draw_list = [
			[[x_min_c, y_min_c, x_max_c, y_max_c], container_number_result, container_number_avg_confidence],
			[[x_min_i, y_min_i, x_max_i, y_max_i], iso_code_result, iso_code_avg_confidence]
		]
		print(new_draw_list)
		for i in new_draw_list:
			image_drawed = draw_rectangle(image_ori, i)
			
		# Save and sending file FTP
		path = self.img_upload(image_drawed,id)
		if 'error' in path :
			path=''
		end_time = datetime.now()
		self.send_data(path,id,end_time,
				container_number_result,container_number_avg_confidence,
				x_min_c,y_min_c,x_max_c,y_max_c,
				iso_code_result,iso_code_avg_confidence,
				x_min_i,y_min_i,x_max_i,y_max_i)
		return image_drawed
