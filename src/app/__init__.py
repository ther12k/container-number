from config import ISO_CODE

from .detection import CNICDetection
from .extract_cn import *
from .ocr import *
if ISO_CODE: from .extract_ic import *