import PySimpleGUI as sg
import subprocess
from rsa_pre import rsa_run
import random
import time

def ecc_return(message):
    run_process = subprocess.run(["./main", message], capture_output=True, text=True)
    if run_process.returncode != 0:
        print("Execution failed:")
        print(run_process.stdout)
        print(run_process.stderr)
    else:
        pass

    import json
    with open('ecc_pre.json') as f:
        data = json.load(f)

    original_message = data['string_plain_text']
    Alice_private_key = data['a_pub_key']
    Alice_public_key = data['a_pri_key']
    Bob_private_key = data['b_pub_key']
    Bob_public_key = data['b_pri_key']
    rk = data['rk']
    pub_x = data['pub_x']
    cipher_text = data['cipher_text']
    plain_text = data['plain_text']
    
    return cipher_text, rk, plain_text



def proxy_re_encryption(message, method):
    # Dummy encryption and decryption functions for demonstration purposes
    start_t = time.time()
    if method == 'ECC':
        alice_encrypted, proxy_re_encrypted, bob_decrypted = ecc_return(message)
        
        # print(bob_decrypted)
    else:
        alice_encrypted, proxy_re_encrypted, bob_decrypted = rsa_run(message, 'qdm3')
    use_time = time.time() - start_t
    # print(f"Time used: {use_time}")
    return alice_encrypted, proxy_re_encrypted, bob_decrypted, use_time


if __name__ == '__main__':
    layout = [
        [sg.Text('Origin Message:', font=('Helvetica', 15, 'bold')), sg.InputText(key='-MESSAGE-')],
        [sg.Text('                                        ECC                              ', font=('Helvetica', 18, 'bold')), sg.Text('RSA       ', font=('Helvetica', 18, 'bold'))],
        [sg.Text('Alice Encrypto', size=(15, 1)), sg.InputText(key='-ECC_ALICE-', size=(40, 2)), sg.InputText(key='-RSA_ALICE-', size=(40, 2))],
        [sg.Text('Proxy Re-Encrypto', size=(15, 1)), sg.InputText(key='-ECC_PROXY-', size=(40, 1)), sg.InputText(key='-RSA_PROXY-', size=(40, 1))],
        [sg.Text('Bob Decrypto', size=(15, 1)), sg.InputText(key='-ECC_BOB-', size=(40, 1)), sg.InputText(key='-RSA_BOB-', size=(40, 1))],
        [sg.Text('Use Time(s)', size=(15, 1)), sg.InputText(key='-ECC_TIME-', size=(40, 1)), sg.InputText(key='-RSA_TIME-', size=(40, 1))],
        [sg.Text('Whether Succeed'), sg.InputText(key='-SUCCESS-', size=(15, 1))],
        [sg.Button('Start')]
    ]

    window = sg.Window('Proxy Re-Encryption (PRE)', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Start':
            message = values['-MESSAGE-']
            print(message)
            # Perform ECC proxy re-encryption
            ecc_alice, ecc_proxy, ecc_bob, u_time = proxy_re_encryption(message, 'ECC')
            window['-ECC_ALICE-'].update(ecc_alice)
            window['-ECC_PROXY-'].update(ecc_proxy)
            window['-ECC_BOB-'].update(ecc_bob)
            window['-ECC_TIME-'].update(u_time)
            
            # Perform RSA proxy re-encryption
            rsa_alice, rsa_proxy, rsa_bob, u_time = proxy_re_encryption(message, 'RSA')
            window['-RSA_ALICE-'].update(rsa_alice)
            window['-RSA_PROXY-'].update(rsa_proxy)
            window['-RSA_BOB-'].update(rsa_bob)
            window['-RSA_TIME-'].update(u_time)
            
            # Update success status
            success = "Yes" if message else "No"
            window['-SUCCESS-'].update(success)

    window.close()
