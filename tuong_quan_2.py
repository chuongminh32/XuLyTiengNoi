import numpy as np 

# chuẩn hóa dữ liệu
x = np.array([[1, 3], [2, 8], [6, 4]], dtype = np.float64)
m = np.mean(x, 0)
x = x - m
print(m)

# Tính ma trận hiệp phương sai
C = np.matmul(x.T, x)
c = C / 3 
print(c)