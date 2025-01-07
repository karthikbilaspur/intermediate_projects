from flask import Flask, render_template, request, redirect, url_for
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes
import os

app = Flask(__name__)

def aes_encrypt(plaintext, key):
    # Generate a random 128-bit IV.
    iv = os.urandom(16)
    
    # Create a Cipher instance with AES-CBC mode.
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the plaintext to ensure it's a multiple of the block size.
    padder = padding.PKCS7(cipher.algorithm.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    # Encrypt the padded plaintext.
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + ciphertext

def rsa_encrypt(plaintext, public_key):
    # Encrypt the plaintext using the public key.
    ciphertext = public_key.encrypt(
        plaintext,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return ciphertext

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aes', methods=['GET', 'POST'])
def aes():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        key = os.urandom(32)  # 256-bit key
        
        if request.form['submit'] == 'Encrypt':
            ciphertext = aes_encrypt(plaintext.encode(), key)
            return render_template('aes.html', ciphertext=ciphertext.hex(), key=key.hex())
        elif request.form['submit'] == 'Decrypt':
            ciphertext = bytes.fromhex(request.form['ciphertext'])
            key = bytes.fromhex(request.form['key'])
            iv = ciphertext[:16]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
            unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            return render_template('aes.html', plaintext=plaintext.decode())
    return render_template('aes.html')

@app.route('/rsa', methods=['GET', 'POST'])
def rsa():
    if request.method == 'POST':
        plaintext = request.form['plaintext'].encode()
        
        if request.form['submit'] == 'Encrypt':
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()
            ciphertext = rsa_encrypt(plaintext, public_key)
            return render_template('rsa.html', ciphertext=ciphertext.hex(), private_key=private_key.private_bytes(
                encoding='PEM',
                format='PKCS8',
                encryption_algorithm=None
            ).decode())
        elif request.form['submit'] == 'Decrypt':
            ciphertext = bytes.fromhex(request.form['ciphertext'])
            private_key = request.form['private_key'].encode()
            private_key = rsa.private_key_from_pem(private_key)
            plaintext = private_key.decrypt(
                ciphertext,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return render_template('rsa.html', plaintext=plaintext.decode())
    return render_template('rsa.html')

@app.route('/aes', methods=['GET', 'POST'])
def aes():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        key = request.form['key']
        
        # Validate input
        if not plaintext or not key:
            flash('Please enter plaintext and key', 'error')
            return redirect(url_for('aes'))
        
        # Validate key length
        if len(key) != 32 and len(key) != 48 and len(key) != 64:
            flash('Invalid key length', 'error')
            return redirect(url_for('aes'))
        
        # Proceed with encryption/decryption
        # ...

@app.route('/rsa', methods=['GET', 'POST'])
def rsa():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        private_key = request.form['private_key']
        
        # Validate input
        if not plaintext or not private_key:
            flash('Please enter plaintext and private key', 'error')
            return redirect(url_for('rsa'))

@app.route('/aes', methods=['GET', 'POST'])
def aes():
    try:
        # Encryption/decryption logic
        # ...
    except ValueError as e:
        flash(f'Invalid input: {e}', 'error')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')

@app.route('/rsa', methods=['GET', 'POST'])
def rsa():
    try:
        # Encryption/decryption logic
        # ...
    except ValueError as e:
        flash(f'Invalid input: {e}', 'error')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')


if __name__ == '__main__':
    app.run(debug=True)
    
    from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# SHA-256
def sha256_hash(plaintext):
    digest = hashes.Hash(hashes.SHA256(), default_backend())
    digest.update(plaintext.encode())
    return digest.finalize().hex()

# MD5
def md5_hash(plaintext):
    digest = hashes.Hash(hashes.MD5(), default_backend())
    digest.update(plaintext.encode())
    return digest.finalize().hex()

# BLAKE2
def blake2_hash(plaintext):
    digest = hashes.Hash(hashes.BLAKE2s(32), default_backend())
    digest.update(plaintext.encode())
    return digest.finalize().hex()

@app.route('/hash', methods=['GET', 'POST'])
def hash_function():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        hash_type = request.form['hash-type']
        
        if hash_type == 'sha256':
            return sha256_hash(plaintext)
        elif hash_type == 'md5':
            return md5_hash(plaintext)
        elif hash_type == 'blake2':
            return blake2_hash(plaintext)
        
        from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.hazmat.backends import default_backend

# ECDSA
def ecdsa_sign(plaintext, private_key):
    signature = private_key.sign(
        plaintext.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    return signature.hex()

def ecdsa_verify(plaintext, signature, public_key):
    try:
        public_key.verify(
            bytes.fromhex(signature),
            plaintext.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except:
        return False

# RSA
def rsa_sign(plaintext, private_key):
    signature = private_key.sign(
        plaintext.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature.hex()

def rsa_verify(plaintext, signature, public_key):
    try:
        public_key.verify(
            bytes.fromhex(signature),
            plaintext.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except:
        return False

@app.route('/sign', methods=['GET', 'POST'])
def digital_signature():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        signature_type = request.form['signature-type']
        private_key = request.form['private-key']
        public_key = request.form['public-key']
        
        if signature_type == 'ecdsa':
            return ecdsa_sign(plaintext, private_key)
        elif signature_type == 'rsa':
            return rsa_sign(plaintext, private_key)
        from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Diffie-Hellman
def diffie_hellman_key_exchange(private_key, peer_public_key):
    shared_key = private_key.exchange(peer_public_key)
    return shared_key.hex()

# Elliptic Curve Diffie-Hellman
def ecdh_key_exchange(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    return shared_key.hex()

@app.route('/key-exchange', methods=['GET', 'POST'])
def key_exchange_algorithm():
    if request.method == 'POST':
        private_key = request.form['private-key']
        peer_public_key = request.form['peer-public-key']
        key_exchange_type = request.form['key-exchange-type']
        
        if key_exchange_type == 'diffie-hellman':
            return diffie_hellman_key_exchange(private_key, peer_public_key)
        elif key_exchange_type == 'ecdh':
            return ecdh_key_exchange(private_key, peer_public_key)
        from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ECB
def ecb_encrypt(plaintext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(cipher.algorithm.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext.hex()

def ecb_decrypt(ciphertext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()
    unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

# CFB
def cfb_encrypt(plaintext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext.hex()

def cfb_decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()
    return plaintext.decode()

# OFB
def ofb_encrypt(plaintext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext.hex()

def ofb_decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()
    return plaintext.decode()

@app.route('/block-cipher', methods=['GET', 'POST'])
def block_cipher_mode():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        key = request.form['key']
        iv = request.form['iv']
        cipher_mode = request.form['cipher-mode']
        
        if cipher_mode == 'ecb':
            return ecb_encrypt(plaintext.encode(), bytes.fromhex(key))
        elif cipher_mode == 'cfb':
            return cfb_encrypt(plaintext.encode(), bytes.fromhex(key), bytes.fromhex(iv))
        elif cipher_mode == 'ofb':
            return ofb_encrypt(plaintext.encode(), bytes.fromhex(key), bytes.fromhex(iv))
        import secrets

def generate_random_key(length):
    return secrets.token_bytes(length).hex()

@app.route('/random-key', methods=['GET', 'POST'])
def random_key_generation():
    if request.method == 'POST':
        length = int(request.form['length'])
        return generate_random_key(length)
    
    from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def pbkdf2_encrypt(plaintext, password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    # Use key for encryption

def argon2_encrypt(plaintext, password, salt):
    # Implement Argon2 encryption
    pass

def bcrypt_encrypt(plaintext, password, salt):
    # Implement Bcrypt encryption
    pass

@app.route('/password-based-encryption', methods=['GET', 'POST'])
def password_based_encryption():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        password = request.form['password']
        salt = request.form['salt']
        encryption_type = request.form['encryption-type']
        
        if encryption_type == 'pbkdf2':
            return pbkdf2_encrypt(plaintext, password, salt)
        elif encryption_type == 'argon2':
            return argon2_encrypt(plaintext, password, salt)
        elif encryption_type == 'bcrypt':
            return bcrypt_encrypt(plaintext, password, salt)
        
        from cryptography.hazmat.primitives import homomorphic

def homomorphic_encrypt(plaintext):
    # Implement homomorphic encryption
    pass

@app.route('/homomorphic-encryption', methods=['GET', 'POST'])
def homomorphic_encryption():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        return homomorphic_encrypt(plaintext)
    
    from cryptography.hazmat.primitives import ntru, mceliece, sphincs

def ntru_encrypt(plaintext):
    # Implement NTRU encryption
    pass

def mceliece_encrypt(plaintext):
    # Implement McEliece encryption
    pass

def sphincs_encrypt(plaintext):
    # Implement SPHINCS encryption
    pass

@app.route('/quantum-resistant-cryptography', methods=['GET', 'POST'])
def quantum_resistant_cryptography():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        encryption_type = request.form['encryption-type']
        
        if encryption_type == 'ntru':
            return ntru_encrypt(plaintext)
        elif encryption_type == 'mceliece':
            return mceliece_encrypt(plaintext)
        elif encryption_type == 'sphincs':
            return sphincs_encrypt(plaintext)