import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Egen FFT (radix-2 Cooley-Tukey)
# ------------------------------------------------------------

def fft(x):
    """Beräknar FFT för en signal med längd N = 2^k."""
    n = len(x)

    if n == 1:
        return x

    even = fft(x[::2])
    odd = fft(x[1::2])

    result = np.zeros(n, dtype=complex)

    for k in range(n // 2):
        w = np.exp(-2j * np.pi * k / n)
        result[k] = even[k] + w * odd[k]
        result[k + n // 2] = even[k] - w * odd[k]

    return result


# ------------------------------------------------------------
# 2. Eget högpassfilter
# ------------------------------------------------------------

def highpass(x, fs, fc):
    """Approximerar ett första ordningens RC-högpassfilter."""
    dt = 1 / fs
    rc = 1 / (2 * np.pi * fc)
    alpha = rc / (rc + dt)

    y = np.zeros(len(x))
    for n in range(1, len(x)):
        y[n] = alpha * (y[n - 1] + x[n] - x[n - 1])

    return y


# ------------------------------------------------------------
# 3. Skapa testsignal
# ------------------------------------------------------------

def create_signal(t):
    frequencies = [1, 5, 10, 15, 20, 25, 30, 35]
    signal = np.zeros_like(t)

    for freq in frequencies:
        signal += np.sin(2 * np.pi * freq * t)

    signal += 5.0  # DC-offset
    return signal


# ------------------------------------------------------------
# 4. FFT-analys
# ------------------------------------------------------------

def calculate_amplitude_spectrum(signal, fs):
    spectrum = fft(signal)
    amplitude = np.abs(spectrum) / len(signal)

    half = len(signal) // 2
    frequencies = np.arange(len(signal)) * fs / len(signal)
    frequencies = frequencies[:half]
    amplitude = amplitude[:half]
    amplitude[1:] *= 2

    return frequencies, amplitude


# ------------------------------------------------------------
# 5. Plotting
# ------------------------------------------------------------

def plot_time_signal(t, original, filtered):
    plt.figure()
    plt.plot(t, original, label="Original")
    plt.plot(t, filtered, label="Efter högpassfilter")
    plt.xlabel("Tid [s]")
    plt.ylabel("Spänning [V]")
    plt.title("Tidssignal")
    plt.legend()
    plt.grid(True)



def plot_frequency_spectrum(frequencies, amplitude):
    plt.figure()
    plt.plot(frequencies, amplitude)
    plt.xlabel("Frekvens [Hz]")
    plt.ylabel("Amplitud")
    plt.title("FFT efter högpassfilter")
    plt.xlim(0, 100)
    plt.grid(True)


# ------------------------------------------------------------
# 6. Huvudprogram
# ------------------------------------------------------------

def main():
    fs = 1024
    n = 1024
    t = np.arange(n) / fs

    x = create_signal(t)
    fc = 10.0
    x_filtered = highpass(x, fs, fc)

    frequencies, amplitude = calculate_amplitude_spectrum(x_filtered, fs)

    plot_time_signal(t, x, x_filtered)
    plot_frequency_spectrum(frequencies, amplitude)
    plt.show()


if __name__ == "__main__":
    main()