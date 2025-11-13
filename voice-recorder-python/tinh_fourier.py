import numpy as np
N = 512 
x = np.zeros((N,1), dtype="float32")

for i in range (1, N):
    if i % 2 == 1:
        x[i] = 1
    else:
        x[i] = -1
X = np.fft.fft(x)
# Nếu cần thì tách thành 2 thành phần là thực và ảo 
XR = X.real
XI = X.imag

S = abs(X)
pass
f = open('fourier.txt', 'wt')
str = ''
for i in range(0, 257):
    str = '%3d %10.4f\n' % (i, S[i])
f.write(str)
f.close()



