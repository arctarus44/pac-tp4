import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
import random as rnd
from tools import *

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
	param.write("[{0}]\n".format(PARAM))
	for key in param_dict.keys():
		param.write(key + "=" + str(param_dict[key]) + "\n")
	param.close()

def compute_param(p, q):
	"""Compute the parameters needed to forge a new Elgamal signature.
	Return a tuple a value (b, c)"""
	if os.path.exists(PARAM_FILE):
		import configparser as cp
		config = cp.ConfigParser()
		config.read(PARAM_FILE)
		return config.getint(PARAM, B), config.getint(PARAM, C)
	else:
		b = rnd.randint(0,p)
		c = rnd.randint(0,p)

		i = 0
		while xgcd(c, q) != 1:
			i += 1
			c = rnd.randint(0,p)
			print(str(i) + " Generate a new c")
		save_param({B : b, C : c})
		return b, c

def forge_sign(p, g, h):
	q = p - 1

	b, c = compute_param(p, q)

	r = (pow(g, b, q) * pow(h, c, q)) % p

	s = (-r * modinv(c, q)) % q

	m = (b*s) % q
	return {M : m, SIGNATURE : (r, s)}


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
		print(result)
	except clt.ServerError as err:
		print_serverError_exit(err)
