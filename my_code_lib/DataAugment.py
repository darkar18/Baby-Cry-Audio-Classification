import soundfile as sf
import os
import librosa
import numpy as np

DIR = os.pardir
DATA = os.path.join("","./gveres donateacry-corpus master donateacry_corpus_cleaned_and_updated_data/")
list_of_classes = [i for i in os.listdir(DATA) if '_uniform' in i]


class AudioAugmentation():
    def read_audio_file(self, file_path):
        data, sample_rate = sf.read(file_path)
        print(type(data))
        return data, sample_rate
    
    def write_audio_file(self, file, data, sample_rate):
        sf.write(file, data, sample_rate)
        
    def add_noise(self, data,noise_factor):
        noise = np.random.randn(len(data))
        augmented_data = data + noise_factor * noise
        # Cast back to same data type
        augmented_data = augmented_data.astype(type(data[0]))
        return augmented_data
    
    def shift(self, data):
        y_shift = data.copy()
        timeshift_fac = 0.5 * 2 * (np.random.uniform() - 0.5)  # up to 20% of length
        print("timeshift_fac = ", timeshift_fac)
        start = int(y_shift.shape[0] * timeshift_fac)
        print(start)
        if (start > 0):
            y = np.pad(y_shift,(start,0),mode='constant')[0:y_shift.shape[0]]
        else:
            y = np.pad(y_shift,(0,-start),mode='constant')[0:y_shift.shape[0]]
        return y.T
    
    def stretch(self, data, rate=1.1):
        input_length = len(data)
        streching = data.copy()
        streching = librosa.effects.time_stretch(streching.astype('float'), rate=1.1)
        if len(streching) > input_length:
            streching = streching[:input_length]
        else:
            streching = np.pad(streching, (0, max(0, input_length - len(streching))), "constant")
        #data = librosa.effects.time_stretch(data, rate)
        return streching
aa = AudioAugmentation()
def do_augmentation():
    for dir in list_of_classes:
        if dir != 'hungry':
            path = os.path.join(DATA,dir)
            os.chdir(path)
            for file in os.listdir(path):
                if not file.startswith('.'):
                    print(file)
                    Adata, sr = aa.read_audio_file(os.path.join(path,file))
                    # aa.plot_time_series(data)
                    # Adding noise to sound
                    data_noise = aa.add_noise(Adata,0.005)
                    data_roll = aa.shift(Adata)
                    # aa.plot_time_series(data_roll)
                    # Stretching the sound
                    data_stretch = aa.stretch(Adata, rate = 0.8)
                    # aa.plot_time_series(data_stretch)
                    # Write generated sounds
                    aa.write_audio_file('generated2_' + file, data_roll, sr)
                    aa.write_audio_file('generated1_' + file, data_noise, sr)
                    aa.write_audio_file('generated3_' + file, data_stretch, sr)
