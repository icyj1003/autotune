"""
Author: Khoi Bui
Created on: July 10, 2022
"""
from autotune import wave_shift, spliting
import numpy as np
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import json


consumer2 = KafkaConsumer(
    'autotune',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    api_version=(0, 11, 5),
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
producer2 = KafkaProducer(bootstrap_servers=['localhost:9092'],
                          api_version=(0, 11, 5),
                          max_request_size=100000000,
                          value_serializer=lambda v: json.dumps(
    v).encode('utf-8')
)
for message in consumer2:
    print('Receive')
    content = message.value
    raw = np.array(content['raw'], dtype='float32')
    track = np.array(content['track'], dtype='float32')
    track_vocal, _ = spliting(track, sr=content['sr'])
    output = wave_shift(
        raw=raw, vocal=track_vocal, sr=content['sr'])[0]
    print('Done')
    producer2.send('output', {'output': output.tolist(), 'status': 'OK'})
    print('Sent')
    producer2.flush()
