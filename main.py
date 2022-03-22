import cv2
import time
from src import MainProcess
from adam_io import DigitalOutput
from src.utils import Adam6050DInput, logging
from src.utils.camera import Camera
from adam_io import DigitalOutput

class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=2)
		self.camera_run  	= self.camera.run()
		self.adam			= Adam6050DInput()
		self.app         	= MainProcess()
		self.current_B1		= 1
		self.delay_time		= 2.5
		self.start_time		= 0
	
	def __write_video(self, filename):
		size = (int(self.camera_run.get(4)), int(self.camera_run.get(3)))
		return cv2.VideoWriter(f'{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 20, (1080,1920))

	def run(self):
		logging.info('Starting Application')
		while True:
			adam_inputs = self.adam.di_inputs()
			B1 			= adam_inputs[2][1]

			# Condition Trigger on lamp D0, D2
			if self.current_B1 == 1 and B1 == 0:
				self.adam.di_output(DigitalOutput(array=[0,0,1,0,0,0]))

			# Condition read camera:
			if self.current_B1 == 0 and B1 == 1:
				if self.start_time == 0: time.time()
				while True:
					ret, frame = self.camera_run.read()
					if not ret:
						self.camera.release(ret=False)
						self.capture = self.camera.run()
						time.sleep(1)
						continue
					if time.time() - self.start_time >= self.delay_time:
						logging.info('Capture camera')
						frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
						drawed = self.app.main(frame, id=int(time.time()))
						#cv2.imwrite('result.jpg', drawed)
						cv2.imwrite(f'results/{int(time.time())}.jpg', drawed)
						self.adam.di_output(DigitalOutput(array=[0,0,0,0,0,0]))
						self.start_time = 0; break
						
			self.current_B1 = B1
			key = cv2.waitKey(30)
			if key == 27: break

		self.camera.release()

if __name__ == '__main__':
	application  = RunApplication()
	application.run()

