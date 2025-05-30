import random
from sympy import isprime


def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num
        
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        return old_r, old_s, old_t

    g, s, t = extended_gcd(e, phi)
    if g != 1:
        raise Exception("No modular inverse")
    else:
        return s % phi

def generate_rsa_keys(bits=512):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537  
    if gcd(e, phi) != 1:
        raise Exception("e and phi(n) are not coprime")
    
    d = mod_inverse(e, phi)
    
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key

def encrypt(public_key, message):
    n, e = public_key
    return pow(message, e, n)

def decrypt(private_key, ciphertext):
    n, d = private_key
    return pow(ciphertext, d, n)

if __name__ == "__main__":
    public_key, private_key = generate_rsa_keys(bits=17)  
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    message = 42 
    ciphertext = encrypt(public_key, message)
    print(f"Encrypted: {ciphertext}")

    decrypted_message = decrypt(private_key, ciphertext)
    print(f"Decrypted: {decrypted_message}")
