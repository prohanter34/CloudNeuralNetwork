from fastapi import FastAPI
from database.main import Database
from server.dataModels.models import User
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
print('start')

path = 'localhost'
if 'MY_PATH' in os.environ:
    path = os.environ["MY_PATH"]

database = Database()


@app.post("/auth/registration")
def registration(user: User) -> object:
    # results = database.put_user(user.login, user.password, user.email)
    # todo

    response = {
        "recultCode": 0,
        "email": user.email,
        "login": user.login
    }
    return response


@app.post('/{}/'.format(path) + "auth/login")
def login(user: User) -> object:
    results = database.take_user(user.login)

    response = {
        "resultCode": 0,
        "email": results[2],
        "login": results[0]
    }
    return response


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