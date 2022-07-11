import numpy as np
import librosa
from numpy import dtype
import streamlit as st
from globals import sr
from kafka import KafkaProducer, KafkaConsumer
import json
from json import loads
import scipy.io.wavfile


producer1 = KafkaProducer(bootstrap_servers=['localhost:9092'],
                          api_version=(0, 11, 5),
                          max_request_size=100000000,
                          value_serializer=lambda v: json.dumps(
    v).encode('utf-8')
)

consumer2 = KafkaConsumer(
    'output',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    api_version=(0, 11, 5),
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

raw_file = st.file_uploader('Tải lên file vocal', accept_multiple_files=False)

if raw_file:
    st.audio(raw_file, format=raw_file.type)

track_file = st.file_uploader('Tải lên track', accept_multiple_files=False)

if track_file:
    st.audio(track_file, format=track_file.type)

if raw_file and track_file:
    process = st.button('Process')

    if process:
        raw, _ = librosa.load(raw_file, sr=sr)
        track, _ = librosa.load(track_file, sr=sr)
        producer1.send(
            'autotune', {'raw': raw.tolist(),
                         'track': track.tolist(),
                         'sr': sr})
        producer1.flush()
    error = False
    with st.spinner('Chờ chút'):
        for item in consumer2:
            if item.value.get('status') == 'OK':
                scipy.io.wavfile.write(
                    './cache/output.wav', sr, np.array(item.value.get('output'), dtype='float32'))
                break
            else:
                error = True
                break
    if not error:
        st.success('Hoàn tất!')
        audio_file = open('./cache/output.wav', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    else:
        st.error('Lỗi gì rồi')
