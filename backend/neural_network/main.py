from tensorflow import keras
from keras.layers import Dense, Flatten
from keras.datasets import mnist
from lib.lib import Request, Model, Structure, Dataset, Train


dataset = mnist.load_data()
(x_train, y_train), (x_test, y_test) = dataset


############## backend test
model = Model(opt_fn="adam", loss_fn="categorical_crossentropy")
structure = Structure(neuron_count=[128, 200, 10], hidden_layer_count=2,
                      act_fn=['relu', 'relu', 'softmax'])
dataset = Dataset(learning_data_input=x_train, input_type="mnist", depth_input_data=255,
                  input_data_scale=28, learning_data_output=y_train)
train = Train(epochs=10, validation_split=0.1, batch_size=32)

request = Request(dataset=dataset, model=model, structure=structure, train=train)

####################

print(x_train[0], y_train[0])
class NeuralNetwork(Request):
    def create_model(self):
        model = keras.models.Sequential()
        # model.add(Dense(units=784, input_shape=(28, 28, 1)))
        model.add(Flatten(input_shape=(28, 28, )))
        count: int = self.structure.hidden_layer_count
        for i in range(count):
            model.add(Dense(units=self.structure.neuron_count[i], activation=self.structure.act_fn[i]))
        model.add(Dense(units=self.structure.neuron_count[-1], activation=self.structure.act_fn[-1]))
        model.compile(optimizer=self.model.opt_fn, loss=self.model.loss_fn, metrics=["accuracy"])
        return model


    def prepare_dataset(self):
        self.dataset.learning_data_input = self.dataset.learning_data_input / self.dataset.depth_input_data
        self.dataset.learning_data_output = keras.utils.to_categorical(self.dataset.learning_data_output, 10)

    def train_model(self, model):
        model.fit(x=self.dataset.learning_data_input, y=self.dataset.learning_data_output,
                  batch_size=self.train.batch_size, epochs=self.train.epochs,
                  validation_split=self.train.validation_split)
        return model


neuralnetwork = NeuralNetwork(model=request.model, structure=request.structure,
                              train=request.train, dataset=request.dataset)

model = neuralnetwork.create_model()
neuralnetwork.prepare_dataset()
model = neuralnetwork.train_model(model)


