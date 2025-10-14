# -*- coding: utf-8 -*-
# coding=utf-8  # Agrega esta línea para declarar la codificación
#cd /volume1/Drive/panel_plex
#comando gunicorn -b 0.0.0.0:8096 -w 4 app:app
#acceder http://panelplex.ddns.net:8096 o http://panelplex.synology.me:8096
from flask import Flask, render_template, request, redirect, url_for,flash
import json
from datetime import datetime, timedelta
import requests
import random
import string
import uuid
from plexapi.server import PlexServer
from werkzeug.serving import run_simple
import schedule
import time
import threading 
from flask import Flask, render_template, request, redirect, url_for, session as sessionFlask,send_file,jsonify
import os

#   CARACTERISTICAS DE LA APP
#
#   Creacion de usuarios en plex
#   Tabla con los usuarios existentes en tu servidor con filtro para facilitar la busqueda
#   Eliminacion automatica de usuarios al vencer la fecha limite
#   Eliminacion de usuarios de tu servidor
#   Invitacion de usuarios a tu servidor
#   Modificacion de pantallas y fechas de vencido
#   Cierre automatico de sesion cuando superan las pantallas (necesario Plex Pass e instalar tautulli)
#   Menu de avisos que te muestra los usuarios los cuales estan a punto de caducar su subscripcion 
#   Creacion de usuarios DEMO
#   Codigos de colores para saber si estan invitados, si no tienen acceso o si su mensualidad ha caducado
#   Eliminacion de bibliotecas (anadir lista de bibliotecas)
#   Conectar app en remoto 
#   Controlar acceso con login
#   Guardar valores de modificacion usuarios proximos a expirar
#   Filtros para las listas

#   controlar con try catch todos los sitios donde se necesite api o url y escribir excepcion en log con todos los datos posibles
#   Ponerle astirsco rojo a los labels(input) obligatorios
#   Anadir una especie de "key" online para poder usar la app

app = Flask(__name__, template_folder='templates',static_folder='static')
app.secret_key = 'secreta'

#Variables como guia de donde obtenerlas
PLEX_SERVER_URL = "http://192.168.1.2:32400"
PLEX_TOKEN = "tSiiwBwrz8mPByT4gKR5" #El token se obtiene cogiendo una peli, dando a los 3 puntos, obtener informacion, ver XML y en la URL encontramos el token
TAUTULLI_URL = "http://192.168.1.2:8181"
TAUTULLI_APIKEY = "wP6dWbKUjBR7F0ncFFkiqz1UxMzqgIVO" #se encuentra en settigns > web interface IMPORTANTE: tener bien confitgurado tautulli

USUARIOS_JSON = "usuarios.json"

def detenerPantalla(email):
    # Cargar datos actuales desde usuarios.json
    with open(USUARIOS_JSON, 'r') as usuarios_json:
        usuarios = json.load(usuarios_json)

    try:
        # Buscar el usuario por email y obtener el servidor al que pertenece
        servidor_usuario = None
        for login_info in usuarios.get('login', []):
            for servidor in login_info.get('servidores', []):
                for usuario in servidor.get('usuarios', []):
                    if usuario['email'] == email:
                        servidor_usuario = servidor
                        break
                if servidor_usuario:
                    break
            if servidor_usuario:
                break

        if servidor_usuario:
            # Obtener la URL y API de Tautulli del servidor
            tautulli_url = servidor_usuario.get('urlTautulli', '')
            tautulli_apikey = servidor_usuario.get('apiTautulli', '')

            url = f"{tautulli_url}/api/v2?apikey={tautulli_apikey}&cmd=get_activity"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                print(data)
                sessions = data["response"]["data"]["sessions"]

                for session in sessions:
                    session_id = session["session_id"]
                    user = session["email"]
                    custom_message = "Has superado el limite de pantallas, cierra Plex en algun dispositivo"

                    if user == email:
                        url = f"{tautulli_url}/api/v2?apikey={tautulli_apikey}&cmd=terminate_session&session_id={session_id}&message={custom_message}"

                        response = requests.get(url)

                        if response.status_code == 200:
                            print(f"Sesion con ID {session_id} detenida exitosamente en el servidor {servidor_usuario['nombre_server']}.")
                        else:
                            print(f"Error al detener la sesion en el servidor {servidor_usuario['nombre_server']}. Codigo de estado: {response.status_code}")
                            print(response.text)
            else:
                print(f"Error al obtener informacion de sesiones en el servidor {servidor_usuario['nombre_server']}. Codigo de estado: {response.status_code}")
                print(response.text)
        else:
            print(f"No se encontro el usuario con el correo electronico {email} en ningun servidor.")
    except Exception as e:
        message = f"Error posiblemente con Tautulli en el metodo 'detenerPantalla' [revisar url y api tautulli]: {e}"
        escribir_log_error(message)

def detener_reproductor_si_es_necesario(email, plex):
    # Obtener información del usuario desde el JSON
    usuarios = cargar_usuarios()
    usuario = next((usuario for usuario in usuarios if usuario["email"] == email), None)

    if usuario:      
        # Obtener información sobre las sesiones del usuario actual
        sesiones_usuario = plex.sessions()
        sesiones_activas = [sesion for sesion in sesiones_usuario if sesion.user.email == email]

        # Comparar sesiones activas con el límite permitido
        limite_pantallas = int(usuario["pantallas"])
        if len(sesiones_activas) > limite_pantallas:
            # Autenticar al usuario para obtener un token
            detenerPantalla(email)

