from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    email: str = None

class Data(BaseModel):
    opt_fn: str  # "adam"
    loss_fn: str  # "categorical_crossentropy"

    neuron_count: list[int] # [128, 200, 27]
    hidden_layer_count: int  # 2
    act_fn: list[str]  # ['relu', 'relu', 'softmax']

    depth_input_data: int # 255

    epochs: int # 10
    validation_split: float # 0.1
    batch_size: int # 32

class Final(BaseModel):
    neuralnetwork_file_name: str # путь к файлу готовой нейронки