# import tkinter as tk
# from tkinter import messagebox as msb
# from tkinter import ttk
# import tkinter.filedialog as fd
# import soundfile as sf
# import numpy as np


# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.data = None

#         self.title("Speech Signal Processing")
#         # Tạo widget
#         self.cvs_figure = tk.Canvas(
#             self, width=600, height=600, relief=tk.SUNKEN, border=1
#         )

#         lblf_upper = tk.LabelFrame(self)
#         btn_open = tk.Button(lblf_upper, text="Open", width=12, command=self.open_file)
#         btn_cut = tk.Button(lblf_upper, text="Cut", width=12, command=self.cut_file)
#         btn_view = tk.Button(lblf_upper, text="View", width=12, command=self.view_cut)
#         btn_spec = tk.Button(
#             lblf_upper, text="Spectogram", width=12, command=self.spectogram
#         )

#         btn_open.grid(row=0, padx=5, pady=5)
#         btn_cut.grid(row=1, padx=5, pady=5)
#         btn_view.grid(row=2, padx=5, pady=5)
#         btn_spec.grid(row=3, padx=5, pady=5)

#         # Đưa widget lên lưới
#         self.cvs_figure.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
#         lblf_upper.grid(row=0, column=1, padx=5, pady=6, sticky=tk.N)

#     def open_file(self):
#         filetypes = [("wave files", "*.wav")]
#         filename = fd.askopenfilename(title="Open wave files", filetypes=filetypes)
#         if filename:
#             print(filename)
#         self.recording = False
#         self.data, fs = sf.read(filename, dtype="int16")
#         L = len(self.data)
#         N = L // 600

#         lst_values = []
#         for i in range(1, N + 1):
#             s = "%10d" % i
#             lst_values.append(s)

#         yc = 300
#         # Xoá canvas
#         self.cvs_figure.delete(tk.ALL)
#         for x in range(0, 600 - 1):
#             # Convert samples to Python int to avoid int16 overflow during arithmetic
#             a = int(self.data[x * N])
#             b = int(self.data[(x + 1) * N])
#             y1 = (a + 32767) * 600 // 65535 - 300
#             y2 = (b + 32767) * 600 // 65535 - 300
#             self.cvs_figure.create_line(x, yc - y1, x + 1, yc - y2, fill="green")

#     def cut_file(self):
#         start = 38 * 600 - 100
#         end = 49 * 600 - 100
#         data_temp = self.data[start:end]
#         self.data = data_temp.copy()
#         L = len(self.data)

#     def view_cut(self):
#         L = len(self.data)
#         N = L // 600
#         lst_values = []
#         for i in range(1, N + 1):
#             s = "%10d" % i
#             lst_values.append(s)

#         yc = 300
#         # Xoá canvas
#         self.cvs_figure.delete(tk.ALL)
#         for x in range(0, 600 - 1):
#             # Convert samples to Python int to avoid int16 overflow during arithmetic
#             a = int(self.data[x * N])
#             b = int(self.data[(x + 1) * N])
#             y1 = (a + 32767) * 600 // 65535 - 300
#             y2 = (b + 32767) * 600 // 65535 - 300
#             self.cvs_figure.create_line(x, yc - y1, x + 1, yc - y2, fill="green")

#     def spectogram(self):
#         L = len(self.data)
#         data_temp = self.data / 32768
#         data_temp = data_temp.astype("float32")
#         N = L // 600
#         yc = 300
#         index = 0
#         zeroes = np.zeros((112,), dtype="float32")
#         for i in range(0, 600):
#             frame = self.data[i * N : i * N + 400]
#             frame = np.hstack((frame, zeroes))
#             X = np.fft.fft(frame)
#             S = abs(X)
#             gray = np.zeros((257,), np.float32)
#             for j in range(len(S)):
#                 val = S[j] * 255 / 512
#                 val = max(val, 1e-10)  # tránh log(0)
#                 gray = 20 * np.log10(val)  # tính log (dB)
#                 gray = np.clip(gray, 0, 255)  # giữ trong khoảng 0–255
#                 color = "#%02x%02x%02x" % (int(gray), int(gray), int(gray))
#                 self.cvs_figure.create_line(i, 300 - j, i, 300 - j - 1, fill=color)


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()