def conceder_acceso_biblioteca(email):

    # Cargar datos actuales desde usuarios.json
    usuarios = cargar_usuarios_session()

    # Buscar el usuario por email
    usuario_modificar = next((usuario for usuario in usuarios if usuario["email"] == email), None)
    try:
        if usuario_modificar:
            # Obtener la fecha actual sin la hora
            fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # Convertir la fecha de expiración del usuario "pepito" a un objeto datetime
            expiracion = datetime.strptime(usuario_modificar['expiracion'], '%d/%m/%Y')
            
            if fecha_actual <= expiracion:

                sess = requests.Session()
                # Ignore verifying the SSL certificate
                sess.verify = False  # '/path/to/certfile'
                # If verify is set to a path to a directory,
                # the directory must have been processed using the c_rehash utility supplied
                # with OpenSSL.
                if sess.verify is False:
                    # Disable the warning that the request is insecure, we know that...
                    import urllib3

                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                plex = PlexServer(devolverApiPlexSession("urlPlex"), devolverApiPlexSession("apiPlex"), session=sess)

                sections_lst = [x.title for x in plex.library.sections()]

                filterMovies = {}  # Inicializar los diccionarios de filtro
                filterTelevision = {}
                filterMusic = {}

                try:
                    plex.myPlexAccount().inviteFriend(user=email, server=plex, sections=sections_lst, allowSync=True,
                                                allowCameraUpload=False, allowChannels=True, filterMovies=filterMovies,
                                                filterTelevision=filterTelevision, filterMusic=filterMusic)
                    
                    usuario_modificar["codigoColor"] = "1"

                    # Guardar los cambios en usuarios.json
                    guardar_usuarios(usuarios)
                    
                    return render_template('exito.html', email=email)

                except:
                    return render_template('fallo.html', mensaje=f"el email {email} Ya tiene una invitacion activa, no necesita otra invitacion")
            else:
                flash(f"Antes de invitar debes prolongar la expiracion del usuario {email}.     ", 'error')
                return redirect(url_for('lista_usuarios'))
    except Exception as e:
        message = f"Error al invitar usuario a la biblioteca en el metodo 'conceder_acceso_biblioteca' [revisar url y api plex]: {e}"
        escribir_log_error(message)
        flash(f"Error al invitar a usuario, revise el token o url de su servidor plex", 'error')
        return redirect(url_for('lista_usuarios'))

def generar_contrasena_aleatoria():
    # Caracteres permitidos
    caracteres = string.ascii_letters + string.digits + ".-"

    # Al menos un número, una mayúscula, una minúscula y un "." o "-"
    contrasena = (
        random.choice(string.digits) +
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_lowercase) +
        random.choice(".-") +
        ''.join(random.choice(caracteres) for _ in range(4))  # Resto de la contrasena
    )

    # Completa la contrasena con caracteres aleatorios hasta llegar a la longitud deseada
    while len(contrasena) < 10:
        contrasena += random.choice(caracteres)

    # Mezcla los caracteres para mayor aleatoriedad
    contrasena = ''.join(random.sample(contrasena, len(contrasena)))

    return contrasena

#Para los metodos que necesiten cargar solo los usuarios del cliente
def cargar_usuarios_session():
    try:
       with open(USUARIOS_JSON) as f:
            data = json.load(f)

            # Obtener el nombre del login actual desde la sesión
            login_actual = sessionFlask['username']

            # Buscar el conjunto de usuarios correspondiente
            for login_info in data.get('login', []):
                if login_info.get('session') and login_info['session'][0].get(login_actual):
                    for servidor in login_info.get('servidores', []):
                        if servidor.get('activo') == "1":
                            return servidor.get('usuarios', [])

            # Si no se encuentra el login actual con servidor activo, devolver una lista vacía
            return {}
    except FileNotFoundError:
        return {}
    
#para cuando se necesita buscar todos los usuarios de todos los clientes a la hora de dar de baja expirados
def cargar_usuarios():
    try:        
        with open(USUARIOS_JSON) as fil:
            data = json.load(fil)

            # Obtener todos los usuarios de todos los conjuntos
            todos_los_usuarios = []
            for login_info in data.get('login', []):
                servidores = login_info.get('servidores', [])
                for servidor in servidores:
                    usuarios_servidor = servidor.get('usuarios', [])
                    todos_los_usuarios.extend(usuarios_servidor)

            return todos_los_usuarios
    except FileNotFoundError:
        return []
    
def cargarSessionJson():
    try:
        with open(USUARIOS_JSON, 'r') as sessionJson:
            data = json.load(sessionJson)

        sesiones_de_login = []

        for login_session in data.get('login', []):
            sesiones_de_login.extend(login_session.get('session', []))

        return sesiones_de_login

    except FileNotFoundError:
        print(f'Error: El archivo {USUARIOS_JSON} no fue encontrado.')
        return None
    except json.JSONDecodeError:
        print(f'Error: No se pudo decodificar el contenido JSON en {USUARIOS_JSON}.')
        return None
    
