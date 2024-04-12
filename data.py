import pandas as pd
from models import db, persona, relacion

df_personas = pd.read_excel('archivos/personas.xlsx', sheet_name="personas")
df_relacion = pd.read_excel('archivos/personas.xlsx', sheet_name="relacion")

print(df_relacion.columns)

def poblar_db():
    for i in range(len(df_personas)):
        print(df_personas.iloc[i]['documento'])
        datos = {"documento" : df_personas.iloc[i]['documento'], 
                "nombre" : df_personas.iloc[i]['nombre'], 
                "cargo" : df_personas.iloc[i]['cargo'],
                "clave" : df_personas.iloc[i]['documento']

                }
        db.session.add(persona(datos))
    db.session.commit()

    for i in range(len(df_relacion)):
        print(df_personas.iloc[i]['documento'])
        datos = {"documento_jefe" : df_personas.iloc[i]['documento_jefe'], 
                "documento_empleado" : df_personas.iloc[i]['documento_empleado']

                }
        db.session.add(relacion(datos))
    db.session.commit()
    