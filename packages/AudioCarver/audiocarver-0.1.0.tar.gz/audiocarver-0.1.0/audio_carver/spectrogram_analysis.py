import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from audio_conversion import *

def get_spectogram(audio, sampling_rate):
    D_db = librosa.amplitude_to_db(np.abs(audio), ref=np.max)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(D_db, sr=sampling_rate, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Original Spectrogram')
    plt.show()

def compare_spectrograms(filename, filename_sc):
    audio, sr = load_wavfile(filename)
    audio_sc, sr_sc = load_wavfile(filename_sc)
    D_db = librosa.amplitude_to_db(np.abs(audio), ref=np.max)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(D_db, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Original Spectrogram')
    xmin, xmax, ymin, ymax = plt.axis()
    plt.show()
    D_db_sc = librosa.amplitude_to_db(np.abs(audio_sc), ref=np.max)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(D_db_sc, sr=sr_sc, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Carved Spectrogram')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.show()

def get_MFCC(audio, sampling_rate):
    orgMFCC = librosa.feature.mfcc(y=audio, sr=sampling_rate)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(orgMFCC, sr=sampling_rate, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Original MFCC')

def compare_MFCC(filename, filename_sc):
    audio, sr = load_wavfile(filename)
    audio_sc, sr_sc = load_wavfile(filename_sc)
    orgMFCC = librosa.feature.mfcc(y=audio, sr=sr)
    orgcarvedMFCC = librosa.feature.mfcc(y=audio_sc, sr=sr_sc)

    plt.figure(figsize=(10, 6))
    librosa.display.specshow(orgMFCC, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Original MFCC')
    xmin, xmax, ymin, ymax = plt.axis()
    plt.ylim([0, ymax])
    plt.show()

    plt.figure(figsize=(10, 6))
    librosa.display.specshow(orgcarvedMFCC, sr=sr_sc, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Carved MFCC')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.ylim([0, ymax])
    plt.show()