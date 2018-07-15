#!/usr/bin/python3.6

import subprocess
import os
import signal
import sys
import getpass


def get_file_path():
    
    try:
        file_path = None
    
        while not file_path:
            file_path = input('Enter the path to the file to encrypt: ')
    
        if os.path.isfile(file_path):
            return file_path
    
        else:
            print('\n------------------------')
            print(f"-  {'Invalid file path!'}  -")
            print('------------------------\n')
            file_path = None

    except KeyboardInterrupt:
        print('\n\nKeyboard Interupt, Exiting...\n')
        sys.exit()

def get_password():
    
    try:
        password = None
        
        while not password:
            password = getpass.getpass(prompt='Enter the encryption passphrase: ', stream=None)
            confirm_password = getpass.getpass(prompt='Confirm the encryption passphrase: ', stream=None)
    
            if password == confirm_password:
                return password
    
            else:
                print('\n---------------------------')
                print(f"-  {'Passwords must match!'}  -")
                print('---------------------------\n')
        
                password = None
        
    except KeyboardInterrupt:
        print('\n\nKeyboard Interupt, Exiting...\n')
        sys.exit()

def encrypt_file(file_path, password_match):
    
    if os.path.isfile(f"{file_path}{'.gpg'}"):
        print('\n--------------------------')
        print(f"-  {'File Already Exists!'}  -")
        print('--------------------------\n')
        print(f"{file_path}{'.gpg'} already exists.\n")
        
        return "exists"
        
    command = f" echo {password_match} | gpg -c --batch --quiet --no-tty --cipher-algo AES256 --passphrase-fd 0 {file_path}"
    exec_cmd = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE)
    exec_cmd.wait()

    try:
        os.killpg(os.getpgid(exec_cmd.pid), signal.SIGTERM) 

    except ProcessLookupError:
        pass

    return True
    
def exit_program(file_path):
    print('\n----------------------------')
    print(f"-  {'Encryption Successful.'}  -")
    print('----------------------------\n')
    
    print(f"{file_path}{'.gpg'}")
    print(f"\nBye.\n")
    
    sys.exit()
    
def main():
    file_path = None
    
    while not file_path:
        file_path = get_file_path()
        
        password_match = None
    
        while not password_match:        
            password_match = get_password()
        
            encrypted_file = None
    
            while not encrypted_file:
                encrypted_file = encrypt_file(file_path, password_match)
                
                if encrypted_file == 'exists':
                    file_path = None
            
                elif encrypted_file == True:
                    print(file_path)
                    exit_program(file_path)
                    
                    
if __name__ == '__main__':
    main()
