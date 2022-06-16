import librosa
import vamp
import numpy as np

y, sr = librosa.load('./output/nangtho/vocals.wav')
ans = vamp.collect(y[77*sr:80*sr], sr, "pyin:localcandidatepyin")
print(ans)

# for pl in vamp.list_plugins():
#     print(pl)
