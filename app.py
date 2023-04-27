from flask import Flask, render_template, request
import requests

app = Flask(__name__)



@app.route('/')

def base():
    return render_template('base.html')

@app.route('/vendedores.html')

def consulta():
    return render_template('vendedores.html')

@app.route('/formulario.html')
def form():
    return render_template('formulario.html')

@app.route('/resultado.html')
def resul():
    return render_template('resultado.html')

@app.route('/formulario.html', methods=['GET', 'POST'])
def alta_vendedor():
    if request.method == 'POST':
        # Obtener el valor de la base de datos del formulario
        base = request.form['base']

        # Crear el diccionario con los datos a enviar
        data = {
            "Codigo": request.form['codigo'],
            "Nombre": request.form['nombre'],
            "NroDocumento": request.form['nro_documento']
        }

        # Crear los headers con la información de autorización y autenticación
        headers = {
            "accept": "application/json",
            "IdCliente": "APIALEX",
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3VhcmlvIjoiQURNSU4iLCJwYXNzd29yZCI6IjFhZjIwZWY4Njk5MjI0MzU1ZTdjNWQ3MTYwY2JlMjAzOTIwZWU4MGU1Zjg5ZDFmNjM5OTQ1YTQ2OWM0OWFkMmEiLCJleHAiOiIxNjg3NjM4OTEyIn0.NCAE0WEuhppe2fLOO21gtWy658F-Uh95iWWUfZ0NpVU",
            "BaseDeDatos": base,
            "Content-Type": "application/json"
        }

        # Hacer la solicitud POST a la API
        url = "http://190.220.155.74:8008/api.Dragonfish/Vendedor/"
        response = requests.post(url, json=data, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
             mensaje = "Alta de vendedor exitosa."
        elif response.status_code in [409]:
             mensaje = "El código ya existe."
        else:
             mensaje = f"SOLICITUD REALIZADA CORRECTAMENTE: {response.status_code}"
             print(response.status_code)

        return render_template('resultado.html', mensaje=mensaje)

    return render_template('base.html')



@app.route('/vendedores.html', methods=['GET', 'POST'])
def index():
    r = None
    error_message = None
    if request.method == 'POST':
        codigo = request.form['codigo']
        base_de_datos = request.form['base_de_datos']
        payload = {'query':codigo}
        r = requests.get('http://190.220.155.74:8008/api.Dragonfish/Vendedor/', 
                 params=payload, 
                 headers={'IdCliente' : "APIALEX", 
                          'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3VhcmlvIjoiQURNSU4iLCJwYXNzd29yZCI6IjFhZjIwZWY4Njk5MjI0MzU1ZTdjNWQ3MTYwY2JlMjAzOTIwZWU4MGU1Zjg5ZDFmNjM5OTQ1YTQ2OWM0OWFkMmEiLCJleHAiOiIxNjg3NjM4OTEyIn0.NCAE0WEuhppe2fLOO21gtWy658F-Uh95iWWUfZ0NpVU', 
                          'BaseDeDatos' : base_de_datos
                           }
                 
                 ) # define un tiempo de espera de 30 segundos      
                        
        if r is not None and r.status_code == 200:
            resultados = r.json()         
            return render_template('resultados.html', resultados=resultados)
        else:
            print(f"Error en la solicitud: {r.status_code}")
            if r is not None and r.status_code == 404:
                error_message = "El vendedor no existe en la base de datos."
    return render_template('vendedores.html', error=error_message)


if __name__ == '__main__':
    app.run()
   
