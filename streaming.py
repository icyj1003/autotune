import soundfile as sf
import scipy.io.wavfile
import numpy as np
import wave
import io
from scipy.io.wavfile import write
import pyaudio
import json

FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1
RATE = 44100


audio = pyaudio.PyAudio()


stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
all = []
try:
    frames = []
    print("* recording")
    print("Press CTRL+C to stop")
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if len(frames) > 0:
            temp = frames.pop(0)
            all.append(temp)
            # print(temp)
            #! Echo stream.write(temp, CHUNK)
    print("* done echoing")

except KeyboardInterrupt:
    a = bytes()
    for i in all:
        a = a + i
# this is my table of chunks of audio data
    output = wave.open('output.wav', 'wb')
    output.setnchannels(CHANNELS)
    output.setsampwidth(2)
    output.setframerate(RATE)
    output.writeframes(b''.join(all))

    # * Play and close stream
    stream.write(a)
    stream.stop_stream()
    stream.close()
    audio.terminate()
