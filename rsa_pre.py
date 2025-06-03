import pickle
import random

def load_keys_from_file(filename, pri_key=random.randint(1, 99)):
    with open(filename, 'rb') as file:
        keys = pickle.load(file)
    
    random_int = pri_key % len(keys)
    key = keys[random_int]
    return key

def encrypt_rsa(m, e, n):
    return pow(m, e, n)

def proxy_decrypt(c, d1, n):
    return pow(c, d1, n)

def final_decrypt(c_proxy, d2, n):
    return pow(c_proxy, d2, n)


def rsa_run(m, pri_key):
    # message to number
    m = int.from_bytes(m.encode(), 'big')
    pri_key = int.from_bytes(pri_key.encode(), 'big')

    keys = load_keys_from_file('keys.pkl', pri_key)
    e = keys['e']
    d = keys['d']
    d1 = keys['d1']
    d2 = keys['d2']
    n = keys['n']

    c = encrypt_rsa(m, e, n)

    c_proxy = proxy_decrypt(c, d1, n)

    m_decrypted = final_decrypt(c_proxy, d2, n)

    # assert m == m_decrypted, "Decryption failed"

    m = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()

    return c, c_proxy, m

def run(m, pri_key):
    # message to number
    m = int.from_bytes(m.encode(), 'big')
    pri_key = int.from_bytes(pri_key.encode(), 'big')
    print(f"Message: {m}")
    print(f"Private Key: {pri_key}")

    keys = load_keys_from_file('keys.pkl', pri_key)
    e = keys['e']
    d = keys['d']
    d1 = keys['d1']
    d2 = keys['d2']
    n = keys['n']

    c = encrypt_rsa(m, e, n)
    print(f"Encrypted message: {c}")

    c_proxy = proxy_decrypt(c, d1, n)
    print(f"Proxy decrypted message: {c_proxy}")


    m_decrypted = final_decrypt(c_proxy, d2, n)
    print(f"Final decrypted message: {m_decrypted}")

    assert m == m_decrypted, "Decryption failed"
    print("Decryption successful!")

    m = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
    print(f"Original message: {m}")
    return c, c_proxy, m
if __name__ == "__main__":
    run('hello', 'qdm3')
