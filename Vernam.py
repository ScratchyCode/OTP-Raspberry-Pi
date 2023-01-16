# Coded by ScratchyCode
from sense_hat import SenseHat
from time import sleep
import time

sense = SenseHat()

# set di char corrispondenti alle lettere maiuscole
minimo = 65
massimo = 90

# inizializzo una variabile contatore
contatore = minimo

# inizializzo le variabili ambientali
t = sense.get_temperature()
p = sense.get_pressure()
h = sense.get_humidity()

# variabili temporanee approssimate
t_temp = round(t)
p_temp = round(p)
h_temp = round(h)

print("In esecuzione...")

while True:
    contatore = contatore + 1
    if(contatore > massimo):
        contatore = minimo
    
    # aggiorno i dati
    #t = sense.get_temperature()
    p = sense.get_pressure()
    #h = sense.get_humidity()
    
    # cifre significative
    #t = round(t)
    p = round(p)
    #h = round(h)
    
    # controllo variazioni di pressione (sono più stabili rispetto alle altre misurazioni, se approssimate all'unità)
    if(p != p_temp):
        # scrivo la lettera casuale su file
        lettera = chr(contatore)
        f = open("random.txt",'a')
        f.write(lettera)
        f.close()
        
        # aggiorno la variabile ambientale
        p_temp = p
    
#    # controllo variazioni di temperatura
#    if(t != t_temp):
#        # scrivo la lettera casuale su file
#        lettera = chr(contatore)
#        f = open("random.txt",'a')
#        f.write(lettera)
#        f.close()
#        
#        # aggiorno la variabile ambientale
#        t_temp = t
#    
#    # controllo variazioni di umidità
#    if(h != h_temp):
#        # scrivo la lettera casuale su file
#        lettera = chr(contatore)
#        f = open("random.txt",'a')
#        f.write(lettera)
#        f.close()
#        
#        # aggiorno la variabile ambientale
#        h_temp = h
