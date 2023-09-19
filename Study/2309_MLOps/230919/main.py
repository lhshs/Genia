import tensorflow as tf
from easydict import EasyDict

if __name__ == '__main__':
        # print('Hello Docker tf!', tf.__version__)
        # print('Goodbye Docker tf!', tf.__version__)

        edict = EasyDict()
        edict.hello = "world🌳"
        print("edict: ", edict)