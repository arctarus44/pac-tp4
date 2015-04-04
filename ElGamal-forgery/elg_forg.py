import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
import random as rnd
from tools import *
from fractions import gcd

PARAM = "Param"

ELG_FORGERY = "/ElGamal-forgery/"
PK = "/PK"
VERIFY = "/verify"

PK_URL = ELG_FORGERY + PK + NAME
VERIFY_URL = ELG_FORGERY + VERIFY + NAME

B = 'b'
C = 'c'
P = 'p'
G = 'g'
H = 'h'
M = 'm'
R = 0
S = 1
SIGNATURE = 'signature'

PARAM_FILE = "param.txt"

def xgcd(a,b):
	u = (1,0)
	v = (0,1)
	while b!= 0:
		q, r= divmod(a,b)
		a=b
		b=r
		tmp=(u[0]-q*v[0], u[1] -q*v[1])
		u=v
		v=tmp
	return a,u[0],u[1]


def save_param(param_dict):
	param = open(PARAM_FILE, 'w')
	print("Saving parameters in file.")
	param.write("[{0}]\n".format(PARAM))
	for key in param_dict.keys():
		param.write(key + "=" + str(param_dict[key]) + "\n")
	param.close()

def compute_param(p, q):
	"""Compute the parameters needed to forge a new Elgamal signature.
	Return a tuple a value (b, c)"""
	if os.path.exists(PARAM_FILE):
		print("Parameters file exists. Extracting parameters from file.")
		import configparser as cp
		config = cp.ConfigParser()
		config.read(PARAM_FILE)
		return config.getint(PARAM, B), config.getint(PARAM, C)
	else:
		b = rnd.randint(0,p)
		c = rnd.randint(0,p)

		i = 0
		while gcd(c, q) != 1:
			i += 1
			c = rnd.randint(0,p)
			print("Generation of a new c attemp ", str(i))
		save_param({B : b, C : c})
		return b, c

def check_sign(p, g, h, r, s, m):
	value = (pow(h, r, p) * pow(r, s, p)) % p
	return value == pow(g, m, p);

def forge_sign(p, g, h):
	q = p - 1

	b, c = compute_param(p, q)

	r = (pow(g, b, p) * pow(h, c, p)) % p
	s = (-r * modinv(c, q)) % q

	m = (b*s) % q
	if check_sign(p, g, h, r, s, m): # Check if the signature is correct
		return {M : m, SIGNATURE : (r, s)}
	else:						# The signature are not correct
		print("Bad signature. :-(\nGoodbye.")
		exit(1)


def get_pubkey():
	"""Retrieve the public key of the PS3 on the server. Return a triplet
	of param (p, g, h)"""
	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(PK_URL)
	except clt.ServerError as err:
		print_serverError_exit(err)
	return result[P], result[G], result[H]

if __name__ == "__main__":
	p, g, h = get_pubkey()

	sign = forge_sign(p, g, h)

	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(VERIFY_URL, sign)
		print(result[STATUS])
	except clt.ServerError as err:
		print_serverError_exit(err)
