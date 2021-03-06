from uuid import uuid4
from hashlib import pbkdf2_hmac

import binascii
import os
import random

from core.database.controller import Controller
from core.auth.util import generateID, generateHashedPassword

def generateUsers(role):
    # get json file of user queries from randomuser.me
    r = 1
    #requests.get('https://randomuser.me/api/?nat=us&results=10&inc=name,login,email,phone').json()

    # parse the results of json file and create a model for extract data from
    results = r['results']
    parsed = list(map(lambda x: {
                    'user_id': generateID(),
                    'name': x['name']['first'] + ' ' + x['name']['last'], 
                    'login': x['login']['username'], 
                    'password': x['login']['password'], 
                    'email': x['email'],
                    'contact': x['phone'],
                    'role': role}, results))

    # write to txt file
    with open('./user_log/results_{}.txt'.format(role.split(" ")[0]), 'a') as f:
        for col in parsed[0].keys():
            f.write('{:<24} '.format(col))
        f.write('\n\n')
        for entry in parsed:
            for attr in entry.keys():
                f.write('{:<24} '.format(entry[attr]))
            f.write('\n')
        f.close()
    
    # success
    print("Users created!")
    return parsed

def generateAccountManagers(db_controller):
    # creates an account manager in the database using randomuser.me queries

    results = generateUsers('account manager')
    
    titles = ("major accounts manager", "medium accounts manager", "small accounts manager")

    # insert entries into the user, personnel, account_managers tables
    for entry in results:
        hash_pw = generateHashedPassword(entry['password'])
        db_controller.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (entry['user_id'], entry['role'], entry['login'], hash_pw))
        db_controller.cursor.execute("INSERT INTO personnel VALUES (?, ?, ?, 'Windsor Drive', '0');", (entry['user_id'], entry['name'], entry['email']))
        db_controller.cursor.execute("INSERT INTO account_managers VALUES (?, ?, '8th Street South');", (entry['user_id'], random.choice(titles)))
    
    db_controller.connection.commit()

def main():
    print(generateHashedPassword('dispatcher'))

if __name__ == "__main__":
    main()
