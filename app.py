from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from util import create_app, db
from models import persona, relacion, evaluacion
from datetime import datetime
import pandas as pd

df_personas = pd.read_excel('archivos/personas.xlsx', sheet_name="personas")
df_relacion = pd.read_excel('archivos/personas.xlsx', sheet_name="relacion")

app = create_app()

@app.route('/poblar')
def poblar():
    for i in range(len(df_personas)):
        #print(df_personas.iloc[i]['documento'])
        datos = {"documento" : str(df_personas.iloc[i]['documento']), 
                "nombre" : df_personas.iloc[i]['nombre'], 
                "cargo" : df_personas.iloc[i]['cargo'],
                "clave" : df_personas.iloc[i]['documento']

                }
        db.session.add(persona(datos))
    db.session.commit()

    for i in range(len(df_relacion)):
        #print(df_personas.iloc[i]['documento'])
        datos = {"documento_jefe" : str(df_relacion.iloc[i]['documento_jefe']), 
                "documento_empleado" : str(df_relacion.iloc[i]['documento_empleado'])

                }
        db.session.add(relacion(datos))
    db.session.commit()
    return "base de datos poblada"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        documento = request.form['documento']
        clave = request.form['clave']
        return redirect(url_for('verificacion', documento = documento, clave = clave))  
    
@app.route('/verificacion/<documento>/<clave>')
def verificacion(documento, clave):
    p = persona.query.filter_by(per_documento=documento, per_clave = clave).first()
    if p is not None:
        r = relacion.query.filter_by(rel_documento_jefe = documento).all()
        if len(r) > 0:
            # Consulta con join y filtro
            resultados = db.session.query(relacion, persona).join(persona, relacion.rel_documento_empleado == persona.per_documento).\
                filter(relacion.rel_documento_jefe == documento).all()

            # Iterar sobre los resultados
            for tabla1, tabla2 in resultados:
                print(f"Tabla1: {tabla1.rel_documento_empleado}, Tabla2: {tabla2.per_nombre}")
            return render_template('evaluados.html', resultados = resultados)
        else:
            return "evaluado"
    else: 
        return redirect(url_for('login'))
    #return render_template('index.html', usuario = usuario)

@app.route('/evaluar/<documento_empleado>/<documento_jefe>', methods=['GET', 'POST'])
def evaluar(documento_empleado, documento_jefe):
    if request.method == 'GET':
        jefe = persona.query.filter_by(per_documento=documento_jefe).first()
        empleado = persona.query.filter_by(per_documento=documento_empleado).first()
        return render_template('formulario.html', jefe = jefe, empleado = empleado, fecha = datetime.now().date())
    else:
        if documento_empleado != documento_jefe:
            tipo = "EV"
        else:
            tipo = "AV"
        for i in range(1, 12):
            data = {
                "tipo": tipo,
                "documento_empleado": documento_empleado,
                "documento_jefe": documento_jefe,
                "pregunta": str(i),
                "valor": request.form["pregunta_" + str(i)]

            }
            e = evaluacion(data)
            db.session.add(e)
        db.session.commit()
        return redirect('/verificacion/'+documento_jefe+'/'+documento_jefe)

@app.route('/ver_eval/<documento_empleado>/<documento_jefe>', methods=['GET', 'POST'])
def ver_eval(documento_empleado, documento_jefe):
    if request.method == 'GET':
        jefe = persona.query.filter_by(per_documento=documento_jefe).first()
        empleado = persona.query.filter_by(per_documento=documento_empleado).first()
        eval = evaluacion.query.filter_by(evl_documento_jefe = documento_jefe, evl_documento_empleado = documento_empleado).all()
        
        return render_template('formulario_ver.html', jefe = jefe, empleado = empleado, fecha = datetime.now().date(), resultado = eval)
    else:
        return redirect('/verificacion/'+documento_jefe+'/'+documento_jefe)


@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route("/productos/")
def principal():
    data = producto.query.all()
    diccionario_productos = {}
    for d in data:
        p = {"id": d.id,
             "nombre": d.producto_nombre,
             "cantidad": d.producto_cantidad,
             "valor": d.producto_valor
            }
        diccionario_productos[d.id] = p
    return diccionario_productos

@app.route("/agregar/<nombre>/<int:cantidad>/<int:valor>")
def agregar(nombre, cantidad, valor):
    datos = {"nombre": nombre,
             "cantidad": cantidad,
             "valor": valor
            }
    p = producto(datos)
    db.session.add(p)
    db.session.commit()
    return redirect("/productos/")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    p = producto.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect("/productos/")

@app.route("/actualizar/<int:id>/<nombre>/<int:cantidad>/<int:valor>")
def actualizar(id, nombre, cantidad, valor):
    p = producto.query.filter_by(id=id).first()
    p.producto_nombre = nombre
    p.producto_cantidad = cantidad
    p.producto_valor = valor
    db.session.commit()
    return redirect("/productos/")

@app.route("/buscar/<int:id>")
def buscar(id):
    d = producto.query.filter_by(id=id).first()
    p = {"id": d.id,
         "nombre": d.producto_nombre,
         "cantidad": d.producto_cantidad,
         "valor": d.producto_valor
        }
    return p


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="8080") 