def guardar_usuarios(usuarios):
    try:
        file_path = os.path.join(os.getcwd(), USUARIOS_JSON)
        print(os.path.exists(file_path))
        print(os.stat(file_path))

        with open(USUARIOS_JSON) as fi:
            # Agrega esta línea para imprimir el contenido del archivo
            data = json.load(fi)

            # Obtener el nombre del login actual desde la sesión
            login_actual = sessionFlask['username']

            # Buscar el conjunto de usuarios correspondiente
            for login_info in data.get('login', []):
                if login_info.get('session') and login_info['session'][0].get(login_actual):
                    # Buscar el servidor activo
                    servidor_activo = next((server for server in login_info['servidores'] if server['activo'] == "1"), None)

                    if servidor_activo:
                        # Agregar usuarios al servidor activo
                        servidor_activo['usuarios'] = usuarios

                        # Guardar los cambios en el archivo JSON
                        with open(USUARIOS_JSON, "w") as write_file:
                            json.dump(data, write_file, indent=2)
                    else:
                        print("No hay servidor activo para el usuario.")
                    break
    except FileNotFoundError as e:
        print(f"Error al abrir el archivo: {e}")
        # Manejar el caso cuando el archivo no existe
        # Aquí podrías crear un nuevo archivo con la estructura adecuada
        pass

def crear_cuenta_plex(username, duration,pantallas):
    try:
        contrasena = generar_contrasena_aleatoria()
        url = 'https://plex.tv/api/v2/users'
        identificador_cliente = str(uuid.uuid4())

        payload = {
            'username': username,
            'email': username,
            'password': contrasena,
            'pantallas': pantallas
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Plex-Client-Identifier': identificador_cliente  

        }

        response = requests.post(url, json=payload, headers=headers)
        # Verifica si la solicitud fue exitosa (código de respuesta 201)
        if response.status_code == 201:
            # Verifica si la solicitud fue exitosa (código de respuesta 201)
            # Simulación: Actualiza el archivo JSON con la información de la cuenta
            usuarios = cargar_usuarios_session()
            nueva_cuenta = {"email": username, "contrasena": contrasena, "expiracion": (datetime.now() + timedelta(days=30*int(duration))).strftime("%d/%m/%Y"),"pantallas":pantallas,"codigoColor":"0","telegram":"-","discord":"-","whatsapp":"-"}
            usuarios.append(nueva_cuenta)
            guardar_usuarios(usuarios)
            return True
        elif response.status_code == 422:
            flash(f"La cuenta con el correo electronico {username} ya existe en Plex.", 'error')
            return False
        else:
            print(f"Error al crear usuario. Codigo de respuesta: {response.status_code}")
            print(f"Contenido de la respuesta: {response.text}")
            return False

    except Exception as e:
        message = f"Error al crear cuenta plex en el metodo 'crear_cuenta_plex' [revisar url y api plex]: {e}"
        escribir_log_error(message)
        flash(f"Error al crear la cuenta PLEX, revisa tu token y url de tu servidor plex", 'error')
        return False

@app.route('/index')
def index():
    # Verificar si el usuario ha iniciado sesión
    if 'username' in sessionFlask:
        proviene_de_modificar = request.args.get('proviene_de_modificar', False)
        current_user =sessionFlask["username"]
        servidores = obtener_servidores(current_user)
        # Verificar si el usuario tiene servidores
        if not servidores:
            # Si no tiene servidores, puedes redirigirlo a otra página o renderizar una plantilla diferente
            return render_template('sin_servidores.html', current_user=current_user,servidores=servidores)
        
        return render_template('index.html',proviene_de_modificar=proviene_de_modificar,current_user=current_user,servidores=servidores)
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))
    
def obtener_servidores(nombre_usuario):
    # Lee el contenido del archivo JSON
    with open('usuarios.json', 'r') as servidoresJson:
        data = json.load(servidoresJson)

    # Busca la entrada correspondiente al nombre de usuario
    for entry in data.get('login', []):
        if entry.get('session', [])[0].get(nombre_usuario):
            # Retorna la lista de servidores asociados a ese usuario
            return entry.get('servidores', [])

    # Si no se encuentra el usuario, retorna una lista vacía
    return []

