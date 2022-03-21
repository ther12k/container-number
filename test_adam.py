import socket
import time

UDP_IP_ADDRESS = '192.168.8.101'
UDP_PORT_NO = 5168

adam_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
adam_sock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
print(adam_sock)
while True:
	data, addr = adam_sock.recvfrom(1024)
	#test = [1 if not i==0 else 0 for i in data[:9]]
	#print(test)
	#print(data.decode('unicode_escape').encode('utf-8'))
	print([i for i in data])
	time.sleep(0.1)
