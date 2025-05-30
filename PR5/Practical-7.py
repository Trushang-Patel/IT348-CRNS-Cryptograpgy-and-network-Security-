import sympy
import random
import psutil
import time

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

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

def mod_inverse(a, m):
    gcd_value, x, y = extended_gcd(a, m)
    if gcd_value != 1:
        raise ValueError(f"{a} and {m} are not coprime, modular inverse does not exist.")
    else:
        return x % m

def generate_large_prime(decimal_digits):
    return sympy.randprime(10**(decimal_digits-1), 10**decimal_digits)

def generate_public_exponent(phi_n, decimal_digits):
    e = random.randint(10**(decimal_digits-1), 10**decimal_digits - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(10**(decimal_digits-1), 10**decimal_digits - 1)
    return e

def generate_keys(decimal_digits):
    cpu_before, ram_before = get_system_utilization()

    p = generate_large_prime(decimal_digits)
    q = generate_large_prime(decimal_digits)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = generate_public_exponent(phi_n, decimal_digits)

    cpu_during_gen, ram_during_gen = get_system_utilization()

    d = mod_inverse(e, phi_n)

    cpu_after, ram_after = get_system_utilization()

    print("\nKey Generation Utilization:")
    print(f"CPU Before Key Generation: {cpu_before}% | RAM Before Key Generation: {ram_before}%")
    print(f"CPU During Key Generation: {cpu_during_gen}% | RAM During Key Generation: {ram_during_gen}%")
    print(f"CPU After Key Generation: {cpu_after}% | RAM After Key Generation: {ram_after}%")
    
    return ((n, e), (n, d), p, q)

def encrypt(message, pub_key):
    n, e = pub_key
    cipher_text = [pow(ord(char), e, n) for char in message]
    return cipher_text

def decrypt(cipher_text, priv_key):
    n, d = priv_key
    message = ''.join([chr(pow(char, d, n)) for char in cipher_text])
    return message

def get_system_utilization():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return cpu, ram

def rsa_algorithm(message, decimal_digits):
    start_time = time.time()

    pub_key, priv_key, p, q = generate_keys(decimal_digits)
    
    cpu_before_enc, ram_before_enc = get_system_utilization()
    
    cipher_text = encrypt(message, pub_key)

    cpu_during_enc, ram_during_enc = get_system_utilization()
    
    decrypted_message = decrypt(cipher_text, priv_key)
    
    cpu_after_enc, ram_after_enc = get_system_utilization()

    end_time = time.time()

    print(f"\nOriginal Message: {message}")
    print(f"Ciphertext: {cipher_text}")
    print(f"Decrypted Message: {decrypted_message}")

    print("\nSystem Utilization During Encryption/Decryption:")
    print(f"CPU Before Encryption: {cpu_before_enc}% | RAM Before Encryption: {ram_before_enc}%")
    print(f"CPU During Encryption: {cpu_during_enc}% | RAM During Encryption: {ram_during_enc}%")
    print(f"CPU After Encryption: {cpu_after_enc}% | RAM After Encryption: {ram_after_enc}%")

    print(f"Execution Time: {end_time - start_time:.6f} seconds")
    print(f"Generated Prime p: {p}")
    print(f"Generated Prime q: {q}")
    print(f"Public Exponent e: {pub_key[1]}")
    print(f"Private Exponent d: {priv_key[1]}")

if __name__ == "__main__":
    message = input("Enter the message to encrypt: ")
    decimal_digits = int(input("Enter the number of decimal digits for p, q, and e: "))
    rsa_algorithm(message, decimal_digits)
