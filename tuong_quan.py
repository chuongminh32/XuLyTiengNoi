import random 
random.seed(100)

# Tạo số ngẫu nhiên (0,1)
n = 100000 
x = []
for i in range(0, n):
    x1 = 0.4*random.random() - 1.2
    x2 = 0.4*random.random() - 0.2
    v = [x1, x2]
    x.append(v)
m1 = 0
m2 = 0
sum1 = 0.0
sum2 = 0.0
for i in range(0, n):
    sum1 = sum1 + x[i][0]
    sum2 = sum2 + x[i][1]
m1 = sum1 / n 
m2 = sum2 / n 
m = [m1,m2]
print('m1 = %.2f' % m1)
print('m2 = %.2f' % m2)

# Tính ma trận hiệp phương sai: covariance
C = [[0,0],[0,0]]
for i in range(0, n):
    C[0][0] = C[0][0] + x[i][0] * x[i][0] - m[0]*m[0]
    C[0][1] = C[0][1] + x[i][0] * x[i][1] - m[0]*m[1]
    C[1][0] = C[1][0] + x[i][1] * x[i][0] - m[1]*m[0]
    C[1][1] = C[1][1] + x[i][1] * x[i][1] - m[1]*m[1]
C[0][0] = C[0][0] / n 
C[0][1] = C[0][1] / n 
C[1][0] = C[1][0] / n 
C[1][1] = C[1][1] / n 
