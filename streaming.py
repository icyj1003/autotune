import soundfile as sf
import scipy.io.wavfile
import numpy as np
import wave
import io
from scipy.io.wavfile import write
import pyaudio
import json

"""
numberofbuffers = duration * sample_rate / buffersize
"""

FORMAT = pyaudio.paInt16
CHANNELS = 1
BUFFERSIZE = 1024
RATE = 44100


audio = pyaudio.PyAudio()

# * Choose record devices
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ",
              audio.get_device_info_by_host_api_device_index(0, i).get('name'))

device_id = int(input('Device ID: '))
vocal = audio.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   output=True,
                   input_device_index=device_id,
                   frames_per_buffer=BUFFERSIZE)
all = []
count = 0
try:
    frames = []
    print("* recording")
    print("Press CTRL+C to stop")
    while True:
        data = vocal.read(BUFFERSIZE)
        frames.append(data)
        if len(frames) != 0:
            temp = frames.pop(0)
            all.append(temp)
            # * Real-time playback:
            vocal.write(temp, BUFFERSIZE)
    print("* done echoing")

except KeyboardInterrupt:
    a = bytes()
    for i in all:
        a = a + i
    # * Save vocal.wav:
    output = wave.open('vocal.wav', 'wb')
    output.setnchannels(CHANNELS)
    output.setsampwidth(2)
    output.setframerate(RATE)
    output.writeframes(b''.join(all))

    # * Play and close stream:
    vocal.stop_stream()
    vocal.close()
    audio.terminate()
