
CREATE TABLE viniedos(
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    nombre VARCHAR(200),
    superficie FLOAT NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    localidad VARCHAR(300) NOT NULL,
    pais VARCHAR(200) NOT NULL
);
INSERT INTO viniedos (id,nombre,superficie,localidad,pais) VALUES ("f2e984f0-d4e7-4cf4-be1e-2fb5e064211a","Viñedo Vista Andina",7,"Tunuyán-Mendoza","Argentina")
INSERT INTO viniedos (id,nombre,superficie,localidad,pais) VALUES ("45cc3968-675a-4be5-ad15-1a8d8eee86ef","Finca Sol de los Andes",10,"Tunuyán-Mendoza","Argentina")

CREATE TABLE parcelas(
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    id_viniedo VARCHAR(100) NOT NULL,
    nombre VARCHAR(200),
    superficie FLOAT NOT NULL,
    latitud VARCHAR(15),
    longitud VARCHAR(15),
    FOREIGN KEY (id_viniedo) REFERENCES viniedos(id)
);

INSERT INTO parcelas (id,id_viniedo,nombre,superficie,latitud,longitud) VALUES ('53f1b371-1045-447a-ab8e-cdb4c93b6b04','f2e984f0-d4e7-4cf4-be1e-2fb5e064211a','Parcela A',1.5,"-33.5778960","-69.0695519");

CREATE TABLE suelos(
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    composicion TEXT,
    drenaje VARCHAR(20),
    pH DECIMAL(4, 2),
    retencionAgua VARCHAR(20),
    texturaSuelo VARCHAR(20),
    capacidadAireacion VARCHAR(20),
    retencionNutrientes VARCHAR(20),
    propiedadesViticultura TEXT
)

CREATE TABLE tipoDeSueloParcela(
    id_suelo VARCHAR(100) NOT NULL,
    id_parcela VARCHAR (100) NOT NULL,
    FOREIGN KEY (id_suelo) REFERENCES suelos(id),
    FOREIGN KEY (id_parcela) REFERENCES parcelas(id)
)

CREATE TABLE tareas(
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    nombre_tarea VARCHAR(255),
    descripcion TEXT,
    fecha_creacion DATE,
    fecha_limite DATE,
    prioridad VARCHAR(50), /*'Alta', 'Media', 'Baja'*/
    estado VARCHAR(40) /*'Pendiente', 'En progreso', 'Completada'*/
);

CREATE TABLE tareasPorParcela(
    id_parcela VARCHAR (100) NOT NULL,
    id_tarea VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_parcela) REFERENCES parcelas(id),
    FOREIGN KEY (id_tarea) REFERENCES tareas(id)
)

INSERT INTO tareas (id,nombre_tarea,fecha_creacion,fecha_limite,prioridad,estado) VALUES ('64d51c1e-51a8-47ac-b577-ff8dbfc5e6f4','Poda de viñedos','2023-11-28','2023-12-25','Media','Pendiente');

INSERT INTO tareas (id,nombre_tarea,descripcion,fecha_creacion,fecha_limite,prioridad,estado) VALUES ('b9d7c5f4-5001-4e2c-914f-75fa80f247f2','Control de humedad y riego','Monitorear y ajustar el riego de las vides','2023-11-21','2023-12-30','Media','Pendiente');

INSERT INTO tareas (id,nombre_tarea,descripcion,fecha_creacion,fecha_limite,prioridad,estado) VALUES ('96f8d9d5-6f0f-4e36-8272-68784990c973','Fertilización y aplicación de nutrientes','','2023-11-16','2023-12-21','Media','Pendiente');


/*
Peticion especial
*/


update viniedos set coordenadas = ST_GeomFromText('POLYGON((-69.1277077 -33.5844884, -69.1281368 -33.5808417, -69.1274502 -33.5806272, -69.127536 -33.5800194, -69.1256048 -33.5798763, -69.1261198 -33.5712593, -69.1184379 -33.5709375, -69.1172792 -33.5840594, -69.1275789 -33.5845242, -69.1277077 -33.5844884))') WHERE id = "f2e984f0-d4e7-4cf4-be1e-2fb5e064211a"

