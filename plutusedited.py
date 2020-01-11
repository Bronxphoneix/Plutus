# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# Edited by Bronx Phoneix ( Add Compressed Adress and Bitcoin Module)
# https://github.com/Isaacdelly/Plutus
from timeit import timeit
import os
import pickle
import multiprocessing
import bitcoin as btc
import random

DATABASE = r'database/MAR_23_2019/'
gpkey = lambda: random.randrange(2**256)
addal = lambda pkey: btc.pubkey_to_address(btc.privkey_to_pubkey(pkey))
caddal = lambda pkey: btc.pubkey_to_address(btc.compress(btc.privkey_to_pubkey(pkey))) 

def process(pkey, address, caddress, database):
	if address in database[0] or \
	   address in database[1] or \
	   address in database[2] or \
	   address in database[3] or \
       caddress in database[0] or \
	   caddress in database[1] or \
	   caddress in database[2] or \
	   caddress in database[3]:
		with open('plutus.txt', 'a') as file:
			file.write('Private : ' + str(btc.encode_privkey(pkey,'hex')) + '\n' +
			           'Address : ' + str(address) + '\n' +
                       'cAddress: ' + str(addressc)+'\n\n')
	else: 
		print(str(address)+" "+str(caddress)+" "+str(btc.encode_privkey(pkey,'hex')))

def main(database):
    while True:
        pkey = gpkey()
        address = addal(pkey)
        caddress = caddal(pkey)
        process(pkey, address, caddress, database)

if __name__ == '__main__':
	database = [set() for _ in range(4)]
	count = len(os.listdir(DATABASE))
	half = count // 2
	quarter = half // 2
	for c, p in enumerate(os.listdir(DATABASE)):
		print('\rreading database: ' + str(c + 1) + '/' + str(count), end = ' ')
		with open(DATABASE + p, 'rb') as file:
			if c < half:
				if c < quarter: database[0] = database[0] | pickle.load(file)
				else: database[1] = database[1] | pickle.load(file)
			else:
				if c < half + quarter: database[2] = database[2] | pickle.load(file)
				else: database[3] = database[3] | pickle.load(file)
	print('DONE')
	# To verify the database size, remove the # from the line below
	#print('database size: ' + str(sum(len(i) for i in database))); quit()
	for cpu in range(multiprocessing.cpu_count()):
		multiprocessing.Process(target = main, args = (database, )).start()
