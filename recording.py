import time
import pyaudio
import wave

filename = 'track.wav'

# * Set chunk size of 1024 samples per data frame
chunk = 1024

# * Open the track file
wf = wave.open(filename, 'rb')

# * Create an interface to PortAudio
p = pyaudio.PyAudio()

# * Choose record devices
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ",
              p.get_device_info_by_host_api_device_index(0, i).get('name'))

device_id = int(input('Device ID: '))

# * Open a .Stream object to write the WAV file to
track = p.open(format=p.get_format_from_width(wf.getsampwidth()),
               channels=wf.getnchannels(),
               rate=wf.getframerate(),
               output=True,)

vocal = p.open(format=p.get_format_from_width(wf.getsampwidth()),
               channels=wf.getnchannels(),
               rate=wf.getframerate(),
               input=True,
               output=True,
               input_device_index=device_id,
               frames_per_buffer=chunk)

frames = []
# * Read first chunks
data = wf.readframes(chunk)
# * record time (s)
rtime = 5

# * Start playing track and recording vocal
start = time.time()
while data != '' and time.time() - start < rtime:
    track.write(data)
    data = wf.readframes(chunk)
    frames.append(vocal.read(chunk))
    vocal.write(data, chunk)

data = wf.readframes(chunk)
frames.append(vocal.read(chunk))

# * Create bytes array
array = bytes()
for b in frames[1:]:
    array = array + b

# * Save vocal.wav:
output = wave.open('vocal.wav', 'wb')
output.setnchannels(wf.getnchannels())
output.setsampwidth(2)
output.setframerate(wf.getframerate())
output.writeframes(b''.join(frames[1:]))

# * Close stream:
vocal.write(array)
vocal.stop_stream()
vocal.close()
track.close()
p.terminate()
