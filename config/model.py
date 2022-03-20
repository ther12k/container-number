import os

#========================== DIRECTORY =====================================
ROOT 					= os.path.normpath(os.path.dirname(__file__))

DIRECTORY_MODEL         = os.path.expanduser('~/.Halotec/Models')

DIRECTORY_LOGGER        = os.path.expanduser('~/.Halotec/Loggers')

#============================ MODELS ======================================
DETECTION_MODEL = {
	'container_number_iso_code' : {
		'filename'	: 'model_container_number_gray.pt',
        'url' 		: 'https://www.dropbox.com/s/jjwcr82wlcwtwrj/container_number_gray.pt?dl=1',
        'file_size' : 14753191
	}
}

#============================ CLASESS ======================================
CLASSES_DETECTION   = ['container_number', 'iso_code']
CLASSES_FILTERED    = ['container_number', 'iso_code']