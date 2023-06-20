import hashlib

def Fhash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()