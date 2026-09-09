Simple FFT code with high pass filter Sure. The code is a small digital signal-processing experiment. It creates a known test signal, removes its DC component with a high-pass filter, calculates the frequency spectrum using our own FFT implementation, and plots the results.

Import the libraries
import numpy as np import matplotlib.pyplot as plt

NumPy is used for arrays, mathematical operations, complex numbers, sine waves, etc. Matplotlib is used to plot the signals.

Our own FFT function
def fft(x): N = len(x) if N == 1: return x

x is the input signal and N is the number of samples.

The FFT works recursively. Eventually, the signal is divided until each part contains only one sample. At that point there is nothing more to divide, so:

return x

Then:

even = fft(x[::2]) odd = fft(x[1::2])

splits the signal into even and odd sample positions.

For example:

x = [1, 2, 3, 4] even = [1, 3] odd = [2, 4]

Each half is then passed through fft() again.

The results are combined using the twiddle factor:

W = np.exp(-2j * np.pi * k / N)

which represents

W_N^k=e^{-j2\pi k/N}.

The butterfly operation is:

X[k] = even[k] + W * odd[k] X[k + N // 2] = even[k] - W * odd[k]

or mathematically:

X[k]=E[k]+W_N^kO[k]

X[k+N/2]=E[k]-W_N^kO[k].

This is a basic radix-2 Cooley–Tukey FFT. Therefore, our implementation assumes that N is a power of two, such as 256, 512, 1024, etc.

⸻

The high-pass filter
The second function removes DC and very slowly changing parts of the signal:

def highpass(x, fs, fc):

Here:

x = input signal
fs = sampling frequency
fc = cutoff frequency
We first calculate the sampling interval:

dt = 1 / fs

For example, with

f_s=1024\text{ Hz}

the time between samples is

\Delta t=\frac{1}{1024}\approx0.000977\text{ s}.

We then calculate the equivalent RC time constant:

RC = 1 / (2 * np.pi * fc)

because an analog RC high-pass filter has the cutoff frequency

f_c=\frac{1}{2\pi RC}.

Then:

alpha = RC / (RC + dt)

calculates the coefficient used by our digital approximation of the RC filter.

The actual filtering happens here:

for n in range(1, len(x)): y[n] = alpha * ( y[n-1] + x[n] - x[n-1] )

which implements

y[n]=\alpha \left( y[n-1]+x[n]-x[n-1] \right).

The important part is

x[n]-x[n-1].

A constant voltage gives zero difference. For example:

5-5=0.

Therefore, a constant DC voltage eventually disappears from the output.

⸻

Define the sampling
fs = 1024 N = 1024 t = np.arange(N) / fs

We take 1024 samples per second:

f_s=1024\text{ Hz}.

We also take exactly 1024 samples:

N=1024.

Therefore, the measurement lasts

T=\frac{N}{f_s} =\frac{1024}{1024} =1\text{ second}.

This particular choice also gives us a convenient FFT frequency resolution:

\Delta f=\frac{f_s}{N} =\frac{1024}{1024} =\boxed{1\text{ Hz}}.

So FFT bins correspond to:

bin 0 → 0 Hz bin 1 → 1 Hz bin 2 → 2 Hz ... bin 10 → 10 Hz ... bin 50 → 50 Hz

⸻

Create the test signal
We create a 10 Hz sine wave:

signal_10Hz = 1.0 * np.sin(2 * np.pi * 10 * t)

which mathematically is

x_1(t)=1.0\sin(2\pi10t).

Its amplitude is 1 V.

We also create a 50 Hz sine wave:

signal_50Hz = 0.5 * np.sin(2 * np.pi * 50 * t)

or

x_2(t)=0.5\sin(2\pi50t).

Its amplitude is 0.5 V.

We combine them:

x = signal_10Hz + signal_50Hz

and add a DC offset:

DC = 5.0 x = x + DC

So our complete input signal is

\boxed{ x(t)=5+ \sin(2\pi10t) + 0.5\sin(2\pi50t) }

and contains:

Component Frequency Amplitude DC 0 Hz 5 V sine 10 Hz 1 V sine 50 Hz 0.5 V

⸻

Apply the high-pass filter
fc = 1.0 x_filtered = highpass(x, fs, fc)

We choose a cutoff frequency of

f_c=1\text{ Hz}.

The DC component at 0 Hz is strongly rejected.

The 10 Hz and 50 Hz components are well above the cutoff frequency, so most of those signals pass through.

Conceptually:

5 V DC ───────────┐ │ 10 Hz sine ───────┼──> High-pass ──> mainly 10 Hz + 50 Hz │ 50 Hz sine ───────┘ ↑ fc = 1 Hz

⸻

Perform the FFT
Now we send the filtered signal into our FFT:

X = fft(x_filtered)

Before the FFT we have a signal as a function of time:

x[n].

After the FFT we have information as a function of frequency:

X[k].

So conceptually:

Time domain Frequency domain voltage amplitude │ │ │ ∿∿∿∿∿ │ │ │ │ │ │ └───────> time FFT └────┼───────┼──> Hz 10 50

⸻

Create the frequency axis
frequencies = np.arange(N) * fs / N

FFT output index k corresponds to frequency

\boxed{ f_k=\frac{k f_s}{N} }

and because here f_s=N=1024:

f_k=k.

So index 10 represents 10 Hz and index 50 represents 50 Hz.

⸻

Convert complex FFT values into amplitudes
The FFT produces complex numbers, so we first calculate their magnitudes:

amplitude = np.abs(X) / N

np.abs(X) calculates

|X[k]|= \sqrt{ \operatorname{Re}(X[k])^2+ \operatorname{Im}(X[k])^2 }.

We divide by N to scale the FFT magnitude relative to the number of samples.

⸻

Keep only positive frequencies
For a real-valued signal, the FFT contains a mirrored negative-frequency half.

Therefore:

half = N // 2 frequencies = frequencies[:half] amplitude = amplitude[:half]

keeps only:

0\le f <\frac{f_s}{2}.

Since

f_s=1024\text{ Hz},

the highest frequency of interest is the Nyquist frequency:

f_\mathrm{Nyquist}=\frac{1024}{2}=512\text{ Hz}.

Because we removed the negative half, we compensate by doubling the positive-frequency amplitudes:

amplitude[1:] = 2 * amplitude[1:]

For this example that should give approximately:

A(10\text{ Hz})\approx1

and

A(50\text{ Hz})\approx0.5.

The high-pass filter causes a small amplitude and phase modification, so the values are not mathematically identical to an unfiltered ideal sinusoid.

⸻

Plot the signals
The first graph compares:

plt.plot(t, x, label="Original") plt.plot(t, x_filtered, label="After high-pass filter")

The original signal oscillates around approximately 5 V, while the high-pass-filtered signal eventually oscillates around approximately 0 V.

The second graph:

plt.plot(frequencies, amplitude)

shows the frequency spectrum.

You should see strong peaks around:

\boxed{10\text{ Hz}}

and

\boxed{50\text{ Hz}}.

The complete signal chain

The whole program can therefore be summarized as:

Generate test signal │ ▼ 5 V DC offset

10 Hz / 1 V
50 Hz / 0.5 V │ ▼ ┌─────────────────┐ │ High-pass filter│ │ fc = 1 Hz │ └────────┬────────┘ │ │ removes DC ▼ ┌─────────────────┐ │ Our FFT │ └────────┬────────┘ │ ▼ complex X[k] │ ▼ |X[k]| │ ▼ Amplitude spectrum │ ▼ 10 Hz → ~1 V 50 Hz → ~0.5 V
One thing I would change for the next experiment is to plot the FFT before and after the high-pass filter on the same scale. That makes the large 0 Hz peak from the 5 V DC offset and its removal immediately visible.

The concepts used here are standard in DSP and Python-based signal-processing education; useful references include Qayyum (2025), Fast Fourier Transform Implementation Project as an FPGA Learning Tool (⁠IEEE); Moustafa et al. (2025), A smart web-based power quality and energy monitoring system… (⁠IEEE); Han (2024), Implementation of Fast Fourier Transform in image processing, signal processing and acoustics (⁠IET); Li et al. (2026), Research and implementation of wideband radio signal channelization based on RFSoC (⁠IOP); Abostait et al. (2023), Design and FPGA-based hardware implementation… (⁠Electronics); Gondhalekar et al. (2025), On the Adaptation of Mixed-Radix Fast Fourier Transform… (⁠IEEE); Hekkala (2025), GNSS narrowband interference mitigation for IoT devices (⁠University of Oulu); and Rippel et al., Development of a Permittivity-Meter (⁠PDF)
