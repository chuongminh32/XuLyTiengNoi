import numpy as np 
from sklearn.decomposition import PCA
f = open('mix_01.txt', 'rt')
data = f.read()
f.close()
data = data.split()
x1 = []
for value in data:
    x1.append(int(value)/32768)

f = open('mix_02.txt', 'rt')
data = f.read()
f.close()
data = data.split()
x2 = []
for value in data:
    x2.append(int(value)/32768)
n = len(x1)


x = np.zeros((n, 2), np.float64)
for i in range(0, n):
    x[i][0] = x1[i]
    x[i][1] = x2[i]
# chuẩn hóa dữ liệu  
m = np.mean(x,0)
x = x - m

pca = PCA(white=true)


# Tính ma trận hiệp phương sai 
C = np.matmul(x.T, x)
C = C/n
print(C)