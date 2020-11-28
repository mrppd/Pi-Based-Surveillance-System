# -*- coding: utf-8 -*-
"""
Created on Thu May  2 01:40:43 2019

@author: Pronaya
"""

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import statistics as st
import noisereduce as nr
import numpy as np
import scipy.fftpack as sp
from scipy.io.wavfile import read
from scipy.io.wavfile import write     # Imported libaries such as numpy, scipy(read, write), matplotlib.pyplot
from scipy import signal
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

url = "G:\Work\Educational info\Gottingen\WSN lab\ProjectWork"

def stereoToMono(audiodata):
    #d = (audiodata[:,0] + audiodata[:,1]) / 2
    d = audiodata.sum(axis=1) / 2
    return np.array(d, dtype='float')

def amplify(audiodata, times):
    return audiodata*times

fs=16000
duration = 120  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float32')
print("Recording Audio")
sd.wait()
print("Audio recording complete , Play Audio")
sd.play(myrecording, fs*1)

myrecording_mono = stereoToMono(myrecording)
sd.play(myrecording_mono, fs*1)

myrecording_mono_amp = amplify(myrecording_mono, 300)
sd.play(myrecording_mono_amp, fs*1)
sd.wait()
print("Play Audio Complete")

write(url+"\sound.wav", fs, myrecording_mono_amp) # Saving it to the file.



rec_silent = sd.rec(10 * fs, samplerate=fs, channels=2, dtype='float32')
sd.wait()
sd.play(rec_silent, fs*1)
rec_silent_mono = stereoToMono(rec_silent)
rec_silent_mono_amp = amplify(rec_silent_mono, 300)
sd.play(rec_silent_mono_amp, fs*1)
sd.wait()


output = nr.reduce_noise(
    audio_clip=myrecording_mono_amp,
    noise_clip=rec_silent_mono_amp,
    n_std_thresh=2,
    prop_decrease=0.95,
)
output = amplify(output, 10)
sd.play(output, fs*1)
sd.wait()



len(myrecording_mono_amp)
myrecording_mono_amp_FT = sp.rfft(myrecording_mono_amp, 255)
rec_silent_mono_amp_FT = sp.rfft(rec_silent_mono_amp, 255)

plt.plot(myrecording_mono_amp_FT)
plt.plot(rec_silent_mono_amp_FT)

#myrecording_mono_amp_FT_n = myrecording_mono_amp_FT[myrecording_mono_amp_FT<200]
#myrecording_mono_amp_FT_n =  myrecording_mono_amp_FT_n[myrecording_mono_amp_FT_n>-200]


plt.plot(myrecording_mono_amp_FT)

new_rec_FT = myrecording_mono_amp_FT - rec_silent_mono_amp_FT
new_rec = sp.irfft(myrecording_mono_amp_FT[5:100], 80000)
plt.plot(new_rec)

sd.play(new_rec, fs*1)
sd.wait()






b,a = signal.butter(5, 1000/(fs/2), btype='highpass') # ButterWorth filter 4350
filteredSignal = signal.lfilter(b,a,myrecording_mono_amp)
plt.plot(filteredSignal) # plotting the signal.
plt.title('Highpass Filter')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Amplitude')


c,d = signal.butter(5, 380/(fs/2), btype='lowpass') # ButterWorth low-filter
newFilteredSignal = signal.lfilter(c,d,filteredSignal) # Applying the filter to the signal
plt.plot(newFilteredSignal) # plotting the signal.
plt.title('Lowpass Filter')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Amplitude')


sd.play(newFilteredSignal, fs*1)
sd.wait()
print("Play Audio Complete")