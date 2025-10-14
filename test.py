from flask import Flask, render_template, request, redirect, url_for, session as sessionFlask
import json

USUARIOS_JSON = "usuarios.json"

def guardar_usuarios(usuarios):
    try:
        with open(USUARIOS_JSON, "r") as file:
            data = json.load(file)

            # Obtener el nombre del login actual desde la sesión
            login_actual = sessionFlask['username']

            # Buscar el conjunto de usuarios correspondiente
            for login_info in data.get('login', []):
                if login_info.get('session') and login_info['session'][0].get(login_actual):
                    # Actualizar la lista de usuarios
                    login_info['usuarios'] = usuarios

                    # Guardar los cambios en el archivo JSON
                    with open(USUARIOS_JSON, "w") as write_file:
                        json.dump(data, write_file, indent=2)
                    break
    except FileNotFoundError as e:
        print(f"Error al abrir el archivo: {e}")
        # Manejar el caso cuando el archivo no existe
        # Aquí podrías crear un nuevo archivo con la estructura adecuada
        pass

guardar_usuarios("d")