@app.route('/crear_cuenta', methods=['POST'])
def crear_cuenta():
    if 'username' in sessionFlask:
        username = request.form.get('username')
        duration = request.form.get('duration')
        pantallas = request.form.get('pantallas')
        

        if crear_cuenta_plex(username, duration,pantallas):
            return redirect(url_for('lista_usuarios'))

        return redirect(url_for('index'))
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/lista_usuarios',methods=['GET'])
def lista_usuarios():
    if 'username' in sessionFlask:
        proviene_de_modificar = request.args.get('proviene_de_modificar', False)
        usuarios = cargar_usuarios_session()
        servidores = obtener_servidores(sessionFlask['username'])
        return render_template('lista_usuarios.html', usuarios=[{"email": usuario["email"], "contrasena": usuario["contrasena"], "expiracion": usuario["expiracion"],"pantallas": usuario["pantallas"],"codigoColor": usuario["codigoColor"]} for usuario in usuarios],proviene_de_modificar=proviene_de_modificar,current_user=sessionFlask["username"],servidores=servidores)
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/eliminar_cuenta/<email>', methods=['POST'])
def eliminar_cuenta(email):
    if 'username' in sessionFlask:
        eliminar_acceso_biblioteca_route(email,False)
        usuarios = cargar_usuarios_session()
        usuarios = [usuario for usuario in usuarios if usuario["email"] != email]
        guardar_usuarios(usuarios)
        print(f"Se ha eliminado el usuario {email}.")

        return redirect(url_for('lista_usuarios'))
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/modificar_expiracion/<email>')
def modificar_expiracion(email):
    datos = cargar_usuarios_session()

    if 'username' in sessionFlask:
        # Buscar el usuario correspondiente en tus datos
        usuario = None
        for user in datos:
            if user["email"] == email:
                usuario = user
                break            

        if usuario:
            return render_template('modificar.html', email=email, usuario=usuario)
        else:
            # Manejar el caso en que no se encuentre el usuario
            return render_template('modificar.html',email=email)
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/procesar_modificacion/<email>', methods=['POST','GET'])
def procesar_modificacion(email):
    if 'username' in sessionFlask:
        # Obtén los datos del formulario
        numero_pantallas = int(request.form.get('numero_pantallas'))
        whatsapp = request.form.get('whatsapp')
        discord = request.form.get('discord')
        telegram = request.form.get('telegram')
        

        # Cargar datos actuales desde usuarios.json
        usuarios = cargar_usuarios_session()

        # Buscar el usuario por email
        usuario_modificar = next((usuario for usuario in usuarios if usuario["email"] == email), None)

        if usuario_modificar:
            # Actualizar número de pantallas y expiración
            usuario_modificar["pantallas"] = str(numero_pantallas)
            
            # Obtener la fecha actual y sumarle el número de meses
            if request.form.get('expiracion') != None:
                expiracion = int(request.form.get('expiracion'))
                fecha_expiracion_actual = datetime.strptime(usuario_modificar["expiracion"], "%d/%m/%Y")
                nueva_expiracion = fecha_expiracion_actual + timedelta(days=30 * expiracion)
                usuario_modificar["expiracion"] = nueva_expiracion.strftime("%d/%m/%Y")
                if not usuario_modificar["codigoColor"] == "1":
                    usuario_modificar["codigoColor"] = "0"
                
            if whatsapp == '' or whatsapp == None:
                usuario_modificar['whatsapp'] = "-"
            else:
                usuario_modificar['whatsapp'] = whatsapp

            if discord == '' or discord == None:
                usuario_modificar['discord'] = "-"
            else:
                    usuario_modificar['discord'] = discord
            if telegram == '' or telegram == None:
                usuario_modificar['telegram'] = "-"
            else:
                usuario_modificar['telegram'] = telegram

            # Guardar los cambios en usuarios.json
            guardar_usuarios(usuarios)

            flash(f"Modificacion exitosa para el usuario {email}", 'success')
        else:
            flash(f"No se encontro el usuario con el correo {email}", 'error')

        return redirect(url_for('lista_usuarios',proviene_de_modificar=True))
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/conceder_acceso_biblioteca/<email>', methods=['POST'])
def conceder_acceso_biblioteca_route(email):
    if 'username' in sessionFlask:
        return conceder_acceso_biblioteca(email)
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/eliminar_acceso_biblioteca/<email>', methods=['POST'])
def eliminar_acceso_biblioteca_route(email,automatico=False):
    try:
        sess = requests.Session()
        # Ignore verifying the SSL certificate
        sess.verify = False  # '/path/to/certfile'
        # If verify is set to a path to a directory,
        # the directory must have been processed using the c_rehash utility supplied
        # with OpenSSL.
        if sess.verify is False:
            # Disable the warning that the request is insecure, we know that...
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Deshabilitar la advertencia sobre certificados SSL no seguros
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Crear una sesión y deshabilitar la verificación del certificado SSL
        session = requests.Session()
        session.verify = False

        # Conectar al servidor Plex
        plex = PlexServer(devolverApiPlexSession("urlPlex"), devolverApiPlexSession("apiPlex"), session=session)

        # Obtener la cuenta de MyPlex
        account = plex.myPlexAccount()

        # Buscar al usuario por su correo electrónico
        friend = next((friend for friend in account.users() if friend.email == email), None)
        if friend:
            account.removeFriend(friend)

            # Cargar datos actuales desde usuarios.json
            usuarios = cargar_usuarios()

            # Buscar el usuario por email
            usuario_modificar = next((usuario for usuario in usuarios if usuario["email"] == email), None)

            if usuario_modificar:
                usuario_modificar["codigoColor"] = "2"

                # Guardar los cambios en usuarios.json
                guardar_usuarios(usuarios)
            if not automatico:
                print(f"Se ha revocado el acceso para el usuario {email}.")
        else:
            if not automatico:
                flash(f"El correo {email} no ha aceptado aun la invitacion o no ha sido invitado", 'error')
        if not automatico:
            return redirect(url_for('lista_usuarios'))
    except Exception as e:
        message = f"Error al eliminar invitacion en el metodo 'eliminar_acceso_biblioteca' sobre el usuario {email} [revisar url y api plex]: {e}"
        escribir_log_error(message)
        flash(f"Error al eliminar invitacion, revisar token y url de tu servidor plex", 'error')
        return redirect(url_for('lista_usuarios'))
        
