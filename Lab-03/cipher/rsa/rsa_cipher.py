import rsa
import os

if not os.path.exists('cipher/rsa/keys'):
    os.makedirs('cipher/rsa/keys')

class RSACipher:
    def generate_keys(self):
        (pubkey, privkey) = rsa.newkeys(2048)
        with open('cipher/rsa/keys/publicKey.pem', 'wb') as p:
            p.write(pubkey.save_pkcs1())
        with open('cipher/rsa/keys/privateKey.pem', 'wb') as p:
            p.write(privkey.save_pkcs1())

    def load_keys(self):
        with open('cipher/rsa/keys/privateKey.pem', 'rb') as p:
            privkey = rsa.PrivateKey.load_pkcs1(p.read())
        with open('cipher/rsa/keys/publicKey.pem', 'rb') as p:
            pubkey = rsa.PublicKey.load_pkcs1(p.read())
        return privkey, pubkey

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('utf-8'), key)

    def decrypt(self, ciphertext, key):
        return rsa.decrypt(ciphertext, key).decode('utf-8')

    def sign(self, message, key):
        return rsa.sign(message.encode('utf-8'), key, 'SHA-256')

    def verify(self, message, signature, key):
        try:
            rsa.verify(message.encode('utf-8'), signature, key)
            return True
        except:
            return False