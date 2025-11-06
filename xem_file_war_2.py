import soundfile as sf

data, sf = sf.read("trial_01.wav", dtype="int16")
L = len(data)
print("L = %d" % L)
pass
