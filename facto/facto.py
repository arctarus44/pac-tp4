import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
import math
from tools import *

CLS_AA = 'A+'
CLS_A = 'A'
CLS_B = 'B'
CLS_C = 'C'
CLS_D = 'D'

LVL_1 = '1'
LVL_2 = '2'
LVL_3 = '3'
LVL_4 = '4'

CHALLENGE_NAME = "/factoring"
GET_NUMBER_URL = CHALLENGE_NAME + "/get/{0}/{1}"
SUBMIT_URL = CHALLENGE_NAME + "/submit" + NAME

ID = 'id'
N = 'n'
FACTORS = "factors"


def get_number(cls, lvl):
	"""Retreive from the server the number to factorize. Return a dictionary
	with two keys : number and id"""
	srv = clt.Server(BASE_URL)
	try:
		return srv.query(GET_NUMBER_URL.format(lvl, cls))
	except clt.ServerError as err:
		print_serverError_exit(err)

def isPrime(a):
	x = True
	for i in (2, a):
		while x:
			if a // i == 0:
				x = False
			else:
				x = True
	return x

def est_premier(p):
	if(p == 1):
		return False
	if(p % 2 == 0):
		return True

	sqr = math.sqrt(p)
	cpt = 3
	while(cpt <= sqr):
		if(p % cpt == 0):
			return False
		cpt += 2

	return True

def dividy_by_Simple(number):
	numbers = []
	count = 0

	while number != 1:
		i = 2
		sqrt_number = math.sqrt(number)
		done = False
		print(str(count) + " number " + str(number), file=sys.stderr)
		while not done and i <= number:
			if est_premier(i):
				print(i)
				if (number % i)  == 0:
					count += 1
					os.system("notify-send \"no " + str(count) + " prime factor found : " + str(i) + "\"")
					numbers.append(i)
					number = number // i
					done = True
			if i == 2:
				i+=1
			else:
				i+=2

	return numbers

if __name__ == "__main__":
	print("Retreive number to factorize")
	response = get_number(CLS_D, LVL_2)
	id = response[ID]
	n = response[N]
	print("Finding factors")
	factors = dividy_by_Simple(n)
	save = open("./factors", 'w')
	save.write(str(factors))
	save.close()
	print(factors)
	result = {ID: id, FACTORS: factors}
	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(SUBMIT_URL, result)
	except ServerError as err:
		print_serverError_exit(err)

	os.system("notify-send \"finish" + result + "\" -i ~/.face.icon" )
