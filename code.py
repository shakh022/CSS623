# Importing necessary modules
from tkinter import *
from tkinter import filedialog
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64
import os

# Function to pad the data to be encrypted
def pad(s):
    """
    Pads the input data to match the block size for encryption.

    Args:
    - s: Input data to be padded

    Returns:
    - Padded data to match the block size for encryption
    """
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

# Function to derive a key from a password using PBKDF2
def derive_key(password, salt=b'salt_', key_length=32, iterations=100_000):
    """
    Derives a key from a password using PBKDF2.

    Args:
    - password: Password used to derive the key
    - salt: Optional salt value (default is 'salt_')
    - key_length: Length of the key in bytes (default is 32)
    - iterations: Number of iterations (default is 100,000)

    Returns:
    - Derived key using PBKDF2
    """
    return PBKDF2(password, salt, dkLen=key_length, count=iterations)

# Function to encrypt a file
def encrypt_file(file_name, key):
    """
    Encrypts a file using AES encryption.

    Args:
    - file_name: Name of the file to be encrypted
    - key: Key used for encryption
    """
    with open(file_name, 'rb') as f:
        plaintext = f.read()
    
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext))
    
    with open(file_name + ".enc", 'wb') as f:
        f.write(ciphertext)

# Function to decrypt a file
def decrypt_file(file_name, key):
    """
    Decrypts a file previously encrypted using AES encryption.

    Args:
    - file_name: Name of the file to be decrypted
    - key: Key used for decryption
    """
    with open(file_name, 'rb') as f:
        ciphertext = f.read()
    
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(ciphertext).rstrip(b"\0")
    
    with open(file_name[:-4], 'wb') as f:
        f.write(decrypted_text)

# Function to open a file dialog for user file selection
def openFile():
    """
    Opens a file dialog for selecting a file.
    """
    global file
    file = filedialog.askopenfilename(initialdir="/", title="Select file")
    print("Selected File:", file)

# Function to initiate file encryption
def encrypt():
    """
    Initiates the file encryption process.
    """
    password = code.get().encode('utf-8')
    key = derive_key(password)
    if not file or not key:
        print("Please select a file and enter a key.")
        return
    
    encrypt_file(file, key)
    print("File encrypted successfully.")

# Function to initiate file decryption
def decrypt():
    """
    Initiates the file decryption process.
    """
    password = code.get().encode('utf-8')
    key = derive_key(password)
    if not file or not key:
        print("Please select a file and enter a key.")
        return
    
    decrypt_file(file, key)
    print("File decrypted successfully.")

# Function to create the main user interface screen
def main_screen():
    """
    Creates the main user interface screen using tkinter.
    """
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

# Starting point of the program
if __name__ == "__main__":
    main_screen()
