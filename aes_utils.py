from Cryptodome.Random import get_random_bytes
from rsa_utils import encrypt_with_rsa, decrypt_with_rsa

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

    data = encrypt_with_rsa(rsa_publickey, out)

    with open(outfile, 'wb') as f:
        f.write(data)

def read_aes_keys(file_extensions, size, rsa_privatekey, infile):
    with open(infile, 'rb') as f:
        data = f.read()

    decrypted = decrypt_with_rsa(rsa_privatekey, data)

    keymap = dict()

    for fe in file_extensions:
        keymap[fe] = decrypted[:size//8]
        decrypted = decrypted[size//8:]
    return keymap
