import hashlib
import random
import string


def make_salt():
    return ''.join([random.choice(string.ascii_letters) for char in range(5)])

def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    salty_hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(salty_hash, salt)

def check_pw_hash(password, salty_hash):
    salt = salty_hash.split(',')[1]
    if make_pw_hash(password, salt) == salty_hash:
        return True
    return False 
