from Crypto.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import os

def generate_and_write_rsa_key(privPath:str, pubPath:str, password:str):
    key = RSA.generate(2048)
    encrypted_key = key.export_key(passphrase=password, pkcs=8, protection="scryptAndAES128-CBC")
    pubkey = key.public_key().export_key()

    with open(privPath, 'wb') as f:
        f.write(encrypted_key)

    with open(pubPath, 'wb') as f:
        f.write(pubkey)

    return key

def read_rsa_keys(privPath:str, pubPath:str, password:str):
    if not (os.path.exists(privPath) or os.path.exists(pubPath)):
        raise FileNotFoundError
    elif not os.path.exists(privPath) or not os.path.exists(pubPath):
        raise ValueError("One RSA key file not found!")

    with open(privPath, 'rb') as f:
        privData = f.read()
    key = RSA.import_key(privData, passphrase=password)
    with open(pubPath, 'rb') as f:
        pubData = f.read()
    pubkey = RSA.import_key(pubData)

    if key.public_key() == pubkey:
        return key
    print("PRIVATE KEY AND PUBLIC KEY DON't MATCH!")
    exit(1)

def get_rsa_key(privPath:str, pubPath:str, password:str):
    try:
        key = read_rsa_keys(privPath, pubPath, password)
    except FileNotFoundError:
        print("Neither key file exists, creating RSA keys...")
        key = generate_and_write_rsa_key(privPath, pubPath, password)
        print("generated key!")
    return key

def encrypt_with_rsa(pub_key, msg):

    cipher_rsa = PKCS1_OAEP.new(pub_key)
    cipher_data = cipher_rsa.encrypt(msg)
    return cipher_data

def decrypt_with_rsa(prv_key, msg):
    cipher_rsa = PKCS1_OAEP.new(prv_key)
    plain_data = cipher_rsa.decrypt(msg)
    return plain_data

def buffered_encrypt_with_rsa(pub_key, msg):
    cipher_data = b''
    while len(msg) > 0:
        cipher_data+=encrypt_with_rsa(pub_key, msg[:128])
        msg = msg[128:]
    return cipher_data

def buffered_decrypt_with_rsa(prv_key, msg):
    plain_data = b''
    while len(msg)>0:
        plain_data+=decrypt_with_rsa(prv_key, msg[:256])
        msg = msg[256:]
    return plain_data

def sign_message(private_key, message):
    hash_code = SHA256.new(message.encode())
    signature = pkcs1_15.new(private_key).sign(hash_code)
    return signature

def verify_signature(public_key, message, signature):
    hash_code = SHA256.new(message.encode())

    try:
        pkcs1_15.new(public_key).verify(hash_code, signature)
        print('=== valid')
        return True

    except ValueError:
        print('=== no valid')
        return False

    except Exception as error:
        print(f'there was an error {error}')
        return False
