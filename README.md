# encryptdir-py

A simple Python application to securely encrypt and decrypt specified files in specified directories.  
Created for assignment 1 of COMP-3750 at the University of Windsor, Winter 2023

## Requirements

- Python3, and Pip

## Set Up

First install necessary dependencies:

```bash
pip3 install -r requirements.txt
```

Next, copy the sample config file, and then edit it to your liking:

```bash
cp sample_config.yml config.yml
```

## Running The Application

Depending on whether you want to encrypt or decrypt directories, you can run the following:

```bash
# to encrypt files
python3 run.py ENCRYPT "put your password here"

# to decrypt files
python3 run.py DECRYPT "put your password here"
```

### Testing The Application

If you're a Linux user, a handy bash script is included to make testing this application easier. Simply run:

```bash
./test_environment_setup.sh
```

and a bunch of files and directories will be created under the `test_environment` directory. All files are plaintext, despite their file extensions. Simply `cat` them or open them in a text editor to verify.

Now, rename `test_config.yml` to `config.yml` to set it as the configuration for your next run. Take note that there are some directories that were created by the script that do not appear in `test_config.yml`. **This was done on purpose** to allow users to verify that **only** the directories specified are encrypted/decrypted. The same is true for file extensions, not all file extensions in the test environment are encrypted, so you can verify that the configuration is actually being used.

Now, simply run the following to test encrypting the specified directories in the test environment:

```bash
# any password will do
python3 run.py ENCRYPT "password"
```

Head over to `test_environment` to verify the proper files/directories were encrypted. Now, to test decryption, run the following:

```bash
# must be same password as before
python3 run.py DECRYPT "password
```

Now, you'll be able to verify that all of the encrypted files are now decrypted!
