#!/usr/bin/env python
# coding: utf-8

import socket
import json
import rsa
from collections import namedtuple
import time

import hashlib
import binascii
import os
from gmpy2 import mpz, iroot, powmod, mul, t_mod



def to_bytes(n):
	""" Return a bytes representation of a int """
	return n.to_bytes((n.bit_length() // 8) + 1, byteorder='big')

def from_bytes(b):
	""" Makes a int from a bytestring """
	return int.from_bytes(b, byteorder='big')

def get_bit(n, b):
	""" Returns the b-th rightmost bit of n """
	return ((1 << b) & n) >> b

def set_bit(n, b, x):
	""" Returns n with the b-th rightmost bit set to x """
	if x == 0: return ~(1 << b) & n
	if x == 1: return (1 << b) | n

def cube_root(n):
	return int(iroot(mpz(n), 3)[0])

def generate_msg(client_id):
	msg = "Go left at the blue tree".encode("ASCII")
	infos={'client_id': client_id, 'msg': msg.decode("utf-8")}
	msg_auth=json.dumps(infos).encode('utf-8')
	return msg_auth


def generate_fake_signature():
	message = "Ciao, mamma!!".encode("ASCII")
	message_hash = hashlib.sha256(message).digest()
	ASN1_blob = rsa.pkcs1.HASH_ASN1['SHA-256']
	suffix = b'\x00' + ASN1_blob + message_hash
	binascii.hexlify(suffix)
	sig_suffix = 1
	for b in range(len(suffix)*8):
		if get_bit(sig_suffix ** 3, b) != get_bit(from_bytes(suffix), b):
			sig_suffix = set_bit(sig_suffix, b, 1)
	while True:
		prefix = b'\x00\x01' + os.urandom(2048//8 - 2)
		sig_prefix = to_bytes(cube_root(from_bytes(prefix)))[:-len(suffix)] + b'\x00' * len(suffix)
		sig = sig_prefix[:-len(suffix)] + to_bytes(sig_suffix)
		if b'\x00' not in to_bytes(from_bytes(sig) ** 3)[:-len(suffix)]: break

	return sig




priv_keys={}
with open("priv_keys.txt") as f:
	i=0
	for key in f:
		n,e,d,p,q=key.strip().split(",")
		KeyObject = namedtuple('KeyObject', 'n e d p q')
		priv_keys[i]=rsa.PrivateKey(int(n),int(e),int(d),int(p),int(q))
		i=i+1


hote = "localhost"
port = 15555



for i in range(3):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect((hote, port))
	msg_auth=generate_msg(i)
	print("Sending message to the server",i+1," msg\n")
	soc.send(msg_auth)
	print("Message was sent, waiting for server authentication !\n")
	response = soc.recv(2048)
	print ("Server's response after sending the message is : ",response,"\n")
	signature = rsa.sign("Go left at the blue tree".encode("ASCII"), priv_keys[i], 'SHA-1') 
	soc.send(signature)
	print("Signature is sent !\n")
	time.sleep(1)
	response = soc.recv(1024)
	if(response.decode("utf-8")  == "Connected"):
		print ("Server's response for client ",i+1," is : ",response.decode("utf-8"),"\n")
	else:
		print("Sorry, Client ",i+1," is not connected\n")
	print ("Close\n\n\n")
	soc.close()

time.sleep(1)
print("\n\n\n******  Trying to forge a signature for client 3 with e = 3\n\n\n")
time.sleep(5)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((hote, port))
infos={'client_id': 3, 'msg': "Ciao, mamma!!".encode("ASCII").decode("utf-8")}
msg_auth=json.dumps(infos).encode('utf-8')
print("Sending message to the server",i+1," msg\n")
soc.send(msg_auth)
print("Message was sent, waiting for server authentication !\n")
response = soc.recv(2048)
print ("Server's response after sending the message is : ",response,"\n")
signature = generate_fake_signature()
soc.send(signature)
print("Signature is sent !\n")
time.sleep(2)
time.sleep(1)
response = soc.recv(1024)
if(response.decode("utf-8")  == "Connected"):
	print ("Server's response for fake account is : ",response.decode("utf-8"),"\n")
else:
	print("Sorry: Client ",i," is not connected\n")
print ("Close\n\n\n")
soc.close()
