import numpy as np
from scipy import signal


def generate_waveform(frequency, sample_rate, waveform_type):
    if waveform_type == 1:
        return generate_sine_wave(frequency, sample_rate)
    elif waveform_type == 2:
        return generate_square_wave(frequency, sample_rate)
    elif waveform_type == 3:
        return generate_sawtooth_wave(frequency, sample_rate)
    elif waveform_type == 4:
        return triangle_wave(frequency, sample_rate)
    else:
        return None


def generate_sine_wave(frequency, sample_rate):
    t = np.linspace(0, 1, sample_rate, False)
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    return audio.astype(np.float32)


def generate_square_wave(frequency, sample_rate):
    t = np.linspace(0, 1, sample_rate, False)
    audio = 0.5 * signal.square(2 * np.pi * frequency * t)
    return audio.astype(np.float32)


def generate_sawtooth_wave(frequency, sample_rate):
    t = np.linspace(0, 1, sample_rate, False)
    audio = 0.5 * signal.sawtooth(2 * np.pi * frequency * t)
    return audio.astype(np.float32)


def triangle_wave(frequency, sample_rate):
    t = np.linspace(0, 1, int(sample_rate / frequency), False)
    triangle_wave_data = 2 * np.abs(2 * (t * frequency - np.floor(0.5 + t * frequency))) - 1
    return (triangle_wave_data * (2**15 - 1)).astype(np.int16)

