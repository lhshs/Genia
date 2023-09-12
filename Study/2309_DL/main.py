from load import DataLoad
from model import LeNet

# data load
x_train, x_val, y_train, y_val = DataLoad(28)._data()

# model
print("🔻 Modeling Start🔻")
model = LeNet('adam', 'sparse_categorical_crossentropy', 'accuracy', 3)

# train
print("🌈 Model Training🌈")
model._fit(x_train, y_train)

# inference


# evaluate
print("🌈 Model Evaluate🌈")
model._fit(x_val, y_val)

# upload 


'''
if __name__ == "__main__":

    path = "D:/dogs_vs_cats/dogs_vs_cats/train/"

    print("data load")
    df = loading(path)    # train data
    # df = loading(path,target_nan=True) ## inference data
    print(df.head())

    print("preprocess")
    
    print("pass preprocess")


'''