# https://www.youtube.com/watch?v=MhOdbtPhbLU
# see if I can get one of these for conv layers
import numpy as np
import glob
import librosa
import os
def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)
    # spectogram with shape 60 and 100
    melspec = librosa.feature.melspectrogram(X, n_mels = 60, sr=sample_rate)
    logspec = librosa.logamplitude(melspec)
    y_shape = logspec.shape[1]
    if y_shape < 101:
        diff= 101-y_shape
        mod = diff%2
        if mod==0:
            pad = int(diff/2)
            logspec = np.pad(logspec, [(0, 0), (pad, pad)], mode='constant')
        else:
            pad_left = int(np.floor(diff/2))
            pad_right = pad_left + 1
            logspec = np.pad(logspec, [(0, 0), (pad_left, pad_right)], mode='constant')
        
    return logspec[:,:100].reshape(1,60,100,1)

def parse_audio_files(parent_dir,sub_dirs,file_ext="*.wav"):
    features, labels = None, np.empty(0)
    files = []
    for label, sub_dir in enumerate(sub_dirs):
        for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
            files.append(fn)
            try:
                logspec = extract_feature(fn)
            except Exception as e:
                print( "Error encountered while parsing file: ", fn, str(e))
                continue
            if features is None:
                features = logspec
            else:
                features = np.concatenate((features,logspec), axis=0)
            labels = np.append(labels, fn.split('/')[2].split('-')[1])
    return np.array(features), np.array(labels, dtype = np.int),files

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = 10#len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode