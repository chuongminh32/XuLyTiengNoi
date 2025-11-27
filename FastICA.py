import numpy as np 
from scipy import signal 
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA

# ... các import khác (ví dụ: import numpy as np) ...

# Dòng code gây lỗi (sẽ hoạt động sau khi import):
ics = FastICA(n_components=3, whiten="arbitrary-variance")
# ...

np.random.seed(100)
n_samples = 2000
time = np.linspace(0, 8, n_samples)
s1 = np.sin(2 * time)  # Signal 1 : sine wave
s2 = np.sign(np.sin(3 * time))  # Signal 2 : square wave
s3 = signal.sawtooth(2 * np.pi * time)  # Signal 3: saw tooth wave
S = np.vstack([s1, s2, s3])  # Stack the signals
S = S.T
S += 0.2 * np.random.normal(size=S.shape)  # Add noise

# chuẩn hóa bằng cách chia cho độ lệch chuẩn để có mean = 0
S = S/S.std(axis=0)



# Tạo tín hiệu trộn 
A= np.array([[1, 1, 1], [0.5, 2, 1.0], [1.5, 1.0, 2.0]])  # Mixing matrix

X = np.matmul(S, A.T)

# compute ICA
ics = FastICA(n_components=3, whiten="arbitrary-variance")
SR = ics.fit_transform(X)  # Reconstruct signals
sr = SR[:,0]
plt.plot(time, sr)
plt.show()
pass