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


if __name__ == "__main__":
    app.run(debug=True)
