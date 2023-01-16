# Coded by ScratchyCode
# Utile per controllare la distribuzione in frequenza delle lettere generate, che approssimerà asintoticamente una distribuzione uniforme
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# lista di lettere generate (di prova)
SENTENCE = "AABBCCDDEEGGHHIIKKKKKKKKLMNO"

SENTENCE = sorted(SENTENCE)
SENTENCE = ''.join(SENTENCE) # lista -> stringa

# genera l'istogramma
letters_hist = Counter(SENTENCE.lower().replace('\n',''))
counts = letters_hist.values()
letters = letters_hist.keys()

# graficare i dati
bar_x_locations = np.arange(len(counts))
plt.bar(bar_x_locations, counts, align = 'center')
plt.xticks(bar_x_locations, letters)
plt.grid()
plt.show()
