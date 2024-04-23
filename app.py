from flask import Flask, render_template, abort, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/buscador')
def buscador():
    return render_template("buscador.html")


@app.route('/lista', methods=["GET", "POST"])
def lista():
    if request.method == "POST":
        # Obtener el equipo de búsqueda del formulario
        cadena_busqueda = request.form.get('cadena', '')

        try:
            # Construir la ruta completa al archivo JSON
            ruta_json = os.path.join(app.root_path, 'static', 'EQUIPOS.json')
            
            # Intentar cargar el archivo JSON
            with open(ruta_json, 'r') as archivo:
                datos = json.load(archivo)

            # Filtrar los datos según la cadena de búsqueda
            datos_filtrados = [match for match in datos if any(team.startswith(cadena_busqueda) for team in match['teams'])]

            # Si no se encuentran partidos que coincidan, mostrar todos los partidos
            if not datos_filtrados:
                datos_filtrados = datos

        except FileNotFoundError:
            # Si el archivo no se encuentra, abortar con un error 404
            abort(404)
        
        # Renderizar la plantilla 'lista.html' y pasar los datos filtrados
        return render_template('lista.html', datos=datos_filtrados)
    else:
        # Si la solicitud es GET, simplemente renderiza la plantilla 'lista.html'
        return render_template('lista.html', datos=[])
    

@app.route('/detalle/<id_match>')
def detalles(id_match):
    try:
        # Cargar los datos del partido con el ID proporcionado desde el archivo JSON
        with open('static/EQUIPOS.json', 'r') as archivo:
            datos = json.load(archivo)
        
        # Buscar el partido con el ID proporcionado
        partido = next((match for match in datos if match['match_id'] == id_match), None)
        
        if partido:
            # Obtener los detalles del partido
            kickoff_time = partido.get('kickoff_time', '')
            goals = partido.get('goals', {})
            location = partido.get('location', '')

            # Renderizar la plantilla 'detalles.html' y pasar los datos del partido
            return render_template('detalles.html', id_match=id_match, kickoff_time=kickoff_time, goals=goals, location=location)
        else:
            mensaje_error = f"No se encontró ningún partido con el ID {id_match}. <a href='/'>Volver al inicio</a>"
            return mensaje_error, 404
    except FileNotFoundError:
        # Si el archivo no se encuentra, abortar con un error 404
        abort(404)
    
if __name__ == "__main__":
    app.run(debug=True)
