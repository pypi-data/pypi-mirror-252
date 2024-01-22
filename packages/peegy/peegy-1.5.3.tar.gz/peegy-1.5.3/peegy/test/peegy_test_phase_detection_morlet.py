import astropy.units as u
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from ssqueezepy import Wavelet


reference_frequency = 40 * u.Hz
half_width = 40 * u.ms
fs = 512*8 * u.Hz
# M is just for plot. We use CWT for convolution
M = 1000
time = np.arange(M) / fs
s = (half_width.to(u.s) * fs)
w = reference_frequency * (2 * s * np.pi) / fs
wavelet = signal.morlet2(M, s, w)
plt.plot(time, abs(wavelet) / np.max(abs(wavelet)))
plt.plot(time, np.real(wavelet) / np.max(abs(wavelet)))
plt.show()

# define test stimuli and reference signal
duration = 1 * u.s
time = np.arange(0, int(duration * fs)) / fs
ini_phase = np.pi / 2 * u.rad
# reference is cosine convolved with wavelet so that phase includes the filter response
wavelet = Wavelet('morlet')
# Wx, scales = cwt(np.cos(2 * np.pi * reference_frequency * u.rad * time - ini_phase), wavelet)
# freqs_cwt = scale_to_freq(scales, wavelet, time.shape[0], fs=fs.value)
# _ifreq = np.argwhere(freqs_cwt == reference_frequency.value)
# reference_signal = Wx.T[:, _ifreq[0]]
# reference_signal = signal.cwt(np.cos(2 * np.pi * reference_frequency * u.rad * time - ini_phase),
#                               signal.morlet2, widths=[s], w=w).T * u.dimensionless_unscaled
reference_signal = (np.cos(2 * np.pi * reference_frequency * u.rad * time[:, None] - ini_phase) +
                    1j * np.sin(2 * np.pi * reference_frequency * u.rad * time[:, None] - ini_phase))
reference_signal = reference_signal / np.abs(reference_signal)

fig1, axs = plt.subplots(2)
# now we estimate the phase changes for a range of phase transitions at the mid-point of the time axis
for phase in np.linspace(0, np.pi * 0.9, 10) * u.rad:
    # generate test signal
    data = (np.cos(2 * np.pi * u.rad * reference_frequency * time - ini_phase)[:, None] +
            0.1 * np.random.randn(time.size, 1))
    # generate phase transition
    data[data.shape[0] // 10::] = (np.cos(2 * np.pi * u.rad * reference_frequency * time[data.shape[0] // 10::] -
                                          ini_phase + phase)[:, None] +
                                   0.1 * np.random.randn(time[data.shape[0] // 10::].size, 1))

    data[data.shape[0] // 4::] = (np.cos(2 * np.pi * u.rad * reference_frequency * time[data.shape[0] // 4::] -
                                         ini_phase + 2 * phase)[:, None] +
                                  0.1 * np.random.randn(time[data.shape[0] // 4::].size, 1))

    # convolve signal with complex-wavelet
    y_filter = np.zeros(data.shape, dtype=complex)
    ####
    # wavelet = Wavelet('morlet')
    # Wx, scales = cwt(data.value.T, wavelet)
    # freqs_cwt = scale_to_freq(scales, wavelet, y_filter.shape[0], fs=fs.value)
    # _ifreq = np.argwhere(freqs_cwt == reference_frequency.value)
    # y_filter = Wx.T[:, _ifreq[0], ...]
    ####
    if data.ndim == 1:
        y_filter = signal.cwt(data.value, signal.morlet2, widths=[s], w=w)
        y_filter = y_filter[:, None, None]
    if data.ndim == 2:
        for _i in range(y_filter.shape[1]):
            y_filter[:, _i] = signal.cwt(data[:, _i].value, signal.morlet2,
                                         widths=[s], w=w)
            y_filter = y_filter[:, None]
    if data.ndim == 3:
        for _i in range(y_filter.shape[1]):
            for _j in range(y_filter.shape[2]):
                y_filter[:, _i, _j] = signal.cwt(data[:, _i, _j].value, signal.morlet2,
                                                 widths=[s], w=w)
    # make unitary complex vector for phase estimation
    normalized_vector = y_filter / np.abs(y_filter)
    # if data comes in trials, then we average
    average_vector = np.mean(normalized_vector, axis=2)
    axs[0].plot(time, data, label='signal')
    axs[0].plot(time, np.real(reference_signal), label='ref')
    # compute phase difference
    # instantaneous_phase_difference = np.unwrap(np.angle(average_vector) * u.rad - np.angle(reference_signal), axis=0)
    instantaneous_phase_difference = np.unwrap(np.angle(average_vector) * u.rad - np.angle(reference_signal), axis=0)
    axs[1].plot(time, instantaneous_phase_difference * 180 / np.pi, label='{:}'.format(phase * 180 / np.pi))
    axs[1].legend()
plt.show()
plt.show()
