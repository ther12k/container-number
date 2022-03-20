import cv2
from src import MainProcess

app = MainProcess()

image = cv2.imread('10.jpg')
app.main(image)