import os
from urllib.parse import quote_plus
from flask import Flask, request, render_template, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Recuperar variables de entorno
usuario = quote_plus(os.environ['MONGO_USER'])
clave = quote_plus(os.environ['MONGO_PASS'])
cluster = os.environ['MONGO_CLUSTER']
base_datos = os.environ['MONGO_DB']

# URI segura
uri = f"mongodb+srv://{usuario}:{clave}@{cluster}/{base_datos}?retryWrites=true&w=majority"

# Conexión a MongoDB
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client[base_datos]
coleccion = db["mi_coleccion"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sensor = request.form['sensor']
        valor = float(request.form['valor'])
        unidad = request.form['unidad']
        ubicacion = request.form['ubicacion']

        coleccion.insert_one({
            "sensor": sensor,
            "valor": valor,
            "unidad": unidad,
            "ubicacion": ubicacion
        })
        return redirect('/')

    datos = list(coleccion.find({}, {"_id": 0}))
    return render_template('index.html', datos=datos)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
