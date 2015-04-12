import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
from tools import *

PIERRE  = 88275625857605
FEUILLE = 19779480974019653
CISEAUX = 18939445432636760

SHIFUMI = "/shifumi-deathmatch"
INSERT_COIN = "/insert-coin"
INSERT_URL = SHIFUMI + INSERT_COIN + NAME

START = "/start"
START_URL = SHIFUMI + START + NAME

STATUS_URL = SHIFUMI + "status/" + NAME

MOVE_URL = SHIFUMI + "/move"

MASTER_KAN = "message from Master Kan"

STATUS = 'status'
COMMITMENT = 'commitment'
CIPHERTEXT = 'ciphertext'
PK = 'PK'
P = 'p'
G = 'g'
H = 'h'
X = 'x'
R = 'r'
S = 's'

FOOBAR = "foobar"

SECT_KEY = "Key"
P_KEY_FILE = "elgamal_private.key"

# Our private key
p = 0
g = 0
h = 0
x = 0

srv = None

def start_deathmatch():
	try:
		result = srv.query(INSERT_URL)
	except clt.ServerError as err:
		print_serverError_exit(err)
	print("Master Kan : \"{0}\"".format(result[MASTER_KAN]))

def random_move():
	pass
def handle_move(server_move):
	response = {FOOBAR : server_move[FOOBAR]}
	elg = Elgamal(p, g, h, x)
	if STATUS in server_move.keys():
		print("Server is waiting")
		commitment = {PK : {P : p, G : g, H : h}}
		cipher = elg.encrypt(CISEAUX)
		commitment[CIPHERTEXT] =[cipher[0], cipher[1]]
		response[COMMITMENT] = commitment
		print(response)
		print(srv.query(MOVE_URL, response))
	else: # We assume the server is a nice guy
		print("NOPE -> TODO")
		exit(1)


def launch_round():
	try:
		result = srv.query(START_URL)
	except clt.ServerError as err:
		print_serverError_exit(err)

	handle_move(result)
	for i in range(0, 99):
		pass

def init_private_key():
	"""Retreive a private key from the file elgamal_private.key.
	Return p, g, h, and x."""
	if os.path.exists(P_KEY_FILE):
		global p, g, h, x
		print("Private key file exists. Extracting key from file.")
		import configparser as cp
		config = cp.ConfigParser()
		config.read(P_KEY_FILE)
		p = config.getint(SECT_KEY, P)
		g = config.getint(SECT_KEY, G)
		h = config.getint(SECT_KEY, H)
		x = config.getint(SECT_KEY, X),
	else:
		print("Private key file does not exists. Exiting.")
		exit(1)


if __name__ == "__main__":
	srv = clt.Server(BASE_URL)
	init_private_key()
	start_deathmatch()
	launch_round()
