from django.shortcuts import render
from cryptography.fernet import Fernet
# Create your views here.

def encryption(text,key):
    encryption_key = Fernet(key)
    encrypted_message = encryption_key.encrypt(text.encode())
    return encrypted_message

def decryption(text,key):
    decryption_key = Fernet(key)
    decrypted_message = decryption_key.decrypt(text).decode()
    return decrypted_message