def eliminar_acceso_biblioteca_route_global(email,automatico=False):
    try:
        sess = requests.Session()
        # Ignore verifying the SSL certificate
        sess.verify = False  # '/path/to/certfile'
        # If verify is set to a path to a directory,
        # the directory must have been processed using the c_rehash utility supplied
        # with OpenSSL.
        if sess.verify is False:
            # Disable the warning that the request is insecure, we know that...
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Deshabilitar la advertencia sobre certificados SSL no seguros
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Crear una sesión y deshabilitar la verificación del certificado SSL
        session = requests.Session()
        session.verify = False

        # Cargar datos actuales desde usuarios.json
        with open(USUARIOS_JSON, 'r') as eliminarGlobal:
            data = json.load(eliminarGlobal)

        # Buscar el usuario por email
        usuario_modificar = next((usuario for login_info in data['login'] for server in login_info.get('servidores', []) for usuario in server.get('usuarios', []) if usuario['email'] == email), None)

        if usuario_modificar:
            servidor_usuario = next((server for login_info in data['login'] for server in login_info.get('servidores', []) if any(usuario['email'] == email for usuario in server.get('usuarios', []))), None)

            # Obtener la URL de Plex y la API de Plex del usuario
            url_plex = servidor_usuario.get('urlPlex', '')
            api_plex = servidor_usuario.get('apiPlex', '')

            # Conectar al servidor Plex con los nuevos datos
            plex = PlexServer(url_plex, api_plex, session=session)

            # Obtener la cuenta de MyPlex
            account = plex.myPlexAccount()

            # Buscar al usuario por su correo electrónico
            friend = next((friend for friend in account.users() if friend.email == email), None)

            if friend:
                account.removeFriend(friend)

                # Aquí puedes realizar las operaciones que necesites en el servidor Plex
                # (por ejemplo, eliminar contenido, etc.)

                # Modificar el usuario en usuarios.json
                usuario_modificar["codigoColor"] = "2"

                # Guardar los cambios en usuarios.json
                guardar_usuarios(data)

                if not automatico:
                    print(f"Se ha revocado el acceso para el usuario {email} en el servidor activo.")
            else:
                if not automatico:
                    flash(f"El correo {email} no ha aceptado aun la invitacion o no ha sido invitado", 'error')
        else:
            if not automatico:
                flash(f"No hay servidor activo para el usuario {email}.", 'error')

        if not automatico:
            return redirect(url_for('lista_usuarios'))
    except Exception as e:
        message = f"Error al eliminar invitacion en el metodo 'eliminar_acceso_biblioteca_route_global' sobre el usuario {email} [revisar url y api plex]: {e}"
        escribir_log_error(message)

def detener_sesiones_excedentes_global():
    try:
        # Cargar datos actuales desde usuarios.json
        with open(USUARIOS_JSON, 'r') as detenerSesiones:
            data = json.load(detenerSesiones)

        for login_info in data.get('login', []):
            for servidor in login_info.get('servidores', []):
                for usuario in servidor.get('usuarios', []):
                    # Obtener la URL de Plex y la API de Plex del usuario
                    url_plex = servidor.get('urlPlex', '')
                    api_plex = servidor.get('apiPlex', '')

                    # Crear el objeto PlexServer
                    plex_server = PlexServer(url_plex, api_plex)

                    # Realizar las acciones necesarias, por ejemplo:
                    detener_reproductor_si_es_necesario(usuario["email"], plex_server)
    except Exception as e:
        message = f"Error al detener la sesion del usuario {usuario['email']} 'detener_sesiones_excedentes_global' [revisar url y api plex]: {e}"
        escribir_log_error(message)

# Función para ejecutar la aplicación Flask
def run_flask_app():
    run_simple('0.0.0.0', 8096, app, use_reloader=False)

# Método para eliminar acceso si la fecha de expiración ha pasado
def revisar_fechas_expiracion():
    # Obtener la lista de usuarios (cámbialo según tu implementación)
    usuarios = cargar_usuarios()

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Iterar sobre los usuarios y eliminar acceso si la fecha ha pasado
    for usuario in usuarios:
        fecha_expiracion = datetime.strptime(usuario["expiracion"], "%d/%m/%Y")
        if fecha_expiracion <= fecha_actual:
            eliminar_acceso_biblioteca_route_global(usuario["email"],True)

@app.route('/generar_demo', methods=['POST'])
def generar_demo():
    if 'username' in sessionFlask:
        username = request.form.get('demo_username')
        #0.06 es 1h y media
        
        if crear_cuenta_plex(username,0.06,1):
            conceder_acceso_biblioteca(username)
            # Programar la eliminación del usuario después de 1 hora y media
            schedule.every(1).hour.at(":30").do(eliminar_cuenta_demo, username)
            return redirect(url_for('lista_usuarios'))

        return redirect(url_for('index'))
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

def eliminar_cuenta_demo(email):
    schedule.every(1).hour.at(":30").do(eliminar_cuenta_demo_retardo,email)

def eliminar_cuenta_demo_retardo(email):
    
    eliminar_acceso_biblioteca_route(email,True)
    usuarios = cargar_usuarios()
    usuarios = [usuario for usuario in usuarios if usuario["email"] != email]
    guardar_usuarios(usuarios)
    print(f"Se ha eliminado el usuario {email}.")

