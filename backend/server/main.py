import uvicorn
import uuid
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from neural_network.main import NeuralNetwork
from server.dataModels.models import User, Data, Final
from lib.lib import Request, Model, Structure, Dataset, Train
from database.main import Database

app = FastAPI()
print('start')

path = 'localhost'
if 'MY_PATH' in os.environ:
    path = os.environ["MY_PATH"]

database = Database()


@app.post("/auth/registration")
def registration(user: User) -> object:
    results = database.put_user(user.login, user.password, user.email)
    response = {
        "resultCode": 0,
        "email": user.email,
        "login": user.login
    }
    if results[0] == "0":
        return response
    else:
        response["resultCode"] = 1
        response["email"] = ""
        response["login"] = ""
        return response


@app.post("/auth/login")
def login(user: User) -> object:
    results = database.take_user(user.login)

    response = {
        "resultCode": 1,
        "email": "",
        "login": ""
    }

    if results[0] == "1":
        return response
    elif results[0][2] == user.password:
        response = {
            "resultCode": 0,
            "email": results[0][3],
            "login": results[0][1]
        }
        return response
    else:
        response["resultCode"] = 2
        return response


@app.post("/data")
def user_data(data: Data, dataset: UploadFile) -> object:

    contents = dataset.file.read()
    file_name = dataset.filename
    file_path = "./" + "".join(str(uuid.uuid4()).split("-")) + file_name
    with open(file_path, "wb") as f:
        f.write(contents)
    dataset.file.close()

    model = Model(opt_fn=data.opt_fn, loss_fn=data.loss_fn)
    structure = Structure(neuron_count=data.neuron_count,
                          hidden_layer_count=data.hidden_layer_count,
                          act_fn=data.act_fn)
    file = open(file_path, "r")
    dataset_model = Dataset(learning_data=file,
                            input_type=dataset.filename.split(".")[-1],
                            depth_input_data=data.depth_input_data)
    train = Train(epochs=data.epochs, validation_split=data.validation_split,
                  batch_size=data.batch_size)

    request = Request(dataset=dataset_model, model=model, structure=structure,
                      train=train)
    neuralnetwork = NeuralNetwork(model=request.model,
                                  structure=request.structure,
                                  train=request.train, dataset=request.dataset)

    model = neuralnetwork.create_model()
    model = neuralnetwork.train_model(model)
    neuralnetwork_file_name = "".join(str(uuid.uuid4()).split("-"))
    neuralnetwork_file_path = "../final/" + neuralnetwork_file_name + ".keras"
    neuralnetwork.save_model(model, neuralnetwork_file_path)

    response = {"neuralnetwork_file_name": neuralnetwork_file_name,
                "resultCode": 200}
    return response

@app.post("/final")
def download_file(final: Final) -> object:
    return FileResponse(path=("../final/" + final.neuralnetwork_file_name + ".keras"))


origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app")