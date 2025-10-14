# Usa la imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido local a la imagen en /app
COPY . /app

# Instala las dependencias necesarias
RUN pip install -r requirements.txt

# Expone el puerto 5000 para que puedas acceder a tu aplicación Flask
EXPOSE 5000

# Comando para ejecutar tu aplicación cuando el contenedor se inicie
CMD ["python", "tu_app.py"]