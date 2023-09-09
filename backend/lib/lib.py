

class Request:
    def __init__(self, structure, model, dataset, train):
        self.train = train
        self.dataset = dataset
        self.model = model
        self.structure = structure


class Dataset:
    def __init__(self, learning_data_input: [], input_type: str,
                 depth_input_data: int, input_data_scale: int, learning_data_output: []):
        # array??? / датасет на вход
        self.learning_data_input = learning_data_input
        # String / тип входных данных
        self.input_type = input_type
        # int глубина входных данных / (255 для RGB картинки)
        self.depth_input_data = depth_input_data
        # int / размер входных данных (кол-во пикселей одной картинки)
        self.input_data_scale = input_data_scale
        # array??? / датасет на выход
        self.learning_data_output = learning_data_output


class Structure:
    def __init__(self, hidden_layer_count: int, neuron_count: [int],
                act_fn: [str]):
        # int / кол-во скрытых слоёв нейронов
        self.hidden_layer_count = hidden_layer_count
        # int_array / кол-во нейронов в каждом слое
        self.neuron_count = neuron_count
        # string_array / функция активации (длинна массива на 1 больше hidden_layer_count)
        self.act_fn = act_fn


class Model:
    def __init__(self, opt_fn: str, loss_fn: str):
        # string / способ оптимизации (градиентный спуск)
        self.opt_fn = opt_fn
        # string / функция потерь
        self.loss_fn = loss_fn


class Train:
    def __init__(self, epochs: int, validation_split: float, batch_size: int):
        # int / кол-во повторений обучения
        self.epochs = epochs
        # float / размер шага (при градиентном спуске)
        self.validation_split = validation_split
        # int / кол-во повторений между оптимизацией
        self.batch_size = batch_size