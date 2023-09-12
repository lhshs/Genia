import tensorflow as tf
import tensorflow.keras as keras

from sklearn.model_selection import train_test_split

class DataLoad:
    
    def __init__(self, reshape_dim :int, test_size :float=0.2):
        self.reshape_dim = reshape_dim
        self.test_size = test_size

    # data load
    def _load_data(self):
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        print(x_train.shape)
        print(y_train.shape)
        print(x_test.shape)
        print(y_test.shape)
        return x_train, y_train # , x_test, y_test
    
    # train_test_split
    def _train_test_split(self, x, y):
        return train_test_split(x, y, test_size=self.test_size)
    
    # reshape
    def _reshape(self, data):
        return data.reshape(-1, self.reshape_dim, self.reshape_dim, 1)
    
    # normalize
    def _normalize(self, data):
        return data / 255.0
    
    # modeling data
    def _data(self):
        x_train, y_train = self._load_data()
        x_train, x_val, y_train, y_val = self._train_test_split(x_train, y_train)

        x_train = self._normalize(x_train)
        x_val = self._normalize(x_val)
        y_train = self._normalize(y_train)
        y_val = self._normalize(y_val)

        return x_train, x_val, y_train, y_val


        