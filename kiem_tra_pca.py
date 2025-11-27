import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

rng = np.random.default_rng(100)
n = 72000
# Tạo dữ liệu 2 chiều có phân phối Gauss
x = rng.normal(size=(n, 2))

# Làm trắng dữ liệu 
pca = PCA(whiten=True)
y = pca.fit_transform(x)

# Tính ma trận hiệp phương sai
C = np.matmul(y.T, y)
print(C/n)
print("Done")
