import numpy as np 
# import tensorflow as tf 
# from tensorflow import keras
import librosa 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import minmax_scale
import glob 

def load_model(path): 
    m = None 
    if path is not None: 
        return m 
    return m 

class AInimalsModel:

    def __init__(self, path = None, nb_classes = 5): 
        self.m = load_model(path)
        self.nb_classes = nb_classes

    def __call__(self, x_im): 
        preds = self.m(x_im)

    def get_spectrogam(self, audio_path, start_at, window, 
                        n_mels = 224): 
        y, sr = librosa.load(audio_path)
        y_trimmed = y[int(start_at * sr): int(start_at * sr) + int(window * sr)]
        mel = librosa.feature.melspectrogram(y_trimmed, n_mels = n_mels)
        db = librosa.power_to_db(mel)
        db = minmax_scale(db)
        db_array = (np.asarray(db)*255).astype(np.uint8)
        return db_array

    def get_preds(self, audio_path, start_at, window): 
        spectro = self.get_spectrogam(audio_path, start_at, window)
        if self.m is not None: 
            preds = self.m(x)
        else: 
            out = np.random.uniform(0.,1.,size = (self.nb_classes,))
            preds = np.exp(out)/np.exp(out).sum()
        
        print('Best guess: {} - Preds: {}'.format(np.argmax(preds), preds))
        return preds, np.argmax(preds), spectro


if __name__ == "__main__": 
    m = AInimalsModel()
    #m.get_spectrogam(glob.glob('./*.wav')[0],0, 3)
    m.get_preds(glob.glob('./*.wav')[0],0, 3)