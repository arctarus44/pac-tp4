import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
import math
import atexit
from tools import *
import signal

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

primes_list = []
new_prime = []

current_number = 0


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
	if p == 1:
		return False
	if p == 2:
		return True
	if p % 2 == 0:
		return False
	if p % 10 == 5:
		return False

	p_str = str(p)
	sum_digits = 0
	for digit_str in p_str:
		sum_digits += int(digit_str)
	if sum_digits % 3 == 0:
		return False

	sqr = math.sqrt(p)
	cpt = 3
	while(cpt <= sqr):
		if(p % cpt == 0):
			return False
		cpt += 2

	return True

def read_prime_file():
	global primes_list
	file = open("primes.txt", 'r')
	line = file.readline()
	while line != '':
		primes_list.append(int(line))
		line = file.readline()
	file.close()
	print(str(len(primes_list)) + " prime numbers read")

def save_prime():
	global new_prime
	print("save prime number found")
	file = open("primes.txt", 'a')
	for prime in new_prime:
		file.write(str(prime) + "\n")
	print(str(len(new_prime)) + " prime numbers saved")
	file.close()

def dividy_by_Simple(number):
	global primes_list
	global new_prime
	global current_number
	count = 0
	numbers = []

	print("using compute prime number")

	while number != 1:
		found = False
		for prime in primes_list:
			current_number = prime
			if (number % prime) == 0:
				numbers.append(prime)
				count+=1
				print(str(count) + " number " + str(number) + " -> " + str(prime))
				found = True
				number = number // prime
				break

		if found:
			continue

		print("Fin de la liste de premier précalculé")

		if len(primes_list) == 0: # pas encore de premier calculé
			i = 2
		else:					# On a trouvé un diviseur premier déjà calcul
			i = primes_list[-1] + 2 # Si nombre premier -> impair donc + 2 pour ne pas avoir de nombre pair

		done = False
		sqrt_number = math.sqrt(number)
		while not done and i <= sqrt_number:
			current_number = i
			if est_premier(i):
				new_prime.append(i)
				if (number % i) == 0:
					count+=1
					print(str(count) + " number " + str(number) + " -> " + str(i))
					numbers.append(i)
					number = number // i
					done = True
			if i == 2:
				i+=1
			else:
				i+=2

	return numbers

def print_current_number(signum, frame):
	print("current number : " + str(current_number))

if __name__ == "__main__":

	atexit.register(save_prime)

	signal.signal(signal.SIGUSR1, print_current_number)

	print("Reading prime number from file")
	read_prime_file()
	print("Retreive number to factorize")
	response = get_number(CLS_D, LVL_2)
	id = response[ID]
	n = response[N]
	print("Finding factors")
	factors = dividy_by_Simple(n)

	save = open("./factors.txt", 'w')
	save.write(str(factors))
	save.close()

	result = {ID: id, FACTORS: factors}
	srv = clt.Server(BASE_URL)

	try:
		result = srv.query(SUBMIT_URL, result)
		print(result)
	except ServerError as err:
		print_serverError_exit(err)
