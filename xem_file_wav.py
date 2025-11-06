import numpy as np

# đọc thủ công header của một file WAV
f = open("trial_01.wav", "rb")

# Đọc định danh file
chunkID = f.read(4)
print("%c%c%c%c" % (chunkID[0], chunkID[1], chunkID[2], chunkID[3]))

# Đọc kích thước của file
chunkSize = f.read(4)
chunkSize = (
    chunkSize[3] * 256**3 + chunkSize[2] * 256**2 + chunkSize[1] * 256 + chunkSize[0]
)
print("%d" % chunkSize)

# Đọc định dạng
format = f.read(4)
print("%c%c%c%c" % (format[0], format[1], format[2], format[3]))

# Đọc phần định dạng
subChunk1D = f.read(4)
print("%c%c%c%c" % (subChunk1D[0], subChunk1D[1], subChunk1D[2], subChunk1D[3]))

# Đọc kích thước của phần định dạng
# Convert from bytes to integer value follow ing little-endian format
subChunk1Size = f.read(4)
subChunk1Size = (
    subChunk1Size[3] * 256**3
    + subChunk1Size[2] * 256**2
    + subChunk1Size[1] * 256
    + subChunk1Size[0]
)
print("%d" % subChunk1Size)

# Đọc chuẩn PCD
audioFormat = f.read(2)
audioFormat = audioFormat[1] * 256 + audioFormat[0]
print("Chuẩn PCD là: %d" % audioFormat)

# Đọc số kênh
numberChannels = f.read(2)
numberChannels = numberChannels[1] * 256 + numberChannels[0]
print("Số kênh: %d" % numberChannels)

# Đọc tần số mẫu
sampleRate = f.read(4)
sampleRate = (
    sampleRate[3] * 256**3
    + sampleRate[2] * 256**2
    + sampleRate[1] * 256
    + sampleRate[0]
)
print("Tần số lấy mẫu hay tốc độ lấy mẫu: %d" % sampleRate)

# Đọc byte rate
byteRate = f.read(4)
byteRate = byteRate[3] * 256**3 + byteRate[2] * 256**2 + byteRate[1] * 256 + byteRate[0]
print("Tốc độ byte: %d" % byteRate)

# Đọc block align
blockAlign = f.read(2)
blockAlign = blockAlign[1] * 256 + blockAlign[0]
print("Số byte của một block: %d" % blockAlign)

# Bit per sample
bitsPerSample = f.read(2)
x = bitsPerSample
bitsPerSample = bitsPerSample[1] * 256 + bitsPerSample[0]
print("Số lượng bit của một mẫu: %d" % bitsPerSample)

# Đọc phần dữ liệu
subChunk2D = f.read(4)
print("%c%c%c%c" % (subChunk2D[0], subChunk2D[1], subChunk2D[2], subChunk2D[3]))

# Đọc kích thước của phần dữ liệu
dataSizeByte = f.read(4)
dataSizeByte = (
    dataSizeByte[3] * 256**3
    + dataSizeByte[2] * 256**2
    + dataSizeByte[1] * 256
    + dataSizeByte[0]
)
print("Kích thước phần dữ liệu: %d" % dataSizeByte)

dataSize = dataSizeByte // 2
data = np.zeros((dataSize), np.int16)

for i in range(9, dataSize):
    x = f.read(2)
    y = int.from_bytes(x, byteorder="little", signed=True)
    data[i] = y
    # if dem < 100:
    #     print("Mẫu thứ %d: %d" % (i + 1, data[i]))
    #     dem += 1

f.close()
pass