@app.route('/usuarios_proximos_expirar')
def usuarios_proximos_expirar():
    if 'username' in sessionFlask:
        usuarios = cargar_usuarios_session()

        # Lista para almacenar usuarios próximos a expirar
        usuarios_proximos_expirar = []

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Calcular la fecha límite (2 días desde la fecha actual)
        fecha_limite = fecha_actual + timedelta(days=2)
        servidores = obtener_servidores(sessionFlask['username'])

        # Filtrar usuarios cuya fecha de expiración esté a 2 días de caducar
        for usuario in usuarios:
            expiracion_str = usuario.get('expiracion', '')
            
            # Convertir la cadena de expiración a un objeto datetime
            expiracion = datetime.strptime(expiracion_str, '%d/%m/%Y')
            
            # Calcular la diferencia de días
            dias_restantes = abs((fecha_actual - expiracion).days)
            
            if fecha_actual < expiracion <= fecha_limite:
                usuarios_proximos_expirar.append(usuario)
        return render_template('alertas.html', usuarios_proximos=usuarios_proximos_expirar,current_user=sessionFlask["username"],servidores=servidores)
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/modificar_contacto/<email>',methods=['POST'])
def modificar_contacto(email):
    if 'username' in sessionFlask:
        return render_template('modificar_contacto.html', email=email)
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/guardar_modificacion_contacto/<email>', methods=['POST'])
def guardar_modificacion_contacto(email):
    if 'username' in sessionFlask:
        # Obtén los nuevos valores de Telegram, WhatsApp y Discord del formulario
        nuevo_telegram = request.form.get('telegram')
        nuevo_whatsapp = request.form.get('whatsapp')
        nuevo_discord = request.form.get('discord')

        usuarios = cargar_usuarios_session()
        # Encuentra el usuario por su correo electrónico
        usuario = next((user for user in usuarios if user['email'] == email), None)

        if usuario:
            if nuevo_telegram == '':
                nuevo_telegram = ' - '
            if nuevo_whatsapp == '':
                nuevo_whatsapp = ' - '
            if nuevo_discord == '':
                nuevo_discord = ' - '
            # Actualiza los campos del usuario con los nuevos valores
            usuario['telegram'] = nuevo_telegram
            usuario['whatsapp'] = nuevo_whatsapp
            usuario['discord'] = nuevo_discord

            # Guardar usuarios actualizados en el archivo JSON
            guardar_usuarios(usuarios)

        # Redirige a la página de lista de usuarios o a donde desees después de guardar los cambios
        return redirect('/usuarios_proximos_expirar')
    else:
        # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
        return redirect(url_for('login'))

@app.route('/lista_biblioteca',methods=['GET'])
def lista_biblioteca():
    try:
        if 'username' in sessionFlask:
            sess = requests.Session()
            # Ignore verifying the SSL certificate
            sess.verify = False  # '/path/to/certfile'
            # If verify is set to a path to a directory,
            # the directory must have been processed using the c_rehash utility supplied
            # with OpenSSL.
            if sess.verify is False:
                # Disable the warning that the request is insecure, we know that...
                import urllib3

                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            plex = PlexServer(devolverApiPlexSession("urlPlex"), devolverApiPlexSession("apiPlex"), session=sess)

            sections_lst = [x.title for x in plex.library.sections()]

            servidores = obtener_servidores(sessionFlask['username'])
            return render_template('lista_bibliotecas.html',bibliotecas=sections_lst,current_user=sessionFlask["username"],servidores=servidores)
        else:
            # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
            return redirect(url_for('login'))
    except Exception as e:
        message = f"Error al mostrar la lista de bibliotecas en el metodo 'lista_biblioteca' [revisar url y api plex]: {e}"
        escribir_log_error(message)
        flash(f"Ha ocurrido un error en la lista de biblioteca, revisa los token y url de tu servidor plex", 'error')
        return redirect(url_for('index'))
        

@app.route('/eliminar_biblioteca/<biblioteca>', methods=['POST'])
def eliminar_biblioteca(biblioteca):
    try:
        if 'username' in sessionFlask:
            # Conectarse a Plex
            sess = requests.Session()
            sess.verify = False  # Ignorar la verificación del certificado SSL

            if sess.verify is False:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            plex = PlexServer(devolverApiPlexSession("urlPlex"), devolverApiPlexSession("apiPlex"), session=sess)

            # Encontrar la sección de la biblioteca por título
            library_section = next((section for section in plex.library.sections() if section.title == biblioteca), None)

            if library_section:
                # Eliminar la sección de la biblioteca
                library_section.delete()
                print(f'Se ha eliminado la biblioteca "{biblioteca}" exitosamente.')
            else:
                print(f'Error: No se encontro la biblioteca con el titulo "{biblioteca}".')

            # Redirigir o renderizar la plantilla actualizada
            return redirect(url_for('lista_biblioteca'))
        else:
            # Si no ha iniciado sesión, redirigir a la pantalla de inicio de sesión
            return redirect(url_for('login'))
    except Exception as e:
        message = f"Error al eliminar la biblioteca en el metodo 'eliminar_biblioteca' [revisar url y api plex]: {e}"
        escribir_log_error(message)
        flash(f"No se ha eliminado la biblioteca, revise su token o url de su servidor plex", 'error')
        return redirect(url_for('lista_biblioteca'))

def check_credentials(username, password):
    # Leer el archivo JSON de usuarios
    with open(USUARIOS_JSON) as f:
        data = json.load(f)

    # Verificar si el usuario y la contraseña coinciden en cualquier sesión
    for login_info in data.get('login', []):
        for session in login_info.get('session', []):
            if session.get(username) and session[username] == password:
                return True

    return False

@app.route('/')
def login():
    return render_template('login.html')

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['POST'])
def login_post():
    try:
        username = request.form['username']
        password = request.form['password']

        # Verificar las credenciales en el archivo JSON
        if check_credentials(username, password):
            # Inicio de sesión exitoso, almacenar el usuario en la sesión
            sessionFlask['username'] = username
            return redirect(url_for('index'))
        else:
            # Inicio de sesión fallido, regresar a la pantalla de inicio de sesión
            return redirect(url_for('login'))
    except Exception as e:
        # Imprime detalles del error
        print(f"Error en /login: {str(e)}")
        return "Error interno del servidor", 500
    
# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar el usuario de la sesión al cerrar sesión
    sessionFlask.pop('username', None)
    return redirect(url_for('login'))

@app.route('/lista_servidores')
def lista_servidores():
    # Lee el archivo usuarios.json y lo convierte en un diccionario Python
    with open('usuarios.json', 'r') as file:
        usuarios_data = json.load(file)

    # Implementa la lógica para obtener los servidores del usuario conectado (aquí, se usa un usuario de ejemplo)
    user_key = sessionFlask["username"]
    user_servers = []
    for login_data in usuarios_data['login']:
        for session_data in login_data['session']:
            if user_key in session_data:
                # Utilizamos la referencia al usuario actual
                user_servers.extend(login_data['servidores'])
                
    return render_template('lista_servidores.html', user_servers=user_servers)


# Ruta para mostrar el formulario de añadir nuevo servidor
@app.route('/nuevo_servidor')
def nuevo_servidor():
    return render_template('nuevo_servidor.html')

# Ruta para manejar la adición de un nuevo servidor
@app.route('/agregar_servidor', methods=['POST'])
def agregar_servidor():
    # Lee el archivo usuarios.json y lo convierte en un diccionario Python
    with open('usuarios.json', 'r') as file:
        usuarios_data = json.load(file)

    # Implementa la lógica para agregar un nuevo servidor al usuario conectado
    user_key = sessionFlask["username"]

    for login_data in usuarios_data['login']:
        for session_data in login_data['session']:
            if user_key in session_data:
                nuevo_servidor = {
                    'nombre_server':request.form.get('nombre_server'),
                    'activo':'0',
                    'urlPlex': request.form.get('urlPlex'),
                    'apiPlex': request.form.get('tokenPlex'),
                    'urlTautulli': request.form.get('urlTautulli'),
                    'apiTautulli': request.form.get('tokenTautulli'),
                    'usuarios':[]
                }

                # Agrega el nuevo servidor a la lista de servidores del usuario
                login_data['servidores'].append(nuevo_servidor)

                # Guarda los cambios en el archivo usuarios.json
                with open('usuarios.json', 'w') as file:
                    json.dump(usuarios_data, file, indent=2)

                return jsonify({'success': True})

    return jsonify({'success': False})

@app.route('/modificar_servidor/<nombre_servidor>', methods=['POST'])
def modificar_servidor(nombre_servidor):
    return render_template('configurar_servidor.html', servidor=obtener_servidor_por_nombre(nombre_servidor))

@app.route('/guardar_servidor/<nombre_servidor>', methods=['POST'])
def guardar_servidor(nombre_servidor):
    servidor = obtener_servidor_por_nombre(nombre_servidor)

    # Si se envía el formulario, actualiza los campos con los nuevos valores
    servidor['urlPlex'] = request.form.get('urlPlex')
    servidor['apiPlex'] = request.form.get('tokenPlex')
    servidor['urlTautulli'] = request.form.get('urlTautulli')
    servidor['apiTautulli'] = request.form.get('tokenTautulli')
    if request.form.get('nombre_server') != '':
        servidor['nombre_server'] = request.form.get('nombre_server')
    else:
        servidor['nombre_server'] = nombre_servidor
    # Guarda el servidor actualizado en tu JSON o base de datos
    guardar_servidor_actualizado(servidor,nombre_servidor)

    # Redirige a la lista de servidores después de la modificación
    return redirect(url_for('lista_servidores'))

def obtener_servidor_por_nombre(nombre_servidor):
    # Debes implementar la lógica para obtener el servidor por nombre desde tu JSON o base de datos
    # Este es solo un ejemplo, puedes tener una función que busque en tu estructura de datos
    # y devuelva el servidor correspondiente
    # Iterar sobre los usuarios y sus servidores
    with open(USUARIOS_JSON) as serversJson:
        usuarios_data = json.load(serversJson)

    for usuario in usuarios_data['login']:
        for server in usuario['servidores']:
            if server.get('nombre_server') == nombre_servidor:
                return server
    
    # Si no se encuentra el servidor, puedes devolver None o lanzar una excepción según tus necesidades
    return None

def guardar_servidor_actualizado(servidor_actualizado,nombre_servidor):
    # Debes implementar la lógica para guardar el servidor actualizado en tu JSON o base de datos
    # Este es solo un ejemplo, puedes tener una función que actualice tu estructura de datos
    with open(USUARIOS_JSON) as guardarServerJson:
        usuarios_data = json.load(guardarServerJson)
    for index, server in enumerate(usuarios_data['login'][0]['servidores']):
        if server['nombre_server'] == nombre_servidor:
            usuarios_data['login'][0]['servidores'][index] = servidor_actualizado
            break
    # Después de actualizar, guarda el JSON actualizado
    with open('usuarios.json', 'w') as file:
        json.dump(usuarios_data, file, indent=4)

def devolverApiPlexSession(solicitud):
    # Cargar datos actuales desde usuarios.json
    with open(USUARIOS_JSON, 'r') as devolverApiPlexSession:
        data = json.load(devolverApiPlexSession)

    username = sessionFlask.get('username')

    for login_info in data["login"]:
        for session_info in login_info["session"]:
            if username in session_info:
                # Encontrar el servidor activo para el usuario logueado
                for servidor_info in login_info["servidores"]:
                    if servidor_info["activo"] == "1":
                        if solicitud == "apiPlex":
                            return servidor_info["apiPlex"]
                        elif solicitud == "urlPlex":
                            return servidor_info["urlPlex"]
                        elif solicitud == "apiTautulli":
                            return servidor_info["apiTautulli"]
                        elif solicitud == "urlTautulli":
                            return servidor_info["urlTautulli"]

    # Retornar None si no se encuentra el usuario logueado o no hay servidor activo
    return None

