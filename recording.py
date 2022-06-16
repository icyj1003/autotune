import numpy as np
from ffpyplayer.player import MediaPlayer
import cv2
from audioop import mul
import time
from bs4 import Tag
import pyaudio
import wave
import multiprocessing
import playsound


def record(duration, device_input):
    chunk = 1024
    channels = 1
    format = pyaudio.paInt16
    rate = 44100
    p = pyaudio.PyAudio()
    vocal = p.open(format=format,
                   channels=channels,
                   rate=rate,
                   input=True,
                   output=True,
                   input_device_index=device_input,
                   frames_per_buffer=chunk)
    frames = []
    for i in range(0, int(rate / chunk * duration)):
        data = vocal.read(chunk)
        frames.append(data)

    print('End record')
    output = wave.open('vocal.wav', 'wb')
    output.setnchannels(channels)
    output.setsampwidth(2)
    output.setframerate(rate)
    output.writeframes(b''.join(frames[10:]))


def play_track():
    chunk = 1024
    channels = 1
    format = pyaudio.paInt16
    rate = 48000
    # * Create an interface to PortAudio
    p = pyaudio.PyAudio()
    wf = wave.open('track.wav', 'rb')
    track = p.open(format=format,
                   channels=wf.getnchannels(),
                   rate=wf.getframerate(),
                   output=True,)
    while True:
        data = wf.readframes(chunk)
        if data == '':
            break
        track.write(data)

    print('End track')


def PlayVideo():
    video = cv2.VideoCapture('karaoke.mp4')
    player = MediaPlayer('karaoke.mp4')
    while True:
        grabbed, frame = video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            # audio
            img, t = audio_frame
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    # * Create an interface to PortAudio
    p = pyaudio.PyAudio()
    # * Choose record devices
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ",
                  p.get_device_info_by_host_api_device_index(0, i).get('name'))

    device_input = int(input('Device ID: '))

    video = cv2.VideoCapture('karaoke.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    seconds = frame_count / fps
    print(seconds)
    track = multiprocessing.Process(target=play_track)
    vocal = multiprocessing.Process(
        target=record, args=(20, device_input))
    karaoke = multiprocessing.Process(
        target=PlayVideo)

    karaoke.start()
    vocal.start()
    p.terminate()
