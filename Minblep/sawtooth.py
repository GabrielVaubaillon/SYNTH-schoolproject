import matplotlib.pyplot as plt
import numpy as np

from minblep_tables import *
from slope_dd_table import *

# minBLEP table oversampling factor (must be a power of two)
MINBLEP_PHASES = 64
MINBLEP_PHASE_MASK = 63

# length in samples of (truncated) step discontinuity delta
STEP_DD_PULSE_LENGTH = 72

# length in samples of (truncated) slope discontinuity delta
SLOPE_DD_PULSE_LENGTH = 71

# the longer of the two above
LONGEST_DD_PULSE_LENGTH = max(STEP_DD_PULSE_LENGTH, SLOPE_DD_PULSE_LENGTH)

# Delay between start of DD pulse and the discontinuity, in samples:
DD_SAMPLE_DELAY = 4

# Audio Sampling frequency
SAMPLERATE = 48000

# Note pitch
frequency = 440

# Number of periods to generate
nper = 5
nsamples = nper * SAMPLERATE // frequency

# Init output vector
y = np.zeros( (nsamples + DD_SAMPLE_DELAY ,1), float)


# Building the waveform
# ---------------------

b = 0.5
w = frequency / SAMPLERATE

phase = 0.0

index = 0

while index < nsamples :
    
    phase = phase + w
    
    if phase >= 1.0:
        phase -= 1.0

        r = MINBLEP_PHASES * phase/w
        i = round(r - 0.5)
        r = r - i
        j = index
        i = i & MINBLEP_PHASE_MASK

        while i < (MINBLEP_PHASES * STEP_DD_PULSE_LENGTH):
            if j < nsamples:
                y[j] += step_dd_table[i][0] + r * step_dd_table[i][1]
            i += MINBLEP_PHASES
            j += 1

    y[index + DD_SAMPLE_DELAY] += 0.5 - phase
    index += 1

# On affiche la forme temporelle :
tdomain = plt.figure(1)
plt.plot([i for i in range(len(y))],y)
tdomain.show()


signal = y
# Performs Hanning Windowing
N = nsamples + DD_SAMPLE_DELAY
win = np.hanning(N)
y2 = win * signal.transpose()

# Calculate and displays spectrums
spectrum = np.fft.fft(y2)
spectrum = np.fft.fftshift(spectrum)
spectrum = abs(spectrum)+ np.finfo(float).eps
spectrum = spectrum[0]
spectrum = spectrum[N//2:N]
spectrum = 20 * np.log(spectrum)
maxspectrum = max(spectrum)
spectrum = [i - maxspectrum for i in spectrum]

# Builds frequency (x) scale
f = [SAMPLERATE/N * i for i in range(0,N//2+1)]

fdomain = plt.figure(2)
plt.plot(f,spectrum)
plt.xscale("log")
fdomain.show()

# To keep figures alive :
input("Press ENTER to continue")
