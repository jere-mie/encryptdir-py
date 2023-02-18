import sys
import yaml
import os
from rsa_utils import get_rsa_key
from aes_utils import get_aes_keys, verify_aes_keychain_signature, encrypt_file, decrypt_file

def get_config(config_path:str):
    with open(config_path, 'r') as f:
        contents = yaml.safe_load(f)
    return contents

def main():
    if len(sys.argv) != 3:
        print('usage: python3 run.py ENCRYPT/DECRYPT "password here"')
        exit(1)
    if sys.argv[1] == 'ENCRYPT':
        config = get_config('config.yml')
        password = sys.argv[2]
        rsa_key = get_rsa_key(config['private_key'], config['public_key'], password)
        aeskeys = get_aes_keys(config['files'], config['key_size'], rsa_key, config['aes_key'])
        print("AES Keychain verified!" if verify_aes_keychain_signature(rsa_key.public_key(), config['aes_key']) else "AES Keychain NOT verified!")
        directories = config['directories']
        for d in directories:
            for root, _, files in os.walk(f"./test_environment/{d}", topdown=False):
                for name in files:
                        # check file extension
                        ext = os.path.splitext(name)[1][1:]
                        if ext in config['files']:
                            encrypt_file(root, name, aeskeys[ext])

    elif sys.argv[1] == 'DECRYPT':
        config = get_config('config.yml')
        password = sys.argv[2]
        rsa_key = get_rsa_key(config['private_key'], config['public_key'], password)
        aeskeys = get_aes_keys(config['files'], config['key_size'], rsa_key, config['aes_key'])
        print("AES Keychain verified!" if verify_aes_keychain_signature(rsa_key.public_key(), config['aes_key']) else "AES Keychain NOT verified!")
        directories = config['directories']
        for d in directories:
            for root, _, files in os.walk(f"./test_environment/{d}", topdown=False):
                for name in files:
                        # check file extension
                        ext = os.path.splitext(name)[1][1:]
                        if ext in config['files']:
                            decrypt_file(root, name, aeskeys[ext])
    else:
        print(f"Unknown option: {sys.argv[1]}")
        print('usage: python3 run.py ENCRYPT/DECRYPT "password here"')

if __name__ == '__main__':
    main()
