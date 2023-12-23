CREATE DATABASE cloudneuralnetwork
\c cloudneuralnetwork
CREATE TABLE users (
    id serial,
    login VARCHAR(50) NOT NULL PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL
);

CREATE TABLE networks (
    id serial PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    login VARCHAR NOT NULL REFERENCES users(login),
    path VARCHAR NOT NULL,
    optimization VARCHAR(50) NOT NULL,
    lossfn VARCHAR(50) NOT NULL,
    activations VARCHAR(50)[] NOT NULL,
    neuroncount INTEGER[] NOT NULL
);
