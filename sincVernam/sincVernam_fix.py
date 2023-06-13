# Coded by Pietro Squilla
# Fix basato sulla combinazione non lineare della password e del contatore
import hashlib
import base64
import getpass
import time
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac

def seed_da_stringa(s):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    return hashlib.sha512(s.encode('utf-8')).digest()

def cifratura_vernam(messaggio, chiave):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    return bytes(a ^ b for a, b in zip(messaggio, chiave))

def genera_chiave(seed, lunghezza):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    informazioni = b"chiave cifratura vernam"
    hkdf = HKDF(algorithm=hashes.SHA512(), length=lunghezza, salt=None, info=informazioni)
    return hkdf.derive(seed)

def calcola_hmac(chiave, messaggio):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    h = hmac.HMAC(chiave, hashes.SHA512())
    h.update(messaggio)
    return h.finalize()

def hash_password(password, contatore):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    password_contatore = password + str(contatore)
    hashed = hashlib.sha256(password_contatore.encode()).hexdigest()
    return hashed

def main():
    contatore = 0
    password = getpass.getpass("Password iniziale: ")
    while True:
        try:
            scelta = input("Vuoi cifrare (C), decifrare (D) o uscire (E)? ")
            
            if scelta.upper() == 'C':
                messaggio = input("Messaggio: ")
                messaggio_originale = messaggio.encode()
                messaggio = base64.b64encode(messaggio_originale)
                
                time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
                password_agg = hash_password(password, contatore)
                seed = seed_da_stringa(password_agg)
                chiave = genera_chiave(seed, len(messaggio))
                
                hmac_messaggio = calcola_hmac(chiave, messaggio_originale)
                messaggio_cifrato = cifratura_vernam(messaggio, chiave)
                messaggio_cifrato_base64 = base64.urlsafe_b64encode(messaggio_cifrato + hmac_messaggio)
                
                print("Messaggio cifrato:", messaggio_cifrato_base64.decode())
                contatore += 1
            
            elif scelta.upper() == 'D':
                messaggio_cifrato_base64 = input("Messaggio cifrato: ")
                messaggio_cifrato_hmac = base64.urlsafe_b64decode(messaggio_cifrato_base64)
                messaggio_cifrato = messaggio_cifrato_hmac[:-64]
                hmac_ricevuto = messaggio_cifrato_hmac[-64:]
                
                time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
                password_agg = hash_password(password, contatore)
                seed = seed_da_stringa(password_agg)
                chiave = genera_chiave(seed, len(messaggio_cifrato))
                
                messaggio = cifratura_vernam(messaggio_cifrato, chiave)
                messaggio_originale = base64.b64decode(messaggio)
                
                hmac_calcolato = calcola_hmac(chiave, messaggio_originale)
                
                if hmac_ricevuto != hmac_calcolato:
                    raise ValueError("L'integrità del messaggio è stata compromessa!")
                
                print("Messaggio decifrato:", messaggio_originale.decode())
                contatore += 1
            
            elif scelta.upper() == 'E':
                break
            
            else:
                print("Scelta non valida. Per favore inserisci 'C' per cifrare, 'D' per decifrare, o 'E' per uscire.")
        
        except Exception as e:
            print(f"Si è verificato un errore: {e}\n")

if __name__ == "__main__":
    main()

