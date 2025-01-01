import sys
import hashlib
import os
import requests
from getpass import getpass

def hash_pswrd(pswrd):
    hashed_pswrd = hashlib.sha1(pswrd.encode()).hexdigest()
    return hashed_pswrd

pswrd = getpass()
hashed_pswrd = hash_pswrd(pswrd)
hash_start = hashed_pswrd[0:5]
breaches_found = 0

passwords = requests.get('https://api.pwnedpasswords.com/range/' + hash_start).text.split('\n')

for line in passwords :
    pswrd_from_database_with_number = hash_start + line.strip().lower()
    pswrd_from_database = line.strip().lower()[0:35]
    pswrd_from_database = hash_start + pswrd_from_database
    if hashed_pswrd == pswrd_from_database:
        breaches_found = pswrd_from_database_with_number[41:len(pswrd_from_database_with_number)]
        print(pswrd_from_database_with_number)
        break
if breaches_found == 0:
    print('0 data breaches found')
else: 
    print(str(breaches_found) + ' data breaches found')
