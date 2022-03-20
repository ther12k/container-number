import cv2
import time

from src import MainProcess
from src.utils.camera import Camera
from src.utils import Adam6060Output

from src.utils import logging


class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=2)
		self.camera_run  	= self.camera .run()
		self.app         	= MainProcess()
		self.skip_frame  	= False

	
	def __write_video(self, filename):
		size = (int(self.camera_run.get(3)), int(self.camera_run.get(4)))
		return cv2.VideoWriter(f'{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 10, size)

	def run(self):
		start_time 	= time.time()
		timestamp	= int(start_time)
  
		logging.info(f'======== Damage Detection Started ========')
		logging.info(f'Id : {timestamp}')

		# Define Write Video
		#out_video =  self.__write_video(timestamp)

		while True:
			ret, frame = self.camera_run.read()
			if not ret:
				logging.error(f'Message : Error reading frame')
				self.camera.release(ret=False)
				self.capture = self.camera.run()
				time.sleep(1)
			else:
				if not self.skip_frame:
					drawed = self.app.main(frame)
					#out_video.write(drawed)
					self.skip_frame = True
				else: self.skip_frame = False
			
			key_window = self.camera.show(drawed)
			if key_window == 27: break

		self.out.release()
		self.camera.release()

if __name__ == '__main__':
	adam_out    = Adam6060Output()
	aplication  = RunApplication()
	
	while True:
		di3 = adam_out.di_output(3)
		if di3:
			aplication.run()
