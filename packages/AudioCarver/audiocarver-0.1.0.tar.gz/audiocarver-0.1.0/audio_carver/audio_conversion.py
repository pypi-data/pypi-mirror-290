import librosa
import numpy as np
import soundfile as sf

audio = None
sampling_rate = None

def load_wavfile(filename):
    global audio, sampling_rate
    audio, sampling_rate = librosa.load(filename, sr=None, mono=True)
    return audio, sampling_rate

def get_stft(audio):
    matrix = librosa.stft(audio)
    return matrix

def get_istft(complex_spectrogram):
    reconstructed_signal = librosa.istft(complex_spectrogram)
    return reconstructed_signal

def extract_mag_pha(matrix):
    magnitude = np.abs(matrix)
    phase = np.angle(matrix)
    return magnitude, phase

def extract_pow_pha(matrix):
    power = np.abs(matrix)**2
    phase = np.angle(matrix)
    return power, phase

def sig_to_wav(output_filename, magnitude, phase):
    complex_spectrogram = magnitude * np.exp(1j * phase)
    reconstructed_signal = get_istft(complex_spectrogram)
    sf.write(output_filename, reconstructed_signal, sampling_rate)