@app.route('/eliminar_servidor/<nombre_servidor>', methods=['POST'])
def eliminar_servidor(nombre_servidor):

    with open(USUARIOS_JSON, 'r') as eliminarJsonServer:
        usuarios_data = json.load(eliminarJsonServer)

    for usuario in usuarios_data['login']:
        for servidor in usuario['servidores']:
            if servidor['nombre_server'] == nombre_servidor:
                usuario['servidores'].remove(servidor)
                guardar_datos_usuarios(usuarios_data)  # Implementa la función guardar_datos_usuarios() según tus necesidades.

    # Después de eliminar el servidor, redirecciona a la página de lista de servidores.
    return redirect('/lista_servidores')

def guardar_datos_usuarios(usuarios_data):
    with open('usuarios.json', 'w') as file:
        json.dump(usuarios_data, file, indent=4)

@app.route('/conectar/<nombre_servidor>', methods=['POST'])
def conectar(nombre_servidor):
    # Cargar el archivo JSON
    with open('usuarios.json') as conectarServer:
        data = json.load(conectarServer)

    # Obtener el nombre del usuario actual desde la sesión
    login_actual = sessionFlask['username']

    # Buscar el usuario actual en la lista de usuarios
    usuario_actual = next((usuario for usuario in data['login'] if usuario['session'][0].get(login_actual)), None)

    # Verificar si el usuario tiene algún servidor activo
    tiene_servidor_activo = any(server['activo'] == "1" for server in usuario_actual['servidores'])

    # Buscar el servidor por nombre
    for server in usuario_actual['servidores']:
        if server['nombre_server'] == nombre_servidor and server['activo'] == "0":
            # Desactivar cualquier otro servidor activo del mismo usuario
            for otro_server in usuario_actual['servidores']:
                if otro_server['activo'] == "1":
                    otro_server['activo'] = "0"

            # Activar el estado del servidor actual y guardar el JSON
            server['activo'] = "1"
            with open('usuarios.json', 'w') as actualizaServer:
                json.dump(data, actualizaServer, indent=4)

            flash(f"Conectado con exito", 'success')
            return redirect('/lista_servidores')
        elif server['nombre_server'] == nombre_servidor and server['activo'] == "1" and tiene_servidor_activo:
            flash(f"Este servidor ya esta conectado", 'error')

    return redirect('/lista_servidores')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/crear_usuario_admin', methods=['POST'])
def crear_usuario_admin():
    if request.method == 'POST':
        nombre_usuario = request.form['nombreUsuario']
        password = request.form['password']
        user_password = request.form['userPassword']

        # Verificar la contraseña antes de permitir la creación del usuario
        if password == "panelPlex":
           # Obtener los datos actuales del JSON
            with open('usuarios.json', 'r') as crearAdmin:
                data = json.load(crearAdmin)

            # Asegurarse de que la lista 'login' tenga al menos un elemento
            login_data = data.setdefault('login', [])
            existing_user = next((user for user in login_data if user.get('session') and nombre_usuario in user['session'][0]), None)
            if not existing_user:
                # Añadir la nueva sesión al usuario
                new_user = {"session": [{nombre_usuario: user_password}], "servidores": []}
                login_data.append(new_user)

                # Guardar los datos actualizados en el JSON
                with open('usuarios.json', 'w') as file:
                    json.dump(data, file, indent=2)

                # Flash message para indicar que el usuario se ha creado exitosamente
                flash(f'Usuario "{nombre_usuario}" creado exitosamente.', 'success')

                # Después de realizar las acciones, puedes redirigir a una página o realizar otras operaciones según tus necesidades.
                return redirect(url_for('admin'))
            else:
                # Flash message para indicar que el nombre de usuario ya existe
                flash(f'El nombre de usuario "{nombre_usuario}" ya existe. Por favor, elige otro.', 'error')
        else:
            flash(f"Contrasena incorrecta", 'error')
            return redirect(url_for('admin'))

def escribir_log_error(error_message):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    usuarioSession = ""
    try:
        usuarioSession = sessionFlask['username']
    except:
        usuarioSession = "GLOBAL"
    
    log_entry = f"{timestamp} - {usuarioSession} - {error_message}\n-----------------------------------------------------\n"

    with open("logs.txt", "a") as log_file:
        log_file.write(log_entry)



if __name__ == '__main__':
    #Habria que hacer un metodo de eliminacion global tambien, que lo que haga es buscar a que servidor pertenece el usuario para coger su api y demas para poder eliminar sin iniciar session
    revisar_fechas_expiracion()
    # Programar la verificación y detención de sesiones cada 5 minutos
    schedule.every(1).minutes.do(detener_sesiones_excedentes_global)
    schedule.every().day.at("00:00").do(revisar_fechas_expiracion)

    # Crear un hilo para ejecutar la aplicación Flask
    flask_thread = threading.Thread(target=run_flask_app)

    # Iniciar la ejecución de la aplicación Flask en un hilo
    flask_thread.start()

    # Ejecutar el bucle principal de schedule en el hilo principal
    while True:
        schedule.run_pending()
        time.sleep(1)
    