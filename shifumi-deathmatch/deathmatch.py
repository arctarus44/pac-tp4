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

MASTER_KAN = "message from Master Kan"

STATUS = 'status'
COMMITMENT = 'commitment'
CIPHERTEXT = 'ciphertext'
PK = 'PK'
P = 'p'
G = 'g'
H = 'h'

def start_round():
	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(START_URL)
	except clt.ServerError as err:
		print_serverError_exit(err)
	return result

def start_deathmatch():
	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(INSERT_URL)
	except clt.ServerError as err:
		print_serverError_exit(err)
	print("Master Kan : \"{0}\"".format(result[MASTER_KAN]))

def aux():
	done = False
	result = start_round()
	while not done:
		try:
			ciphertext = result[COMMITMENT][CIPHERTEXT]
			pk = result[COMMITMENT][PK]
			elg = Elgamal(pk[P], pk[G], pk[H])
			a = ciphertext[0]
			m = ciphertext[0]
			p = elg.decrypt(a, m)
			print(p)
			done = True
		except KeyError:
			print("nouvelle tentative")
			result = start_round()

if __name__ == "__main__":
	start_deathmatch()
	start_round()
