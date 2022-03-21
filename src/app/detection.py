import os
import sys
import torch
import requests
from tqdm import tqdm
from pathlib import Path
import numpy as np

from config import(
	DIRECTORY_MODEL, 
	DETECTION_MODEL,
	CLASSES_DETECTION
)

class CNICDetection:
	'''
	Load custom model YoloV5
	for detection  container number and iso code
	'''
	def __init__(self, model_name):
		self.model_name = model_name
		self.device     = 'cuda' if torch.cuda.is_available() else 'cpu'
		self.model_path = os.path.join(DIRECTORY_MODEL, DETECTION_MODEL[self.model_name]['filename'])
		self.__check_model()
		self.model      = self.__load_model(self.model_path)
		

	@staticmethod
	def __load_model(model_path):
		try: model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		except: sys.exit('Error load model')
		return model
			
	def __check_model(self):
		'''
		Checking model in model_path
		download model if file not found
		'''
		Path(DIRECTORY_MODEL).mkdir(parents=True, exist_ok=True)
		if not os.path.isfile(self.model_path):
			print(f'Downloading {self.model_name} detection model, please wait.')
			response = requests.get(DETECTION_MODEL[self.model_name]['url'], stream=True)
			
			progress = tqdm(response.iter_content(1024), 
						f'Downloading {DETECTION_MODEL[self.model_name]["filename"]}', 
						total=DETECTION_MODEL[self.model_name]['file_size'], unit='B', 
						unit_scale=True, unit_divisor=1024)
			with open(self.model_path, 'wb') as f:
				for data in progress:
					f.write(data)
					progress.update(len(data))
				print(f'Done downloaded {DETECTION_MODEL[self.model_name]["filename"]} detection model.')
		else:
			print(f'Load {DETECTION_MODEL[self.model_name]["filename"]} detection model.')

	@staticmethod
	def filter_and_crop(img, results, min_confidence=0.2):
		'''
		Format result(
			[tensor([[586.12500,  58.78125, 729.37500,  88.03125,   0.93164,   0.00000],
			[646.12500,  84.46875, 682.12500, 108.28125,   0.90234,   1.00000]], device='cuda:0')]
		)
		Filter min confidence prediction and classes id/label (container_number or iso_code)
		Cropped image and get index max value confidence lavel
		and retrun (container_number, iso_code) -> (image, confidence, bbox)
		'''
		max_conf_container_number, img_container_number, bbox_container_number  = 0, np.array([], dtype=np.uint8), list()
		max_conf_iso_code, img_iso_code, bbox_iso_code                          = 0, np.array([], dtype=np.uint8), list()
		results_format = results.xyxy
		print(results_format)
		if len(results_format[0]) >= 1:
			for i in range(len(results_format[0])):
				classes_name = CLASSES_DETECTION[int(results_format[0][i][-1])]
				confidence = float(results_format[0][i][-2])
				
				if classes_name == 'container_number' and confidence >= min_confidence:
					if confidence > max_conf_container_number:
						max_conf_container_number = confidence
						x1, y1 = int(results_format[0][i][0]), int(results_format[0][i][1])
						x2, y2 = int(results_format[0][i][2]), int(results_format[0][i][3])
						cropped_img = img[y1-5 : y2+5, x1-5 : x2+5]
						bbox_container_number = [x1-5, y1-5, x2+5, y2+5]
						img_container_number = cropped_img
					else:
						max_conf_container_number   = max_conf_container_number
						bbox_container_number       = bbox_container_number
						img_container_number        = img_container_number

				if classes_name == 'iso_code' and confidence >= min_confidence:
					if confidence > max_conf_iso_code:
						max_conf_iso_code = confidence
						x1, y1 = int(results_format[0][i][0]), int(results_format[0][i][1])
						x2, y2 = int(results_format[0][i][2]), int(results_format[0][i][3])
						cropped_img = img[y1-20 : y2+20, x1-20 : x2+20]
						bbox_iso_code = [x1-20, y1-20, x2+20, y2+20]
						img_iso_code = cropped_img
					else:
						max_conf_iso_code   = max_conf_iso_code
						bbox_iso_code       = bbox_iso_code
						img_iso_code        = img_iso_code
		else:
			max_conf_container_number, img_container_number, bbox_container_number  = 0, np.array([], dtype=np.uint8), list()
			max_conf_iso_code, img_iso_code, bbox_iso_code                          = 0, np.array([], dtype=np.uint8), list()

		container_number = (img_container_number, max_conf_container_number, bbox_container_number)
		iso_code         = (img_iso_code, max_conf_iso_code, bbox_iso_code)

		return (container_number, iso_code)

	@staticmethod
	def release():
		'''
			Empty cache cuda memory
		'''
		torch.cuda.empty_cache()
	
	def detection(self, image, image_size=None):
		'''
		Prediction image object detectionn YoloV5
		Args:
			image(numpy.ndarray) : image/frame
		Return:
			results_prediction(models.common.Detections) : results -> convert to (results.xyxy/resultsxywh)
		'''
		if image_size: results = self.model(image, size=image_size)
		else: results = self.model(image)
		return results
