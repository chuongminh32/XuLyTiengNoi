import matplotlib.pyplot as plt
import numpy as np

n = 1000 
t = np.linspace(0, 0.5, n)
A = 1
f1 = 10 
y1 = A * np.sin(2 * np.pi * f1 * t)

f2 = 100 
y2 = A * np.sin(2 * np.pi * f2 * t)

y = y1 + y2

plt.plot(t, y)
plt.xlabel('Time (s)')
plt.title('Sum two since waves')
plt.ylabel('Amplitude')
plt.show()