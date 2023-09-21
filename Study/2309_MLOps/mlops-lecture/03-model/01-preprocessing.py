from sklearn.model_selection import train_test_split

import pandas as pd
import pickle

if __name__ =="__main__":
    
    df = pd.read_csv("./train_data.csv")

    users = df["user_id"].unique()
    movies = df["movie_id"].unique()

    # user2idx = {}
    # for i, user in enumerate(users):
    #     user2idx[user] = i
    user2idx = {user: i for i, user in enumerate(users)}
    movie2idx = {movie: i for i, movie in enumerate(movies)}

    df["user_id"] = df["user_id"].apply(lambda x: user2idx[x])
    df["movie_id"] = df["movie_id"].apply(lambda x: movie2idx[x])

    n_dict = dict(
        n_users=len(users),
        n_movies=len(movies),
    )
    train_data, valid_data = train_test_split(df)
    train_data.to_csv("train_data.df", index=False)
    valid_data.to_csv("valid_data.df", index=False)
    
    with open("n_dict.pickle", "wb") as f:
        pickle.dump(n_dict, f)

        
    

