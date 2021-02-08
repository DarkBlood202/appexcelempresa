# Configuracion inicial para el servidor de correo
Cambiar las credenciales del correo en "settings.py"
	EMAIL_HOST_USER = ""
	EMAIL_HOST_PASSWORD = ""
Estas serán las credenciales del remitente de las hojas de liquidación.
Para que el correo funcione tiene que habilitar una opción de google,
primer resultado de buscar: "google less secure apps" en google
te ubicas en la carpeta que contenga el archivo manage.py y corres los siguientes comandos:

# Instalamos requerimientos
pip install -r requirements.txt

# Creamos migraciones
python manage.py makemigrations 

# Migramos
python manage.py migrate   

# Crearemos las credenciales del super usuario (usuario, correo, contraseña)
python manage.py createsuperuser

# Cargamos archivos estáticos a la aplicación
python manage.py collectstatic

# Corremos servidor local
python manage.py runserver   

Importar excel:
	1. Ingresar al localhost/admin e ingresar credenciales del superusuario
	2. Seleccionar el elemento al que se desea cargar la data
	3. En la zona superior, hacer click en el botón ("Importar").
	4. Subir el archivo excel (.xlsx) con los datos requeridos (no olvidar hacer click en "Subir archivo")

Ver data importada:
	1. Ingresar al localhost/admin e ingresar credenciales del superusuario
	2. Ingresar al elemento deseado (repartidores, restaurantes, pedidos, envios)
	3. En acciones ("Actions") se podrá descargar así como también enviar hoja 
	de liquidación seleccionando un restaurante o repartidor

Ajustar intervalo de fechas (se verá reflejado en las hojas de liquidación):
	1. Ingresar al localhost/admin e ingresar credenciales del superusuario
	2. Seleccionar "repartidor" o "restaurante"
	3. En la zona superior, hacer click en el botón ("Definir fechas")
	4. Introduce la fecha de inicio y de fin del periodo deseado en formato (dd/mm/yyyy)

IMPORTANTE:
La hoja de cálculo compartida le hemos tenido que realizar modificaciones para que Python pueda leerlo sin problemas (sucede que python no puede identificar fórmulas, tuvimos que convertir todos los valores a estáticos para que pueda ser importado correctamente). 
He adjuntado la hoja de cálculo de ejemplo que te permite importar los datos correctamente llamado "PlantillaExcel" (ahora subdividido en 4 plantillas, 1 por cada hoja)

Sobre las tecnologías usadas están detalladas en requirements.txt:
Django 3.1. (framework python)
Python 3.9 (lenguaje backend)
SQLite3 (base de datos SQL)
SMPT (envío de correos)
¿Porqué Django? Te adjunto un pequeño tutorial con todos los beneficios:
https://devcode.la/blog/por-que-usar-django/

	
	
