import uvicorn
import uuid
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from backend.neural_network.main import NeuralNetwork
from backend.server.dataModels.models import User, Data, Final
from backend.lib.lib import Request, Model, Structure, Dataset, Train
from backend.database.main import Database

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

# @app.get("/data", response_class=HTMLResponse)
# async def read_items():
#     html_content = """
#     <!DOCTYPE html>
#     <html>
#        <body>
#           <form method="post" action="http://127.0.0.1:8000/data"  enctype="multipart/form-data">
#              opt_fn : <input type="text" name="opt_fn" value=adam><br>
#              loss_fn : <input type="text" name="loss_fn" value=categorical_crossentropy><br>
#              neuron_count : <input type="text" name="neuron_count" value=128,200,27><br>
#              hidden_layer_count : <input type="text" name="hidden_layer_count" value=2><br>
#              act_fn : <input type="text" name="act_fn" value=relu,relu,softmax><br>
#              depth_input_data : <input type="text" name="depth_input_data" value=255><br>
#              epochs : <input type="text" name="epochs" value=10><br>
#              validation_split : <input type="text" name="validation_split" value=0.1><br>
#              batch_size : <input type="text" name="batch_size" value=32><br>
#              <label for="dataset">Choose files to upload</label>
#              <input type="file" id="file" name="dataset">
#              <input type="submit" value="submit">
#           </form>
#        </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content, status_code=200)

@app.post("/data")
def user_data(data: Data, dataset: UploadFile) -> object:
# def user_data(opt_fn: str = Form(...),
#               loss_fn: str = Form(...),
#               neuron_count: str = Form(...),
#               hidden_layer_count: str = Form(...),
#               act_fn: str = Form(...),
#               depth_input_data: str = Form(...),
#               epochs: str = Form(...),
#               validation_split: str = Form(...),
#               batch_size: str = Form(...),
#               dataset: UploadFile = File(...)) -> object:

    contents = dataset.file.read()
    file_name = dataset.filename
    file_path = "./" + "".join(str(uuid.uuid4()).split("-")) + file_name
    with open(file_path, "wb") as f:
        f.write(contents)
    dataset.file.close()

    # data = Data(opt_fn=opt_fn,loss_fn=loss_fn,neuron_count=list(map(int, neuron_count.split(","))),
    #             hidden_layer_count=hidden_layer_count,act_fn=act_fn.split(","),
    #             depth_input_data=depth_input_data,epochs=epochs,
    #             validation_split=validation_split,batch_size=batch_size)

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
    neuralnetwork_file_path = "../final/" + "".join(str(uuid.uuid4()).split("-")) + ".keras"
    neuralnetwork.save_model(model, neuralnetwork_file_path)

    response = {"neuralnetwork_file_path": neuralnetwork_file_path,
                "resultCode": 200}
    return response

@app.get("/final")
def download_file(final: Final) -> object:
    return FileResponse(path=final.neuralnetwork_file_path)


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