-- Ejemplo de inserción de coordenadas para un viñedo con ID '1'
INSERT INTO viniedos (id, nombre, superficie, provincia, localidad, pais, coordenadas)
VALUES ('1', 'Nombre del Viñedo', 150.5, 'Provincia A', 'Localidad X', 'Pais Y',
        ST_GeomFromText('POLYGON((-69.1277077 -33.5844884, -69.1281368 -33.5808417, -69.1274502 -33.5806272, -69.127536 -33.5800194, -69.1256048 -33.5798763, -69.1261198 -33.5712593, -69.1184379 -33.5709375, -69.1172792 -33.5840594, -69.1275789 -33.5845242, -69.1277077 -33.5844884))'));



coordenadas_parcela = [
                    [-69.1278309, -33.5845126],
                    [-69.128058, -33.5806069],
                    [-69.1274786, -33.580589],
                    [-69.1275001, -33.5799812],
                    [-69.1256332, -33.5799455],
                    [-69.1252472, -33.5843788],
                    [-69.1277575, -33.5845039]
 ]


 'POLYGON((-69.1278309 -33.5845126,-69.1280580 -33.5806069,-69.1274786 -33.5805890,-69.1275001 -33.5799812,-69.1256332 -33.5799455,-69.1252472 -33.5843788,-69.1277575 -33.5845039))'


 parcela 2


 INSERT INTO parcelas (id, id_viniedo, nombre, superficie, longitud, latitud, coordenadas)
 VALUES
 ('erf1b373-1045-447a-ab8e-cdb4c93b8ss5','f2e984f0-d4e7-4cf4-be1e-2fb5e064211a','Parcela B',2,"-33.5736995","-69.1199017",ST_GeomFromText('POLYGON((-69.1220713, -33.5709709, -69.1183376 -33.5708279, -69.1179514 -33.5761555, -69.1215563 -33.5762985, -69.1220812 -33.5710906))'));



'POLYGON((-69.1220713, -33.5709709, -69.1183376 -33.5708279, -69.1179514 -33.5761555, -69.1215563 -33.5762985, -69.1220812 -33.5710906))'


INSERT INTO parcelas (id, id_viniedo, nombre, superficie, longitud, latitud, coordenadas)
VALUES
('b9d7c5f4-5001-4e2c-914f-75fa80f247f2','f2e984f0-d4e7-4cf4-be1e-2fb5e064211a','Parcela C',2.5,
 "-33.5776325", "-69.1235066", ST_GeomFromText('POLYGON((-69.1261673 -33.5711250, -69.1220904 -33.5709820, -69.1210657 -33.5843196, -69.1251803 -33.5843898, -69.1261244 -33.5711965, -69.1261673 -33.5711250))')
 )


 INSERT INTO parcelas (id, id_viniedo, nombre, superficie, longitud, latitud, coordenadas)
VALUES
('a8e6d4g5-5001-4e2c-914f-25gb90f458e3','f2e984f0-d4e7-4cf4-be1e-2fb5e064211a','Parcela D',1.5,
 "-33.5796705", "-69.1193867", ST_GeomFromText('POLYGON((-69.1172409 -33.5842111, -69.1178417 -33.5763096, -69.1215754 -33.5764884, -69.1210175 -33.5843183, -69.1172838 -33.5841396, -69.1172409 -33.5842111))'))
 )

 ST_GeomFromText('POLYGON((-69.1172409 -33.5842111, -69.1178417 -33.5763096, -69.1215754 -33.5764884, -69.1210175 -33.5843183, -69.1172838 -33.5841396, -69.1172409 -33.5842111))')


CREATE TABLE rendimientos