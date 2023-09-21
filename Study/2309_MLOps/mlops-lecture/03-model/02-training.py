import pandas as pd
import pickle

from model import MF, DeepMF

from argparse import ArgumentParser
import json
import os


parser = ArgumentParser()
parser.add_argument("-e", "--epochs", type=int, default=16)
parser.add_argument("-b", "--batch_size", type=int, default=128)
parser.add_argument(
    "-nlt",
    "--n_latent_factors",
    type=int,
    default=64
)
parser.add_argument("-m", "--model_type", type=str, default="mf")
parser.add_argument("-drp", "--dropout", type=float, default=0.25)

args = parser.parse_args()

if __name__ == "__main__":
    
    epochs = int(os.getenv("EPOCHS")) if os.getenv("EPOCHS") else args.epochs
    batch_size = int(os.getenv("BATCH_SIZE")) if os.getenv("BATCH_SIZE") else args.batch_size
    model_type = os.getenv("MODEL_TYPE") if os.getenv("MODEL_TYPE") else args.model_type
    n_latent_factors = int(os.getenv("N_LATENT_FACTORS")) if os.getenv("N_LATENT_FACTORS") else args.n_latent_factors
    dropout = float(os.getenv("DROPOUT")) if os.getenv("DROPOUT") else args.dropout

    train_data = pd.read_csv("train_data.df")
    valid_data = pd.read_csv("valid_data.df")

    with open("n_dict.pickle", "rb") as f:
        n_dict = pickle.load(f)

    if model_type == "mf":
        model = MF(
            n_users=n_dict["n_users"],
            n_movies=n_dict["n_movies"],
            n_latent_factors=n_latent_factors,
        )

    elif model_type == "deepmf":
        model = DeepMF(
            n_users=n_dict["n_users"],
            n_movies=n_dict["n_movies"],
            n_latent_factors=n_latent_factors,
            dropout=dropout,
        )

    history = model.train(
        train_data=train_data,
        valid_data=valid_data,
        epochs=epochs,
        batch_size=batch_size,
        verbose=2,
    )

    result = model.evaluate(valid_data)
    result = round(result, 4)
    print(f"VAL_LOSS={result}")

    metrics = {
        "metrics": [
            {
                "name": "VAL_LOSS",
                "numberValue": result,
                "format": "RAW"
            }
        ]
    }

    with open("mlpipeline-metrics.json", "w") as f:
        json.dump(metrics, f)
