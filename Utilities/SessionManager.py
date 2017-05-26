import random
import string
import time

#gernerate session id for better organised data
def generateSessionID():
    x = ''.join(random.sample(string.ascii_letters+string.digits, 32))
    x += ''.join(random.sample(string.ascii_letters+string.digits, 16))
    x += str(time.time()).replace('.','') #add time in case of the same id
    return  x