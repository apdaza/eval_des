from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class relacion(db.Model):
    id = db.Column("rel_id", db.Integer, primary_key=True)
    rel_documento_jefe = db.Column(db.String(50))
    rel_documento_empleado = db.Column(db.String(50))
    
	
    def __init__(self, datos):
        self.rel_documento_empleado = datos["documento_empleado"]
        self.rel_documento_jefe = datos["documento_jefe"]

class persona(db.Model):
    id = db.Column("per_id", db.Integer, primary_key=True)
    per_documento = db.Column(db.String(50))
    per_nombre = db.Column(db.String(50))
    per_cargo = db.Column(db.String(50))
    per_clave = db.Column(db.String(50))
    
    def __init__(self, datos):
        self.per_documento = datos["documento"]
        self.per_nombre = datos["nombre"]
        self.per_cargo  = datos["cargo"]
        self.per_clave  = datos["documento"]

class evaluacion(db.Model):
    id = db.Column("per_id", db.Integer, primary_key=True)
    evl_tipo = db.Column(db.String(2))
    evl_documento_jefe = db.Column(db.String(50))
    evl_documento_empleado = db.Column(db.String(50))
    evl_pregunta = db.Column(db.Integer)
    evl_valor = db.Column(db.Integer)

    def __init__(self, datos):
        self.evl_tipo = datos["tipo"]
        self.evl_documento_empleado = datos["documento_empleado"]
        self.evl_documento_jefe = datos["documento_jefe"]
        self.evl_pregunta = datos["pregunta"]
        self.evl_valor = datos["valor"]
        
"""

CREATE TABLE MNTPE.PE_EVALUACION_PERSONA (
	EVP_COD VARCHAR2(11) NOT NULL,
	EVP_PRG_COD VARCHAR2(11) NOT NULL,
	EVP_EVL_COD NUMBER(38,0) NOT NULL,
	EVP_NRO_DOC_EVALUA NUMBER(11,0) NOT NULL,
	EVP_VALOR NUMBER(4,0) NOT NULL,
	EVP_ESTADO VARCHAR2(2) NOT NULL,
	EVP_FECHA_CREACION DATE NOT NULL,
);


CREATE TABLE MNTPE.PE_NIVEL_PUNTUACION (
	NVL_COD NUMBER(38,0) NOT NULL,
	NVL_NOMBRE VARCHAR2(50) NOT NULL,
	NVL_DESCRIPCION VARCHAR2(100) NULL,
	NVL_VALOR_MIN NUMBER(4,0) NULL,
	NVL_VALOR_MAX NUMBER(4,0) NULL,
	NVL_ESTADO VARCHAR2(2) NOT NULL,
	NVL_FECHA_CREACION DATE NOT NULL,
);

CREATE TABLE MNTPE.PE_PREGUNTA_EVAL (
	PRG_COD VARCHAR2(11) NOT NULL,
	PRG_CATEGORIA VARCHAR2(100) NOT NULL,
	PRG_TEXTO VARCHAR2(255) NOT NULL,
	PRG_MAX_VALOR NUMBER(3,0) NOT NULL,
	PRG_PESO_EVAL NUMBER(3,0) NULL,
	PRG_ESTADO VARCHAR2(2) NOT NULL,
	PRG_FECHA_CREACION DATE NOT NULL,
);

CREATE TABLE MNTPE.PE_EVALUACION_PUNTUACION (
	EVP_EVL_COD NUMBER(38,0) NOT NULL,
	EVP_NVL_COD NUMBER(38,0) NOT NULL,
	EVP_ESTADO VARCHAR2(2) NOT NULL,
	EVP_FECHA_CREACION DATE NOT NULL,
);

"""