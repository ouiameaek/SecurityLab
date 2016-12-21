import socket
import json
import rsa
import ../rsa0LD
from ../rsa0LD import common
from rsa import key as keyfile
from ../rsa0LD import pkcs1 as old
from collections import namedtuple
import time


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('localhost', 15555))

pub_keys={}

with open("pub_keys.txt") as f:
	i=0
	for key in f:
		n,e=key.strip().split(",")
		pub_keys[i]=keyfile.PublicKey(int(n),int(e))
		i=i+1
		

while True:
	socket.listen(5)
	client, address = socket.accept()
	print ("{} connected".format( client ))

	
	data=json.loads(client.recv(2048).decode('utf8'))
	client_id = data['client_id']
	msg = data['msg']
	print("client ",client_id+1," message is : ",msg)
	print("asking client for signature !")
	client.send("send signature".encode("ASCII"))
	time.sleep(1)
	signature = client.recv(2048)
	response = old.verify(msg.encode('utf-8'), signature,pub_keys[int(client_id)])
	if(response):
		client.send("Connected".encode('ASCII'))
	else:
		client.send("Not Connected".encode('ASCII'))
	print("Signature received & answer is sent\n Connection closed with client ",client_id+1,"\n")
	client.close()
	
			
print ("Close")

stock.close()
