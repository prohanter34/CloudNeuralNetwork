import psycopg2
import os
import json


class Database:
    def __init__(self):
        entry_data = str(os.path.dirname(os.path.abspath(__file__)))
        entry_data += "/option_for_connect.json"
        entry_data = os.path.normpath(entry_data)

        entry_data = open(entry_data, "r")
        entry_data = json.load(entry_data)

        self.conn = psycopg2.connect(**entry_data)
        self.cursor = self.conn.cursor()

    def take_user(self, login):
        try:
            self.cursor.execute(F"SELECT * FROM users WHERE login='{login}';")
            return list(self.cursor.fetchall())
        except:
            return list("1")

    def put_user(self, login, password, email):
        try:
            self.cursor.execute(f"INSERT INTO users(login, password, email) VALUES ('{login}', '{password}', '{email}');")
            self.conn.commit()
            return list("0")
        except:
            return list("1")

    def take_users_networks(self, login):
        try:
            self.cursor.execute(f"SELECT * FROM networks where login='{login}';")
            return list(self.cursor.fetchall())
        except:
            return list("1")

    def put_network(self, name, path, login, optimization, lossfn, activations_arr, neuroncount_arr):
        activations = ""
        for i in activations_arr:
            activations += '"' + i + '"'
            activations += " ,"
        activations = activations[:-2]

        neuroncount = ""
        for i in neuroncount_arr:
            neuroncount += str(i)
            neuroncount += " ,"
        neuroncount = neuroncount[:-2]

        try:
            self.cursor.execute(f"INSERT INTO networks(name, path, login, optimization, " +
                                f"lossfn, activations, neuroncount) " +
                                f"VALUES ('{name}', '{path}', '{login}', " +
                                f"'{optimization}', '{lossfn}', " + "'{" + activations + "}'" + ",'{" + neuroncount + "}');")
            self.conn.commit()
            return list("0")
        except:
           return list("1")

    def take_network_params(self, id):
        try:
            self.cursor.execute(f"SELECT * FROM networks WHERE id='{id}'")
            return list(self.cursor.fetchall())
        except:
            return list('1')