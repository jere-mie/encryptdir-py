from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from rsa_utils import buffered_encrypt_with_rsa, buffered_decrypt_with_rsa, sign_message, verify_signature
import hashlib

def create_aes_key(size):
    size_in_bytes = size//8  # 128 bits / 8 = 16 bytes (1 byte = 8 bits)
    sec_key = get_random_bytes(size_in_bytes)
    return sec_key

def gen_aes_keys(file_extensions, size):
    keymap = dict()
    for fe in file_extensions:
        keymap[fe] = create_aes_key(size)
    return keymap

def write_aes_keys(keymap, file_extensions, rsa_publickey, outfile):
    out = b''
    for fe in file_extensions:
        out+=keymap[fe]

    data = buffered_encrypt_with_rsa(rsa_publickey, out)

    with open(outfile, 'wb') as f:
        f.write(data)

def read_aes_keys(file_extensions, size, rsa_privatekey, infile):
    with open(infile, 'rb') as f:
        data = f.read()

    decrypted = buffered_decrypt_with_rsa(rsa_privatekey, data)

    keymap = dict()

    for fe in file_extensions:
        keymap[fe] = decrypted[:size//8]
        decrypted = decrypted[size//8:]
    return keymap

def get_aes_keys(file_extensions, size, rsa_privatekey, keychain_file):
    try:
        keymap = read_aes_keys(file_extensions, size, rsa_privatekey, keychain_file)
        return keymap
    except FileNotFoundError:
        keymap = gen_aes_keys(file_extensions, size)
        write_aes_keys(keymap, file_extensions, rsa_privatekey.public_key(), keychain_file)
        sign_aes_keychain(rsa_privatekey, keychain_file)
        return keymap

def sign_aes_keychain(rsa_privatekey, keychain_file):
    with open(keychain_file, 'rb') as f:
        data = f.read()
    hash = hashlib.md5(data).hexdigest()
    signature = sign_message(rsa_privatekey, hash)
    with open(f'{keychain_file}.signature', 'wb') as f:
        f.write(signature)
    return signature

def verify_aes_keychain_signature(rsa_publickey, keychain_file):
    with open(keychain_file, 'rb') as f:
        data = f.read()
    hash = hashlib.md5(data).hexdigest()
    with open(f'{keychain_file}.signature', 'rb') as f:
        signature = f.read()
    return verify_signature(rsa_publickey, hash, signature)

def aes_encrypt_message(msg, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(msg, AES.block_size))
    return cipher_text, cipher.iv

def aes_decrypt_message(msg, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(msg), AES.block_size)

def encrypt_file(base_path, file_name, aes_key):
    sig = hashlib.md5(file_name.encode()).digest()
    with open(f'{base_path}/{file_name}', 'rb') as f:
        contents = f.read()

    # file is already encrypted
    if contents[:16] == sig:
        return
    encrypted, iv = aes_encrypt_message(contents, aes_key)
    with open(f'{base_path}/{file_name}', 'wb') as f:
        f.write(sig)
        f.write(iv)
        f.write(encrypted)

def decrypt_file(base_path, file_name, aes_key):
    with open(f'{base_path}/{file_name}', 'rb') as f:
        hash = f.read(16)

        # file is not encrypted
        if hash != hashlib.md5(file_name.encode()).digest():
            f.close()
            return

        iv = f.read(16)
        contents = f.read()
    decrypted = aes_decrypt_message(contents, aes_key, iv)
    with open(f'{base_path}/{file_name}', 'wb') as f:
        f.write(decrypted)
