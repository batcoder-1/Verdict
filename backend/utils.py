from pwdlib import PasswordHash

password_hash=PasswordHash.recommended()
DUMMY_HASH=password_hash.hash("test@1234")

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password,hash_password):
    return password_hash.verify(password,hash_password)