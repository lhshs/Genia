from sklearn.model_selection import train_test_split
from utils.connector import MinioClient

import pandas as pd
import pickle

import settings


if __name__ =="__main__":

    # df = pd.read_csv("./train_data.csv")
    df = MinioClient.get_df("train_data.csv")
    print("df loaded successfully!", df.head())

    users = df["user_id"].unique()
    movies = df["movie_id"].unique()

    user2idx = {user: i for i, user in enumerate(users)}
    movie2idx = {movie: i for i, movie in enumerate(movies)}

    df["user_id"] = df["user_id"].apply(lambda x: user2idx[x])
    df["movie_id"] = df["movie_id"].apply(lambda x: movie2idx[x])

    n_dict = dict(
        n_users=len(users),
        n_movies=len(movies),
    )
    train_data, valid_data = train_test_split(df)

    pip_name = settings.PIP_NAME
    print("pip_name: ", pip_name)

    MinioClient.put_df(f"{pip_name}/train_data.df", train_data)
    MinioClient.put_df(f"{pip_name}/valid_data.df", valid_data)
    MinioClient.put_pickle(f"{pip_name}/n_dict.pickle", n_dict)

