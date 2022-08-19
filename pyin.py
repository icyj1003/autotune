"""
Author: Khoi Bui
Created on: June 12, 2022
"""
import librosa
import vamp
import numpy as np


def pyin(y, sr):

    notes = vamp.collect(y, sr,
                         plugin_key="pyin:pyin",
                         output='notes',
                         parameters={'threshdistr': 0.15,
                                     'onsetsensitivity': 0,
                                     'lowampsuppression': 0.1,
                                     'prunethresh': 0.05
                                     }
                         )
    return [(float(item['timestamp']), float(item['duration']), float(item['values'][0])) for item in notes['list']]
