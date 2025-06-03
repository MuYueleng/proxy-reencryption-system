import json
import random
from Crypto.Util import number
from Crypto.PublicKey import RSA
from tqdm import tqdm

def generate_rsa_keys(bits=1024):
    key = RSA.generate(bits)
    n = key.n
    e = key.e
    d = key.d
    p = key.p
    q = key.q
    phi = (p-1) * (q-1)
    return (e, n), (d, n, phi)

#  return d1, d2, d1 * d2 = d mod phi
def split_secret_key(d, phi):
    d1 = random.randint(1, phi)
    d2 = (d * pow(d1, -1, phi)) % phi
    return d1, d2

# Save keys to a file
def save_keys_to_file(filename, keys):
    with open(filename, 'w') as file:
        json.dump(keys, file)

# Main function to generate and save keys
def run():
    (e, n), (d, n, phi) = generate_rsa_keys()
    d1, d2 = split_secret_key(d, phi)
    keys = {
        'e': e,
        'd': d,
        'd1': d1,
        'd2': d2,
        'n': n
    }
    return keys


def main():
    # 如果抛出异常
    sum_keys = []
    import pickle
    correct_n = 0
    Num = 20
    for i in tqdm(range(Num)):
        try:
            run()
            sum_keys.append(run())
            correct_n += 1
            if correct_n == 100:
                break
        except Exception as e:
            pass
    print(f"Generate {correct_n} keys successfully!")
    with open('keys.pkl', 'wb') as f:
        pickle.dump(sum_keys, f)


if __name__ == "__main__":
    main()