import tkinter as tk
from tkinter import messagebox as msb
from tkinter import ttk
import tkinter.filedialog as fd
import soundfile as sf
import numpy as np


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data = None

        self.title("Speech Signal Processing")
        # Tạo widget
        self.cvs_figure = tk.Canvas(
            self, width=600, height=600, relief=tk.SUNKEN, border=1
        )

        lblf_upper = tk.LabelFrame(self)
        btn_open = tk.Button(lblf_upper, text="Open", width=12, command=self.open_file)
        btn_cut = tk.Button(lblf_upper, text="Cut", width=12, command=self.cut_file)
        btn_view = tk.Button(lblf_upper, text="View", width=12, command=self.view_cut)
        btn_spec = tk.Button(
            lblf_upper, text="Spectogram", width=12, command=self.spectogram
        )

        btn_open.grid(row=0, padx=5, pady=5)
        btn_cut.grid(row=1, padx=5, pady=5)
        btn_view.grid(row=2, padx=5, pady=5)
        btn_spec.grid(row=3, padx=5, pady=5)

        # Đưa widget lên lưới
        self.cvs_figure.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        lblf_upper.grid(row=0, column=1, padx=5, pady=6, sticky=tk.N)

    def open_file(self):
        filetypes = [("wave files", "*.wav")]
        filename = fd.askopenfilename(title="Open wave files", filetypes=filetypes)
        if filename:
            print(filename)
        self.recording = False
        self.data, fs = sf.read(filename, dtype="int16")
        L = len(self.data)
        N = L // 600

        lst_values = []
        for i in range(1, N + 1):
            s = "%10d" % i
            lst_values.append(s)

        yc = 300
        # Xoá canvas
        self.cvs_figure.delete(tk.ALL)
        for x in range(0, 600 - 1):
            # Convert samples to Python int to avoid int16 overflow during arithmetic
            a = int(self.data[x * N])
            b = int(self.data[(x + 1) * N])
            y1 = (a + 32767) * 600 // 65535 - 300
            y2 = (b + 32767) * 600 // 65535 - 300
            self.cvs_figure.create_line(x, yc - y1, x + 1, yc - y2, fill="green")

    def cut_file(self):
        start = 38 * 600 - 100
        end = 49 * 600 - 100
        data_temp = self.data[start:end]
        self.data = data_temp.copy()
        L = len(self.data)

    def view_cut(self):
        L = len(self.data)
        N = L // 600
        lst_values = []
        for i in range(1, N + 1):
            s = "%10d" % i
            lst_values.append(s)

        yc = 300
        # Xoá canvas
        self.cvs_figure.delete(tk.ALL)
        for x in range(0, 600 - 1):
            a = int(self.data[x * N])
            b = int(self.data[(x + 1) * N])
            y1 = (a + 32767) * 600 // 65535 - 300
            y2 = (b + 32767) * 600 // 65535 - 300
            self.cvs_figure.create_line(x, yc - y1, x + 1, yc - y2, fill="green")

    def spectogram(self):
        L = len(self.data)
        N = L // 600
        yc = 300
        
        # Clear canvas
        self.cvs_figure.delete(tk.ALL)
        
        zeroes = np.zeros((112,), dtype="float32")
        
        for i in range(0, 600):
            # Extract frame
            frame = self.data[i * N : i * N + 400].astype("float32")
            frame = np.hstack((frame, zeroes))
            
            # Compute FFT
            X = np.fft.fft(frame)
            S = np.abs(X[:257])  # Only take first 257 points (half + DC)
            
            # Convert to dB scale, avoiding log(0)
            S_db = np.zeros_like(S)
            for j in range(len(S)):
                if S[j] > 0:
                    S_db[j] = 20 * np.log10(S[j] / 512 + 1e-10)
                else:
                    S_db[j] = -100  # Very low value for silence
            
            # Normalize to 0-255 range
            # Typical dB range is -100 to 0
            gray_values = np.clip((S_db + 100) * 255 / 100, 0, 255)
            
            # Draw spectrogram column
            for j in range(len(gray_values)):
                gray_val = int(gray_values[j])
                color = "#%02x%02x%02x" % (gray_val, gray_val, gray_val)
                self.cvs_figure.create_line(i, 300 - j, i, 300 - j - 1, fill=color)


if __name__ == "__main__":
    app = App()
    app.mainloop()