CREATE DATABASE proyecto_e1;

CREATE TABLE Ubicaciones(
    id_ubicacion INT,
    salon VARCHAR(255),
    PRIMARY KEY (id_ubicacion),  
);

CREATE TABLE Dispositivos(
    id_dispositivo INT,
    num_serie VARCHAR(255),
    modelo VARCHAR(255),
    marca VARCHAR(255),
    id_ubicacion INT,
    PRIMARY KEY (id_dispositivo),
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion),  
);

CREATE TABLE Sensores(
    id_sensor INT,
    nom_sensor VARCHAR(255),
    marca VARCHAR(255),
    modelos VARCHAR(255),
    _precision FLOAT,
    antiguedad INT,
    id_dispositivo INT,
    id_param INT,
    PRIMARY KEY (id_sensor),
    FOREIGN KEY(id_dispositivo) REFERENCES Dispositivos(id_dispositivo),

);

CREATE TABLE Parametros (
    id_param INT,
    valorMaximo FLOAT,
    valorMinimo FLOAT,
    alertaMaxima INT,
    alertaMinima INT,
    id_sensor INT,

    PRIMARY KEY (id_param),
    FOREIGN KEY(id_sensor) REFERENCES Sensores(id_sensor),

);

CREATE TABLE Mediciones(
    id_medicion INT,
    tiemp_medi INT,
    id_param INT,
    id_sensor INT,
    id_dispositivo INT,
    PRIMARY KEY (id_medicion),
    FOREIGN KEY (id_param) REFERENCES Parametros(id_param),
    FOREIGN KEY (id_sensor) REFERENCES Sensores(id_sensor),
    FOREIGN KEY (id_dispositivo) REFERENCES Dispositivos(id_dispositivo),

);







