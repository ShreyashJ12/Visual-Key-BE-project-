import hashlib

# SHA 256
a_string = 'A child in a pink dress is climbing up a set of stairs in an entry way .'
hashed_string = hashlib.sha256(a_string.encode('utf-8')).hexdigest()
print("SHA Output:",hashed_string)
