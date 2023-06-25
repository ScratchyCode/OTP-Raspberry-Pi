# Generatore chiavi casuali
È stato pensato per monitorare i dati ambientali attraverso una raspberry ed introdurre l'entropia sufficiente nel programma.

Quello che viene eseguito è un ciclo infinito per incrementare una variabile in un range fissato e leggere lo stato della variabile
quando si verificano le condizioni ambientali stocastiche come piccole variazioni della pressione atmosferica.

Viene cosi prodotta una sequenza casuale, dimostrabile attraverso l'istogramma delle frequenze si osservano solo distribuzioni uniformi sulle chiavi generate.

# One-Time-Pad
È il tentativo di implementare un cifrario a flusso di tipo OTP attraverso il fix delle falle crittografiche del noto RC4, cercando di far coesistere la sicurezza dei cifrari OTP alla praticità dei cifrari più moderni come AES.

Un cifrario OTP è un cifrario perfetto perchè è matematicamente sicuro.

L'idea di base è quella di usare il cifrario Vigenere, insicuro di per sè, ed imporre particolari condizioni sulle chiavi per creare un nuovo cifrario, di tipo OTP, chiamato Vernam.

Le condizioni sono:
1) chiave crittografica lunga quanto il testo in chiaro
2) casualità della chiave
3) ad ogni testo in chiaro da cifrare deve corrispondere una chiave diversa (One Time Pad)

Il cifrario cosi definito resiste anche al bruteforce delle chiavi con potenza di calcolo infinita, perchè implementa il concetto di crittografia negabile, in quanto nel processo di crittoanalisi si estrarrebbero tutti i possibili testi di senso compiuto e non si potrebbe dire quale messaggio sia stato veramente scambiato.

# sincVernam.py
In sincVernam.py non si usa la matrice di Vigenere per la codifica ma l'operatore XOR per estendere l'alfabeto a tutti i char.

Essendo il cifrario Vernam di difficile implementazione per l'onerosa gestione delle chiavi, si cerca di adottare dei compromessi.

Il processo di crittografia è il seguente:
1) richiesta di una password
2) generazione dell'hash crittografico della password da usare come seed
3) inizializzazione di un generatore di numeri peseudocasuali crittograficamente sicuro usando l'hash precedente come seed
4) generare una sequenza di numeri pseudocasuali ma crittograficamente sicura da usare come chiave crittografica
5) eseguire lo XOR tra testo in chiaro e chiave crittografica
6) incrementare un contatore da appendere alla password iniziale per generare chiavi crittografiche sempre diverse
7) iterare i passaggi precedenti su messaggi in chiaro nuovi

Vengono quindi soddisfatte tutte le condizioni del cifrario Vernam:
1) la prima implementando un generatore che garantisce la lunghezza della chiave con il minimo sforzo
2) la casualità non c'è per consentire di ricavare le chiavi crittografiche a partire da una password, ci si avvicina alla sicurezza OTP per l'uso di un generatore pseudocasuale crittograficamente sicuro
3) per ogni nuovo messaggio in chiaro viene derivata una nuova chiave crittografica impossibile da ricavare senza conoscere la password iniziale

Inoltre viene calcolato un hash di integrità del messaggio ed appeso al testo cifrato.

Si potrebbe anche appendere alla fine del testo cifrato il contatore per garantire la sincronia e poter correggere errori di sincronizzazione nel caso in cui qualche messaggio venga perso. Il valore di questo contatore può essere pubblico svolgendo il ruolo logico di salt crittografico per la derivazione di nuove password.

Viene anche impostato un tempo di delay casuale di elaborazione dentro alle varie funzioni per mitigare attacchi di timing ed è aggiunto al messaggio in chiaro un timestamp con data e ora della cifratura per mitigare gli attacchi di replica.

# Crittoanalisi
1) L'unica crittoanalisi nota è sulla password, punto in cui il cifrario è più vulnerabile ad attacchi di bruteforce per esempio, ritenuti mitigabili però attraverso la forza della password scelta come per altri cifrari ritenuti sicuri come AES. Si consiglia di usare il cifrario all'interno di adeguati standard e protocolli sulla gestione delle password.

2) La crittografia negabile si ottiene trasformando il cifrario a flusso in un cifrario a blocchi che contengano un numero di char in chiaro uguali a quelli del digest dell'algoritmo di hashing crittografico usato, come per esempio sha512, e la derivazione di nuovi hash per ogni blocco di testo in chiaro.

# OTP.py
Il programma riprende la versione fixata di sincVernam.py ed aggiunge la possibilità di usare, oltre ad una password, un file di dati casuali come chiave crittografica, bypassando a derivazione delle chiavi generate con un generatore pseudocasuale.

La generazione di chiavi pseudocasuali subentra nel momento in cui viene esaurito il file usato come chiave crittografica, perchè ad ogni byte di messaggio cifrato o decifrato corrisponde una riduzione di un byte del file chiave tramite il suo troncamento, evitandone il reimpiego e garantendo la sicurezza OTP. 

L'uso sicuro richiede lo sviluppo di un protocollo ed un framework all'interno del quale avviene la gestione delle chiavi casuali e della sincronizzazione delle comunicazioni.
