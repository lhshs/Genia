import pandas as pd
import pickle

from model import MF

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-e', '--epochs', type=int, default=16)
parser.add_argument('-b', '--batch_size', type=int, default=128)
parser.add_argument('-nlt', 
                    '--n_latent_factors', 
                    type=int, 
                    default=64
)
args = parser.parse_args()

epochs = args.epochs
batch_size = args.batch_size
n_latent_factors = args.n_latent_factors


if __name__ == '__main__':
    # preprocessed_df = pd.read_csv('./preprocessed_df.csv')
    train_data = pd.read_csv('train_data.df')
    valid_data = pd.read_csv('valid_data.df')

    with open('n_dict.pickle','rb') as f:
        n_dict = pickle.load(f)

    # print(preprocessed_df)
    # print('n_dict : ', n_dict)
    
    # n_latent_factors = 64
    model = MF(
        n_users = n_dict['n_users'],
        n_movies = n_dict['n_movies'],
        n_latent_factors = n_latent_factors
    )
    history = model.train(
            train_data = train_data,
            valid_data = valid_data,
            epochs=epochs,
            batch_size=batch_size,
            verbose=2
    )
    print(model.model.summary())