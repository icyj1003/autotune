"""
Author: Khoi Bui
Created on: July 10, 2022
"""
from pydub import AudioSegment
import os
import random
import librosa
import numpy as np
import warnings
from globals import sr
from psola import shift_pitch
from pyin import pyin
import scipy.io.wavfile

warnings.filterwarnings('ignore')


def wave_shift(vocal, raw, sr):

    notes = pyin(vocal, sr)
    output = raw.copy()

    for note in notes:
        try:
            begin = note[0]
            end = begin + note[1]
            f_new = note[2]
            f0, voiced_flag, voiced_probs = librosa.pyin(output[int(begin*sr):int(end*sr)],
                                                         fmin=40,
                                                         fmax=1600, sr=sr)
            f_ori = f0[~np.isnan(f0)].mean()

            f_ratio = f_new/f_ori
            f_dif = abs(f_new - f_ori)
            if f_ratio > 0 and f_dif > 5:
                output[int(begin*sr):int(end*sr)
                       ] = shift_pitch(output[int(begin*sr):int(end*sr)], sr, f_ratio)
        except:
            pass

    return output, sr


def random_shift(vocal_file, output_file, sr, n_notes=3):
    vocal, _ = librosa.load(vocal_file, sr=sr)
    notes = pyin(vocal, sr)
    output = vocal.copy()
    dif = [-1, -2, 1, 2, 3, 0]
    for note in random.sample(notes, 3):
        try:
            begin = note[0]
            end = begin + note[1]
            output[int(begin*sr):int(end*sr)] = \
                shift_pitch(vocal[int(begin*sr):int(end*sr)],
                            sr, 2 ** (np.random.choice(dif)/12))
        except:
            pass
    scipy.io.wavfile.write(output_file, sr, output)


def spliting(audio, sr=sr, format='wav'):
    scipy.io.wavfile.write('./cache/temp.wav', sr, audio)
    os.system(
        f"""spleeter separate -p spleeter:2stems ./cache/temp.wav -o ./cache/ -c {format}""")
    out, _ = librosa.load('./cache/temp/vocals.wav', sr=sr)
    return out, _


def file_shift(vocal_file, raw_file, output_file, sr):

    vocal, _ = librosa.load(vocal_file, sr=sr)
    raw, _ = librosa.load(raw_file, sr=sr)

    notes = pyin(vocal, sr)
    output = raw.copy()

    for note in notes:
        try:
            begin = note[0]
            end = begin + note[1]
            f_new = note[2]
            f0, voiced_flag, voiced_probs = librosa.pyin(output[int(begin*sr):int(end*sr)],
                                                         fmin=40,
                                                         fmax=1600, sr=sr)
            f_ori = f0[~np.isnan(f0)].mean()

            f_ratio = f_new/f_ori
            f_dif = abs(f_new - f_ori)
            print(note, f_dif)

            if f_ratio > 0 and f_dif > 5:
                output[int(begin*sr):int(end*sr)
                       ] = shift_pitch(output[int(begin*sr):int(end*sr)], sr, f_ratio)
        except:
            pass

    scipy.io.wavfile.write(output_file, sr, output)


def convert(y, sr):
    y = np.array(y * (1 << 15), dtype='int16')
    audio_segment = AudioSegment(
        y.tobytes(),
        frame_rate=sr,
        sample_width=y.dtype.itemsize,
        channels=1
    )
    return audio_segment


def merge(sound1, sound2, sr):
    a, _ = librosa.load("./accompaniment.wav", sr=sr)
    b, _ = librosa.load("./vocals.wav", sr=sr)
    a1 = convert(sound1, sr)
    b1 = convert(sound2, sr)
    combined = a1.overlay(b1)
    combined.export(".cache/merged.wav", format='wav')
