import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. EGEN FFT
# ============================================================

def fft(x):
    N = len(x)

    # Rekursionens slut
    if N == 1:
        return x

    # Dela upp i jämna och udda sampel
    even = fft(x[::2])
    odd = fft(x[1::2])

    X = np.zeros(N, dtype=complex)

    # Kombinera resultaten
    for k in range(N // 2):

        W = np.exp(-2j * np.pi * k / N)

        X[k] = even[k] + W * odd[k]

        X[k + N // 2] = even[k] - W * odd[k]

    return X


# ============================================================
# 2. EGET HÖGPASSFILTER
# ============================================================

def highpass(x, fs, fc):

    dt = 1 / fs

    RC = 1 / (2 * np.pi * fc)

    alpha = RC / (RC + dt)

    y = np.zeros(len(x))

    for n in range(1, len(x)):

        y[n] = alpha * (
            y[n-1]
            + x[n]
            - x[n-1]
        )

    return y


# ============================================================
# 3. SKAPA EN TESTSIGNAL
# ============================================================

fs = 1024          # samplingsfrekvens [Hz]
N = 1024           # antal sampel

t = np.arange(N) / fs


# Två sinusvågor
signal_10Hz = 1.0 * np.sin(2 * np.pi * 10 * t)

signal_50Hz = 0.5 * np.sin(2 * np.pi * 50 * t)


# Lägg ihop dem
x = signal_10Hz + signal_50Hz


# Lägg till DC-offset
DC = 5.0

x = x + DC


# ============================================================
# 4. HÖGPASSFILTRERA
# ============================================================

fc = 1.0       # gränsfrekvens 1 Hz

x_filtered = highpass(x, fs, fc)


# ============================================================
# 5. FFT
# ============================================================

X = fft(x_filtered)


# ============================================================
# 6. SKAPA FREKVENSAXEL
# ============================================================

frequencies = np.arange(N) * fs / N


# ============================================================
# 7. BERÄKNA AMPLITUD
# ============================================================

amplitude = np.abs(X) / N


# Vi använder bara positiva frekvenser
half = N // 2

frequencies = frequencies[:half]

amplitude = amplitude[:half]


# Korrigera amplituden eftersom vi bara visar
# den positiva halvan av spektrumet
amplitude[1:] = 2 * amplitude[1:]


# ============================================================
# 8. RITA TIDSSIGNALEN
# ============================================================

plt.figure()

plt.plot(t, x, label="Original")
plt.plot(t, x_filtered, label="Efter högpassfilter")

plt.xlabel("Tid [s]")
plt.ylabel("Spänning [V]")

plt.title("Tidssignal")

plt.legend()
plt.grid()

plt.show()


# ============================================================
# 9. RITA FFT
# ============================================================

plt.figure()

plt.plot(frequencies, amplitude)

plt.xlabel("Frekvens [Hz]")
plt.ylabel("Amplitud")

plt.title("FFT efter högpassfilter")

plt.xlim(0, 100)

plt.grid()

plt.show()