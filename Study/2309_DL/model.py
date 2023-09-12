from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Conv2D, AveragePooling2D, Flatten, Dense, ZeroPadding2D


class LeNet:
    def __init__(self, optimizer, loss, metrics, epochs):
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.epochs = epochs
        self.model = None


    def _fit(self, x_train, y_train):
        model = Sequential([InputLayer(input_shape = (28, 28, 1)),   
                            ZeroPadding2D((2,2)),
                            Conv2D(6, 5, activation='tanh'),
                            AveragePooling2D(strides=2),
                            Conv2D(16, 5, activation='tanh'),
                            AveragePooling2D(strides=2),
                            Conv2D(120, 5, activation='tanh'),
                            Flatten(),
                            Dense(84, activation='tanh'),
                            Dense(10, activation='softmax')
                        ])
        model.compile(optimizer = self.optimizer, 
                      loss = self.loss, 
                      metrics = self.metrics)
        self.model = model
        return model.fit(x_train, y_train, epochs = self.epochs)  
        
    def _evaluate(self, x_val, y_val):
        model = self.model
        return model.evaluate(x_val, y_val)
        


    # def _evaluate(train_input, train_target):
    #     predict = self.predict(train_input)
    #     print("R2 Score: ", round(r2_score(predict, train_target),4))


    # def _save(self, path):
    #     self.model.save(path)