from tkinter import *
from tkinter import filedialog
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64
import os

# Function to pad the data to be encrypted
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

# Function to derive a key from a password using PBKDF2
def derive_key(password, salt=b'salt_', key_length=32, iterations=100_000):
    return PBKDF2(password, salt, dkLen=key_length, count=iterations)

# Function to encrypt a file
def encrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        plaintext = f.read()
    
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext))
    
    with open(file_name + ".enc", 'wb') as f:
        f.write(ciphertext)

# Function to decrypt a file
def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        ciphertext = f.read()
    
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(ciphertext).rstrip(b"\0")
    
    with open(file_name[:-4], 'wb') as f:
        f.write(decrypted_text)

def openFile():
    global file
    file = filedialog.askopenfilename(initialdir="/", title="Select file")
    print("Selected File:", file)

def encrypt():
    password = code.get().encode('utf-8')
    key = derive_key(password)
    if not file or not key:
        print("Please select a file and enter a key.")
        return
    
    encrypt_file(file, key)
    print("File encrypted successfully.")

def decrypt():
    password = code.get().encode('utf-8')
    key = derive_key(password)
    if not file or not key:
        print("Please select a file and enter a key.")
        return
    
    decrypt_file(file, key)
    print("File decrypted successfully.")

def main_screen():
    global root
    global code
    global file

    root = Tk()
    root.geometry("375x398")
    root.title("Encryption Decryption file")

    Label(text="Select file for encryption/decryption", fg='black', font=("calibri", 13)).place(x=10, y=10)
    Button(text="Browse file", height="2", width=23, bg="grey", fg="white", bd=0, command=openFile).place(x=10, y=50)

    Label(text="Enter password for encryption/decryption", fg='black', font=("calibri", 13)).place(x=10, y=100)
    code = StringVar()
    Entry(textvariable=code, width=19, bd=0, font=("arial", 25), show="*").place(x=10, y=140)

    Button(text="Encrypt", height="2", width=23, bg="#ed3833", fg="white", bd=0, command=encrypt).place(x=10, y=200)
    Button(text="Decrypt", height="2", width=23, bg="#00bd56", fg="white", bd=0, command=decrypt).place(x=200, y=200)

    root.mainloop()

main_screen()
