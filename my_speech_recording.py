import tkinter as tk
from tkinter import messagebox as msb
from tkinter import ttk
import tkinter.filedialog as fd

import sounddevice as sd
import queue
import soundfile as sf
import threading


class App(tk.Tk):
    def	__init__(self):
        super().__init__()
        # Create a queue to contain the audio data
        self.q = queue.Queue()
        # Declare variables and initialise them
        self.recording = False
        self.file_exists = False    
        self.data = None
        self.index = 0  # Changed from -1 to 0

        self.title('Speech Signal Processing')
        # Tạo widget
        self.cvs_figure = tk.Canvas(self, width = 600, height = 300, relief = tk.SUNKEN, border = 1)

        lblf_upper = tk.LabelFrame(self)
        btn_open = tk.Button(lblf_upper, text = 'Open', width = 8, command=self.open_file)
        btn_cut = tk.Button(lblf_upper, text = 'Cut', width = 8, command=self.cut_file)
        btn_record = tk.Button(lblf_upper, text = 'Record', width = 8, command=lambda m=1:self.threading_rec(m))
        btn_stop = tk.Button(lblf_upper, text = 'Stop', width = 8, command=lambda m=2:self.threading_rec(m))
        btn_play = tk.Button(lblf_upper, text = 'Play', width = 8, command=lambda m=3:self.threading_rec(m))


        btn_open.grid(row = 0, padx = 5, pady = 5)
        btn_cut.grid(row = 1, padx = 5, pady = 5)
        btn_record.grid(row = 2, padx = 5, pady = 5)
        btn_stop.grid(row = 3, padx = 5, pady = 5)
        btn_play.grid(row = 4, padx = 5, pady = 5)

        lblf_lower = tk.LabelFrame(self)
        self.factor_zoom = tk.StringVar()
        self.cbo_zoom = ttk.Combobox(lblf_lower, width = 7, textvariable = self.factor_zoom)
        self.cbo_zoom.bind('<<ComboboxSelected>>', self.factor_zoom_changed)

        self.cbo_zoom['state'] = 'readonly'

        btn_next = tk.Button(lblf_lower, text = 'Next', width = 8, command = self.btn_next_click)
        btn_prev = tk.Button(lblf_lower, text = 'Prev', width = 8, command = self.btn_prev_click)


        self.cbo_zoom.grid(row = 0, padx = 5, pady = 5)
        btn_next.grid(row = 1, padx = 5, pady = 5)
        btn_prev.grid(row = 2, padx = 5, pady = 5)

        # Đưa widget lên lưới
        self.cvs_figure.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = 5)
        lblf_upper.grid(row = 0, column = 1, padx = 5, pady = 6, sticky = tk.N)
        lblf_lower.grid(row = 1, column = 1, padx = 5, pady = 6, sticky = tk.S)


    def factor_zoom_changed(self, event):
        factor_zoom = self.factor_zoom.get()
        self.index = 0  # Changed from -1 to 0
        print(factor_zoom)

    #Fit data into queue
    def callback(self, indata, frames, time, status):
        self.q.put(indata.copy())


    #Functions to play, stop and record audio
    #The recording is done as a thread to prevent it being the main process
    def threading_rec(self, x):
        if x == 1:
            #If recording is selected, then the thread is activated
            t1=threading.Thread(target = self.record_audio)
            t1.start()
        elif x == 2:
            #To stop, set the flag to false
            self.recording = False
            msb.showinfo(title = 'Stop Recording', message="Recording finished")
            self.data, fs = sf.read("trial.wav", dtype = 'int16')
            L = len(self.data)
            N = L // 600

            lst_values = []
            for i in range(1, N+1):
                s = '%10d' % i
                lst_values.append(s)
            self.cbo_zoom['values'] = lst_values 

            yc = 150
            # Xoá canvas
            self.cvs_figure.delete(tk.ALL)
            for x in range(0, 600-1):
                a = int(self.data[x*N])
                b = int(self.data[(x+1)*N])
                y1 = (a + 32767)*300//65535 - 150
                y2 = (b + 32767)*300//65535 - 150
                self.cvs_figure.create_line(x, yc-y1, x+1, yc-y2, fill = 'green')

        elif x == 3:
            #To play a recording, it must exist.
            if self.file_exists:
                #Read the recording if it exists and play it
                data, fs = sf.read("trial.wav", dtype='float32') 
                sd.play(data,fs)
                sd.wait()
            else:
                #Display and error if none is found
                msb.showerror(title = 'Error', message="Record something to play")

    #Recording function
    def record_audio(self):
        #Set to True to record
        self.recording = True   
        #Create a file to save the audio
        msb.showinfo(title = 'Recording Speech', message = "Speak into the mic")
        with sf.SoundFile("trial.wav", mode='w', samplerate = 16000,
                            channels = 1) as file:
        #Create an input stream to record audio without a preset time
                with sd.InputStream(samplerate = 16000, channels = 1, callback = self.callback):
                    while self.recording == True:
                        #Set the variable to True to allow playing the audio later
                        self.file_exists = True
                        #write into file
                        file.write(self.q.get())

    def btn_zoom_click(self):
        if self.data is None:
            return
            
        self.cvs_figure.delete(tk.ALL)
        yc = 150
        i = self.index
        
        # Check bounds
        if i*600 + 600 > len(self.data):
            return
            
        for x in range(0, 600-1):
            a = int(self.data[i*600 + x])
            b = int(self.data[i*600 + x + 1])
            y1 = (a + 32767)*300//65535 - 150
            y2 = (b + 32767)*300//65535 - 150
            self.cvs_figure.create_line(x, yc-y1, x+1, yc-y2, fill = 'green')

    def btn_next_click(self):
        if self.data is None:
            return
            
        factor_zoom = self.factor_zoom.get()
        if not factor_zoom:
            msb.showwarning(title='Warning', message='Please select a zoom factor first')
            return
            
        factor_zoom = int(factor_zoom.strip()) 
        data_temp = self.data[::factor_zoom]
        L = len(data_temp)
        N = L // 600
        
        # Check if we can go next
        if self.index >= N - 1:
            msb.showinfo(title='Info', message='Already at the end')
            return
            
        self.index = self.index + 1
        i = self.index
        print("index =", i)
        
        # Bounds check
        if i*600 + 600 > len(data_temp):
            self.index = self.index - 1  # Revert
            msb.showinfo(title='Info', message='Cannot go further')
            return
            
        self.cvs_figure.delete(tk.ALL)
        yc = 150
        for x in range(0, 600-1):
            a = int(data_temp[i*600 + x])
            b = int(data_temp[i*600 + x + 1])
            y1 = (a + 32767)*300//65535 - 150
            y2 = (b + 32767)*300//65535 - 150
            self.cvs_figure.create_line(x, yc-y1, x+1, yc-y2, fill = 'green')
            
    def btn_prev_click(self):
        if self.data is None:
            return
            
        factor_zoom = self.factor_zoom.get()
        if not factor_zoom:
            msb.showwarning(title='Warning', message='Please select a zoom factor first')
            return
            
        factor_zoom = int(factor_zoom.strip()) 
        data_temp = self.data[::factor_zoom]
        L = len(data_temp)
        N = L // 600
        
        # Check if we can go previous
        if self.index <= 0:
            msb.showinfo(title='Info', message='Already at the beginning')
            return
            
        self.index = self.index - 1
        i = self.index
        print("index =", i)
        
        self.cvs_figure.delete(tk.ALL)
        yc = 150
        for x in range(0, 600-1):
            a = int(data_temp[i*600 + x])
            b = int(data_temp[i*600 + x + 1])
            y1 = (a + 32767)*300//65535 - 150
            y2 = (b + 32767)*300//65535 - 150
            self.cvs_figure.create_line(x, yc-y1, x+1, yc-y2, fill = 'green')
            
    def open_file(self):
        filetypes = [("wave files", "*.wav")]
        filename = fd.askopenfilename(title="Open wave files", filetypes=filetypes)
        if filename:    
            print(filename)
        else:
            return
            
        self.recording = False
        self.data, fs = sf.read(filename, dtype = 'int16')
        L = len(self.data)
        N = L // 600

        lst_values = []
        for i in range(1, N+1):
            s = '%10d' % i
            lst_values.append(s)
        self.cbo_zoom['values'] = lst_values 
        
        # Reset index when loading new file
        self.index = 0

        yc = 150
        # Xoá canvas
        self.cvs_figure.delete(tk.ALL)
        for x in range(0, 600-1):
            # Convert samples to Python int to avoid int16 overflow during arithmetic
            a = int(self.data[x*N])
            b = int(self.data[(x+1)*N])
            y1 = (a + 32767)*300//65535 - 150
            y2 = (b + 32767)*300//65535 - 150
            self.cvs_figure.create_line(x, yc-y1, x+1, yc-y2, fill = 'green')
            
    def cut_file(self):
        if self.data is None:
            msb.showerror(title='Error', message='No audio data loaded')
            return
            
        start = 38*600 - 100
        end = 49*600 - 100
        
        # Bounds checking
        if start < 0 or end > len(self.data):
            msb.showerror(title='Error', message='Cut range exceeds audio length')
            return
            
        data_temp = self.data[start: end]
        self.data = data_temp.copy()
        
        # Reset index after cutting
        self.index = 0
        msb.showinfo(title='Success', message='Audio cut successfully')
        
if __name__ == "__main__":
    app	=	App()
    app.mainloop()