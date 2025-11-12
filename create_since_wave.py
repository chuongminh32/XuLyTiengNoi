import matplotlib.pyplot as plt
import numpy as np

n = 1000 
t = np.linspace(0, 0.5, n)
A = 1
f = 10 
y = A * np.sin(2 * np.pi * f * t)
plt.plot(t, y)
plt.xlabel('Time (s)')
plt.title('Song since co f = 10 Hz va A = 1')
plt.ylabel('Amplitude')
plt.grid(visible=True)
plt.show()