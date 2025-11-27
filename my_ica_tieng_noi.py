import numpy as np 
import sounddevice as sd

fs = 16000
f = open('mix_01.txt', 'rt')
data = f.read()
f.close()
data = data.split()
x1 = []
for value in data:
    x1.append(int(value)/32768)
s1 = np.array(x1)
s1 = s1.astype(np.float32)
sd.play(s1, fs)
sd.wait()

f = open('mix_02.txt', 'rt')
data = f.read()
f.close()
data = data.split()
x2 = []
for value in data:
    x2.append(int(value)/32768)

s2 = np.array(x2)
s2 = s2.astype(np.float32)
sd.play(s2, fs)
sd.wait()

