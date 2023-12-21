from tensorflow import keras
from keras.layers import Dense, Flatten
from backend.lib.lib import Request


class NeuralNetwork(Request):
    def create_model(self):
        self.prepare_dataset()
        model = keras.models.Sequential()
        model.add(Flatten(input_shape=(self.dataset.input_data_scale, )))
        count: int = self.structure.hidden_layer_count
        for i in range(count):
            model.add(Dense(units=self.structure.neuron_count[i], activation=self.structure.act_fn[i]))
        model.add(Dense(units=self.structure.neuron_count[-1], activation=self.structure.act_fn[-1]))
        model.compile(optimizer=self.model.opt_fn, loss=self.model.loss_fn, metrics=["accuracy"])
        return model


    def prepare_dataset(self):
        self.dataset.prepare_data()
        self.dataset.learning_data_input = self.dataset.learning_data_input / self.dataset.depth_input_data
        self.dataset.learning_data_output = keras.utils.to_categorical(self.dataset.learning_data_output, self.structure
                                                                       .neuron_count[-1])

    def train_model(self, model):
        model.fit(x=self.dataset.learning_data_input, y=self.dataset.learning_data_output,
                  batch_size=self.train.batch_size, epochs=self.train.epochs,
                  validation_split=self.train.validation_split)
        return model

    def save_model(self, model, path: str):
        model.save(filepath=path)