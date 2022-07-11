from globals import chunk, record_latency
import wave
import time
import pyaudio


def recording(track_file, input_device_id=1, output_device_id=0, save=True, save_path='vocal.wav'):
    p = pyaudio.PyAudio()

    # Ready
    for _ in [3, 2, 1]:
        print(f'Start recording in {_}')
        time.sleep(1)

    # Streams
    vocal_stream = p.open(format=pyaudio.get_format_from_width(track_file.getsampwidth()),
                          channels=track_file.getnchannels(),
                          rate=track_file.getframerate(),
                          input=True,
                          input_device_index=input_device_id,
                          frames_per_buffer=chunk)

    track_stream = p.open(
        format=pyaudio.get_format_from_width(track_file.getsampwidth()),
        channels=track_file.getnchannels(),
        rate=track_file.getframerate(),
        output=True
    )

    # recording
    print('Recording...')
    frames = []
    track_data = track_file.readframes(chunk)
    while track_data:
        track_stream.write(track_data)
        frames.append(vocal_stream.read(chunk))
        track_data = track_file.readframes(chunk)

    track_stream.close()
    vocal_stream.close()
    p.terminate()

    # save output
    if save:
        print('Saving...')
        output = wave.open(save_path, 'wb')
        output.setnchannels(track_file.getnchannels())
        output.setsampwidth(track_file.getsampwidth())
        output.setframerate(track_file.getframerate())
        print(len(frames))
        output.writeframes(
            b''.join(frames[record_latency:] + frames[:record_latency]))
        output.close()

    print('Done')


recording(
    track_file=wave.open('./audio_db/splited/4AgFXIVT7hVhBZ5DEOaLu3/vocals.wav', 'rb'), save=True)
