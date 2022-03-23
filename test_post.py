import requests
import datetime
from requests.exceptions import HTTPError


from config import DEVICE_ID, GATE_ID, DATETIME_FORMAT,END_POINT,DELAY_IN_SECONDS,SEND_TIMEOUT,READ_TIMEOUT


# def container_test(): 
#     try:
#         start_time = datetime.datetime.now()
#         url= END_POINT+'container/'
#         print(url)
#         x_min_c=y_min_c=x_max_c=y_max_c=0
#         x_min_i=y_min_i=x_max_i=y_max_i=0
#         end_time = datetime.datetime.now()
#         container_number_result = 'CONTAINER1'
#         container_number_avg_confidence =iso_code_avg_confidence = 90
#         iso_code_result = '45G1'
#         file_path=''
#         json_data = {
# 			'gateId': GATE_ID,
#   			'deviceId': 'container'+DEVICE_ID,
#   			'startTime': start_time.strftime(DATETIME_FORMAT),
#   			'EndTime': end_time.strftime(DATETIME_FORMAT),
# 			'delayInSeconds' : DELAY_IN_SECONDS,
# 			'container': {
# 				'result': container_number_result,
# 				'confidence': container_number_avg_confidence,
# 				'box' : {
# 					"x_min": x_min_c,
# 					"y_min": y_min_c,
# 					"x_max": x_max_c,
# 					"y_max": y_max_c
# 				},
#                 'filePath': file_path
# 			},
# 			'iso_code': {
# 				'result': iso_code_result,
# 				'confidence': iso_code_avg_confidence,
# 				'box' : {
# 					"x_min": x_min_i,
# 					"y_min": y_min_i,
# 					"x_max": x_max_i,
# 					"y_max": y_max_i
# 				},
#                 'filePath': file_path
# 			}
# 		}
#         print('sending...')
#         print(json_data)
#         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#         r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
#         ret = r.json()
#         return ret
#     except HTTPError as e:
#         print(e.response.text)
#     except:
#         return 'send error'

def container_test(container_number_result,container_number_confidence, container_number_path, iso_code_result,iso_code_confidence, iso_code_path, start_time, end_time): 
    try:
        url= END_POINT+'container/'
        print(url)
        x_min_c=y_min_c=x_max_c=y_max_c=0
        x_min_i=y_min_i=x_max_i=y_max_i=0
        json_data = {
			'gateId': GATE_ID,
  			'deviceId': 'container'+DEVICE_ID,
  			'startTime': start_time.strftime(DATETIME_FORMAT),
  			'EndTime': end_time.strftime(DATETIME_FORMAT),
			'delayInSeconds' : DELAY_IN_SECONDS,
			'container': {
				'result': container_number_result,
				'confidence': container_number_confidence,
				'box' : {
					"x_min": x_min_c,
					"y_min": y_min_c,
					"x_max": x_max_c,
					"y_max": y_max_c
				},
                'filePath': container_number_path
			},
			'iso_code': {
				'result': iso_code_result,
				'confidence': iso_code_confidence,
				'box' : {
					"x_min": x_min_i,
					"y_min": y_min_i,
					"x_max": x_max_i,
					"y_max": y_max_i
				},
                'filePath': iso_code_path
			}
		}
        print('sending...')
        print(json_data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
        ret = r.json()
        return ret
    except HTTPError as e:
        print(e.response.text)
    except:
        return 'send error'

def axle_test(result, file_path, start_time, end_time): 
    try:
        url= END_POINT+'axle/'
        print(url)
        json_data = {
			'gateId': GATE_ID,
  			'deviceId': 'axle'+DEVICE_ID,
			'result': result,
			'filePath': file_path,
  			'startTime': start_time.strftime(DATETIME_FORMAT),
  			'EndTime': end_time.strftime(DATETIME_FORMAT),
			'delayInSeconds' : DELAY_IN_SECONDS,
		}
        print('sending...')
        print(json_data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
        ret = r.json()
        return ret
    except HTTPError as e:
        print(e.response.text)
    except:
        return 'send error'


def seal_test(result, confidence, file_path, start_time, end_time): 
    try:
        url= END_POINT+'seal/'
        print(url)
        x_min_c=y_min_c=x_max_c=y_max_c=0
        json_data = {
			'gateId': GATE_ID,
  			'deviceId': 'seal'+DEVICE_ID,
			'result': result,
			'confidence': confidence,
			'box' : {
				"x_min": x_min_c,
				"y_min": y_min_c,
				"x_max": x_max_c,
				"y_max": y_max_c
			},
			'filePath': file_path,
  			'startTime': start_time.strftime(DATETIME_FORMAT),
  			'EndTime': end_time.strftime(DATETIME_FORMAT),
			'delayInSeconds' : DELAY_IN_SECONDS,
		}
        print('sending...')
        print(json_data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
        ret = r.json()
        return ret
    except HTTPError as e:
        print(e.response.text)
    except:
        return 'send error'

def containerdamage_test(result, confidence, file_path, start_time, end_time): 
    try:
        url= END_POINT+'containerdamage/'
        print(url)
        json_data = {
			'gateId': GATE_ID,
  			'deviceId': 'containerdamage'+DEVICE_ID,
			'result': result,
			'confidence': confidence,
			'filePath': file_path,
  			'startTime': start_time.strftime(DATETIME_FORMAT),
  			'EndTime': end_time.strftime(DATETIME_FORMAT),
			'delayInSeconds' : DELAY_IN_SECONDS,
		}
        print('sending...')
        print(json_data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
        ret = r.json()
        return ret
    except HTTPError as e:
        print(e.response.text)
    except:
        return 'send error'


def tag_test(result, confidence, file_path, start_time, end_time): 
    try:
        url= END_POINT+'tag/'
        x_min_c=y_min_c=x_max_c=y_max_c=0
        print(url)
        json_data = {
			'gateId': GATE_ID,
  			'deviceId': 'tag'+DEVICE_ID,
			'result': result,
			'confidence': confidence,
			'box' : {
				"x_min": x_min_c,
				"y_min": y_min_c,
				"x_max": x_max_c,
				"y_max": y_max_c
			},
			'filePath': file_path,
  			'startTime': start_time.strftime(DATETIME_FORMAT),
  			'EndTime': end_time.strftime(DATETIME_FORMAT),
			'delayInSeconds' : DELAY_IN_SECONDS,
		}
        print('sending...')
        print(json_data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
        ret = r.json()
        return ret
    except HTTPError as e:
        print(e.response.text)
    except:
        return 'send error'


#print(container_test())
#print(axle_test(6, "", datetime.datetime.now(), datetime.datetime.now()))
#print(seal_test(1, 87, "", datetime.datetime.now(), datetime.datetime.now()))
# print(containerdamage_test(1, 87, "", datetime.datetime.now(), datetime.datetime.now()))
#print(container_test("CONTAINER4",81, "", "G405", 81, "", datetime.datetime.now(), datetime.datetime.now()))
print(tag_test("F438765", 81, "", datetime.datetime.now(), datetime.datetime.now()))
#print(axle_test(3, "", datetime.datetime.now(), datetime.datetime.now()))