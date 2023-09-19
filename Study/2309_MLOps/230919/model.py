from tensorflow.keras.layers import Input, Embedding, Flatten, dot
from tensorflow.keras.models import Model
import tensorflow as tf

# Matrix Factorization
class MF(object):
    def __init__(self, n_users, n_movies, n_latent_factors):
        self.n_users = n_users
        self.n_movies = n_movies
        self.n_latent_factors = n_latent_factors
        self.model = self._build()
    
    def _build(self):
        # define MF Model
        
        # user
        user_input = Input(
            shape=(1,), name='user_input', dtype='int64'
            )
        user_embedding = Embedding(
            self.n_users, self.n_latent_factors, name='user_embedding'
            )(user_input)
        user_vec = Flatten(name='FlattenUsers')(user_embedding)
        
        # movie
        movie_input = Input(
            shape=(1,), name='movie_input', dtype='int64'
            )
        movie_embedding = Embedding(
            self.n_movies, self.n_latent_factors, name='movie_embedding'
            )(movie_input)
        movie_vec = Flatten(name='FlattenMovies')(movie_embedding)
        
        # dot
        sim_dot_product = dot(
            [user_vec, movie_vec],
            name = "Similarity-Dot-Product",
            axes=1
        )

        model = Model(
            inputs=[user_input, movie_input],
            outputs=sim_dot_product
        )
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, train_data, valid_data, **kwargs):
        X_train, y_train = [
            train_data['user_id'], train_data['movie_id']
        ], train_data['rating']

        X_valid, y_valid = [
            valid_data['user_id'], valid_data['movie_id']
        ], valid_data['rating']
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_valid, y_valid),
            **kwargs
        )
        return history

