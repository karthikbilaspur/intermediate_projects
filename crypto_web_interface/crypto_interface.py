from flask import Flask, render_template, request, redirect, url_for
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

app = Flask(__name__)

def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(cipher.algorithm.block_size).padder()
    padded_data = padder.update(message) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def decrypt_message(ciphertext, key):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']
        if request.form['submit'] == 'Encrypt':
            ciphertext = encrypt_message(message.encode(), key.encode())
            return render_template('index.html', ciphertext=ciphertext.hex())
        elif request.form['submit'] == 'Decrypt':
            plaintext = decrypt_message(bytes.fromhex(request.form['ciphertext']), key.encode())
            return render_template('index.html', plaintext=plaintext.decode())
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)