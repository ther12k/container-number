import cv2
from src import MainProcess

app = MainProcess()

image = cv2.imread('a.jpg')
app.main(image)