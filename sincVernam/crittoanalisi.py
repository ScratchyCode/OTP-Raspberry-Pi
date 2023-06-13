# Coded by Pietro Squilla

# Test eseguito con l'aritmetica modulare che distingue i char ASCII come esempio, con periodo 256.
# Dopo 256 cifrature, si riottiene lo stesso messaggio cifrato di partenza.
# Si dimostra che è possibile ricavare la sequenza pseudocasuale usata come chiave tramite operatore XOR.
import hashlib
import base64
import time
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac

def seed_da_stringa(s):
    return hashlib.sha512(s.encode('utf-8')).digest()

def cifratura_vernam(messaggio, chiave):
    return bytes(a ^ b for a, b in zip(messaggio, chiave))

def genera_chiave(seed, lunghezza):
    informazioni = b"chiave cifratura vernam"
    hkdf = HKDF(algorithm=hashes.SHA512(), length=lunghezza, salt=None, info=informazioni)
    return hkdf.derive(seed)

def calcola_hmac(chiave, messaggio):
    h = hmac.HMAC(chiave, hashes.SHA512())
    h.update(messaggio)
    return h.finalize()

def main():
    contatore = 0
    password = "PasswordSicura" # password predefinita
    messaggio = "Segretissimo" # messaggio predefinito
    messaggio_originale = messaggio.encode()
    messaggio = base64.b64encode(messaggio_originale)
    
    with open("crittoanalisi.txt", "w") as f:
        while contatore <= 256: 
            print(f"Messaggio {contatore}")
            password_agg = "".join(chr((ord(c) + contatore) % 256) for c in password)
            seed = seed_da_stringa(password_agg)
            chiave = genera_chiave(seed, len(messaggio))
            
            hmac_messaggio = calcola_hmac(chiave, messaggio_originale)
            messaggio_cifrato = cifratura_vernam(messaggio, chiave)
            messaggio_cifrato_base64 = base64.urlsafe_b64encode(messaggio_cifrato + hmac_messaggio)
            
            f.write(f"Messaggio cifrato {contatore}: {messaggio_cifrato_base64.decode()}\n")
            contatore += 1

if __name__ == "__main__":
    main()

