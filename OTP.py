# Coded by Pietro Squilla
# consente l'uso di file casuali come chiavi OTP oltre al normale uso dell'algoritmo sincVernam
import hashlib
import base64
import getpass
import time
import random
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac

def seed_da_stringa(s):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    return hashlib.sha512(s.encode('utf-8')).digest()

def cifratura_vernam(messaggio, chiave):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    return bytes(a ^ b for a, b in zip(messaggio, chiave))

def genera_chiave(seed, lunghezza, contatore, file_chiavi=None):
    time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
    if file_chiavi and os.path.exists(file_chiavi):  # se il file esiste leggi la chiave da li, altrimenti genera la chiave dal seed
        return leggi_chiave_da_file(file_chiavi, lunghezza, contatore)
    else:
        informazioni = b"chiave cifratura OTP"
        hkdf = HKDF(algorithm=hashes.SHA512(), length=lunghezza, salt=None, info=informazioni)
        return hkdf.derive(seed)

def leggi_chiave_da_file(file_name, lunghezza, contatore):
    with open(file_name, 'rb') as f:
        f.seek(contatore)  # sposta il puntatore del file
        chiave = f.read(lunghezza)
        if len(chiave) != lunghezza:  # se non ci sono abbastanza byte, solleva un'eccezione
            raise ValueError("Tutti i byte nel file sono stati utilizzati.")
    return chiave

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

def aggiorna_contatore(contatore):
    with open('contatore.txt', 'w') as f:
        f.write(str(contatore))

def main():
    try:
        with open('contatore.txt', 'r') as f:
            contatore = int(f.read())
    except FileNotFoundError:
        contatore = 0

    password = getpass.getpass("Password iniziale: ")
    file_chiavi = input("File chiave OTP (lascia vuoto per derivare la chiave dalla password): ")
    
    while True:
        try:
            scelta = input("Vuoi cifrare (C), decifrare (D), sincronizzare (S) o uscire (X)? ")
            
            if scelta.upper() == 'C':
                messaggio = input("Messaggio: ")
                timestamp = time.strftime("%H:%M:%S %d-%m-%Y", time.localtime())
                messaggio = timestamp + " " + messaggio
                messaggio_originale = messaggio.encode()
                messaggio = base64.b64encode(messaggio_originale)
                
                time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
                password_agg = hash_password(password, contatore)
                seed = seed_da_stringa(password_agg)
                chiave = genera_chiave(seed, len(messaggio), contatore, file_chiavi)
                
                hmac_messaggio = calcola_hmac(chiave, messaggio_originale)
                messaggio_cifrato = cifratura_vernam(messaggio, chiave)
                messaggio_cifrato_base64 = base64.urlsafe_b64encode(messaggio_cifrato + hmac_messaggio)
                
                print("Messaggio cifrato:", messaggio_cifrato_base64.decode())
                contatore += len(chiave)
                aggiorna_contatore(contatore)
                print(f"\n{len(chiave)} byte del file chiave sono stati utilizzati.")
            
            elif scelta.upper() == 'D':
                messaggio_cifrato_base64 = input("Messaggio cifrato: ")
                messaggio_cifrato_hmac = base64.urlsafe_b64decode(messaggio_cifrato_base64)
                messaggio_cifrato = messaggio_cifrato_hmac[:-64]
                hmac_ricevuto = messaggio_cifrato_hmac[-64:]
                
                time.sleep(random.uniform(0.01, 0.5))  # ritardo casuale
                password_agg = hash_password(password, contatore)
                seed = seed_da_stringa(password_agg)
                chiave = genera_chiave(seed, len(messaggio_cifrato), contatore, file_chiavi)
                
                messaggio = cifratura_vernam(messaggio_cifrato, chiave)
                messaggio_originale = base64.b64decode(messaggio)
                
                hmac_calcolato = calcola_hmac(chiave, messaggio_originale)
                
                if hmac_ricevuto != hmac_calcolato:
                    raise ValueError("L'integrità del messaggio è stata compromessa!")
                
                parts = messaggio_originale.decode().split(' ', 2)
                timestamp = parts[0] + ' ' + parts[1]
                messaggio_decifrato = parts[2]
                print("\nTimestamp:", timestamp)
                print("Messaggio decifrato:", messaggio_decifrato)
                contatore += len(chiave)
                aggiorna_contatore(contatore)
                print(f"\n{len(chiave)} byte del file chiave sono stati utilizzati.")
            
            elif scelta.upper() == 'S':
                scarto = int(input("Inserisci il pin di sincronizzazione: "))
                contatore += scarto
                aggiorna_contatore(contatore)
                print("Sincronizzazione eseguita.")
            
            elif scelta.upper() == 'X':
                break
            
            else:
                print("\nScelta non valida. Per favore inserisci 'C' per cifrare, 'D' per decifrare, 'S' per sincronizzare, o 'X' per uscire.")
        
        except Exception as e:
            print(f"\nSi è verificato un errore: {e}\n")

if __name__ == "__main__":
    main()
