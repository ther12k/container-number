import requests
import datetime
from requests.exceptions import HTTPError


from config import DEVICE_ID, GATE_ID, DATETIME_FORMAT,END_POINT,DELAY_IN_SECONDS,SEND_TIMEOUT,READ_TIMEOUT


def container_test(): 
    try:
        start_time = datetime.datetime.now()
        url= END_POINT+'container/'
        print(url)
        x_min_c=y_min_c=x_max_c=y_max_c=0
        x_min_i=y_min_i=x_max_i=y_max_i=0
        end_time = datetime.datetime.now()
        container_number_result = 'CONTAINER1'
        container_number_avg_confidence =iso_code_avg_confidence = 90
        iso_code_result = '45G1'
        file_path=''
        json_data = {
			'gateId': GATE_ID,
  			'deviceId': 'container'+DEVICE_ID,
  			'startTime': start_time.strftime(DATETIME_FORMAT),
  			'EndTime': end_time.strftime(DATETIME_FORMAT),
			'delayInSeconds' : DELAY_IN_SECONDS,
			'container': {
				'result': container_number_result,
				'confidence': container_number_avg_confidence,
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
				'confidence': iso_code_avg_confidence,
				'box' : {
					"x_min": x_min_i,
					"y_min": y_min_i,
					"x_max": x_max_i,
					"y_max": y_max_i
				},
                'filePath': file_path
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

print(container_test())