import numpy as np
N = 16 
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], dtype="float32")  
X = np.fft.fft(x)
# Nếu cần thì tách thành 2 thành phần là thực và ảo 
XR = X.real
XI = X.imag

S = abs(X)
print(S)
x_original = np.fft.ifft(X)
print(x_original)