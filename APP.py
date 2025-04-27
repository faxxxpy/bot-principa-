from config_token import * 


import telebot
from telebot import types
from telebot.types import ForceReply
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import InputMediaPhoto

import os,json,requests,time
from datetime import datetime
from bs4 import BeautifulSoup 
import base64

from PIL import Image, ImageDraw, ImageFont 
from reportlab.pdfgen import canvas 
#from DNI_VIRTUAL.generador_dni import consulta_dni_virtual
import random
from datetime import timedelta
import datetime as dt
import pandas as pd
import re














funders1 = [8169632301]



bot = telebot.TeleBot(TELEGRAM_TOKEN)




dueño = [8169632301]
def cargar_datos_desde_json():
    try:
        with open('./BAN_TOTAL/ids.json', 'r') as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError:
        return {}  # Devuelve un diccionario vacío si el archivo no existe

def guardar_ids_en_json(ids):
    with open('./BAN_TOTAL/ids.json', 'w') as archivo_json:
        json.dump(ids, archivo_json)

@bot.message_handler(commands=["quix"])
def cmd_cred(message):
    user_id = message.from_user.id
    hfirst_name = message.from_user.first_name
    args = message.text.split()

    # Verificar si el usuario tiene permiso para otorgar créditos
    if user_id not in dueño:
        bot.reply_to(message, "❰👺❱ Parece que no tienes permisos para realizar baneos en este lugar. Por favor, ponte en contacto con el administrador del grupo para obtener ayuda adicional.")
        return

    # Verificar si se respondió a un mensaje y obtener el ID del usuario mencionado
    if message.reply_to_message and message.reply_to_message.from_user:
        recipient_id = message.reply_to_message.from_user.id
        recipient_name = message.reply_to_message.from_user.first_name

        # Cargar todos los IDs desde el archivo JSON
        datos_ids = cargar_datos_desde_json()

        # Verificar si el ID del destinatario ya está en los datos cargados desde el archivo JSON
        if str(recipient_id) not in datos_ids:
            # Agregar el nuevo ID al diccionario
            datos_ids[str(recipient_id)] = True

            # Guardar todos los IDs en el archivo JSON
            guardar_ids_en_json(datos_ids)

            print(f"ID '{recipient_id}' guardado en el archivo JSON.")
            bot.reply_to(message, f"🌟 𝗘𝘀𝘁𝗶𝗺𝗮𝗱𝗼 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿:\n\n❰👺❱ El usuario con ID {recipient_id} ha sido baneado.\n❰👺❱ Nombre del destinatario → <code>{recipient_name}</code>\n\nPor favor, asegúrate de que el baneo sea justificado y sigue las políticas del grupo. Si necesitas más detalles o asistencia adicional, no dudes en contactar con el equipo de soporte.", parse_mode="html")
        else:
            bot.reply_to(message, f"🌟 𝗘𝘀𝘁𝗶𝗺𝗮𝗱𝗼 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿:\n\n❰👺❱ EL USUARIO YA ESTÁ BANEADO\n", parse_mode="html")
    else:
        bot.reply_to(message, "[❗️] Debes responder a un mensaje de usuario para Banearle.")
     # Función para cargar los datos desde el archivo JSON
def cargar_datos_desde_jsonv1():
    try:
        with open('./BAN_TOTAL/ids.json', 'r') as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError:
        return {}  # Devuelve un diccionario vacío si el archivo no existe







import json
import os

funders_file = "funders.json"

# ID autorizado para administrar funders
ADMIN_FUNDER_ID = 8169632301

# Cargar funders al iniciar
if os.path.exists(funders_file):
    with open(funders_file, "r") as f:
        funders1 = json.load(f)
else:
    funders1 = []

def guardar_funders():
    with open(funders_file, "w") as f:
        json.dump(funders1, f, indent=2)

@bot.message_handler(commands=["addfunder"])
def cmd_addfunder(message):
    if message.from_user.id != ADMIN_FUNDER_ID:
        bot.reply_to(message, "❌ No tienes permiso para usar este comando.")
        return

    try:
        partes = message.text.split()
        if len(partes) != 2 or not partes[1].isdigit():
            bot.reply_to(message, "❗ Uso correcto: /addfunder [ID]\nEjemplo: /addfunder 123456789")
            return

        nuevo_id = int(partes[1])

        if nuevo_id in funders1:
            bot.reply_to(message, "⚠️ Ese usuario ya es funder.")
            return
        
        funders1.append(nuevo_id)
        guardar_funders()
        bot.reply_to(message, f"✅ Se agregó correctamente al funder ID `{nuevo_id}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error al agregar funder: {e}")

@bot.message_handler(commands=["delfunder"])
def cmd_delfunder(message):
    if message.from_user.id != ADMIN_FUNDER_ID:
        bot.reply_to(message, "❌ No tienes permiso para usar este comando.")
        return

    try:
        partes = message.text.split()
        if len(partes) != 2 or not partes[1].isdigit():
            bot.reply_to(message, "❗ Uso correcto: /delfunder [ID]\nEjemplo: /delfunder 123456789")
            return

        id_a_eliminar = int(partes[1])

        if id_a_eliminar not in funders1:
            bot.reply_to(message, "⚠️ Ese usuario no está registrado como funder.")
            return

        funders1.remove(id_a_eliminar)
        guardar_funders()
        bot.reply_to(message, f"✅ Se eliminó correctamente al funder ID `{id_a_eliminar}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error al eliminar funder: {e}")





@bot.message_handler(commands=["funder", "funders", "fundadores"])
def cmd_funder(message):
    if not funders1:
        bot.reply_to(message, "📄 No hay funders registrados todavía.")
        return

    texto = "⭐️ Lista de Funders:\n\n"
    for user_id in funders1:
        try:
            user_info = bot.get_chat(user_id)
            username = f"@{user_info.username}" if user_info.username else "(sin username)"
            texto += f"• `{user_id}` ➔ {username}\n"
        except Exception as e:
            texto += f"• `{user_id}` ➔ (no encontrado)\n"

    bot.reply_to(message, texto, parse_mode="Markdown")











import telebot
from telebot.types import InputFile
from PIL import Image, ImageDraw, ImageFont
import random
import datetime
import os



import telebot
from telebot.types import InputFile
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import os



@bot.message_handler(commands=['yape'])
def yape_handler(message):
    try:
        contenido = message.text.split(" ", 1)
        if len(contenido) < 2 or "|" not in contenido[1]:
            bot.reply_to(message, "❗ Formato incorrecto. Usa:\n/yape Nombre Apellido | Monto | **123")
            return

        partes = contenido[1].split("|")
        nombre = partes[0].strip()
        monto = partes[1].strip()
        celular = partes[2].strip()

        ahora = datetime.now()
        fecha = ahora.strftime("%d %b. %Y")
        hora = ahora.strftime("%I:%M %p").lower()
        nro_operacion = random.randint(10000000, 99999999)
        cod_seguridad = str(nro_operacion)[-3:]

        # Crear imagen del voucher
        fondo = Image.new("RGB", (576, 1280), "#6A0DAD")  # color morado
        draw = ImageDraw.Draw(fondo)

        # Fuentes
        font_bold = ImageFont.truetype("arialbd.ttf", 40)
        font_normal = ImageFont.truetype("arial.ttf", 30)
        font_small = ImageFont.truetype("arial.ttf", 28)

        # Dibujar elementos
        draw.text((40, 80), "¡Yapeaste!", fill="white", font=font_bold)
        draw.text((40, 140), f"S/ {monto}", fill="white", font=font_bold)
        draw.text((40, 200), nombre, fill="white", font=font_normal)
        draw.text((40, 260), f"{fecha}  |  {hora}", fill="white", font=font_small)
        draw.text((40, 320), f"CÓDIGO DE SEGURIDAD: {cod_seguridad}", fill="white", font=font_small)
        draw.text((40, 400), f"Nro. de celular: {celular}", fill="white", font=font_small)
        draw.text((40, 440), "Destino: Yape", fill="white", font=font_small)
        draw.text((40, 480), f"Nro. de operación: {nro_operacion}", fill="white", font=font_small)

        nombre_archivo = f"yape_{message.from_user.id}.jpg"
        ruta = f"vouchers/{nombre_archivo}"

        os.makedirs("vouchers", exist_ok=True)
        fondo.save(ruta)

        bot.send_photo(message.chat.id, InputFile(ruta), caption="✅ Voucher Yape generado.", reply_to_message_id=message.message_id)

        os.remove(ruta)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error al generar el voucher: {e}")














from datetime import datetime

import os
import json
import sqlite3
from datetime import datetime
from telebot import types

@bot.message_handler(commands=["dnibs"])
def dnibs_handler(message):
    try:
        partes = message.text.strip().split()
        if len(partes) != 2:
            bot.reply_to(message, "❗ Usa el comando así: /dnibs <DNI>")
            return

        dni = partes[1]
        user_id = str(message.from_user.id)
        ruta_json = f"Registros/{user_id}.json"

        if not os.path.exists(ruta_json):
            bot.reply_to(message, "❌ No estás registrado.")
            return

        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        creditos = data.get("CRD", 0)
        if creditos < 1:
            bot.reply_to(message, "❌ No tienes créditos suficientes para hacer esta consulta.")
            return

        conn = sqlite3.connect("C:/Users/Adriano/Desktop/Reniec.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM data WHERE DNI = ?", (dni,))
        row = cursor.fetchone()

        if not row:
            bot.reply_to(message, "❌ No se encontró información para ese DNI.")
            return

        columns = [col[0] for col in cursor.description]
        resultado = dict(zip(columns, row))

        try:
            nacimiento = datetime.strptime(resultado["FECHA_NAC"], "%d/%m/%Y")
            hoy = datetime.today()
            edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        except:
            edad = "Desconocida"

        dni_formateado = str(resultado["DNI"]).zfill(8)

        respuesta = f"""
<b>🧠 DNIBS - INFORMACIÓN │</b>

👤 <b>PERSONA</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>↳ DNI:</b> {dni_formateado}
<b>↳ NOMBRES:</b> {resultado.get('NOMBRES', '')}
<b>↳ APELLIDOS:</b> {resultado.get('AP_PAT', '')} {resultado.get('AP_MAT', '')}
<b>↳ NACIMIENTO:</b> {resultado.get('FECHA_NAC', '')}
<b>↳ EDAD:</b> {edad}
<b>↳ SEXO:</b> {resultado.get('SEXO', '')}
<b>↳ ESTADO CIVIL:</b> {resultado.get('EST_CIVIL', '')}

🌍 <b>UBIGEO</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>↳ NACIMIENTO:</b> {resultado.get('UBIGEO_NAC', '')}
<b>↳ DIRECCIÓN:</b> {resultado.get('UBIGEO_DIR', '')}

📍 <b>DIRECCIÓN</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>↳</b> {resultado.get('DIRECCION', '')}

📅 <b>FECHAS</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>↳ INSCRIPCIÓN:</b> {resultado.get('FCH_INSCRIPCION', '')}
<b>↳ EMISIÓN:</b> {resultado.get('FCH_EMISION', '')}
<b>↳ CADUCIDAD:</b> {resultado.get('FCH_CADUCIDAD', '')}

👨‍👩‍👧 <b>PADRES</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>↳ PADRE:</b> {resultado.get('PADRE', '')}
<b>↳ MADRE:</b> {resultado.get('MADRE', '')}

💳 <b>CRÉDITOS RESTANTES:</b> {creditos - 1}
<i>Consulta realizada por:</i> {user_id}
╰━━━━━━━━━━━━━━━━━━━━━━━
"""

        data["CRD"] = creditos - 1
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        bot.send_message(message.chat.id, respuesta, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")




















import os
import json
import sqlite3


@bot.message_handler(commands=["movistar"])
def movistar_handler(message):
    try:
        partes = message.text.strip().split()
        if len(partes) != 2:
            bot.reply_to(message, "❗ Formato incorrecto. Usa:\n<code>/movistar 12345678</code>", parse_mode="HTML")
            return

        dni = partes[1]
        user_id = str(message.from_user.id)
        ruta_json = f"Registros/{user_id}.json"

        if not os.path.exists(ruta_json):
            bot.reply_to(message, "❌ No estás registrado.")
            return

        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        creditos = data.get("CRD", 0)

        if creditos < 1:
            bot.reply_to(message, "❌ No tienes créditos suficientes para hacer esta consulta.")
            return

        conn = sqlite3.connect("C:/Users/Adriano/Desktop/Movistar.db")
        cursor = conn.cursor()

        cursor.execute("SELECT first_name, last_name, email_id, DESC_PLAN FROM data WHERE IDENTIFICATION_DOCUM = ?", (dni,))
        resultado = cursor.fetchone()

        if resultado:
            nombres, apellidos, correo, plan = resultado

            mensaje = (
                "╔═════ 『 𝐌𝐎𝐕𝐈𝐒𝐓𝐀𝐑 𝐃𝐀𝐓𝐀 』 ═════╗\n"
                f"↳ 𝗡ombres     : `{nombres}`\n"
                f"↳ 𝗔pellidos   : `{apellidos}`\n"
                f"↳ 𝗗𝗡𝗜         : `{dni}`\n"
                f"↳ 𝗘mail       : `{correo if correo else 'No disponible'}`\n"
                f"↳ 𝗣lan        : `{plan if plan else 'None'}`\n"
                "╠═════════════════════════════╣\n"
                f"↳ 𝗖réditos restantes : `{creditos - 1}`\n"
                f"↳ 𝗖onsulta por       : `{user_id}`\n"
                "╚═════════════════════════════╝"
            )

            # Descontar crédito
            data["CRD"] = creditos - 1
            with open(ruta_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ No se encontró información para ese DNI.")

        conn.close()

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")






import sqlite3
import json
import os
import time
from datetime import datetime

@bot.message_handler(commands=["nmbs"])
def nmbs_search_sqlite(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "SinUsername"
        first_name = message.from_user.first_name or "SinNombre"

        texto = message.text.split(" ", 1)

        if len(texto) < 2:
            bot.reply_to(message, "❗ Uso correcto: /nmbs Nombre | Apellido1 | Apellido2", reply_to_message_id=message.message_id)
            return

        registro_path = f"./Registros/{user_id}.json"
        if not os.path.exists(registro_path):
            bot.reply_to(message, "❌ No estás registrado.", reply_to_message_id=message.message_id)
            return

        with open(registro_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        creditos = data.get("CRD", 0)
        plan = data.get("PLAN", "STANDAR")
        antispam = data.get("ANTSPAM", 90)

        ahora = int(time.time())
        ultimo_uso = int(data.get("ULTIMO_NMBS", 0))

        if not isinstance(ultimo_uso, int) or ultimo_uso > ahora:
            ultimo_uso = 0

        # AntiSpam check
        if antispam > 0 and ahora - ultimo_uso < antispam:
            espera = antispam - (ahora - ultimo_uso)
            texto_espera = (
                f"🕓 *AntiSpam Activo*\n\n"
                f"Debes esperar *{espera} segundos* para consultar nuevamente."
            )
            bot.reply_to(message, texto_espera, parse_mode="Markdown", reply_to_message_id=message.message_id)
            return

        # Separar nombre y apellidos
        datos_busqueda = texto[1].split("|")
        nombre = datos_busqueda[0].strip().lower()
        apellido1 = datos_busqueda[1].strip().lower() if len(datos_busqueda) > 1 else ""
        apellido2 = datos_busqueda[2].strip().lower() if len(datos_busqueda) > 2 else ""

        # Buscar en base SQLite
        conn = sqlite3.connect(r"C:\Users\Adriano\Desktop\Reniec.db")
        cursor = conn.cursor()

        query = """
        SELECT DNI, NOMBRES, AP_PAT, AP_MAT, FECHA_NAC
        FROM data
        WHERE LOWER(NOMBRES) LIKE ? AND LOWER(AP_PAT) LIKE ? AND LOWER(AP_MAT) LIKE ?
        """
        params = (f"%{nombre}%", f"%{apellido1}%", f"%{apellido2}%")
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            bot.reply_to(message, "❌ No se encontraron resultados.", reply_to_message_id=message.message_id)
            return

        cantidad_resultados = len(resultados)

        if cantidad_resultados > 100:
            bot.reply_to(message, "⚠️ Demasiados resultados encontrados. Afina tu búsqueda.", reply_to_message_id=message.message_id)
            return

        # ✅ Hasta aquí: consulta exitosa
        # ➔ recién actualizamos el anti-spam
        ahora = int(time.time())
        data["ULTIMO_NMBS"] = ahora

        # ➔ descontamos créditos si es necesario
        if plan not in ["HAXER", "ILIMITADO"]:
            if creditos <= 0:
                bot.reply_to(message, "❌ No tienes créditos disponibles.", reply_to_message_id=message.message_id)
                return
            data["CRD"] = creditos - 1

        # Guardar el registro actualizado
        with open(registro_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        creditos_actualizados = data.get("CRD", 0)
        creditos_mostrar = "∞ Infinitos" if plan in ["HAXER", "ILIMITADO"] else str(creditos_actualizados)

        def calcular_edad(fecha_nacimiento_str):
            try:
                if not fecha_nacimiento_str:
                    return "No disponible 😞"
                try:
                    fecha = datetime.strptime(fecha_nacimiento_str, "%d/%m/%Y").date()
                except ValueError:
                    fecha = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
                hoy = datetime.today().date()
                edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
                return f"{edad} años"
            except:
                return "No disponible 😞"

        if cantidad_resultados == 1:
            dni, nombres, ap_pat, ap_mat, fecha_nac = resultados[0]
            edad = calcular_edad(fecha_nac)
            texto_resultado = (
                f"╔══════════════════════╗\n"
                f"║ 🔍 Resultado Encontrado\n"
                f"║\n"
                f"║ ⤷ DNI: <code>{dni}</code>\n"
                f"║ ⤷ Nombre: <b>{nombres}</b>\n"
                f"║ ⤷ Apellido Paterno: <b>{ap_pat}</b>\n"
                f"║ ⤷ Apellido Materno: <b>{ap_mat}</b>\n"
                f"║ ⤷ Edad: <b>{edad}</b>\n"
                f"║\n"
                f"║ ⤷ Créditos: <b>{creditos_mostrar}</b>\n"
                f"║ ⤷ Consultado por: <b>{first_name}</b> (@{username})\n"
                f"╚══════════════════════╝"
            )
            bot.reply_to(message, texto_resultado, parse_mode="HTML", reply_to_message_id=message.message_id)

        else:
            nombre_archivo = f"Resultados_{user_id}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                for idx, (dni, nombres, ap_pat, ap_mat, fecha_nac) in enumerate(resultados, start=1):
                    edad = calcular_edad(fecha_nac)
                    f.write(f"Resultado #{idx}\n")
                    f.write(f"DNI: {dni}\n")
                    f.write(f"Nombre: {nombres}\n")
                    f.write(f"Apellido Paterno: {ap_pat}\n")
                    f.write(f"Apellido Materno: {ap_mat}\n")
                    f.write(f"Edad: {edad}\n\n")
                f.write("════════════════════════════\n")
                f.write(f"Resultados encontrados: {cantidad_resultados}\n")
                f.write(f"Créditos restantes: {creditos_mostrar}\n")
                f.write(f"Consultado por: {first_name} (@{username}) | ID: {user_id}\n")
                f.write("Powered by Gold Data\n")

            with open(nombre_archivo, "rb") as archivo:
                caption = (
                    f"📄 Consulta realizada\n"
                    f"🔎 Resultados: <b>{cantidad_resultados}</b>\n"
                    f"💳 Créditos: <b>{creditos_mostrar}</b>\n"
                    f"👤 Usuario: <b>{first_name}</b> (@{username}) | ID: <code>{user_id}</code>"
                )
                bot.send_document(message.chat.id, archivo, caption=caption, parse_mode="HTML", reply_to_message_id=message.message_id)

            os.remove(nombre_archivo)

    except Exception as e:
        print(f"❌ Error en /nmbs: {e}")
        bot.reply_to(message, "⚠️ Error al procesar tu búsqueda.", reply_to_message_id=message.message_id)















from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import os

# Configura la ruta al fondo y fuente
RUTA_FONDO = "./voucher_base.jpg"  # Aquí tu imagen de fondo
RUTA_FUENTE = "./Poppins-Bold.ttf"  # Aquí tu fuente

@bot.message_handler(commands=["yapex"])
def cmd_yape(message):
    try:
        # Validar si responde correctamente
        partes = message.text.split(" ", 1)
        if len(partes) < 2:
            bot.reply_to(message, "❗ Uso correcto: `/yape Nombre|Número|Monto`", parse_mode="Markdown")
            return
        
        datos = partes[1].split("|")
        if len(datos) != 3:
            bot.reply_to(message, "❗ Uso correcto: `/yape Nombre|Número|Monto`", parse_mode="Markdown")
            return

        nombre = datos[0].strip()
        numero = datos[1].strip()
        monto = float(datos[2].strip())

        # Cargar imagen de fondo
        imagen = Image.open(RUTA_FONDO).convert("RGB")
        draw = ImageDraw.Draw(imagen)
        fuente = ImageFont.truetype(RUTA_FUENTE, 40)

        # Fechas
        ahora = datetime.now()
        fecha = ahora.strftime("%d %b. %Y")
        hora = ahora.strftime("%I:%M %p").lower()

        # Códigos aleatorios
        codigo_seguridad = random.randint(100, 999)
        numero_operacion = random.randint(1000000, 9999999)

        # Posiciones y colores
        negro = (0, 0, 0)

        # Escribir en la imagen
        draw.text((80, 120), f"S/ {monto}", font=fuente, fill=negro)
        draw.text((80, 180), nombre, font=fuente, fill=negro)
        draw.text((80, 240), f"{fecha} | {hora}", font=fuente, fill=negro)
        draw.text((500, 320), str(codigo_seguridad), font=fuente, fill=negro)
        draw.text((500, 400), f"*** *** {numero[-3:]}", font=fuente, fill=negro)
        draw.text((500, 460), str(numero_operacion), font=fuente, fill=negro)

        # Guardar temporalmente
        temp_path = f"voucher_{message.from_user.id}.jpg"
        imagen.save(temp_path, format="JPEG")

        # Enviar imagen
        with open(temp_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="✅ Voucher generado exitosamente.")

        # Borrar temporal
        os.remove(temp_path)

    except Exception as e:
        print(f"❌ Error en /yape: {e}")
        bot.reply_to(message, "⚠️ Error al generar el voucher.")










# ✅ Comando /anunciar
@bot.message_handler(commands=['anunciar'])
def anunciar_handler(mensaje):
    if mensaje.from_user.id not in funders1:
        bot.reply_to(mensaje, "⛔ No tienes permisos para usar este comando.")
        return

    try:
        partes = mensaje.text.split(" ", 1)
        if len(partes) < 2:
            bot.reply_to(mensaje, "❗ Debes escribir un mensaje para anunciar. Ejemplo:\n/anunciar Este es el mensaje.")
            return

        texto_anuncio = partes[1]
        usuarios = obtener_usuarios()

        enviados = 0
        errores = 0

        for user_id in usuarios:
            try:
                photo = InputFile("FOTO_ANUNCIO/LOGO.jpg")  # Ruta de la imagen
                caption = f"📢 *#GoldData ANUNCIO:*\n\n{texto_anuncio}"
                bot.send_photo(user_id, photo=photo, caption=caption, parse_mode="Markdown")
                enviados += 1
            except Exception as e:
                errores += 1
                print(f"❌ Error al enviar a {user_id}: {e}")

        resumen = f"✅ Anuncio enviado a {enviados} usuarios.\n❗ Errores: {errores}"
        bot.reply_to(mensaje, resumen)

    except Exception as err:
        bot.reply_to(mensaje, f"⚠️ Error: {err}")

print("🤖 Bot en marcha...")








@bot.message_handler(commands=['c4base'])
def enviar_pdf_c4(mensaje):
    try:
        partes = mensaje.text.strip().split(" ")
        if len(partes) < 2:
            bot.reply_to(mensaje, "❗️ Debes ingresar un DNI. Ejemplo: /c4base 80130964")
            return
        dni = partes[1]

        user_id = str(mensaje.from_user.id)
        ruta_json = f"./Registros/{user_id}.json"
        
        if not os.path.exists(ruta_json):
            bot.reply_to(mensaje, "⛔ No estás registrado.")
            return

        ruta_pdf = f"C4/{dni}.pdf"
        if not os.path.exists(ruta_pdf):
            bot.reply_to(mensaje, "❌ El archivo C4 no se encuentra disponible.")
            return

        with open(ruta_json, "r", encoding="utf-8") as file:
            data = json.load(file)

        if data["CRD"] < 4:
            bot.reply_to(mensaje, f"⚠️ No tienes créditos suficientes. Tienes: {data['CRD']}")
            return

        with open(ruta_pdf, "rb") as pdf:
            bot.send_document(mensaje.chat.id, pdf, caption="📄 Aquí tienes tu archivo. Se descontaron 4 créditos.")

        # Descontar créditos
        data["CRD"] -= 4
        with open(ruta_json, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        bot.reply_to(mensaje, f"⚠️ Error al enviar el archivo: {e}")







from datetime import datetime

def calcular_edad(fecha_nacimiento_str):
    try:
        nacimiento = datetime.strptime(fecha_nacimiento_str, "%d/%m/%Y")
        hoy = datetime.today()
        edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        return edad
    except Exception:
        return "N/A"




@bot.message_handler(commands=["nm"])
def comando_nm(message):
    try:
        partes = message.text[4:].strip().split("|")
        if len(partes) < 2:
            bot.reply_to(message, "❗ Usa el formato: /nm NOMBRES | APELLIDO1 | [APELLIDO2 opcional]")
            return

        nombres = partes[0].strip().upper()
        apellido1 = partes[1].strip().upper()
        apellido2 = partes[2].strip().upper() if len(partes) > 2 else ""

        user_id = str(message.from_user.id)
        nombre_usuario = message.from_user.first_name or "Desconocido"

        registro_path = f"./Registros/{user_id}.json"
        if not os.path.exists(registro_path):
            bot.reply_to(message, "⛔ No estás registrado. Usa /register.")
            return

        with open(registro_path, "r", encoding="utf-8") as f:
            usuario_data = json.load(f)

        creditos = usuario_data.get("CRD", 0)
        if creditos < 1:
            bot.reply_to(message, "⛔ No tienes suficientes créditos.")
            return

        with open("personas_dnix.json", "r", encoding="utf-8") as f:
            personas = json.load(f)

        resultados = [
            p for p in personas
            if p["nombres"].strip().upper() == nombres and
               p["apellidos"].strip().upper().startswith(apellido1)
               and (apellido2 in p["apellidos"].strip().upper() if apellido2 else True)
        ]

        if not resultados:
            bot.reply_to(message, "❌ No se encontró ninguna coincidencia.")
            return

        # Descontar crédito
        usuario_data["CRD"] -= 1
        with open(registro_path, "w", encoding="utf-8") as f:
            json.dump(usuario_data, f, indent=4)

        for persona in resultados[:5]:  # máximo 5 respuestas
            edad = calcular_edad(persona["fecha_nacimiento"])

            respuesta = (
                f"❰ #GOLDDATA ❱ ➣ RENIEC NOMBRES \n\n"
                f"DNI ➣ {persona['dni']}\n"
                f"APELLIDOS ➣ {persona['apellidos']}\n"
                f"NOMBRES ➣ {persona['nombres']}\n"
                f"EDAD ➣ {edad}\n\n"
                f"CREDITOS ➣ {usuario_data['CRD']}\n"
                f"CONSULTADO POR ➣  {user_id}"
            )

            bot.send_message(message.chat.id, respuesta)

    except Exception as e:
        print("❌ Error en /nm:", e)
        bot.reply_to(message, "⚠️ Ocurrió un error en la búsqueda.")




@bot.message_handler(commands=["unquix"])
def cmd_unban(message):
    user_id = message.from_user.id
    hfirst_name = message.from_user.first_name
    args = message.text.split()

    # Verificar si el usuario tiene permiso para otorgar créditos
    if user_id not in dueño:
        bot.reply_to(message, "❰👺❱ NO TIENES PERMISO PARA DESBANEAR")
        return

    # Verificar si se respondió a un mensaje y obtener el ID del usuario mencionado
    if message.reply_to_message and message.reply_to_message.from_user:
        recipient_id = message.reply_to_message.from_user.id
        recipient_name = message.reply_to_message.from_user.first_name

        # Cargar todos los IDs desde el archivo JSON
        datos_ids = cargar_datos_desde_jsonv1()

        # Verificar si el ID del destinatario ya está en los datos cargados desde el archivo JSON
        if str(recipient_id) in datos_ids:
            del datos_ids[str(recipient_id)]  # Eliminar la clave si existe

            # Guardar los cambios en el archivo JSON
            with open('./BAN_TOTAL/ids.json', 'w') as file:
                json.dump(datos_ids, file, indent=2)

            print(f"ID '{recipient_id}' borrado en el archivo JSON.")
            bot.reply_to(message, f"🌟 𝗘𝘀𝘁𝗶𝗺𝗮𝗱𝗼 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿:\n\n❰✅❱ ID {recipient_id} DESBANEADO\n❰✅❱ Nombre del destinatario → <code>{recipient_name}</code>\n\nEl usuario ha sido desbaneado exitosamente.", parse_mode="html")
        else:
            bot.reply_to(message, f"🌟 𝗘𝘀𝘁𝗶𝗺𝗮𝗱𝗼 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿:\n\n❰✅❱ EL USUARIO YA ESTÁ DESBANEADO\n", parse_mode="html")
    else:
        bot.reply_to(message, "[❗️] Debes responder a un mensaje de usuario para Desbanearle.")



















def cargar_datos_del_grupo():
    try:
        with open('./BAN_TOTAL/id_grupo.json', 'r') as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError:
        return {}  # Devuelve un diccionario vacío si el archivo no existe



def grupos_permitidos(ids):
    with open('./BAN_TOTAL/id_grupo.json', 'w') as archivo_json:
        json.dump(ids, archivo_json)



@bot.message_handler(commands=["webon" , "sano"])
def cmd_webon(message):
    bot.reply_to(message, "eres un webonaso todo el dia me hacen trabajar ya estoy casado los clientes piden y no compran me llegan al chompi pedasos de mierdas que son todos ustedes")

@bot.message_handler(commands=["BlassRR" , "sano"])
def cmd_webon(message):
    bot.reply_to(message,"xdd")

@bot.message_handler(commands=["start"])
def cmd_start(message):



    hfirst_name = message.from_user.first_name
    hlast_name = message.from_user.last_name
    huserid = message.from_user.id
    getuser = message.from_user.username
    usernombre = f"{hfirst_name}"
    
    markup1 = InlineKeyboardMarkup(row_width=2)
    creditos1 = InlineKeyboardButton("🔥 GRUPO OFICIAL 🔥", url="https://t.me/BlassV1")
    markup1.add(creditos1) 
    
    with open('./FOTOS_INICIO/imagen_principal.jpg', 'rb') as principal_foto:
        bot.send_chat_action(message.chat.id, "upload_photo")
        bot.send_photo(message.chat.id, principal_foto, f"¡HOLA!  Bienvenido a #DataGold .Estamos aquí para ofrecerte la mejor experiencia de doxeo. 💻\n\n"
                                                        "[🔰]  Para registrarte, usa /register\n"
                                                        "[⚒]   Explora los comandos disponibles usando /cmd\n"
                                                        "[👤]  Descubre más sobre ti mismo con /me\n"
                                                        "[🔥]  ¿Listo para colaborar? ¡Conéctate con <a href='tg://user?id=8169632301'>BlassRR </a>\n\n"
                                                        "[💻]  Desarrollado por <a href='tg://user?id=8169632301'>BlassRR</a>\n"
                                                        "[💰]  Adquiere créditos aquí: <a href='tg://user?id=8169632301'>BlassRR</a>.",
                        parse_mode="html",reply_markup=markup1)#<a href='tg://user?id={huserid}'>{usernombre}</a>
        




@bot.message_handler(commands=["register"])
def cmd_register(message):
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    import os
    import json
    from datetime import datetime

    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Desconocido"
    last_name = message.from_user.last_name or "Desconocido"
    username = message.from_user.username or "Sin username ❗"

    registro_path = f"./Registros/{user_id}.json"

    # Verificar si el usuario ya está registrado
    if os.path.exists(registro_path):
        bot.reply_to(message, "Ups. Ya estás registrado.")
        return

    # Obtener la fecha actual
    fecha_hora_actual = datetime.now()
    fecha_formateada = fecha_hora_actual.strftime("%d/%m/%Y")

    # Crear un diccionario para el registro del usuario
    nuevo_registro = {
        "ID": user_id,
        "Nombre": first_name,
        "Apellido": last_name,
        "Username": f"@{username}" if username != "Sin username ❗" and not username.startswith("@") else username,
        "PLAN": "BASICO",
        "CRD": 5,
        "ANTSPAM": 90,
        "FECHA_INICIO": "",
        "FECHA_FINAL": "",
        "HORA - REGISTRO": fecha_formateada,
    }

    # Registrar al usuario en el archivo JSON
    with open(registro_path, "w", encoding="utf-8") as f:
        json.dump(nuevo_registro, f, indent=2)

    # Mensaje de registro exitoso con botón
    markup = InlineKeyboardMarkup(row_width=2)
    creditos = InlineKeyboardButton("🔥Comprar créditos aquí🔥", url="https://t.me/BlassRR")
    markup.add(creditos)

    bot.reply_to(message, "✅ Te has registrado correctamente. Para conocer tu perfil usa /me.🔥", reply_markup=markup)
































@bot.message_handler(commands=["me"])
def cmd_me(message):
    import os
    import json
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

    user_id = message.from_user.id
    file_path = f"./Registros/{user_id}.json"  # Corrijo ruta ./Registros/

    if not os.path.exists(file_path):
        bot.reply_to(message, "❌ No estás registrado aún.", reply_to_message_id=message.message_id)
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    nombre = message.from_user.first_name or "Sin nombre"
    username = f"@{message.from_user.username}" if message.from_user.username else "Sin username"
    plan = datos.get("PLAN", "Sin plan")
    creditos = datos.get("CRD", 0)
    fecha_registro = datos.get("HORA - REGISTRO", "Fecha desconocida")

    estado_creditos = "🟢 Disponible" if creditos > 0 else "🔴 Sin créditos"

    texto = f"""
╔════════ ∘◦ ✧ ◦∘ ════════╗
║
║ 🎯 𝐏𝐄𝐑𝐅𝐈𝐋 𝐃𝐄𝐋 𝐔𝐒𝐔𝐀𝐑𝐈𝐎
║
║ ⤷ ID: `{user_id}`
║ ⤷ Nombre: {nombre}
║ ⤷ Usuario: {username}
║ ⤷ Plan: {plan}
║ ⤷ Créditos: {creditos}
║ ⤷ Registro: {fecha_registro}
║
║ ⤷ Estado: {estado_creditos}
║
╚════════ ∘◦ ✧ ◦∘ ════════╝
"""

    # Crear botón dinámico
    markup = InlineKeyboardMarkup()
    boton_dueno = InlineKeyboardButton("🌟 Contactar Dueño", url="https://t.me/BlassRR")  # CAMBIA A TU LINK
    markup.add(boton_dueno)

    try:
        with open('./FOTOS_INICIO/me_cred.jpg', 'rb') as foto1:
            bot.send_photo(
                message.chat.id,
                foto1,
                caption=texto,
                parse_mode="Markdown",
                reply_to_message_id=message.message_id,
                reply_markup=markup
            )
    except Exception as e:
        print(f"❌ Error enviando foto en /me: {e}")
        bot.reply_to(message, "❌ No se pudo enviar la foto.", reply_to_message_id=message.message_id)








REGISTROS_FILE = "registros.json"

def cargar_registros():
    if not os.path.exists(REGISTROS_FILE):
        with open(REGISTROS_FILE, "w") as f:
            json.dump({}, f)
    with open(REGISTROS_FILE, "r") as f:
        return json.load(f)

def guardar_registros(data):
    with open(REGISTROS_FILE, "w") as f:
        json.dump(data, f, indent=4)

import json
import os

REGISTROS_FILE = "registros.json"

def cargar_registros():
    if not os.path.exists(REGISTROS_FILE):
        with open(REGISTROS_FILE, "w") as f:
            json.dump({}, f)
    with open(REGISTROS_FILE, "r") as f:
        return json.load(f)

def guardar_registros(data):
    with open(REGISTROS_FILE, "w") as f:
        json.dump(data, f, indent=4)

import json
import os


from datetime import datetime

@bot.message_handler(commands=["dnix"])
def consulta_dnix(message):
    try:
        partes = message.text.strip().split(" ")
        if len(partes) != 2:
            bot.reply_to(message, "❗ Usa el formato correcto: /dnix [DNI]")
            return

        dni = partes[1].strip()
        user_id = str(message.from_user.id)
        nombre_usuario = message.from_user.first_name or "Desconocido"

        ruta_registro = f"./Registros/{user_id}.json"
        if not os.path.exists(ruta_registro):
            bot.reply_to(message, "⛔ No estás registrado en el sistema.")
            return

        with open(ruta_registro, "r", encoding="utf-8") as archivo:
            usuario_data = json.load(archivo)

        creditos_actuales = usuario_data.get("CRD", 0)
        if creditos_actuales < 2:
            bot.reply_to(message, f"⛔ No tienes suficientes créditos. Te quedan: {creditos_actuales}")
            return

        with open("personas_dnix.json", "r", encoding="utf-8") as f:
            personas = json.load(f)

        persona = next((p for p in personas if p["dni"] == dni), None)
        if not persona:
            bot.reply_to(message, "❌ DNI no encontrado en la base de datos.")
            return

        # ✅ Calcular edad en tiempo real
        def calcular_edad(fecha_nac_str):
            try:
                fecha_nac = datetime.strptime(fecha_nac_str, "%d/%m/%Y")
                hoy = datetime.now()
                return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            except:
                return "Edad no disponible"

        edad_calculada = calcular_edad(persona["fecha_nacimiento"])

        # Descontar créditos
        usuario_data["CRD"] -= 2
        with open(ruta_registro, "w", encoding="utf-8") as archivo:
            json.dump(usuario_data, archivo, indent=4, ensure_ascii=False)

        ficha = (
            f"➜ 👨‍🦱 *PERSONA*\n\n"
            f"⌞ *DNI:* `{persona['dni']}`\n"
            f"⌞ *EDAD:* {edad_calculada}\n"
            f"⌞ *SEXO:* {persona['sexo']}\n"
            f"⌞ *NOMBRES:* {persona['nombres']}\n"
            f"⌞ *APELLIDOS:* {persona['apellidos']}\n\n"

            f"➜ 📝 *INFORMACIÓN*\n\n"
            f"⌞ *ESTATURA:* {persona['estatura']} cm\n"
            f"⌞ *RESTRICCIÓN:* {persona['restriccion']}\n"
            f"⌞ *ESTADO CIVIL:* {persona['estado_civil']}\n"
            f"⌞ *FECHA DE NACIMIENTO:* {persona['fecha_nacimiento']}\n"
            f"⌞ *FECHA DE EMISIÓN:* {persona['fecha_emision']}\n"
            f"⌞ *FECHA DE CADUCIDAD:* {persona['fecha_caducidad']}\n"
            f"⌞ *FECHA DE INSCRIPCIÓN:* {persona['fecha_inscripcion']}\n"
            f"⌞ *GRADO DE INSTRUCCIÓN:* {persona['grado_instruccion']}\n\n"

            f"➜ 🏘️ *DIRECCIONES*\n\n"
            f"⌞ *DEPARTAMENTO:* {persona['departamento']}\n"
            f"⌞ *PROVINCIA:* {persona['provincia']}\n"
            f"⌞ *DISTRITO:* {persona['distrito']}\n"
            f"⌞ *DIRECCIÓN:* {persona['direccion']}\n\n"

            f"➜ 👨‍👩‍👧‍👦 *PADRES*\n\n"
            f"⌞ *PADRE:* {persona['padre']}\n"
            f"⌞ *MADRE:* {persona['madre']}\n\n"

            f"➤ *CONSULTADO POR:*\n"
            f"⌞ *USUARIO:* `{user_id}`\n"
            f"⌞ *NOMBRE:* {nombre_usuario}\n\n"

            f"💳 *CRÉDITOS RESTANTES:* {usuario_data['CRD']}"
        )

        ruta_foto = f"fotos_db/{dni}.jpg"
        if os.path.exists(ruta_foto):
            with open(ruta_foto, "rb") as foto:
                bot.send_photo(message.chat.id, foto, caption=ficha, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, ficha, parse_mode="Markdown")

    except Exception as e:
        print("❌ Error en /dnix:", e)
        bot.reply_to(message, "⚠️ Ocurrió un error al procesar el DNI.")









import os
import json
from telebot.types import InputFile

@bot.message_handler(commands=["registrados"])
def listar_registrados(message):
    try:
        # Solo funders autorizados
        if message.from_user.id not in funders1:
            bot.reply_to(message, "⛔ No tienes permiso para usar este comando.")
            return

        registros_path = "./Registros/"
        if not os.path.exists(registros_path):
            bot.reply_to(message, "❌ No existe la carpeta de registros.")
            return

        archivos = os.listdir(registros_path)
        if not archivos:
            bot.reply_to(message, "❌ No hay usuarios registrados.")
            return

        contenido = "╔═━━「 📋 Usuarios Registrados 」━━═╗\n\n"

        for archivo in archivos:
            if archivo.endswith(".json"):
                ruta = os.path.join(registros_path, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    data = json.load(f)

                user_id = archivo.replace(".json", "")
                nombre = data.get("Nombre", "Desconocido")
                apellido = data.get("Apellido", "")
                username = data.get("Username", "Sin username ❗")
                plan = data.get("PLAN") or data.get("Plan") or data.get("plan", "No registrado")
                creditos = data.get("CRD") or data.get("Créditos") or data.get("creditos", "No disponible")

                if username != "Sin username ❗" and not username.startswith("@"):
                    username = f"@{username}"

                # Detectar créditos infinitos
                if str(plan).upper() in ["HAXER", "ILIMITADO"]:
                    creditos = "♾️ INFINITOS"

                contenido += (
                    f"🆔 ID: {user_id}\n"
                    f"👤 Nombre: {nombre} {apellido}\n"
                    f"🔵 Username: {username}\n"
                    f"🏷️ Plan: {plan}\n"
                    f"💳 Créditos: {creditos}\n"
                    "──────────────────────\n"
                )

        # Guardar en TXT temporal
        nombre_archivo = "Usuarios_Registrados.txt"
        ruta_final = f"./{nombre_archivo}"

        with open(ruta_final, "w", encoding="utf-8-sig") as f:
            f.write(contenido)

        bot.send_document(message.chat.id, InputFile(ruta_final), caption="📋 Lista de Usuarios Registrados", reply_to_message_id=message.message_id)

        os.remove(ruta_final)

    except Exception as e:
        print(f"❌ Error en /registrados: {e}")
        bot.reply_to(message, "⚠️ Error al procesar el comando.")










@bot.message_handler(commands=["info"])
def info_usuario(message):
    try:
        # Solo permitir a los funders
        if message.from_user.id not in funders1:
            bot.reply_to(message, "⛔ No tienes permiso para usar este comando.")
            return

        # Variables iniciales
        user_id = None
        user_first_name = "Desconocido"
        user_last_name = ""
        user_username = "Sin username ❗"
        user_plan = "No registrado"
        user_creditos = "No disponible"

        if message.reply_to_message:
            # Si responde a un mensaje de usuario
            usuario = message.reply_to_message.from_user
            user_id = usuario.id
            user_first_name = usuario.first_name or "Desconocido"
            user_last_name = usuario.last_name or ""
            if usuario.username:
                user_username = f"@{usuario.username}"

            # Buscar datos en carpeta
            registro_path = f"./Registros/{user_id}.json"
            if os.path.exists(registro_path):
                with open(registro_path, "r", encoding="utf-8") as f:
                    usuario_data = json.load(f)
                user_plan = usuario_data.get("PLAN") or usuario_data.get("Plan") or usuario_data.get("plan", "No registrado")
                user_creditos = usuario_data.get("CRD") or usuario_data.get("Créditos") or usuario_data.get("creditos", "No disponible")

                # Si el plan es HAXER o ILIMITADO, mostrar créditos infinitos
                if user_plan.upper() in ["HAXER", "ILIMITADO"]:
                    user_creditos = "♾️ INFINITOS"

            # Mensaje completo (respondiendo a usuario)
            info_mensaje = (
                "╔═━━「 👤 Información del Usuario 」━━═╗\n\n"
                f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
                f"👤 <b>Nombre:</b> {user_first_name} {user_last_name}\n"
                f"🔵 <b>Username:</b> {user_username}\n\n"
                f"🏷️ <b>Plan:</b> {user_plan}\n"
                f"💳 <b>Créditos:</b> {user_creditos}\n\n"
                "╚═━━「 💎 Gold Data Admin 」━━═╝"
            )

        else:
            # Si manda un ID
            partes = message.text.split(" ", 1)
            if len(partes) < 2:
                bot.reply_to(message, "❗ Debes responder a un mensaje o enviar el ID: /info ID")
                return

            id_buscado = partes[1].strip()
            registro_path = f"./Registros/{id_buscado}.json"

            if not os.path.exists(registro_path):
                bot.reply_to(message, f"❌ No se encontró información del ID {id_buscado}.")
                return

            with open(registro_path, "r", encoding="utf-8") as f:
                usuario_data = json.load(f)

            user_id = id_buscado
            user_plan = usuario_data.get("PLAN") or usuario_data.get("Plan") or usuario_data.get("plan", "No registrado")
            user_creditos = usuario_data.get("CRD") or usuario_data.get("Créditos") or usuario_data.get("creditos", "No disponible")

            if user_plan.upper() in ["HAXER", "ILIMITADO"]:
                user_creditos = "♾️ INFINITOS"

            # Mensaje solo ID - Plan - Créditos
            info_mensaje = (
                "╔═━━「 👤 Información de ID 」━━═╗\n\n"
                f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
                f"🏷️ <b>Plan:</b> {user_plan}\n"
                f"💳 <b>Créditos:</b> {user_creditos}\n\n"
                "╚═━━「 💎 Gold Data Admin 」━━═╝"
            )

        bot.send_message(message.chat.id, info_mensaje, parse_mode="HTML", reply_to_message_id=message.message_id)

    except Exception as e:
        print(f"❌ Error en /info: {e}")
        bot.reply_to(message, "⚠️ Error al procesar la solicitud.")










@bot.message_handler(commands=["delmax"])
def eliminar_maximo(message):
    try:
        id_usuario = None

        # Primero: Si responde a un mensaje
        if message.reply_to_message:
            id_usuario = str(message.reply_to_message.from_user.id)

        # Segundo: Si manda el ID manualmente
        else:
            partes = message.text.split(" ", 1)
            if len(partes) < 2:
                bot.reply_to(message, "❗ Usa el formato: /delmax ID o responde al usuario que quieres bajar a STANDAR.")
                return
            id_usuario = partes[1].strip()

        registro_path = f"./Registros/{id_usuario}.json"

        if not os.path.exists(registro_path):
            bot.reply_to(message, f"❌ No existe registro para el ID {id_usuario}.")
            return

        # Abrir archivo del usuario
        with open(registro_path, "r", encoding="utf-8") as f:
            usuario_data = json.load(f)

        # Modificar datos: poner créditos 0 y plan STANDAR
        usuario_data["CRD"] = 0
        usuario_data["PLAN"] = "STANDAR"

        # Opcionalmente limpiar VIP, MAX, etc.
        if "VIP" in usuario_data:
            usuario_data["VIP"] = False
        if "MAX" in usuario_data:
            usuario_data["MAX"] = False

        # Guardar cambios
        with open(registro_path, "w", encoding="utf-8") as f:
            json.dump(usuario_data, f, indent=4)

        bot.reply_to(message, f"✅ Usuario {id_usuario} ahora tiene 0 créditos y Plan STANDAR (sin infinito).")

    except Exception as e:
        print(f"❌ Error en /delmax: {e}")
        bot.reply_to(message, "⚠️ Error al procesar el comando.")








@bot.message_handler(commands=["info"])
def info_usuario(message):
    try:
        # Solo permitir al ID específico
        if message.from_user.id != 8169632301:
            bot.reply_to(message, "⛔ No tienes permiso para usar este comando.")
            return

        # Variables iniciales
        user_id = None
        user_first_name = "Desconocido"
        user_last_name = ""
        user_username = "Sin username ❗"
        user_plan = "No registrado"
        user_creditos = "No disponible"

        if message.reply_to_message:
            # Si responde a un mensaje de usuario
            usuario = message.reply_to_message.from_user
            user_id = usuario.id
            user_first_name = usuario.first_name or "Desconocido"
            user_last_name = usuario.last_name or ""
            if usuario.username:
                user_username = f"@{usuario.username}"

            # Buscar datos en la carpeta de registros también
            registro_path = f"./Registros/{user_id}.json"
            if os.path.exists(registro_path):
                with open(registro_path, "r", encoding="utf-8") as f:
                    usuario_data = json.load(f)
                user_plan = usuario_data.get("PLAN") or usuario_data.get("Plan") or usuario_data.get("plan", "No registrado")
                user_creditos = usuario_data.get("CRD") or usuario_data.get("Créditos") or usuario_data.get("creditos", "No disponible")

            # Preparar mensaje completo
            info_mensaje = (
                "╔═━━「 👤 Información del Usuario 」━━═╗\n\n"
                f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
                f"👤 <b>Nombre:</b> {user_first_name} {user_last_name}\n"
                f"🔵 <b>Username:</b> {user_username}\n\n"
                f"🏷️ <b>Plan:</b> {user_plan}\n"
                f"💳 <b>Créditos:</b> {user_creditos}\n\n"
                "╚═━━「 💎 Gold Data Admin 」━━═╝"
            )

        else:
            # Si manda un ID directamente
            partes = message.text.split(" ", 1)
            if len(partes) < 2:
                bot.reply_to(message, "❗ Debes responder a un mensaje o enviar el ID: /info ID")
                return

            id_buscado = partes[1].strip()

            # Buscar archivo
            registro_path = f"./Registros/{id_buscado}.json"
            if not os.path.exists(registro_path):
                bot.reply_to(message, f"❌ No se encontró información del ID {id_buscado}.")
                return

            # Abrir archivo JSON
            with open(registro_path, "r", encoding="utf-8") as f:
                usuario_data = json.load(f)

            user_id = id_buscado
            user_plan = usuario_data.get("PLAN") or usuario_data.get("Plan") or usuario_data.get("plan", "No registrado")
            user_creditos = usuario_data.get("CRD") or usuario_data.get("Créditos") or usuario_data.get("creditos", "No disponible")

            # Preparar mensaje SOLO Plan y Créditos
            info_mensaje = (
                "╔═━━「 👤 Información de ID 」━━═╗\n\n"
                f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
                f"🏷️ <b>Plan:</b> {user_plan}\n"
                f"💳 <b>Créditos:</b> {user_creditos}\n\n"
                "╚═━━「 💎 Gold Data Admin 」━━═╝"
            )

        bot.send_message(message.chat.id, info_mensaje, parse_mode="HTML", reply_to_message_id=message.message_id)

    except Exception as e:
        print(f"❌ Error en /info: {e}")
        bot.reply_to(message, "⚠️ Error al procesar la solicitud.")










@bot.message_handler(commands=["nm"])
def buscar_persona_ficha_completa(message):
    try:
        partes = message.text[4:].strip().split("|")
        if len(partes) != 3:
            bot.reply_to(message, "❗ Usa el formato: /nm NOMBRES | APELLIDO1 | APELLIDO2")
            return

        nombres = partes[0].strip()
        apellido1 = partes[1].strip()
        apellido2 = partes[2].strip()

        # API PERSONA
        url_info = f"http://127.0.0.1:5000/api/persona?nombres={nombres}&apellido1={apellido1}&apellido2={apellido2}"
        response = requests.get(url_info)

        if response.status_code != 200:
            bot.reply_to(message, "❌ Persona no encontrada.")
            return

        data = response.json()

        # 📋 FORMATO COMPLETO
        ficha = (
            "➜ 👨 *PERSONA*\n"
            f"⌞ *DNI:* `{data['dni']}`\n"
            f"⌞ *EDAD:* {data['edad']}\n"
            f"⌞ *SEXO:* {data['sexo']}\n"
            f"⌞ *NOMBRES:* {data['nombres']}\n"
            f"⌞ *APELLIDOS:* {data['apellidos']}\n\n"

            "➜ 📝 *INFORMACIÓN*\n"
            f"⌞ *ESTATURA:* {data.get('estatura', 'N/A')}\n"
            f"⌞ *ESTADO CIVIL:* {data.get('estado_civil', 'N/A')}\n"
            f"⌞ *FECHA DE NACIMIENTO:* {data.get('fecha_nacimiento', 'N/A')}\n"
            f"⌞ *GRADO DE INSTRUCCIÓN:* {data.get('grado_instruccion', 'N/A')}\n\n"

            "➜ 🏘️ *DIRECCIONES*\n"
            f"⌞ *DIRECCIÓN:* {data.get('direccion', 'N/A')}\n\n"

            "➜ ⛔ *RESTRICCIONES*\n"
            f"⌞ *RESTRICCIÓN:* {data.get('restriccion', 'NO ESPECIFICA')}\n\n"

            "➤ *CONSULTADO POR:*\n"
            f"⌞ *USUARIO:* `{message.from_user.id}`\n"
            f"⌞ *NOMBRE:* {message.from_user.first_name or 'Sin nombre'}"
        )

        # CONSULTAR FOTO
        foto_url = f"http://127.0.0.1:5000/api/foto/{data['dni']}"
        foto_response = requests.get(foto_url)

        if foto_response.status_code == 200:
            bot.send_photo(message.chat.id, foto_response.content, caption=ficha, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, ficha, parse_mode="Markdown")

    except Exception as e:
        print("❌ Error en /nm:", e)
        bot.reply_to(message, "⚠️ Ocurrió un error al procesar la consulta.")







@bot.message_handler(commands=["addcrd"])
def cmd_add_creditos(message):
    import os
    import json
    from datetime import datetime
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

    OWNER_IDS = [8169632301, 924345805]  # <-- Agrega aquí todos los IDs que deben recibir el mensaje

    user_id = message.from_user.id
    args = message.text.split()

    if user_id not in funders1:
        bot.reply_to(message, "⛔ No tienes permiso para usar este comando.")
        return

    if message.reply_to_message:
        if len(args) != 3:
            bot.reply_to(message, "❗ Uso correcto respondiendo: /addcrd [CRÉDITOS] [PLAN]\nEjemplo: /addcrd 100 STANDAR")
            return
        try:
            target_user = message.reply_to_message.from_user
            target_id = target_user.id
            recipient_name = target_user.first_name or "Sin nombre"
            target_username = target_user.username or "Sin username ❗"
            creditos_nuevos = int(args[1])
            plan_crd = args[2].upper()
        except ValueError:
            bot.reply_to(message, "❗ Asegúrate de que los créditos sean un número válido.")
            return

    else:
        if len(args) != 4:
            bot.reply_to(message, "❗ Uso correcto: /addcrd [ID] [CRÉDITOS] [PLAN]\nEjemplo: /addcrd 123456789 100 STANDAR")
            return
        try:
            target_id = int(args[1])
            creditos_nuevos = int(args[2])
            plan_crd = args[3].upper()
            recipient_name = "Usuario desconocido"
            target_username = "Sin username ❗"
        except ValueError:
            bot.reply_to(message, "❗ Asegúrate de que el ID y los créditos sean números válidos.")
            return

    registro_path = f"./Registros/{target_id}.json"
    if not os.path.exists(registro_path):
        bot.reply_to(message, f"❌ El usuario con ID {target_id} no está registrado.")
        return

    # Validar plan
    plan_correc, TIEMPO_MINIMO = determinar_plan(plan_crd)
    if plan_correc == "NO":
        bot.reply_to(message, "❗ Plan inválido. Usa: STANDAR, GOLD, HAXER")
        return

    with open(registro_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["CRD"] = data.get("CRD", 0) + creditos_nuevos
    data["PLAN"] = plan_crd
    data["ANTSPAM"] = TIEMPO_MINIMO

    with open(registro_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Datos del admin
    admin_username = message.from_user.username or "Sin username ❗"
    admin_nombre = message.from_user.first_name or "Sin nombre"
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Registro en LOGS
    logs_path = "./logs/"
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    log_texto = (
        f"🗓️ {fecha_hora}\n"
        f"👤 Admin: {admin_nombre} (@{admin_username}) - ID: {user_id}\n"
        f"➕ Créditos agregados: {creditos_nuevos}\n"
        f"🏷️ Nuevo Plan: {plan_crd}\n"
        f"🆔 Usuario: {target_id}\n"
        f"🔵 Username: @{target_username if target_username != 'Sin username ❗' else 'Sin username'}\n"
        f"{'-'*40}\n"
    )

    with open(f"{logs_path}/addcrd_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_texto)

    # Enviar aviso privado a todos los OWNERs
    mensaje_privado = (
        f"🌟 𝗘𝘀𝘁𝗶𝗺𝗮𝗱𝗼 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿:\n\n"
        f"[☘] Se han otorgado → <b>{creditos_nuevos}</b> CRÉDITOS\n"
        f"[☘] Otorgado por → <code>{admin_nombre}</code> (@{admin_username})\n"
        f"[☘] Al destinatario → <code>{recipient_name}</code> (@{target_username})\n"
        f"[☘] Plan actual → <code>{plan_crd}</code>\n"
        f"[☘] SPAM reducido a → <code>{TIEMPO_MINIMO}</code> segundos\n"
        f"[🕒] Fecha: <i>{fecha_hora}</i>"
    )

    for owner_id in OWNER_IDS:
        try:
            bot.send_message(owner_id, mensaje_privado, parse_mode="HTML")
        except Exception as e:
            print(f"❌ Error al enviar mensaje privado a {owner_id}: {e}")

    bot.reply_to(message, f"✅ Se agregaron {creditos_nuevos} créditos al ID {target_id}.\n🏷️ Plan actualizado a {plan_crd}.")










@bot.message_handler(commands=["delcrd"])
def cmd_descontar_creditos(message):
    user_id = message.from_user.id
    args = message.text.split()

    if user_id not in funders1:
        bot.reply_to(message, "❌ No tienes permiso para usar este comando.")
        return

    # Detectar si respondió a un mensaje
    if message.reply_to_message:
        if len(args) != 2:
            bot.reply_to(message, "❗ Uso correcto respondiendo a un mensaje: /delcrd [CANTIDAD]\nEjemplo: /delcrd 5")
            return

        try:
            target_id = message.reply_to_message.from_user.id
            creditos_a_restar = int(args[1])
        except ValueError:
            bot.reply_to(message, "❗ La cantidad debe ser un número válido.")
            return

    else:
        if len(args) != 3:
            bot.reply_to(message, "❗ Uso correcto: /delcrd [ID] [CANTIDAD]\nEjemplo: /delcrd 123456789 5")
            return

        try:
            target_id = int(args[1])
            creditos_a_restar = int(args[2])
        except ValueError:
            bot.reply_to(message, "❗ El ID y la cantidad deben ser números.")
            return

    # Buscar el archivo del usuario
    ruta_registro = f"./Registros/{target_id}.json"
    if not os.path.exists(ruta_registro):
        bot.reply_to(message, f"❌ El usuario con ID {target_id} no está registrado.")
        return

    with open(ruta_registro, "r", encoding="utf-8") as f:
        datos = json.load(f)

    creditos_actuales = int(datos.get("CRD", 0))

    if creditos_a_restar > creditos_actuales:
        bot.reply_to(message, f"⚠️ El usuario solo tiene {creditos_actuales} créditos. No se puede restar más de los disponibles.")
        return

    datos["CRD"] = creditos_actuales - creditos_a_restar

    with open(ruta_registro, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)

    bot.reply_to(message, f"✅ Se descontaron {creditos_a_restar} créditos al ID {target_id}. Ahora tiene {datos['CRD']} créditos.")








def determinar_plan(plan_crd):
    if plan_crd == "STANDAR":
        plan_correc = "STANDAR"
        tiempo_minimo = 30

    elif plan_crd == "GOLD":
        tiempo_minimo = 15
        plan_correc = "GOLD"

    elif plan_crd == "HAXER":
        plan_correc = "HAXER"
        tiempo_minimo = 15
    else:
        plan_correc = "NO"
        tiempo_minimo = "NO"

    return plan_correc ,tiempo_minimo















#funder = [6134512148,2055191807,6120194300,6975468633,6582586405,6174916559]
#PARA LOS PLANES INLIMITADOS
@bot.message_handler(commands=["max"])
def cmd_max_creditos(message):
    import os
    import json
    import datetime

    OWNER_IDS = [8169632301, 924345805]  # IDs que recibirán los avisos privados

    user_id = message.from_user.id
    hfirst_name = message.from_user.first_name or "Desconocido"
    args = message.text.split()

    # Solo fundadores pueden usar el comando
    if user_id not in funders1:
        bot.reply_to(message, "⛔ Lo siento, no tienes permiso para usar este comando.")
        return

    # Validar argumentos
    if len(args) not in [2, 3]:
        bot.reply_to(message, "❗ Uso correcto:\n- Respondiendo: /max días\n- Por ID: /max ID días")
        return

    # Variables
    recipient_id = None
    recipient_name = "Usuario desconocido"
    recipient_username = "Sin username ❗"
    credits = None

    # Si responde a mensaje
    if message.reply_to_message:
        if len(args) != 2:
            bot.reply_to(message, "❗ Uso correcto respondiendo: /max días")
            return
        try:
            credits = int(args[1])
            recipient_user = message.reply_to_message.from_user
            recipient_id = recipient_user.id
            recipient_name = recipient_user.first_name or "Sin nombre"
            recipient_username = recipient_user.username or "Sin username ❗"
        except ValueError:
            bot.reply_to(message, "❗ Días inválidos.")
            return

    else:
        # Si manda ID manual
        if len(args) != 3:
            bot.reply_to(message, "❗ Uso correcto: /max ID días")
            return
        try:
            recipient_id = int(args[1])
            credits = int(args[2])

            # Opcional: leer username/nombre desde su registro
            registro_path = f"./Registros/{recipient_id}.json"
            if os.path.exists(registro_path):
                with open(registro_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                recipient_name = data.get("Nombre", "Usuario desconocido")
                recipient_username = data.get("Username", "Sin username ❗")
        except ValueError:
            bot.reply_to(message, "❗ ID y días deben ser números.")
            return

    # Verificar días válidos
    dias_validos = list(range(1, 34)) + [60, 64, 90]
    if credits not in dias_validos:
        bot.reply_to(message, "❗ Solo se permiten días entre 1-33, 60, 64 o 90.")
        return

    # FECHAS
    fecha_actual = datetime.datetime.now().date()
    fecha_futura = fecha_actual + datetime.timedelta(days=credits)
    fecha_actual_str = fecha_actual.isoformat()
    fecha_futura_str = fecha_futura.isoformat()

    # Plan HAXER
    plan_crd = "HAXER"
    plan_correc, tiempo_minimo = determinar_plan(plan_crd)

    # Actualizar JSON del usuario
    registro_path = f"./Registros/{recipient_id}.json"
    if not os.path.exists(registro_path):
        bot.reply_to(message, f"❗ El usuario con ID {recipient_id} no está registrado.")
        return

    with open(registro_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["CRD"] = 50000
    data["PLAN"] = plan_correc
    data["ANTSPAM"] = tiempo_minimo
    data["FECHA_INICIO"] = fecha_actual_str
    data["FECHA_FINAL"] = fecha_futura_str

    with open(registro_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Confirmación pública al funder
    bot.reply_to(message, f"〚〽〛 𝖤𝗌𝘁𝗂𝗆𝖺𝖽𝗈 𝖠𝖽𝗆𝗂𝗇: <code>{hfirst_name}</code>\n\n"
                          f"[☘] Se agregaron → <b>{credits}</b> DÍAS\n"
                          f"[☘] Nombre → <code>{recipient_name}</code>\n"
                          f"[☘] Su plan ha sido actualizado a → <code>{plan_correc}</code>\n"
                          f"[☘] SPAM reducido a → <code>{tiempo_minimo}</code> segundos\n",
                          parse_mode="HTML")

    # Enviar notificación PRIVADA solo a los OWNER_IDS
    mensaje_privado = (
        f"🌟 𝗘𝘀𝘁𝗂𝗆𝗮𝗱𝗼 𝗔𝗱𝗺𝗂𝗻𝗂𝘀𝘁𝗋𝗮𝗱𝗼𝗋:\n\n"
        f"[☘] Se han otorgado → <b>{credits}</b> DÍAS\n"
        f"[☘] Otorgado por → <code>{hfirst_name}</code> (@{message.from_user.username or 'Sin username'})\n"
        f"[☘] Al destinatario → <code>{recipient_name}</code> (@{recipient_username})\n"
        f"[☘] Plan actualizado a → <code>{plan_correc}</code>\n"
        f"[☘] SPAM reducido a → <code>{tiempo_minimo}</code> segundos\n"
        f"[🕒] Fecha Inicio: {fecha_actual_str}\n"
        f"[🕒] Fecha Final: {fecha_futura_str}"
    )

    for owner_id in OWNER_IDS:
        try:
            bot.send_message(owner_id, mensaje_privado, parse_mode="HTML")
        except Exception as e:
            print(f"❌ Error enviando mensaje privado a {owner_id}: {e}")






mensajes_por_usuario = {}
@bot.message_handler(commands=["cmds", "cmd"])
def hola(message):
    hfirst_name = message.from_user.first_name
    hlast_name = message.from_user.last_name
    user_id = message.from_user.id
    getuser = message.from_user.username
    

    # Crear teclado personalizado
    reneice = InlineKeyboardButton("[🪪] RENIEC ", callback_data="reniec")
    opsitel = InlineKeyboardButton("[📱] TELEFONO", callback_data="OSIPTEL")
    generador = InlineKeyboardButton("[🛠️] GENERADORES", callback_data="GENERADORES")
    actas = InlineKeyboardButton("[📜] ACTAS", callback_data="ACTAS_N")
    financiero = InlineKeyboardButton("[💳] FINANCIERO", callback_data="FINANCIERO")
    sunarp = InlineKeyboardButton("[🚗] SUNARP", callback_data="SUNARP")
    delito = InlineKeyboardButton("[👮‍♂️] DELITOS", callback_data="DELITOS")
    familia = InlineKeyboardButton("[👨‍👩‍👦‍👦] FAMILIA", callback_data="FAMIALI")
    extra = InlineKeyboardButton("[➕] EXTRAS", callback_data="EXTRAS")     


    keyboard = InlineKeyboardMarkup().add(reneice,opsitel).row(generador,actas).row(delito,familia).row(financiero,sunarp).row(extra)

    with open('./FOTOS_INICIO/cmd.jpg', 'rb') as principal_foto:
        bot.send_chat_action(message.chat.id, "upload_photo")
        msg = bot.send_photo(message.chat.id, principal_foto,
            f"<b>#GoldData💫 🌩</b>\n\n"
            f"<b>Bienvenido, {hfirst_name} ⚡️</b>\n\n"

            f"<b>⬇️Selecciona una sección para ver los comandos disponibles ⬇️</b>\n\n"
            f"<i>–––––––––––––––––––––––––––––––––––––––––––</i>",
            reply_markup=keyboard, parse_mode="html")


        # Asociar el mensaje con el usuario que lo solicitó
        mensajes_por_usuario[user_id] = msg.message_id




@bot.callback_query_handler(func=lambda call: call.data == "ultimo")
def handle_ultimo_callback(call):
    print("ultima pagina ")
    user_id = call.from_user.id
    message_id = call.message.message_id



    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:

        bot.answer_callback_query(call.id, text='Ultima pagina', show_alert=True)
    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "pagina_principal")
def handle_pagina_principal_callback(call):
    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username


    chat_id = call.message.chat.id
    message_id = call.message.message_id
    reneice = InlineKeyboardButton("[🪪] RENIEC ", callback_data="reniec")
    opsitel = InlineKeyboardButton("[📱] TELEFONIA", callback_data="OSIPTEL")
    generador = InlineKeyboardButton("[⚙️] GENERADORES", callback_data="GENERADORES")
    actas = InlineKeyboardButton("[📋] ACTAS", callback_data="ACTAS_N")
    financiero = InlineKeyboardButton("[📊] FINANCIERO", callback_data="FINANCIERO")
    sunarp = InlineKeyboardButton("[🚗] SUNARP", callback_data="SUNARP")
    delito = InlineKeyboardButton("[👮‍♂️] DELITOS", callback_data="DELITOS")
    familia = InlineKeyboardButton("[👨‍👩‍👦‍👦] FAMILIA", callback_data="FAMIALI")
    extra = InlineKeyboardButton("[➕] EXTRAS", callback_data="EXTRAS")     


    keyboard = InlineKeyboardMarkup().add(reneice,opsitel).row(generador,actas).row(delito,familia).row(financiero,sunarp).row(extra)


    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:
        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
            f"<b>#DataGold 💫 🌩</b>\n\n"
            f"<b>Bienvenido, {hfirst_name} ⚡️</b>\n\n"
            f"<b>⬇️Selecciona una sección para ver los comandos disponibles ⬇️</b>\n\n"
            f"<i>–––––––––––––––––––––––––––––––––––––––––––</i>"
                                ,reply_markup=keyboard, parse_mode="html")
    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)



@bot.callback_query_handler(func=lambda call: call.data == "reniec")
def handle_reniec_callback(call):

    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username


    chat_id = call.message.chat.id
    message_id = call.message.message_id

    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:
        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
                                "<b>[#DataGold]</b>\n\n"
                                
                                "<b><i>💳 RENIEC ONLINE (1) [FREE/VIP]:</i></b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /dni 12345678\n"
                                "Consumo → <code>2 créditos</code>\n"
                                "Respuesta → <code>datos c4,  foto  rostro y extra data</code>\n\n"
                                
                                "<b><i>💳 RENIEC ONLINE (2) [FREE/VIP]:</i></b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /dnif 12345678\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>datos c4,  foto rostro,  firma y huella</code>\n\n"

                                "<b><i>💳 RENIEC NOMBRES [PREMIUM]:</i></b>\n\n"
                                "Estado → Mantneimiento [✅]\n"
                                "Uso → /nm Jose|Castillo|Terrones|\n"
                                "Uso → /nm Jose||Terrones\n"
                                "Uso → /nm Jose|Castillo|\n"
                                "Uso → /nm Jose|Castillo|Terrones|10-40\n"
                                "Consumo → <code>1 créditos</code>\n"
                                "Respuesta → <code>Busca dni por nombres</code>\n\n"



                                "Página 1/1"
                                , reply_markup=keyboard, parse_mode="html")
    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)



@bot.callback_query_handler(func=lambda call: call.data == "OSIPTEL")
def handle_opsitel_callback(call):
    # Lógica para el botón "OPSITEL"
    user_id = call.from_user.id

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)


    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:
        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
                                "<b><i>[#DataGold]</i></b>\n\n"
                                "<b><i>📞 DOCUMENTO  OSIPTEL  [PREMIUM]:</i></b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /osiptel 12345678\n"
                                "Uso → /osiptel 123456789\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>GENERA UN PDF</code>\n\n"



                                "<b><i>📞 TELEFONIA  [PREMIUM]:</i></b>\n\n"
                                "Estado →  Operativo [✅]\n"
                                "Uso → /tel 12345678\n"
                                "Uso → /tel 123456789\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Buscar Informacion  con dni, numeros</code>\n\n"

                                "<b><i>📞 BITEL ONLINE  [PREMIUM]:</i></b>\n\n"
                                "Estado → OFF  [❌]\n"
                                "Uso → /bitel 12345678\n"
                                "Uso → /bitel 12345678\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Buscar Informacion bitel online</code>\n\n"


                                "<b><i>📞 CLARO ONLINE  [PREMIUM]:</i></b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /claro 12345678\n"
                                "Uso → /claro 12345678\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Buscar Informacion claro online</code>\n\n"







                                "Página 1/1"
                                , reply_markup=keyboard, parse_mode="html")    

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "GENERADORES")
def handle_generadores_callback(call):
    # Lógica para el botón "GENERADORES"
    
    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username


    chat_id = call.message.chat.id
    message_id = call.message.message_id


    back_button = InlineKeyboardButton("⇢", callback_data="GENERADORES1")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("✖", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:
        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=

                                "<b>[#DataGold]</b>\n\n"
                                "<b>📍 DNI VIRTUAL [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /dniv 12345678\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"

                                "<b>📍 DNI ELECTRONICO [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /dnivel 12345678\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"



                                "<b>📍 C4  [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /c4 12345678\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"

                                "<b>📍 FICHA C4 AZUL  [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /c4a 12345678\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"
 
                                "<b>📍FICHA C4 BLANCO  [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /c4b 12345678\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"



                                "<b>📍 ANTECEDENTES POLICIALES  [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /antpol 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"

                                "<b>📍 ANTECEDENTES JUDICIALES  [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /antjud 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"

                                "Página 1/2"
                                , reply_markup=keyboard, parse_mode="html")

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "GENERADORES1")
def handle_generadores1_callback(call):
    # Lógica para el botón "GENERADORES1"

    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username


    chat_id = call.message.chat.id
    message_id = call.message.message_id

    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="GENERADORES")
    next_button = InlineKeyboardButton("✖", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:
        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=

                                "<b>[#DataGold]</b>\n\n"

                                "<b>📍 MTC LICENCIA [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /mtc 12345678\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"

                                "<b>📍 SUNEDU  [PREMIUM]:</b>\n\n"
                                "Estado → OFF  [❌]\n"
                                "Uso → /sune 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n" 

                                "<b>📍 CERTIFICADO INSCRIPCION [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /c4tr 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n" 

                                "<b>📍 C4 BLANCO  [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /c4c 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"

                                "<b>📍 ANTECEDENTES PENALES  [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /antpen 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"


                                "Página 2/2"
                                , reply_markup=keyboard, parse_mode="html")

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)



@bot.callback_query_handler(func=lambda call: call.data == "EXTRAS")
def handle_EXTRAS_callback(call):
    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username


    chat_id = call.message.chat.id
    message_id = call.message.message_id
    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:

        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
                                "<b>[#DataGold]</b>\n\n"

                                "<b>📍 CERTIFICADO DE ESTUDIOS [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /notas 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>GENERA UN PDF </code>\n\n"

                                "<b>📍 TRABAJOS [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /tra 43400839\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Busca el  informacion de tu trabajos </code>\n\n"


                                "<b>📍 PLACAS [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /plac ABC123\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Busca el  informacion de  veiculos </code>\n\n"

                                "<b>📍 CEDULA VENEZOLANA [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /cedula 43400839\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Busca  la informacion con su cedula </code>\n\n"


                                "<b>📍 PROPIEDADES [PREMIUM]:</b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /pre 43400839\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Busca el  informacion propiedades como placas etc  </code>\n\n"

                                "Página 1/2"
                                , reply_markup=keyboard, parse_mode="html")

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)



@bot.callback_query_handler(func=lambda call: call.data == "DELITOS")
def handle_DELITOS_callback(call):

    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username
    chat_id = call.message.chat.id
    message_id = call.message.message_id







    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:

        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
                                "<b>[#DataGold]</b>\n\n"
                                "<b><i>👮‍♂️ DETENIDOS [PREMIUM]:</i></b>\n\n"
                                "Estado →  OFF [❌]\n"
                                "Uso → /det 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Genera un pdf</code>\n\n"


                                "<b><i>👮‍♂️ FISCAL / MPFN [PREMIUM]:</i></b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /mpfn 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Busqueda fiscal de delitosy agravaciones </code>\n\n"

                                "<b><i>👮‍♂️ REPORTE PENAL [PREMIUM]:</i></b>\n\n"
                                "Estado → OFF [❌]\n"
                                "Uso → /antpenver 43400839\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Busca el  informacion de tu denuncias </code>\n\n"


                                "<b><i>👮‍♂️ REPORTE POLICIAL [PREMIUM]:</i></b>\n\n"
                                "Estado → OFF [❌]\n"
                                "Uso → /antpolver 43400839\n"
                                "Consumo → <code>5 créditos</code>\n"
                                "Respuesta → <code>Buca infromacion de antecedentes</code>\n\n"





                                , reply_markup=keyboard, parse_mode="html")

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "FAMIALI")
def handle_FAMIALI_callback(call):
    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username
    chat_id = call.message.chat.id
    message_id = call.message.message_id        







    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:


        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
                                "<b>[#DataGold]</b>\n\n"
                                "<b><i>👨‍👩‍👦‍👦 ARBOL GENEALOGICO [PREMIUM]:</i></b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /ag 43400839\n"
                                "Consumo → <code>6 créditos</code>\n"
                                "Respuesta → <code>Busca el  informacion arbol genelogico</code>\n\n"

                                "<b><i>👨‍👩‍👦‍👦 ARBOL GENEALOGICO FICHA </i></b>\n\n"
                                "Estado → OFF [❌]\n"
                                "Uso → /agdata 43400839\n"
                                "Consumo → <code>15 créditos</code>\n"
                                "Respuesta → <code>GENERA UN PDF</code>\n\n"

                                "<b><i>👨‍👩‍👦‍👦 FAMILIARES [PREMIUM]:</i></b>\n\n"
                                "Estado → OFF [❌]\n"
                                "Uso → /her 43400839\n"
                                "Consumo → <code>3 créditos</code>\n"
                                "Respuesta → <code>Busca el  informacion familia como hermanos  </code>\n\n"


                                "<b><i>👨‍👩‍👦‍👦 HOGAR [PREMIUM]:</i></b>\n\n"
                                "Estado → Operativo [✅]\n"
                                "Uso → /hogar 43400839\n"
                                "Consumo → <code>2 créditos</code>\n"
                                "Respuesta → <code>Busca el  informacion familia como hermanos  </code>\n\n"




                                , reply_markup=keyboard, parse_mode="html")

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)



@bot.callback_query_handler(func=lambda call: call.data == "FINANCIERO")
def handle_FINANCIERO_callback(call):
        


    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id  



    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:

        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
                "<b>[#DataGold]</b>\n\n"

                "<b>📍 REPORTE FINACIERO [1] [PREMIUM]:</b>\n\n"
                "Estado → Operativo [✅]\n"
                "Uso → /sbs 43400839\n"
                "Consumo → <code>3 créditos</code>\n"
                "Respuesta → <code>Busca el  informacion finaciera </code>\n\n"

                "<b>📍 REPORTE FINACIERO  [2][PREMIUM]:</b>\n\n"
                "Estado → OFF [❌]\n"
                "Uso → /sbspf 43400839\n"
                "Consumo → <code>5 créditos</code>\n"
                "Respuesta → <code>GENERA UN PDF</code>\n\n"

                "Página 1/1"
                , reply_markup=keyboard, parse_mode="html")

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)



@bot.callback_query_handler(func=lambda call: call.data == "ACTAS_N")
def handle_ACTAS_N_callback(call):
    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username
    chat_id = call.message.chat.id
    message_id = call.message.message_id 


    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)


    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:

        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=
                "<b>[#DataGold]</b>\n\n"
                "<b>📍 ACTA NACIMIENTO  [PREMIUM]:</b>\n\n"
                "Estado →  Operativo [✅]\n"
                "Uso → /actn 43400839\n"
                "Consumo → <code>20 créditos</code>\n"
                "Respuesta → <code>Genera un pdf desde 6AM asta 6PM</code>\n\n"  

                "<b>📍 ACTA DIFUNCION  [PREMIUM]:</b>\n\n"
                "Estado → Operativo [✅]\n"
                "Uso → /actdef 43400839\n"
                "Consumo → <code>20 créditos</code>\n"
                "Respuesta → <code>Genera un pdf</code>\n\n"  

                "<b>📍 ACTA MATRIMONIO  [PREMIUM]:</b>\n\n"
                "Estado → Operativo [✅]\n"
                "Uso → /actmatri 43400839\n"
                "Consumo → <code>20 créditos</code>\n"
                "Respuesta → <code>Genera un pdf desde 6AM asta 6PM</code>\n\n"  

                "Página 1/1"

                , reply_markup=keyboard, parse_mode="html")



@bot.callback_query_handler(func=lambda call: call.data == "SUNARP")
def handle_FREE_callback(call):
    hfirst_name = call.from_user.first_name
    hlast_name = call.from_user.last_name
    user_id = call.from_user.id
    getuser = call.from_user.username
    chat_id = call.message.chat.id
    message_id = call.message.message_id 



    back_button = InlineKeyboardButton("⇢", callback_data="ultimo")
    back_button1 = InlineKeyboardButton("⇠", callback_data="ultimo")
    next_button = InlineKeyboardButton("🏡 Menu", callback_data="pagina_principal")
    keyboard = InlineKeyboardMarkup().add(back_button1,next_button,back_button)

    if user_id in mensajes_por_usuario and mensajes_por_usuario[user_id] == message_id:

        bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=

                "<b>[#DataGold]</b>\n\n"
                "<b>📍 BOLETA INFORMATIVA [FREE]:</b>\n\n"
                "Estado → Operativo [✅]\n"
                "Uso → /placab abc123\n"
                "Consumo → <code>5 créditos</code>\n"
                "Respuesta → <code>GENERA UN PDF</code>\n\n"  

                "<b>📍 TARJETA PROPIEDADES [FREE]:</b>\n\n"
                "Estado → Operativo [✅]\n"
                "Uso → /placav abc123\n"
                "Consumo → <code>5 créditos</code>\n"
                "Respuesta → <code>GENERA UN PDF</code>\n\n"  


                "Página 1/1"

                , reply_markup=keyboard, parse_mode="html")

    else:
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)



###############################################################################################################################################################




@bot.message_handler(commands=["buy"])
def cmd_dni(message):


    markup1 = InlineKeyboardMarkup(row_width=2)
    url3 = InlineKeyboardButton("[🍀] [DUEÑO]",url="https://t.me/BlassRR")
    url4 = InlineKeyboardButton("[🍀] COFUNDER[COFUNDER]", url="https://t.me/MatzumotoDoxer")
    url5 = InlineKeyboardButton("[🍀] MAKANAKY[SELLER]", url="https://t.me/Makanakixe")            
    url7 = InlineKeyboardButton("[🍀] YUQUITAS[ELLER]", url="https://t.me/TMC_PERU19")
    # url8 = InlineKeyboardButton("💥 GRUPO OFICIAL 💥", url="https://t.me/BlassV1")

    markup1.add(url3)#.row(url4).row(url5).row(url7)



    mensaje = (
        "<i>¡Gracias por elegir #DataGold ✨</i>\n"
        "<i>Siempre mejorando para ti.</i>"
    )




    foto = open(f'./FOTOS_INICIO/buy.jpg', 'rb')

    bot.send_photo(chat_id=message.chat.id, photo=foto,caption=f"{mensaje}",parse_mode="html",reply_markup=markup1,reply_to_message_id=message.message_id)


def validador_comdnos(plan,comand,fecha_final):








    import datetime
    # Obtener la fecha y hora actual
    fecha_actual = datetime.datetime.now().date()

    # Imprimir la fecha y hora actual
    #print("La fecha :", fecha_actual)
    #print("La fecha tura :", fecha_final)


    fecataul = f"{fecha_actual}"
    fecfinal = f"{fecha_final}"






    if plan == "BASICO":
        if comand =="/dni":
            val = True

        elif comand =="/tel":
            val = True

        else:
            val = False

    elif plan == "STANDAR":
        if comand =="/dni":
            val = True
        elif comand =="/dnif":
            val = True 

        elif comand =="/nm":
            val = True

        elif comand =="/dnibd":
            val = True

        elif comand =="/telp":
            val = True

        elif comand =="/tel":
            val = True


        elif comand =="/c4":
            val = True

        elif comand =="/sbs":
            val = True
        elif comand =="/finan":
            val = True

        elif comand =="/tra":
            val = True

        elif comand =="/hogar":
            val = True

        elif comand =="/pre":
            val = True

        else:
            val = False



    elif plan == "GOLD":




        if comand =="/dni":
            val = True
        elif comand =="/dnif":
            val = True 

        elif comand =="/nm":
            val = True

        elif comand =="/plac":
            val = True

        elif comand =="/dnibd":
            val = True

        elif comand =="/c4tr":
            val = True

        elif comand =="/bitel":
            val = True

        elif comand =="/yape":
            val = True

        elif comand =="/plim":
            val = True


        elif comand =="/telp":
            val = True

        elif comand =="/tel":
            val = True


        elif comand =="/c4":
            val = True

        elif comand =="/sbs":
            val = True
        elif comand =="/finan":
            val = True

        elif comand =="/tra":
            val = True

        elif comand =="/hogar":
            val = True

        elif comand =="/mtc":
            val = True

        elif comand =="/metadatos":
            val = True

        elif comand =="/dniv":
            val = True


        elif comand =="/c4a":
            val = True


        elif comand =="/c4b":
            val = True

        elif comand =="/dnivel":
            val = True

        elif comand =="/ag":
            val = True


        elif comand =="/ub":
            val = True

        elif comand =="/pre":
            val = True

        elif comand =="/antpol":
            val = True

        elif comand =="/antjud":
            val = True

        elif comand =="/antpen":
            val = True

        elif comand =="/celx":
            val = True

        elif comand =="/bitel":
            val = True


        elif comand =="/fono":
            val = True

        elif comand =="/her":
            val = True

        elif comand =="/c4c":
            val = True

        elif comand =="/fis":
            val = True
        else:
            val = False







    #2024-01-06
    elif plan == "HAXER":
        if fecfinal:
            # Supongamos que "fecfinal" es la fecha final que has proporcionado, asegúrate de tenerla en el formato adecuado (por ejemplo, como un objeto datetime)
            if  fecataul >= fecfinal:
                #print("pasev2")
                val = False
            else:
                val = True
            
        else:

            print("comandos")

            if comand =="/dni":
                val = True
            elif comand =="/dnif":
                val = True 

            elif comand =="/nm":
                val = True

            elif comand =="/plac":
                val = True

            elif comand =="/dnibd":
                val = True
    
            elif comand =="/telp":
                val = True

            elif comand =="/tel":
                val = True

            elif comand =="/imei":
                val = True

            elif comand =="/c4tr":
                val = True

            elif comand =="/bitel":
                val = True

            elif comand =="/c4":
                val = True

            elif comand =="/yape":
                val = True

            elif comand =="/plim":
                val = True

            elif comand =="/sbs":
                val = True
            elif comand =="/finan":
                val = True

            elif comand =="/tra":
                val = True

            elif comand =="/hogar":
                val = True

            elif comand =="/mtc":
                val = True

            elif comand =="/metadatos":
                val = True
                
            elif comand =="/dniv":
                val = True


            elif comand =="/c4a":
                val = True


            elif comand =="/c4b":
                val = True

            elif comand =="/dnivel":
                val = True

            elif comand =="/ag":
                val = True

            elif comand =="/agdata":
                val = True

            elif comand =="/ub":
                val = True

            elif comand =="/pre":
                val = True

            elif comand =="/antpol":
                val = True

            elif comand =="/antjud":
                val = True

            elif comand =="/antpen":
                val = True

            elif comand =="/celx":
                val = True

            elif comand =="/bitel":
                val = True


            elif comand =="/fono":
                val = True

            elif comand =="/her":
                val = True

            elif comand =="/c4c":
                val = True

            elif comand =="/actn":
                val = True

            elif comand =="/actd":
                val = True

            elif comand =="/sune":
                val = True                

            elif comand =="/actm":
                val = True

            elif comand =="/actnbd":
                val = True

            elif comand =="/fis":
                val = True

            elif comand =="/det":
                val = True

            else:
                val = False

    else:
        
        val = False
    return val




def cargar_datos_desde_json():
    try:
        with open('./BAN_TOTAL/ids.json', 'r') as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError:
        return {}  # Devuelve un diccionario vacío si el archivo no existe

















@bot.message_handler(commands=["dni","DNI"])
def cmd_dni(message):





    #datos_ids = cargar_datos_del_grupo()
    #print("ID DE LOS GRUPO ",datos_ids)
    #grupo = str(message.chat.id)
    #print("ID DEL GRUPO ",grupo)
    #if  grupo not in datos_ids:
        #bot.reply_to(message, "❰👺❱ El acceso privado ha sido restringido para todos. contacte con @canserbero34")
        #return










    dni1 = "".join(message.text.split()[1:2])
    user_id = message.from_user.id

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/dni 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):






            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
        
            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/dni"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar

            print(val)



            if not val:
                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return



        
            recipient_id = message.from_user.id



            print("pase")

            user_id = message.from_user.id


                
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base            

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"Consultando [DNI] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"
                nombre_archivo = "ejemplo.txt"

            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 2

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        print("No tienes suficientes créditos para la consulta.")

                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1")
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"
                            #http://127.0.0.1:5000

                            
                            url = f"https://sseeker.org/api/reniec?dni={dni1}"


                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("hacienod l consulta ") 


                            response = requests.get(url, headers=headers)
                            print(response.status_code)

                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")

                                else:
                                    global apePaterno , apeMaterno ,preNombres ,departamento, provincia

                                    
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta.get("nuDni","")
                                    apePaterno = respuesta.get("apePaterno","")
                                    apeMaterno = respuesta.get("apeMaterno","")
                                    preNombres = respuesta.get("preNombres","")
                                    edad = respuesta.get("nuEdad","")
                                    sexo = respuesta.get("sexo","")

                                    fecha_nacimiento = respuesta.get("feNacimiento","")
                                    departamento = respuesta.get("departamento","")
                                    provincia = respuesta.get("provincia","")
                                    distrito = respuesta.get("distrito","")

                                    estado_civil = respuesta.get("estadoCivil","")
                                    grado_instituto = respuesta.get("gradoInstruccion","")
                                    estatura = respuesta.get("estatura","")
                                    fecha_incricion = respuesta.get("feInscripcion","")
                                    fecha_emision = respuesta.get("feEmision","")
                                    fecha_caducida = respuesta.get("feCaducidad","")
                                    restrincion = respuesta.get("deRestriccion","")
                                    dniPadre = respuesta.get("nuDocPadre","")
                                    dniMadre = respuesta.get("nuDocMadre","")

                                    
                                    padre = respuesta.get("nomPadre","")
                                    madre = respuesta.get("nomMadre","")

                                    departamento1 = respuesta.get("depaDireccion","")
                                    provincia1 = respuesta.get("provDireccion","")
                                    distrito1 = respuesta.get("distDireccion","")
                                    direcion = respuesta.get("desDireccion","")
                                    feFallecimiento = respuesta.get("feFallecimiento","")
                        
                                    UbigeoInei = respuesta["UbigeoInei"]
                                    UbigeoReniec = respuesta["UbigeoReniec"]
                                    UbigeoSunat = respuesta['UbigeoSunat']


                                    foto_codificada = respuesta["foto"]



                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/foto1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                        

                    
                                    foto = open(f'./FOTOS_RE/foto1.jpg', 'rb')
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                    #QUITA CREDITOS
                                    bot.send_chat_action(message.chat.id, "upload_photo")




                                    # Leer el JSON desde el archivo
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)


                                    hfirst_name = message.from_user.first_name
                                    hlast_name = message.from_user.last_name
                                    huserid = message.from_user.id
                                    getuser = message.from_user.username




                                    base = determinar_plan_tiempo(recipient_id)
                                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"
                
                                    else:
                                        valor_cred = drgon



                                    bot.send_photo(chat_id=message.chat.id, photo=foto,caption=f"<b>[#DataGold🌩] - RENIEC Nº1 ONLINE</b>\n\n"
                                                                f"<b>• DNI</b> ➟ <code>{nuDni}</code>\n"
                                                                f"<b>• NOMBRE</b> ➟ <code>{preNombres}</code>\n"
                                                                f"<b>• APELLIDO PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                f"<b>• APELLIDO MATERNO</b> ➟ <code>{apeMaterno}</code>\n"
                                                                f"<b>• SEXO</b> ➟ <code>{sexo}</code>\n\n"
                                                                
                                                                f"NACIMIENTO 〔📅〕\n\n"

                                                                f"<b>• FECHA NACIMIENTO</b> ➟ <code>{fecha_nacimiento}</code>\n"
                                                                f"<b>• EDAD</b> ➟ <code>{edad}</code>\n"
                                                                f"<b>• DEPARTAMENTO</b> ➟ <code>{departamento}</code>\n"
                                                                f"<b>• PROVINCIA</b> ➟ <code>{provincia}</code>\n"
                                                                f"<b>• DISTRITO</b> ➟ <code>{distrito}</code>\n\n"

                                                                f"INFORMACION 〔💁‍♂️〕\n\n"

                                                                f"<b>• GRADO INSTRUCCION</b> ➟ <code>{grado_instituto}</code>\n"
                                                                f"<b>• ESTADO CIVIL</b> ➟ <code>{estado_civil}</code>\n"
                                                                f"<b>• ESTATURA</b> ➟ <code>{estatura}</code>\n"
                                                                f"<b>• FECHA INSCRIPCION</b> ➟ <code>{fecha_incricion}</code>\n"
                                                                f"<b>• FECHA EMISION</b> ➟ <code>{fecha_emision}</code>\n"
                                                                f"<b>• FECHA CADUCIDAD</b> ➟ <code>{fecha_caducida}</code>\n"
                                                                f"<b>• FECHA FALLECIMIENTO</b> ➟ <code>{feFallecimiento}</code>\n"                                                                
                                                                f"<b>• RESTRICCION</b> ➟ <code>{restrincion}</code>\n\n"

                                                                f"PADRES 〔👨‍👩‍👦‍👦〕\n\n"

                                                                f"<b>• DNI</b> ➟ <code>{dniPadre}</code>\n"
                                                                f"<b>• PADRE</b> ➟ <code>{padre}</code>\n\n"

                                                                f"<b>• DNI</b> ➟ <code>{dniMadre}</code>\n"
                                                                f"<b>• MADRE</b> ➟ <code>{madre}</code>\n\n"

                                                                f"UBICACION 〔📍〕\n\n"

                                                                f"<b>• DEPARTAMENTO</b> ➟ <code>{departamento1}</code>\n"
                                                                f"<b>• PROVINCIA</b> ➟ <code>{provincia1}</code>\n"
                                                                f"<b>• DISTRITO</b> ➟ <code>{distrito1}</code>\n"
                                                                f"<b>• DIRECCION</b> ➟ <code>{direcion}</code>\n\n"

                                                                f"〔🔅〕UBIGEO\n\n"

                                                                f"<b>• UBIGEO RENIEC</b> ➟ <code>{UbigeoReniec}</code>\n"
                                                                f"<b>• UBIGEO INEI</b> ➟ <code>{UbigeoInei}</code>\n"
                                                                f"<b>• UBIGEO GENERAL</b> ➟<code>{UbigeoSunat}</code>\n\n"

                                                                
                                                                f"<b>💰 Credits : </b> <code>{valor_cred}</code>\n"
                                                                f"<b>🔥 Rango : </b> {plan}\n"
                                                                f"<b>🎖 Solicitado Por:</b>  <a href='tg://user?id={huserid}'>{usernombre}</a>"
                                        ,parse_mode="html",reply_to_message_id=message.message_id)

                                    
                                    ruta_imagen = "./FOTOS_RE/foto1.jpg"


                                    if os.path.exists(ruta_imagen):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen)
                                        print(f"Archivo {ruta_imagen} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen} no existe.")

                                    





                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                #Mensaje de error
                                error_message = f"📢 ¡Ups! El servicio de RENIEC no está disponible  prueba otro comando  con /cmd.⚠️ "

                                # Enviar mensaje de error al chat de Telegram
                                bot.reply_to(message, error_message, parse_mode="html")

                        else:



                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/dni] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/dni 44444444]", parse_mode="html")
                else:



                    markup1 = types.InlineKeyboardMarkup(row_width= 3)
                    a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR" )
                    markup1.add(a1)



                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")




        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["dnif", "DNIF"])
def cmd_dni(message):










    dni1 = "".join(message.text.split()[1:2])


    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/dnif 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):


            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/dnif"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:
                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰"  ,url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [DNI] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3


                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"


                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("CONSULTNADO DNIF")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")


                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta.get("nuDni","")
                                    apePaterno = respuesta.get("apePaterno","")
                                    apeMaterno = respuesta.get("apeMaterno","")
                                    preNombres = respuesta.get("preNombres","")
                                    edad = respuesta.get("nuEdad","")
                                    sexo = respuesta.get("sexo","")

                                    fecha_nacimiento = respuesta.get("feNacimiento","")
                                    departamento = respuesta.get("departamento","")
                                    provincia = respuesta.get("provincia","")
                                    distrito = respuesta.get("distrito","")

                                    estado_civil = respuesta.get("estadoCivil","")
                                    grado_instituto = respuesta.get("gradoInstruccion","")
                                    estatura = respuesta.get("estatura","")
                                    fecha_incricion = respuesta.get("feInscripcion","")
                                    fecha_emision = respuesta.get("feEmision","")
                                    fecha_caducida = respuesta.get("feCaducidad","")
                                    restrincion = respuesta.get("deRestriccion","")
                                    dniPadre = respuesta.get("nuDocPadre","")
                                    dniMadre = respuesta.get("nuDocMadre","")

                                    
                                    padre = respuesta.get("nomPadre","")
                                    madre = respuesta.get("nomMadre","")

                                    departamento1 = respuesta.get("depaDireccion","")
                                    provincia1 = respuesta.get("provDireccion","")
                                    distrito1 = respuesta.get("distDireccion","")
                                    direcion = respuesta.get("desDireccion","")
                                    feFallecimiento = respuesta.get("feFallecimiento","")
                        
                                    UbigeoInei = respuesta["UbigeoInei"]
                                    UbigeoReniec = respuesta["UbigeoReniec"]
                                    UbigeoSunat = respuesta['UbigeoSunat']

                                    # Leer el JSON desde el archivo
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)




                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/fotos0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    foto_codificada = respuesta["firma"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/fotos1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))



                                    foto_codificada = respuesta["Hizquierda"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/fotos2.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    
                                    foto_codificada = respuesta["Hderecha"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/fotos3.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))


                                    

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"
                
                                    else:
                                        valor_cred = drgon

                                    Servicio = "RENIEC"
                                    Comando = "/dnif"
                                   


                                    media_group = []
                                    text = (f"<b>[#DataGold🌩] - RENIEC Nº1 ONLINE</b>\n\n"
                                            f"<b>• DNI</b> ➟ <code>{nuDni}</code>\n"
                                            f"<b>• NOMBRE</b> ➟ <code>{preNombres}</code>\n"
                                            f"<b>• APELLIDO PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                            f"<b>• APELLIDO MATERNO</b> ➟ <code>{apeMaterno}</code>\n"
                                            f"<b>• SEXO</b> ➟ <code>{sexo}</code>\n\n"
                                                                
                                            f"NACIMIENTO 〔📅〕\n\n"

                                            f"<b>• FECHA NACIMIENTO</b> ➟ <code>{fecha_nacimiento}</code>\n"
                                            f"<b>• EDAD</b> ➟ <code>{edad}</code>\n"
                                            f"<b>• DEPARTAMENTO</b> ➟ <code>{departamento}</code>\n"
                                            f"<b>• PROVINCIA</b> ➟ <code>{provincia}</code>\n"
                                            f"<b>• DISTRITO</b> ➟ <code>{distrito}</code>\n\n"

                                            f"INFORMACION 〔💁‍♂️〕\n\n"

                                            f"<b>• GRADO INSTRUCCION</b> ➟ <code>{grado_instituto}</code>\n"
                                            f"<b>• ESTADO CIVIL</b> ➟ <code>{estado_civil}</code>\n"
                                            f"<b>• ESTATURA</b> ➟ <code>{estatura}</code>\n"
                                            f"<b>• FECHA INSCRIPCION</b> ➟ <code>{fecha_incricion}</code>\n"
                                            f"<b>• FECHA EMISION</b> ➟ <code>{fecha_emision}</code>\n"
                                            f"<b>• FECHA CADUCIDAD</b> ➟ <code>{fecha_caducida}</code>\n"
                                            f"<b>• FECHA FALLECIMIENTO</b> ➟ <code>{feFallecimiento}</code>\n"                                            
                                            f"<b>• RESTRICCION</b> ➟ <code>{restrincion}</code>\n\n"

                                            f"PADRES 〔👨‍👩‍👦‍👦〕\n\n"

                                            

                                            f"<b>• DNI</b> ➟ <code></code>\n"
                                            f"<b>• PADRE</b> ➟ <code>{padre}</code>\n\n"

                                            f"<b>• DNI</b> ➟ <code></code>\n"
                                            f"<b>• MADRE</b> ➟ <code>{madre}</code>\n\n"

                                            f"UBICACION 〔📍〕\n\n"

                                            f"<b>• DEPARTAMENTO</b> ➟ <code>{departamento1}</code>\n"
                                            f"<b>• PROVINCIA</b> ➟ <code>{provincia1}</code>\n"
                                            f"<b>• DISTRITO</b> ➟ <code>{distrito1}</code>\n"
                                            f"<b>• DIRECCION</b> ➟ <code>{direcion}</code>\n\n"

                                            f"UBIGEO 〔📍〕\n\n"

                                            f"<b>• UBIGEO RENIEC</b> ➟ <code>{UbigeoReniec}</code>\n"
                                            f"<b>• UBIGEO INEI</b> ➟ <code>{UbigeoInei}</code>\n"
                                            f"<b>• UBIGEO GENERAL</b> ➟<code>{UbigeoSunat}</code>\n\n"


                                            
                                            f"<b>💰 Credits : </b> <code>{valor_cred}</code>\n"
                                            f"<b>🔥 Rango : </b> {plan}\n"
                                            f"<b>🎖 Solicitado Por:</b>  <a href='tg://user?id={huserid}'>{usernombre}</a>"
                                    )


                                    for num in range(4):
                                        media_group.append(InputMediaPhoto(open(f'./FOTOS_RE/fotos%d.jpg' % num, 'rb'),caption = text if num == 0 else '', parse_mode="html"))

                    

                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)




                                    bot.send_chat_action(message.chat.id, "upload_photo")
                                    #bot.send_media_group(message.chat.id, media=media_group)
                                    bot.send_media_group(chat_id=message.chat.id, media=media_group,reply_to_message_id=message.message_id)


                                    ruta_imagen0 = "./FOTOS_RE/fotos0.jpg"
                                    ruta_imagen1 = "./FOTOS_RE/fotos1.jpg"
                                    ruta_imagen2 = "./FOTOS_RE/fotos2.jpg"
                                    ruta_imagen3 = "./FOTOS_RE/fotos3.jpg"


                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                        os.remove(ruta_imagen3)
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")





                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                # Mensaje de error
                                error_message = f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO"

                                                        # Enviar mensaje de error al chat de Telegram
                                bot.reply_to(message, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/dnif] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/dnif 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")




@bot.message_handler(commands=["c4tr","C4"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])
    user_id = message.from_user.id
    

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/c4tr 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/c4tr"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:
                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,  url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [C4TR] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥" ,url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"
                            



                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("hacienod l consulta ")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")


                                else:
                                    
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta["nuDni"]
                                    apePaterno = respuesta["apePaterno"]
                                    apeMaterno = respuesta["apeMaterno"]
                                    preNombres = respuesta["preNombres"]

                                    sexo = respuesta["sexo"]

                                    fecha_nacimiento = respuesta["feNacimiento"]


                                    estado_civil = respuesta["estadoCivil"]
                                    grado_instituto = respuesta["gradoInstruccion"]
                                    estatura = respuesta["estatura"]
                                    fecha_incricion = respuesta["feInscripcion"]

                                    fecha_caducida = respuesta["feCaducidad"]

                                    direcion = respuesta["desDireccion"]
                                    UbigeoInei = "000"
                                    UbigeoReniec ="000"



                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    foto_codificada = respuesta["firma"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))






                                    imagen_fondo = Image.open(f'./C4TR/certificado_inscripcio_HD.jpg')

                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni1}0.jpg')


                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (844,1200) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)


                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (840, 2550) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni1}1.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (500,350) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)


                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (2300, 2900) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)


                                    dibujar = ImageDraw.Draw(imagen_fondo)

                                    #SOLICITUD N

                                    texto1 = f"100595"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1000, 1080)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #DNI
                                    texto1 = f"{nuDni}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (800, 1390)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)                    



                                    #NOMBRE
                                    texto1 = f"{preNombres} {apePaterno} {apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (830, 1470)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #NACIMIENTO



                                    texto1 = f"{fecha_nacimiento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 1610)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #SEXO

                                    texto1 = f"{sexo}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 1690)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #ESTADO CIVIL

                                    texto1 = f"{estado_civil}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 1770)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #FECHA DE INSCRICION

                                    texto1 = f"{fecha_incricion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 1850)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)






                                    #UBIGEO DOMICILIO

                                    texto1 = f"{UbigeoReniec}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 1925)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #DOMICILIO

                                    texto1 = f"{direcion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 2000)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #FECHA DE CADUCIDA

                                    texto1 = f"{fecha_caducida}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 2080)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #RESOLCUION

                                    texto1 = f"**"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 2150)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)










                                    #FECHA DE RESTRINCION

                                    texto1 = f"**"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1120, 2270)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #ESTATURA

                                    texto1 = f"{estatura} M"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2190, 1610)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #GRAODO DE INSTITUCION 

                                    texto1 = f"{grado_instituto}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2190, 1690)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)






                                    #DOC SUSTENTO 

                                    texto1 = f"**"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2190, 1770)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #DOC UBIGEO 

                                    texto1 = f"{UbigeoInei}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2190, 1850)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    import datetime
                                    # Obtener la fecha y hora actual
                                    fecha_actual = datetime.datetime.now()

                                    # Obtener el número del mes actual
                                    mes_actual = fecha_actual.month

                                    # Obtener el nombre del mes actual
                                    nombres_meses = {
                                        1: "enero",
                                        2: "febrero",
                                        3: "marzo",
                                        4: "abril",
                                        5: "mayo",
                                        6: "junio",
                                        7: "julio",
                                        8: "agosto",
                                        9: "septiembre",
                                        10: "octubre",
                                        11: "noviembre",
                                        12: "diciembre"
                                    }
                                    nombre_mes_actual = nombres_meses.get(mes_actual)

                                    texto1 = f"Expedido en Reniec a los 7 dias del mes de {nombre_mes_actual} del 2024"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (560, 4020)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    # EXPIDE
                                    texto1 = f"{preNombres} {apePaterno} {apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (720, 4320)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    texto1 = f"https://serviciosportal.reniec.gob.pe/verifiaciongr"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (910, 5310)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    texto1 = f"85114.879751.500138"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (910, 5380)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 49)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)







                                    texto1 = f"1 de 1"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (910, 5460)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 49)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    texto1 = f"{preNombres} {apePaterno} {apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (910, 5530)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 49)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    texto1 = f"{nuDni}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (910, 5610)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 49)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)






                                    # Obtener la fecha actual
                                    fecha_actual = datetime.date.today()

                                    # Retroceder 14 días
                                    fecha_retrocedida = fecha_actual - datetime.timedelta(days=7)






                                    hora_actualPM = datetime.datetime.now().strftime("%I:%M:%S %p")









                                    texto1 = f"{fecha_retrocedida} {hora_actualPM}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (910, 5685)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 49)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)










                                    # Guarda la imagen con el texto agregado
                                    imagen_fondo.save(f'./C4TR/{dni1}.jpg')




                                    # Cargar la imagen
                                    img = Image.open(f'./C4TR/{dni1}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./C4TR/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./C4TR/{dni1}.jpg', 0, 0)

                                    # Guardar el archivo PDF
                                    pdf.save()

                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"




                                    # Leer el JSON desde el archivo
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)




                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"
                
                                    else:
                                        valor_cred = drgon


                                    Servicio = "RENIEC"
                                    Comando = "/c4tr"
                                

                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./C4TR/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] FICHA C4TR </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)










                                    ruta_imagen0 = f"./FOTOS_RE/{dni2}0.jpg"
                                    ruta_imagen1 = f"./FOTOS_RE/{dni2}1.jpg"
                                    ruta_imagen2 = F"./C4TR/{dni1}.pdf"
                                    #ruta_imagen3 = "./FOTOS_RE/fotos3.jpg"
                                    ruta_imagen4 = f"./C4TR/{dni1}.jpg"

                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                        #os.remove(ruta_imagen3)
                                        os.remove(ruta_imagen4)                                        
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")









                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                # Mensaje de error
                                error_message = f"[📢] El servicio de RENIEC no está disponible en este momento."

                                                        # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")
                                


                                
                                
                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/c4tr] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/c4tr 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")
                

                    
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")




@bot.message_handler(commands=["c4","C4"])
def cmd_dni(message):









    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/c4 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):


            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/c4"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:
                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰"   ,url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [C4] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/+6LVDDgEHWStlMTQx" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"


                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }



                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")


                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta.get("nuDni","")
                                    apePaterno = respuesta.get("apePaterno","")
                                    apeMaterno = respuesta.get("apeMaterno","")
                                    preNombres = respuesta.get("preNombres","")
                                    edad = respuesta.get("nuEdad","")
                                    sexo = respuesta.get("sexo","")

                                    fecha_nacimiento = respuesta.get("feNacimiento","")
                                    departamento = respuesta.get("departamento","")
                                    provincia = respuesta.get("provincia","")
                                    distrito = respuesta.get("distrito","")

                                    estado_civil = respuesta.get("estadoCivil","")
                                    grado_instituto = respuesta.get("gradoInstruccion","")
                                    estatura = respuesta.get("estatura","")
                                    fecha_incricion = respuesta.get("feInscripcion","")
                                    fecha_emision = respuesta.get("feEmision","")
                                    fecha_caducida = respuesta.get("feCaducidad","")
                                    restrincion = respuesta.get("deRestriccion","")
                                    dniPadre = respuesta.get("nuDocPadre","")
                                    dniMadre = respuesta.get("nuDocMadre","")

                                    
                                    padre = respuesta.get("nomPadre","")
                                    madre = respuesta.get("nomMadre","")

                                    departamento1 = respuesta.get("depaDireccion","")
                                    provincia1 = respuesta.get("provDireccion","")
                                    distrito1 = respuesta.get("distDireccion","")
                                    direcion = respuesta.get("desDireccion","")
                                    feFallecimiento = respuesta.get("feFallecimiento","")
                                    #UbigeoInei = "000"
                                    #UbigeoReniec = "000"

                                    UbigeoInei = respuesta["UbigeoInei"]
                                    UbigeoReniec = respuesta["UbigeoReniec"]
                                    #UbigeoSunat = respuesta['UbigeoSunat']






                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    foto_codificada = respuesta["firma"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))



                                    foto_codificada = respuesta["Hizquierda"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}2.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    
                                    foto_codificada = respuesta["Hderecha"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}3.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))













                                    # Abre ambas imágenes
                                    imagen_fondo = Image.open(f'./C4/c4.jpg')
                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}0.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (150,200) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (630, 255) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)

                                    #firma


                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}1.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (220,100) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (595, 530) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)


                                    #huella derecha




                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}3.jpg')
                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (150,180) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)
                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (630, 680) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    #huella izquierda


                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}2.jpg')                                    
                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (150,180) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (630, 910) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    # Crea un objeto ImageDraw para dibujar sobre la imagen
                                    dibujar = ImageDraw.Draw(imagen_fondo)

                                    #dni
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{nuDni}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 222)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 16)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #PRIMER APELLIDO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apePaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 252)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #SEGUNDO APELLIDO 
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 281)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #PRENOMBRES
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{preNombres}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 312)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #GENERO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{sexo}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 342)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)






                                    #FECHA NACIMIENTO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_nacimiento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 421)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #DEPARTAMENTO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{departamento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 451)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #PROVINCIA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{provincia}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 478)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #DISTRITO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{distrito}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 505)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #GRADO DE INTRUCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{grado_instituto}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 560)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #ESTADO CIVIL
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{estado_civil}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 588)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #ESTATURA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{estatura}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 616)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #FECHA DE INSCRIPCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_incricion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 646)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)






                                    #FECHA DE EMICION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_emision}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 678)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #FECHA DE CADUCIDA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_caducida}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 708)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #NOMBRE DEL PADRE
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{padre}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 763)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #NOMBRE DEL MADRE
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{madre}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 793)

                                    #Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)


                                    #RESTRINCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{restrincion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 823)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)







                                    #DEPARTAMENTO1
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{departamento1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 910)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #PROVINCIA1
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{provincia1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 940)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #DISTRITO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{distrito1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 970)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)







                                    texto1 = f"{direcion}"

                                    longitud_linea = 30  # Define la longitud deseada de la línea
                                        
                                    lineas = []
                                    palabras = texto1.split()
                                    linea_actual = ""

                                    for palabra in palabras:
                                        if len(linea_actual) + len(palabra) + 1 <= longitud_linea:
                                            if linea_actual:
                                                linea_actual += " "
                                            linea_actual += palabra
                                        else:
                                            lineas.append(linea_actual)
                                            linea_actual = palabra

                                    if linea_actual:
                                        lineas.append(linea_actual)

                                    texto_formateado = "\n".join(lineas)
                                    #print(texto_formateado)
                                    #DIRECCION
                                    # Define la ubicación y el texto a agregar
                                    texto2 = f"{texto_formateado}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 1005)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto2, fill=(255, 255, 255), font=fuente1)




















                                    # Guarda la imagen con el texto agregado
                                    imagen_fondo.save(f'./C4/{dni1}.jpg')



                                    "segundo"
                                    # Cargamos la imagen

                    

                                    # Cargar la imagen
                                    img = Image.open(f'./C4/{dni1}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./C4/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./C4/{dni1}.jpg', 0, 0)

                                    # Guardar el archivo PDF
                                    pdf.save()



                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "RENIEC"
                                    Comando = "/c4"
                                    

                                    #thumbnail sirve enviar el pdf con foto 

                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./C4/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] FICHA C4 </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)


                                    ruta_imagen0 = f"./FOTOS_RE/{dni2}0.jpg"
                                    ruta_imagen1 = f"./FOTOS_RE/{dni2}1.jpg"
                                    ruta_imagen2 = f"./FOTOS_RE/{dni2}2.jpg"
                                    ruta_imagen3 = f"./FOTOS_RE/{dni2}3.jpg"
                                    ruta_imagen4 = f"./C4/{dni1}.jpg"
                                    ruta_imagen5 = f"./C4/{dni1}.pdf"

                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                        os.remove(ruta_imagen3)
                                        os.remove(ruta_imagen4)
                                        os.remove(ruta_imagen5)                                                                                  
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")









                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                # Mensaje de error
                                error_message = f"[📢] El servicio de RENIEC no está disponible en este momentos. "

                                                        # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/c4] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/c4 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["c4a", "C4a"])
def cmd_dni(message):











    dni1 = "".join(message.text.split()[1:2])


    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/c4a 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):





            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/c4a"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [C4A] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5


                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"http://161.132.47.189:5000/buscardniaux/={dni1}"


                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("C4A")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")


                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta.get("nuDni","")
                                    apePaterno = respuesta.get("apePaterno","")
                                    apeMaterno = respuesta.get("apeMaterno","")
                                    preNombres = respuesta.get("preNombres","")
                                    edad = respuesta.get("nuEdad","")
                                    sexo = respuesta.get("sexo","")

                                    fecha_nacimiento = respuesta.get("feNacimiento","")
                                    departamento = respuesta.get("departamento","")
                                    provincia = respuesta.get("provincia","")
                                    distrito = respuesta.get("distrito","")

                                    estado_civil = respuesta.get("estadoCivil","")
                                    grado_instituto = respuesta.get("gradoInstruccion","")
                                    estatura = respuesta.get("estatura","")
                                    fecha_incricion = respuesta.get("feInscripcion","")
                                    fecha_emision = respuesta.get("feEmision","")
                                    fecha_caducida = respuesta.get("feCaducidad","")
                                    restrincion = respuesta.get("deRestriccion","")
                                    dniPadre = respuesta.get("nuDocPadre","")
                                    dniMadre = respuesta.get("nuDocMadre","")

                                    
                                    padre = respuesta.get("nomPadre","")
                                    madre = respuesta.get("nomMadre","")

                                    departamento1 = respuesta.get("depaDireccion","")
                                    provincia1 = respuesta.get("provDireccion","")
                                    distrito1 = respuesta.get("distDireccion","")
                                    direcion = respuesta.get("desDireccion","")
                                    feFallecimiento = respuesta.get("feFallecimiento","")
                        
                                    #UbigeoInei = respuesta["UbigeoInei"]
                                    #  UbigeoReniec = respuesta["UbigeoReniec"]


                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    foto_codificada = respuesta["firma"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))



                                    foto_codificada = respuesta["Hizquierda"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}2.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    
                                    foto_codificada = respuesta["Hderecha"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}3.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))




                                    # Abre ambas imágenes
                                    imagen_fondo = Image.open(f'./C4A/C4_AZUL_NUEVO.jpg')
                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}0.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (900,1050) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (3250, 1020) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)

                                    #firma


                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}1.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (1220,450) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (3070, 2300) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)


                                    #huella derecha




                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}3.jpg')
                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (720,910) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)
                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (3310, 2960) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    #huella izquierda


                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}2.jpg')                                    
                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (720,910) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (3310, 4050) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    # Crea un objeto ImageDraw para dibujar sobre la imagen
                                    dibujar = ImageDraw.Draw(imagen_fondo)

                                    #dni
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{nuDni}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1075)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 80)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #PRIMER APELLIDO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apePaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1220)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #SEGUNDO APELLIDO 
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1360)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #PRENOMBRES
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{preNombres}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1530)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #GENERO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{sexo}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1665)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)






                                    #FECHA NACIMIENTO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_nacimiento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 2055)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #DEPARTAMENTO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{departamento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 2199)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #PROVINCIA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{provincia}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 2340)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #DISTRITO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{distrito}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 2475)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #GRADO DE INTRUCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{grado_instituto}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 2740)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    #ESTADO CIVIL
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{estado_civil}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 2880)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #ESTATURA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{estatura}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 3010)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #FECHA DE INSCRIPCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_incricion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 3160)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)






                                    #FECHA DE EMICION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_emision}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 3320)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #FECHA DE CADUCIDA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_caducida}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 3460)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #NOMBRE DEL PADRE
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{padre}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 3735)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                    #NOMBRE DEL MADRE
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{madre}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 3880)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)


                                    #RESTRINCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{restrincion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 4025)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)







                                    #DEPARTAMENTO1
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{departamento1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 4445)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #PROVINCIA1
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{provincia1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 4590)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #DISTRITO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{distrito1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 4745)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)


                                    texto1 = f"{direcion}"

                                    longitud_linea = 30  # Define la longitud deseada de la línea
                                        
                                    lineas = []
                                    palabras = texto1.split()
                                    linea_actual = ""

                                    for palabra in palabras:
                                        if len(linea_actual) + len(palabra) + 1 <= longitud_linea:
                                            if linea_actual:
                                                linea_actual += " "
                                            linea_actual += palabra
                                        else:
                                            lineas.append(linea_actual)
                                            linea_actual = palabra

                                    if linea_actual:
                                        lineas.append(linea_actual)

                                    texto_formateado = "\n".join(lineas)

                                    #DIRECCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{texto_formateado}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 4920)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                    # Guarda la imagen con el texto agregado
                                    imagen_fondo.save(f'./C4A/{dni1}.jpg')

                                    # Cargar la imagen
                                    img = Image.open(f'./C4A/{dni1}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./C4A/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./C4A/{dni1}.jpg', 0, 0)



                                    pdf.save()

                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"

                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "RENIEC"
                                    Comando = "/c4a"
                                   

                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./C4A/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] FICHA AZUL C4A</b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                    
                                    ruta_imagen0 = f"./FOTOS_RE/{dni2}0.jpg"
                                    ruta_imagen1 = f"./FOTOS_RE/{dni2}1.jpg"
                                    ruta_imagen2 = f"./FOTOS_RE/{dni2}2.jpg"
                                    ruta_imagen3 = f"./FOTOS_RE/{dni2}3.jpg"
                                    ruta_imagen4 = f"./C4A/{dni1}.jpg"
                                    ruta_imagen5 = f"./C4A/{dni1}.pdf"

                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                        os.remove(ruta_imagen3)
                                        os.remove(ruta_imagen4)
                                        os.remove(ruta_imagen5)                                                                                  
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")


                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/c4a] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/c4a 44444444]", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")

            
@bot.message_handler(commands=["c4b", "C4b"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])


    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/c4b 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):




            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/c4b"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [C4b] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    
                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"


                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("DNIF")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")


                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta.get("nuDni","")
                                    apePaterno = respuesta.get("apePaterno","")
                                    apeMaterno = respuesta.get("apeMaterno","")
                                    preNombres = respuesta.get("preNombres","")
                                    edad = respuesta.get("nuEdad","")
                                    sexo = respuesta.get("sexo","")

                                    fecha_nacimiento = respuesta.get("feNacimiento","")
                                    departamento = respuesta.get("departamento","")
                                    provincia = respuesta.get("provincia","")
                                    distrito = respuesta.get("distrito","")

                                    estado_civil = respuesta.get("estadoCivil","")
                                    grado_instituto = respuesta.get("gradoInstruccion","")
                                    estatura = respuesta.get("estatura","")
                                    fecha_incricion = respuesta.get("feInscripcion","")
                                    fecha_emision = respuesta.get("feEmision","")
                                    fecha_caducida = respuesta.get("feCaducidad","")
                                    restrincion = respuesta.get("deRestriccion","")
                                    dniPadre = respuesta.get("nuDocPadre","")
                                    dniMadre = respuesta.get("nuDocMadre","")

                                    
                                    padre = respuesta.get("nomPadre","")
                                    madre = respuesta.get("nomMadre","")

                                    departamento1 = respuesta.get("depaDireccion","")
                                    provincia1 = respuesta.get("provDireccion","")
                                    distrito1 = respuesta.get("distDireccion","")
                                    direcion = respuesta.get("desDireccion","")
                                    feFallecimiento = respuesta.get("feFallecimiento","")
                        
                                    #UbigeoInei = respuesta["UbigeoInei"]
                                    #  UbigeoReniec = respuesta["UbigeoReniec"]





                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    foto_codificada = respuesta["firma"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))



                                    foto_codificada = respuesta["Hizquierda"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}2.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    
                                    foto_codificada = respuesta["Hderecha"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}3.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))









                                    # Abre ambas imágenes
                                    imagen_fondo = Image.open("./C4B/Ficha_reniec.jpg").convert("RGBA")
                                    imagen_superpuesta = Image.open(f"./FOTOS_RE/{dni2}0.jpg").convert("RGBA")


                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (350, 450)  # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    posicion = (1560, 540)

                                    # Superponer la imagen de la firma redimensionada en la imagen base
                                    imagen_fondo.paste(imagen_superpuesta, posicion, mask=imagen_superpuesta)

                                    #FIRMA

                                    # Cargar la imagen con fondo transparente (firma)
                                    firma_transparente = Image.open(f'./FOTOS_RE/{dni2}1.jpg').convert("RGBA")

                                    # Especificar el tamaño deseado para la firma
                                    nuevo_tamano = (300,290)

                                    imagen_superpuesta = firma_transparente.resize(nuevo_tamano)

                                    # Separar la imagen de la firma en sus componentes RGBA
                                    
                                    # Especificar la posición donde deseas superponer la firma en la imagen base
                                    posicion = (1590, 1190)

                                    # Superponer la imagen de la firma redimensionada en la imagen base
                                    imagen_fondo.paste(imagen_superpuesta, posicion, mask=imagen_superpuesta)



                                    #HUELLA IZQUIERDA

                                    # Cargar la imagen con fondo transparente (firma)
                                    firma_transparente = Image.open(f'./FOTOS_RE/{dni2}2.jpg').convert("RGBA")

                                    # Especificar el tamaño deseado para la firma
                                    nuevo_tamano = (300,290)

                                    # Redimensionar la imagen de la firma al nuevo tamaño
                                    imagen_superpuesta = firma_transparente.resize(nuevo_tamano)

                                    # Especificar la posición donde deseas superponer la firma en la imagen base
                                    posicion = (1590, 1600)
                                    mascara_transparencia = imagen_superpuesta.split()[3]#cambiar


                                    # Superponer la imagen de la firma redimensionada en la imagen base
                                    imagen_fondo.paste(mascara_transparencia, posicion, mask=mascara_transparencia)




                                    #HUELLA DERECHA

                                    # Cargar la imagen con fondo transparente (firma)
                                    firma_transparente = Image.open(f'./FOTOS_RE/{dni2}3.jpg').convert("RGBA")

                                    # Especificar el tamaño deseado para la firma
                                    nuevo_tamano = (300,290)

                                    # Redimensionar la imagen de la firma al nuevo tamaño
                                    imagen_superpuesta = firma_transparente.resize(nuevo_tamano)

                                    # Especificar la posición donde deseas superponer la firma en la imagen base
                                    posicion = (1590, 2200)

                                    mascara_transparencia = imagen_superpuesta.split()[3]#cambiar

                                    # Superponer la imagen de la firma redimensionada en la imagen base
                                    imagen_fondo.paste(mascara_transparencia, posicion, mask=mascara_transparencia)


                                    #######################################################################
                                    dibujar = ImageDraw.Draw(imagen_fondo)


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{nuDni}"
                                    ubicacion1 = (950, 480)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apePaterno}"
                                    ubicacion1 = (950, 535)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apeMaterno}"
                                    ubicacion1 = (950, 590)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{preNombres}"
                                    ubicacion1 = (950, 645)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{sexo}"
                                    ubicacion1 = (950, 695)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_nacimiento}"
                                    ubicacion1 = (950, 750)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # DEPARTAMIENTO DE NACMIENTO 
                                    texto1 = f"{departamento}"
                                    ubicacion1 = (950, 820)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    # PROVINCIA DE NACMIENTO 
                                    texto1 = f"{provincia}"
                                    ubicacion1 = (950, 885)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # DISTRITO DE NACMIENTO 
                                    texto1 = f"{distrito}"
                                    ubicacion1 = (950, 935)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    # GRADO 
                                    texto1 = f"{grado_instituto}"
                                    ubicacion1 = (950, 993)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    # GRADO 
                                    texto1 = f"{estado_civil}"
                                    ubicacion1 = (950, 1050)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    # STATURA 
                                    texto1 = f"{estatura}"
                                    ubicacion1 = (950, 1105)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # FECHA INCRIPCIPN 
                                    texto1 = f"{fecha_incricion}"
                                    ubicacion1 = (950, 1160)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    # NOMBRE  DEL PADRE
                                    texto1 = f"{padre}"
                                    ubicacion1 = (950, 1215)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    # NOMBRE  DEL MADRE
                                    texto1 = f"{madre}"
                                    ubicacion1 = (950, 1270)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    # FECHA EMISION
                                    texto1 = f"{fecha_emision}"
                                    ubicacion1 = (950, 1320)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    # RESTRINVIONES 
                                    texto1 = f"{restrincion}"
                                    ubicacion1 = (950, 1375)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    # DEPARTAMENTO DE DOMICILIO
                                    texto1 = f"{departamento1}"
                                    ubicacion1 = (950, 1428)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    # PROVINCIA DE DOMICILIO
                                    texto1 = f"{provincia1}"
                                    ubicacion1 = (950, 1485)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    # DISTRITO DE DOMICILIO
                                    texto1 = f"{distrito1}"
                                    ubicacion1 = (950, 1537)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    texto1 = f"{direcion}"

                                    longitud_linea = 30  # Define la longitud deseada de la línea
                                        
                                    lineas = []
                                    palabras = texto1.split()
                                    linea_actual = ""

                                    for palabra in palabras:
                                        if len(linea_actual) + len(palabra) + 1 <= longitud_linea:
                                            if linea_actual:
                                                linea_actual += " "
                                            linea_actual += palabra
                                        else:
                                            lineas.append(linea_actual)
                                            linea_actual = palabra

                                    if linea_actual:
                                        lineas.append(linea_actual)

                                    texto_formateado = "\n".join(lineas)




                                    # DIRRECION
                                    texto1 = f"{texto_formateado}"
                                    ubicacion1 = (950, 1590)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # FECHA  DE CADUCIDA FINAL
                                    texto1 = f"{fecha_caducida}"
                                    ubicacion1 = (950, 1692)  # x = alcostado  Y= arriba abajo
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 33)
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # Guardar la imagen resultante
                                    imagen_fondo.save(f"./C4B/{dni1}.png")


                                    




                                    # Cargar la imagen
                                    img = Image.open(f'./C4B/{dni1}.png')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./C4B/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./C4B/{dni1}.png', 0, 0)



                                    pdf.save()

                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"

                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "RENIEC"
                                    Comando = "/c4b"
                                    


                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./C4B/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] FICHA BLANCA C4B</b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)

                                    ruta_imagen0 = f"./FOTOS_RE/{dni2}0.jpg"
                                    ruta_imagen1 = f"./FOTOS_RE/{dni2}1.jpg"
                                    ruta_imagen2 = f"./FOTOS_RE/{dni2}2.jpg"
                                    ruta_imagen3 = f"./FOTOS_RE/{dni2}3.jpg"
                                    ruta_imagen4 = f"./C4B/{dni1}.png"
                                    ruta_imagen5 = f"./C4B/{dni1}.pdf"

                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                        os.remove(ruta_imagen3)
                                        os.remove(ruta_imagen4)
                                        os.remove(ruta_imagen5)                                                                                  
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")



                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                # Mensaje de error
                                error_message = f"[📢] ¡Ups! El servicio de RENIEC no está disponible en este momento."

                                # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/c4b] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/c4b 44444444]", parse_mode="html")
                else:
                    
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")
                
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["c4c","C4C"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/c4c 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):







            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/c4c"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:
                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [C4C] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"



                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("hacienod l consulta ")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 

                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")


                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta.get("nuDni","")
                                    apePaterno = respuesta.get("apePaterno","")
                                    apeMaterno = respuesta.get("apeMaterno","")
                                    preNombres = respuesta.get("preNombres","")
                                    edad = respuesta.get("nuEdad","")
                                    sexo = respuesta.get("sexo","")

                                    fecha_nacimiento = respuesta.get("feNacimiento","")
                                    departamento = respuesta.get("departamento","")
                                    provincia = respuesta.get("provincia","")
                                    distrito = respuesta.get("distrito","")

                                    estado_civil = respuesta.get("estadoCivil","")
                                    grado_instituto = respuesta.get("gradoInstruccion","")
                                    estatura = respuesta.get("estatura","")
                                    fecha_incricion = respuesta.get("feInscripcion","")
                                    fecha_emision = respuesta.get("feEmision","")
                                    fecha_caducida = respuesta.get("feCaducidad","")
                                    restrincion = respuesta.get("deRestriccion","")
                                    dniPadre = respuesta.get("nuDocPadre","")
                                    dniMadre = respuesta.get("nuDocMadre","")

                                    
                                    padre = respuesta.get("nomPadre","")
                                    madre = respuesta.get("nomMadre","")

                                    departamento1 = respuesta.get("depaDireccion","")
                                    provincia1 = respuesta.get("provDireccion","")
                                    distrito1 = respuesta.get("distDireccion","")
                                    direcion = respuesta.get("desDireccion","")
                                    feFallecimiento = respuesta.get("feFallecimiento","")
                                    #UbigeoInei = "000"
                                    #UbigeoReniec = "000"

                                    UbigeoInei = respuesta["UbigeoInei"]
                                    UbigeoReniec = respuesta["UbigeoReniec"]
                                    #UbigeoSunat = respuesta['UbigeoSunat']






                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    foto_codificada = respuesta["firma"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))



                                    foto_codificada = respuesta["Hizquierda"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}2.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    
                                    foto_codificada = respuesta["Hderecha"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}3.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))













                                    # Abre ambas imágenes
                                    imagen_fondo = Image.open(f'./C4C/c4blan.jpg')
                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}0.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (150,200) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (630, 255) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)

                                    #firma


                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}1.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (220,100) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (595, 530) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)


                                    #huella derecha




                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}3.jpg')
                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (150,180) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)
                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (630, 680) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    #huella izquierda


                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni2}2.jpg')                                    
                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (150,180) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (630, 910) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    # Crea un objeto ImageDraw para dibujar sobre la imagen
                                    dibujar = ImageDraw.Draw(imagen_fondo)

                                    #dni
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{nuDni}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 222)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 16)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #PRIMER APELLIDO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apePaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 252)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #SEGUNDO APELLIDO 
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 281)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #PRENOMBRES
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{preNombres}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 312)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #GENERO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{sexo}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 342)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)






                                    #FECHA NACIMIENTO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_nacimiento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 421)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #DEPARTAMENTO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{departamento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 451)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #PROVINCIA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{provincia}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 478)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #DISTRITO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{distrito}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 505)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #GRADO DE INTRUCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{grado_instituto}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 560)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #ESTADO CIVIL
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{estado_civil}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 588)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #ESTATURA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{estatura}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 616)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #FECHA DE INSCRIPCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_incricion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 646)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)






                                    #FECHA DE EMICION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_emision}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 678)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #FECHA DE CADUCIDA
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_caducida}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 708)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #NOMBRE DEL PADRE
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{padre}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 763)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #NOMBRE DEL MADRE
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{madre}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 793)

                                    #Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #RESTRINCION
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{restrincion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 823)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)







                                    #DEPARTAMENTO1
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{departamento1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 910)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                    #PROVINCIA1
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{provincia1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 940)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #DISTRITO
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{distrito1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 970)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    texto1 = f"{direcion}"
                                    longitud_linea = 30  # Define la longitud deseada de la línea
                                    lineas = []
                                    palabras = texto1.split()
                                    linea_actual = ""

                                    for palabra in palabras:
                                        if len(linea_actual) + len(palabra) + 1 <= longitud_linea:
                                            if linea_actual:
                                                linea_actual += " "
                                            linea_actual += palabra
                                        else:
                                            lineas.append(linea_actual)
                                            linea_actual = palabra

                                    if linea_actual:
                                        lineas.append(linea_actual)

                                    texto_formateado = "\n".join(lineas)
                                    print(texto_formateado)
                                    #DIRECCION
                                    # Define la ubicación y el texto a agregar
                                    texto2 = f"{texto_formateado}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (290, 1005)
                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 15)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto2, fill=(0, 0, 0), font=fuente1)




















                                    # Guarda la imagen con el texto agregado
                                    imagen_fondo.save(f'./C4C/{dni1}.jpg')



                                    "segundo"
                                    # Cargamos la imagen

                    

                                    # Cargar la imagen
                                    img = Image.open(f'./C4C/{dni1}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./C4C/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./C4C/{dni1}.jpg', 0, 0)

                                    # Guardar el archivo PDF
                                    pdf.save()



                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    #thumbnail sirve enviar el pdf con foto 



                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "RENIEC"
                                    Comando = "/c4c"
                                    


                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./C4C/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] FICHA BLANCA C4C</b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                    ruta_imagen0 = f"./FOTOS_RE/{dni2}0.jpg"
                                    ruta_imagen1 = f"./FOTOS_RE/{dni2}1.jpg"
                                    ruta_imagen2 = f"./FOTOS_RE/{dni2}2.jpg"
                                    ruta_imagen3 = f"./FOTOS_RE/{dni2}3.jpg"
                                    ruta_imagen4 = f"./C4C/{dni1}.jpg"
                                    ruta_imagen5 = f"./C4C/{dni1}.pdf"

                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                        os.remove(ruta_imagen3)
                                        os.remove(ruta_imagen4)
                                        os.remove(ruta_imagen5)                                                                                  
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")

                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                # Mensaje de error
                                error_message = f"[📢] ¡Ups! El servicio de RENIEC no está disponible en este momento."

                                # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/c4c] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/c4c 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["dniv","DNIV"])
def cmd_dni(message):














    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/dniv 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):



            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/dniv"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return



            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [dniv] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")



                            url = f"https://sseeker.org/api/dnivir?token=acYrJNje9faCXv8I&dni={dni1}"
                            response = requests.get(url)

                            if response.status_code == 200:
                                data = response.json()

                                frontal_base64= data.get('frontal_base64')
                                posterior_base64 = data.get('posterior_base64')






                                # Guardar la imagen en un archivo con ruta dinámica

                                ruta_archivo = f"./DNIVIRTUAL/dni_frontal.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(frontal_base64))


                                ruta_archivo = f"./DNIVIRTUAL/dni_trasero.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(posterior_base64))






                                # Rutas de las dos imágenes que deseas agregar al PDF
                                ruta_imagen2 = f'./DNIVIRTUAL/dni_frontal.jpg'
                                ruta_imagen1 = f'./DNIVIRTUAL/dni_trasero.jpg'

                                # Cargar las imágenes
                                imagen1 = Image.open(ruta_imagen1)
                                imagen2 = Image.open(ruta_imagen2)

                                # Obtener dimensiones de las imágenes
                                width1, height1 = imagen1.size
                                width2, height2 = imagen2.size

                                # Determinar el espacio entre las imágenes
                                espacio_entre_imagenes = 50  # Ajusta este valor para controlar el espacio vertical entre las imágenes

                                # Determinar las dimensiones del nuevo documento PDF
                                pdf_width = max(width1, width2)
                                pdf_height = height1 + height2 + espacio_entre_imagenes

                                # Crear el archivo PDF
                                pdf = canvas.Canvas(f"./DNI_VIRTUAL/dni_generado{dni1}.pdf", pagesize=(pdf_width, pdf_height))

                                # Añadir la primera imagen al archivo PDF
                                pdf.drawInlineImage(ruta_imagen1, 0, height2 + espacio_entre_imagenes, width1, height1)

                                # Añadir la segunda imagen al archivo PDF debajo de la primera con el espacio entre ellas
                                pdf.drawInlineImage(ruta_imagen2, 0, 0, width2, height2)

                                # Guardar el archivo PDF
                                pdf.save()























                                
                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)


                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon



                                Servicio = "RENIEC"
                                Comando = "/dniv"
                                status = "200"
                               

                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)



                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./DNI_VIRTUAL/dni_generado{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] DNI VIRTUAL </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./DNI_VIRTUAL/dni_generado{dni1}.pdf"

                                if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo

                                        os.remove(ruta_imagen0)
                                    
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")


                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")


                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/dniv] seguido de un número de DNI de 8 dígitos \n\n➜ EJEMPLO: [/dniv 44444444]", parse_mode="html")







        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


comandos_nm = {}
@bot.message_handler(commands=["nm"])
def cmd_dni(message):














    dni1 = "".join(message.text.split()[1:2])

    user_id = message.from_user.id
    print(user_id)
    comandos_nm[user_id] = "/nm"






    parts = dni1.split('|')

    if not dni1:
        # Manejar el caso en que no se proporciona ningún argumento
        texto = '<b>[❗️] Formatos Válidos :</b>\n\n'
        texto +=f'<code>/nm Nombre(s)|Paterno|Materno</code>\n'
        texto +=f'<code>/nm Wilfer,Alfredo|Gonzalo|Sanchez</code>\n'
        texto +=f'<code>/nm Wilfer|De+la+cruz|Sanchez</code>\n'
        texto +=f'<code>/nm Wilfer|Gonzalo|De+la+cruz</code>\n'
        # ...
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")
    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):





            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/nm"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:
                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [nm] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3


                    if drgon < 0:
                        markup1 = types.InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")


                    else:
                        




                        try:


                            pre_nombres = parts[0].strip().replace(",", " ")
                            pre_nombres_minusculas = pre_nombres.lower()
                            print(pre_nombres)

                            try :
                                ape_pat = parts[1].strip().replace("+", " ")
                                print(ape_pat)
                                ape_pat_minusculas = ape_pat.lower()
                            except IndexError:
                                print("error de inxd")
                                ape_pat_minusculas = ""
                            


                            try:
                                ape_mat = parts[2].strip().replace("+", " ")
                                ape_mat_minusculas = ape_mat.lower()
                                print(ape_mat)
                            except  IndexError:
                                print("error de inxd")
                                ape_mat_minusculas = ""




                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {pre_nombres}", parse_mode="html")


                        
                        
                            url = f"https://sseeker.org/consultar_api?apePat={ape_pat_minusculas}&apeMat={ape_mat_minusculas}&prenombres={pre_nombres_minusculas}"#&edadMin={edad_min}&edadMax={edad_max}&depaNace=


                            headers = {
                                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                    "accept-language": "es-419,es;q=0.9",
                                    "cache-control": "max-age=0",
                                    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                                    "sec-ch-ua-mobile": "?0",
                                    "sec-ch-ua-platform": "\"Windows\"",
                                    "sec-fetch-dest": "document",
                                    "sec-fetch-mode": "navigate",
                                    "sec-fetch-site": "none",
                                    "sec-fetch-user": "?1",
                                    "upgrade-insecure-requests": "1"
                            }
                            


                            response = requests.get(url, headers=headers)
                            print("SOLISITUD : ",response)
                            time.sleep(4)
                            response = requests.get(url, headers=headers)
                            print("SOLISITUD : ",response)
                        

                            if response.status_code == 200:
                                data = response.json()


            
    
                                respuesta = data['Resultados']
                                print(respuesta)

                                if respuesta == "no se encuentra registrados":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontraron resultados, recuerda no Utilizar tildes Y/O caracteres epeciales que podrian dificultar el filtro de busqueda.", parse_mode="html")
    
                                elif respuesta == "Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                else:
                                    respuesta = data['Resultados']



                                    cantidad_elementos = len(respuesta)
                                    print(cantidad_elementos)
                                    if cantidad_elementos == 0:
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        bot.reply_to(message,f"[⚠️] No se encontraron resultados, recuerda no Utilizar tildes Y/O caracteres epeciales que podrian dificultar el filtro de busqueda.", parse_mode="html")
                                        return




                                    if cantidad_elementos <= 50:

                                        guardar = ""
                                        guardar1 = ""
                                        dnis = []

                                        contadores = 0
                                        keyboard = InlineKeyboardMarkup(row_width=2)
                                        buttons = []
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)     



                                        if 5000 <= drgon <= 50000:
                                            valor_cred = "♾"

                                        else:
                                            valor_cred = drgon



                                        with open(f"./Registros/{recipient_id}.json","r") as file:
                                            mi_json = json.load(file)
                    
                                        mi_json["CRD"] = drgon
    

                                        # Guardar los cambios en el mismo archivo
                                        with open(f'./Registros/{huserid}.json', 'w') as file:
                                            json.dump(mi_json, file, indent=2)






                                
                                        for elemento in respuesta:

                                            dni = elemento['nuDni']
                                            dnis.append(dni)    
                                            nombre = elemento['preNombres']
                                            apePaterno = elemento['apePaterno']
                                            apeMaterno = elemento['apeMaterno']
                                            nuEdad = elemento['nuEdad']

                                            print(f"<b>DNI</b>: {dni}\n<b>EDAD</b>: {nuEdad}\n<b>NOMBRES</b>: {nombre}\n<b>AP PATERNO</b>: {apePaterno}\n<b>AP MATERNO</b>: {apeMaterno}\n\n")

                                        
                                            guardar  +=f"<b>DNI</b>: <code>{dni}</code>\n<b>EDAD</b>: {nuEdad}\n<b>NOMBRES</b>: {nombre}\n<b>AP PATERNO</b>: {apePaterno}\n<b>AP MATERNO</b>: {apeMaterno}\n\n"
                                            guardar1  +=f"DNI: {dni}\nEDAD: {nuEdad}\nNOMBRES: {nombre}\nAP PATERNO: {apePaterno}\nAP MATERNO: {apeMaterno}\n\n"

                                
                                            contador = guardar.count("DNI")
                                            button = InlineKeyboardButton(dni, callback_data=f"nombre_dni_{dni}")
                                            buttons.append(button)

                                            contadores += 1



                                            if contadores % 10 == 0 or contadores == len(respuesta):
                                                # Enviar mensaje con los primeros 10 botones

                                                ## Dividir los botones en filas de dos
                                                for i in range(0, len(buttons), 2):
                                                    keyboard.row(*buttons[i:i + 2])

                                                bot.reply_to(message,f"[#DataGold🌩] → RENIEC NOMBRES\n\nEdad Min:\nEdad Max:\nDepartamento:\n\n{guardar}↞ Puedes visualizar la foto de una coincidencia antes de usar /dni ↠\n\n💰<b>Credits :</b> <code>{valor_cred}</code>\n<b>🎖 Solicitado Por</b> <a href='tg://user?id={huserid}'>{usernombre}</a>",parse_mode="html", reply_markup=keyboard)

                                                guardar = ""
                                                # Reiniciar teclado para los próximos 10 botones
                                                keyboard = InlineKeyboardMarkup(row_width=2)
                                                buttons = []

                                        if len(guardar) > 0:
                                            bot.reply_to(message,f"[#DataGold🌩] → RENIEC NOMBRES\n\nEdad Min:\nEdad Max:\nDepartamento:\n\n{guardar}↞ Puedes visualizar la foto de una coincidencia antes de usar /dni ↠\n\n💰<b>Credits :</b> <code>{valor_cred}</code>\n<b>🎖 Solicitado Por</b> <a href='tg://user?id={huserid}'>{usernombre}</a>",parse_mode="html", reply_markup=keyboard)                                                                          
                            


                                    else:

                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        guardar1 =""


                                        for elemento in respuesta:

                                            dni = elemento['nuDni']

                                            nombre = elemento['preNombres']
                                            apePaterno = elemento['apePaterno']
                                            apeMaterno = elemento['apeMaterno']
                                            nuEdad = elemento['nuEdad']

                                            print(f"<b>DNI</b>: {dni}\n<b>EDAD</b>: {nuEdad}\n<b>NOMBRES</b>: {nombre}\n<b>AP PATERNO</b>: {apePaterno}\n<b>AP MATERNO</b>: {apeMaterno}\n\n")

                                        
                                        
                                            guardar1  +=f"DNI: {dni}\nEDAD: {nuEdad}\nNOMBRES: {nombre}\nAP PATERNO: {apePaterno}\nAP MATERNO: {apeMaterno}\n\n"




                                            contador = guardar1.count("DNI")













                                        with open("./resultados.txt", "w") as archivo:
                                            # Escribir el contenido en el archivo
                                            archivo.write(guardar1)




                                        if 5000 <= drgon <= 50000:
                                            valor_cred = "♾"

                                        else:
                                            valor_cred = drgon



                                        with open(f"./Registros/{recipient_id}.json","r") as file:
                                            mi_json = json.load(file)
                    
                                        mi_json["CRD"] = drgon


                                        # Guardar los cambios en el mismo archivo
                                        with open(f'./Registros/{huserid}.json', 'w') as file:
                                            json.dump(mi_json, file, indent=2)
        




                                        



                                        nombre_archivo = "./resultados.txt"

                                        # Enviar el archivo al usuario
                                        bot.send_document(message.chat.id, open(nombre_archivo, "rb"),caption=f"[#DataGold🌩] - FILTRO - NOMBRES {contador}\n\nSe ha encontrado más nombres para {pre_nombres} - {ape_pat}.\nPara un mejor resultado, la lista de nombres se ha guardado en este archivo de texto.\n\n💰<b>Credits :</b> <code>{valor_cred}</code>\n<b>🎖 Solicitado Por</b> <a href='tg://user?id={huserid}'>{usernombre}</a>",parse_mode="html",reply_to_message_id=message.message_id)       

                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                bot.reply_to(message,f"[⚠️] No se encontraron resultados, recuerda no Utilizar tildes Y/O caracteres epeciales que podrian dificultar el filtro de busqueda.", parse_mode="html")


                        except IndexError:#IndexError

                        
                            error_message = f"[⚠️] No se encontraron resultados, recuerda no Utilizar tildes Y/O caracteres epeciales que podrian dificultar el filtro de busqueda."
                            bot.reply_to(message, error_message, parse_mode="html")










                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"

                    bot.reply_to(message,f"[❌] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")






        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


# Manejar las interacciones con los botones
@bot.callback_query_handler(func=lambda call: call.data.startswith("nombre_dni_"))
def handle_callback_query(call):
    # Obtener el ID del usuario que realizó la consulta
    user_id = call.from_user.id


    message_id = call.message.message_id
    # Verificar si el usuario ha ejecutado el comando "/hogar" antes de permitir la interacción con los botones
    if user_id in comandos_nm and comandos_nm[user_id] == "/nm":
        # El usuario ejecutó el comando "/hogar", permitir la interacción con los botones
        dni = call.data.split("_")[2]
        #bot.reply_to(call.message, f"Este es el DNI seleccionado: {dni}")






        url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni}"
        



        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        print("hacienod l consulta ")


        response = requests.get(url, headers=headers)
        print(response)
                        

        if response.status_code == 200:
            data = response.json()
    
            respuesta = data['Respuesta'][0]

            if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                
                bot.reply_to(call.message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

            elif respuesta == f"Reniec OFF":
                                    
                bot.reply_to(call.message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

            elif respuesta == f"ERROR EN LA RESPUESTA":
                
                bot.reply_to(call.message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

            elif respuesta == f"ERRO DEL SERVIDOR":
                
                bot.reply_to(call.message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


            elif respuesta == "dni cancelado":
                
                bot.reply_to(call.message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")

            else:
                respuesta = data['Respuesta'][0]



                foto_codificada = respuesta["foto"]



                # Guardar la imagen en un archivo con ruta dinámica
                dni2 = f"{dni}"  # Valor de ejemplo para dni1
                ruta_archivo = f"./FOTOS_RE/foto1.jpg"  # Ruta y nombre de archivo con variable dni1
                with open(ruta_archivo, "wb") as archivo:
                    archivo.write(base64.b64decode(foto_codificada))







                nuDni = dni



                foto = open(f'./FOTOS_RE/foto1.jpg', 'rb')


                #QUITA CREDITOS
                bot.send_chat_action(call.message.chat.id, "upload_photo")

                bot.send_photo(call.message.chat.id, foto,f"<b>DNI:</b> <code>{nuDni}</code>\n\n",parse_mode="html", reply_to_message_id=message_id)
                
                ruta_imagen0 = f"./FOTOS_RE/foto1.jpg"

                if os.path.exists(ruta_imagen0):
                    # Eliminar el archivo

                    os.remove(ruta_imagen0)
                
                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")

                else:
                    print(f"El archivo {ruta_imagen0} no existe.")





    else:
        print(f"alvertencia {user_id}")
        # El usuario no ha ejecutado el comando "/hogar", informar que no tiene permiso para interactuar con los botones
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)
        

@bot.message_handler(commands=["plac","PLAC"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/plac ABC123</code>\n'


        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):


            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/plac"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [PLAC] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3
                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1")
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    

                    else:
                        message0 = bot.send_message(message.chat.id,f"𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 🤖 ➟ {dni1}", parse_mode="html")


                        try:
                        
                            url=f"https://api.ddosis.fun/auto?token=O7gBHY9MapZEBH&placa={dni1}"
                            url = f"http://sseeker.org/plac/token=O7gBHY9MapZEBH&numero={dni1}"

                            headers = {
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                "accept-language": "es-419,es;q=0.9",
                                "cache-control": "max-age=0",
                                "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": "\"Windows\"",
                                "sec-fetch-dest": "document",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-site": "none",
                                "sec-fetch-user": "?1",
                                "upgrade-insecure-requests": "1"
                            }

                            response = requests.get(url, headers=headers)
                            if response.status_code == 200:
                                data = response.json()

                            

                                cabeza = data['Resultados']

                                #print(cabeza)

                                propietarios1 = cabeza['titulares']
                                titulares_corregidos = propietarios1.replace('""', '"')
                                datos_json = json.loads(titulares_corregidos)
                                print(datos_json)

                                propietarios = datos_json["propietarios"]
                                
                                
                                primer_propietario = propietarios[0]

                                #guardar = ""

                                #for propietario in propietarios1:

                                    #guardar +=f"- {propietario}\n"

                                    #print(propietario)
                                


    
                                dueños = primer_propietario

                                vin1=cabeza['vin']
                                placa1=cabeza['placa']
                                seri1=cabeza['serie']
                                motor1=cabeza['motor']
                                color1=cabeza['color']
                                marca1=cabeza['marca']
                                modelo1=cabeza['modelo']
                                circulaci=cabeza['estado']
                                lugar=cabeza['sede']

                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)

                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon 

                                #print(cabeza)
                                #print(propietarios1)
                                print(propietarios1)
                                print(placa1)
                                print(seri1)
                                print(motor1)
                                print(color1)
                                print(marca1)
                                print(modelo1)

                                print(circulaci)
                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"

                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                        

                                bot.reply_to(message,f"[#DataGold🌩] - INFO PLACAS Nº1 🚗\n\n<b>N° PLACA</b> ➟ <code>{placa1}</code>\n<b>N° SERIE</b> ➟ <code>{seri1}</code>\n<b>N° VIN</b> ➟ <code>{vin1}</code>\n<b>N° MOTOR</b> ➟ <code>{motor1}</code>\n\n<b>[🛞] ESPECIFICACIONES</b>\n\n<b>COLOR</b> ➟ <code>{color1}</code>\n<b>MARCA</b> ➟ <code>{marca1}</code>\n<b>MODELO</b> ➟ <code>{modelo1}</code>\n<b>ESTADO</b> ➟ <code>En circulación</code>\n<b>SEDE</b> ➟ <code>{lugar}</code>\n<b>AÑO FABRICACION</b> ➟ <code></code>\n<b>CATEGORIA</b> ➟ <code></code>\n<b>TIPO</b> ➟ <code></code>\n<b>CARROCERIA</b> ➟ <code></code>\n\n<b>[📍] DUEÑOS</b>\n\n- <code>{dueños}</code> \n\n💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")






                            else:
                                data = response.json()

                            

                                error = data['error']
                                if  error == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")
                                else:


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>SURNAP</b> no está disponible en este momento", parse_mode="html")



                        except TypeError:
                            print()
                            bot.send_chat_action(message.chat.id, "typing")
                            bot.reply_to(message,"[❗️] No se encontro informacion [PLAC]")


                            
        else:

            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["yapesss","YAPEsss"])
def cmd_dni(message): 












    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/yape 952651905</code>\n'


        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):


            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/yape"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰",url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [YAPE] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    

                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 9 :





                            message0 = bot.send_message(message.chat.id,f"𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 🤖 ➟ {dni1}", parse_mode="html")



                        
                            url=f"https://api.ddosis.fun/yape?token=PMdLBgXJvoIqRgEayDCSTDKanWw&numero={dni1}"

                            headers = {
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                "accept-language": "es-419,es;q=0.9",
                                "cache-control": "max-age=0",
                                "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": "\"Windows\"",
                                "sec-fetch-dest": "document",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-site": "none",
                                "sec-fetch-user": "?1",
                                "upgrade-insecure-requests": "1"
                            }

                            response = requests.get(url, headers=headers)
                            if response.status_code == 200:
                                data = response.json()

                                Data1 = data['data1']


                                if Data1.get("deRespuesta") == "Ok":
                                    daSource = Data1['daSource']
                                    inf_dni = daSource['receiverDocumentNumber']
                                    inf_nombre = daSource['receiverName']


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    bot.reply_to(message,f"[#DataGold🌩] - INFO YAPE Nº1\n\n<b>DNI:</b> <code>{inf_dni}</code>\n<b>NOMBRES:</b> <code>{inf_nombre}</code>\n\n💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")







                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,"[❗️] No se encontro informacion [YAPE]")

                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                bot.reply_to(message,"[❗️] No se encontro informacion [YAPE]")       




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/YAPE] seguido de un número de DNI de 9 dígitos\n\n➜ EJEMPLO: [/YAPE 952651905]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["plimss","PLIMsss"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/plim 952651905</code>\n'


        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):


            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/plim"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [YAPE] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/DARKSITEV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    

                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 9 :





                            message0 = bot.send_message(message.chat.id,f"𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 🤖 ➟ {dni1}", parse_mode="html")



                        
                            url=f"https://api.ddosis.fun/plin?token=PMdLBgXJvoIqRgEayDCSTDKanWw&numero={dni1}"

                            headers = {
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                "accept-language": "es-419,es;q=0.9",
                                "cache-control": "max-age=0",
                                "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": "\"Windows\"",
                                "sec-fetch-dest": "document",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-site": "none",
                                "sec-fetch-user": "?1",
                                "upgrade-insecure-requests": "1"
                            }

                            response = requests.get(url, headers=headers)
                            if response.status_code == 200:
                                data = response.json()

                                Data1 = data['data1']


                                if Data1.get("deRespuesta") == "Ok":
                                    daSource = Data1['daSource']
                                    inf_dni = daSource['receiverDocumentNumber']
                                    inf_nombre = daSource['receiverName']
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon


                                    bot.reply_to(message,f"[#DataGold🌩] - INFO PLIM Nº1\n\n<b>DNI:</b> <code>{inf_dni}</code>\n<b>NOMBRES:</b> <code>{inf_nombre}</code>\n\n💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")







                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,"[❗️] No se encontro informacion [PLIN]")

                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                bot.reply_to(message,"[❗️] No se encontro informacion [PLIN]")       







                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/PLIM] seguido de un número de DNI de 9 dígitos \n\n➜ EJEMPLO: [/PLIM 952651905]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


#ubi
@bot.message_handler(commands=["ubsss"," UBsss"])
def cmd_dni(message):










    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/ub 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/bitel"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:
                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰",url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [bitel] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"http://sseeker.org/buscar/ubicacion?token=acYrJNje9faCXv8I&dni={dni1}"


                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("hacienod l consulta ")


                            response = requests.get(url, headers=headers)
                            print(response)



                            if response.status_code == 200:
                                datav1 = response.json()


                                respuesta = datav1['mensaje']

                                print(respuesta)
                                if  respuesta == f"no hay datos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro informacion", parse_mode="html")

                                else:
                                    data = datav1['respuesta']

                                    dni = data.get('dni')

                                    
                                    preNombres = data.get('nombres')
                                    apePaterno = data.get('apellido_paterno')
                                    apeMaterno = data.get('apellido_materno')
                                    Edad = data.get('Edad')

                                    Teléfono = data.get('fono')
                                    tipo_residencia = data.get('tipo_residencia')
                                    info_geolocalizacion = data.get('GEOLOCALIZACION')
    

    
                                    componentes = info_geolocalizacion.split(", ")
                                    diirecion = componentes[0]
                                    distrito = componentes[1]
                                    provincia = componentes[2]
                                    region = componentes[3]
                                    #codigo_postal = componentes[4]




                                    print(dni)


                                        
                                    url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"


                                    headers = {
                                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                        "accept-language": "es-419,es;q=0.9",
                                        "cache-control": "max-age=0",
                                        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                                        "sec-ch-ua-mobile": "?0",
                                        "sec-ch-ua-platform": "\"Windows\"",
                                        "sec-fetch-dest": "document",
                                        "sec-fetch-mode": "navigate",
                                        "sec-fetch-site": "none",
                                        "sec-fetch-user": "?1",
                                        "upgrade-insecure-requests": "1"
                                    }
                                    print("hacienod l consulta ")


                                    response = requests.get(url, headers=headers)
                                    print(response)
                        

                                    if response.status_code == 200:
                                        data = response.json()
    
                                        respuesta = data['Respuesta'][0]

                                        if  respuesta == f"no hay datos":
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                            bot.reply_to(message,f"[⚠️] No se encontro el ubicacion [UB]", parse_mode="html")

                                        else:
                                            respuesta = data['Respuesta'][0]
                        

                                            foto_codificada = respuesta["foto"]
                                                # Guardar la imagen en un archivo con ruta dinámica
                                            dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                            ruta_archivo = f"./FOTOS_RE/{dni1}.jpg"  # Ruta y nombre de archivo con variable dni1
                                            with open(ruta_archivo, "wb") as archivo:
                                                archivo.write(base64.b64decode(foto_codificada))



                                            # Abre ambas imágenes
                                            imagen_fondo = Image.open(f'./UB_FICHA/ub_ficha.jpg')
                                            imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni1}.jpg')

                                            # Ajusta el tamaño de la imagen superpuesta
                                            nuevo_tamano = (273,340) # especifica el tamaño deseado
                                            imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                            # Pega la imagen superpuesta sobre la imagen de fondo
                                            posicion = (523, 160) # especifica la posición donde se pegará la imagen superpuesta
                                            imagen_fondo.paste(imagen_superpuesta, posicion)




                                            # Crea un objeto ImageDraw para dibujar sobre la imagen
                                            dibujar = ImageDraw.Draw(imagen_fondo)

                                            #dni
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{dni}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (155, 300)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 14)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)

                                            #TELEGONO
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{Teléfono}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (155, 372)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 14)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)


                                            #NOMRES
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{preNombres}  {apePaterno}\n{apeMaterno}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (155, 432)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 14)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)


                                            #comienza los numeros 




                                            #No hay señal
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"No hay señal"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (400, 830)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)









                                            #departmento o region
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{region}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (230, 1190)
    
                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 12)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)


                                            #provincia
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{provincia}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (230, 1215)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 12)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)



                                            #distrito
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{distrito}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (230, 1240)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 12)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)



                                            #direcion
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{diirecion}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (580, 1180)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 14)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)


                                            #tipo domisol
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{tipo_residencia}          PERU"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (500, 1245)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 12)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(000, 000, 000), font=fuente1)

    
                                            # Guarda la imagen con el texto agregado
                                            imagen_fondo.save(f'./UB_FICHA/{dni1}.jpg')

                                        


                                                # Cargar la imagen
                                            img = Image.open(f'./UB_FICHA/{dni1}.jpg')

                                            # Crear el archivo PDF
                                            pdf = canvas.Canvas(f"./UB_FICHA/{dni1}.pdf", pagesize=img.size)

                                            # Añadir la imagen al archivo PDF
                                            pdf.drawImage(f'./UB_FICHA/{dni1}.jpg', 0, 0)



                                            pdf.save()


                                            # Leer el JSON desde el archivo (CREDITOS)
                                            with open(f"./Registros/{recipient_id}.json","r") as file:
                                                mi_json = json.load(file)
                
                                            mi_json["CRD"] = drgon


                                            # Guardar los cambios en el mismo archivo
                                            with open(f'./Registros/{huserid}.json', 'w') as file:
                                                json.dump(mi_json, file, indent=2)

                                            hfirst_name=message.from_user.first_name
                                            huserid=message.from_user.id
                                            usernombre= f"{hfirst_name}"
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                            #thumbnail sirve enviar el pdf con foto 



                                            if 5000 <= drgon <= 50000:
                                                valor_cred = "♾"

                                            else:
                                                valor_cred = drgon

                                            Servicio = "RENIEC"
                                            Comando = "/ub"
                                            status = "200"
                                            

                                            thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                            thumbnail = open(thumbnail_path, 'rb')
                                            document = open(f'./UB_FICHA/{dni1}.pdf', 'rb')
                                            bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] FICHA UBICACION </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)

                                            ruta_imagen3 = f"./FOTOS_RE/{dni1}.jpg"
                                            ruta_imagen4 = f"./UB_FICHA/{dni1}.jpg"
                                            ruta_imagen5 = f"./UB_FICHA/{dni1}.pdf"

                                            if os.path.exists(ruta_imagen3):
                                                # Eliminar el archivo

                                                os.remove(ruta_imagen3)
                                                os.remove(ruta_imagen4)
                                                os.remove(ruta_imagen5)                                                                                  
                                                print(f"Archivo {ruta_imagen3} eliminado con éxito.")
                                            else:
                                                print(f"El archivo {ruta_imagen3} no existe.")

                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                # Mensaje de error
                                error_message = f"[📢] ¡Ups! El servicio de RENIEC no está disponible en este momento."

                                # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/ub] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/ub 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")
    

@bot.message_handler(commands=["antpol"])
def cmd_dni(message):











    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/antpol 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        print(nombre_archivo)
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/antpol"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return


            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [ANTPOL] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"



                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("hacienod l consulta ")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")   
                                

                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")



                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    apePaterno = respuesta["apePaterno"]
                                    apeMaterno = respuesta["apeMaterno"]
                                    preNombres = respuesta["preNombres"]


                                    foto_codificada = respuesta["foto"]
                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                        

                    
                                    
                                    




                    

                                    # Guardar la imagen en un archivo
                    
                                    
                                    
                    

                                    imagen_fondo = Image.open(f'./ANTPOL/CERTIFICADO.JPG')
                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni1}0.jpg')
    
                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (400,555) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (290, 950) # especifica la posición donde se pegará la imagen superpuesta
                                    imagen_fondo.paste(imagen_superpuesta, posicion)
    
                                    # Crea un objeto ImageDraw para dibujar sobre la imagen
                                    dibujar = ImageDraw.Draw(imagen_fondo)
    


                                    #PRIMER NOMBRE

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"GSjhohAHhjoh425gf"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1810, 25)
            
                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


    
                                    #PRIMER NOMBRE

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{dni1}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1000)
            
                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apePaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1110)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1210)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{preNombres}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1310)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)
                    
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"PERU"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1410)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"7821589"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1450, 1510)

                                    # Define la fuente del texto
                                    fuente2 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente2)


                                    from datetime import datetime
                                    # Obtener la fecha y hora actual
                                    fecha_hora_actual = datetime.now()

                                    fecha_hora_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")

                                    # Mostrar la fecha y hora actual
                                    print("Fecha y hora actual:", fecha_hora_formateada)


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{fecha_hora_formateada}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (455, 1760)

                                    # Define la fuente del texto
                                    fuente2 = ImageFont.truetype("./letras/arial.ttf", 28)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente2)






                                    # Guarda la imagen con el texto agregado
                                    imagen_fondo.save(f'./ANTPOL/{dni1}.jpg')



                                    # Cargar la imagen
                                    img = Image.open(f'./ANTPOL/{dni1}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./ANTPOL/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./ANTPOL/{dni1}.jpg', 0, 0)

                                    #Guardar el archivo PDF
                                    pdf.save()

                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon
                                    Servicio = "RENIEC"
                                    Comando = "/antpol"
                                   
                                    #thumbnail sirve enviar el pdf con foto 

                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./ANTPOL/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] FICHA POLICIAL </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)


                                    ruta_imagen0 = f"./FOTOS_RE/{dni2}0.jpg"
                                    ruta_imagen1 = f"./ANTPOL/{dni1}.jpg"
                                    ruta_imagen2 = f"./ANTPOL/{dni1}.pdf"



                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                                                                
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")





                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                # Mensaje de error
                                error_message = f"📢 ¡Ups! El servicio de RENIEC no está disponible en este momento. Por favor, intenta nuevamente más tarde o prueba otro comando  con /cmd.⚠️ "

                                                        # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/antpol] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/antpol 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"                    
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

                    
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["antjud"])
def cmd_dni(message):










    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/antjud 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        print(nombre_archivo)
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/antjud"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return


            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [ANTIJUF] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"



                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("hacienod l consulta ")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]


                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")   
                                       

                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")



                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta["nuDni"]
                                    apePaterno = respuesta["apePaterno"]
                                    apeMaterno = respuesta["apeMaterno"]
                                    preNombres = respuesta["preNombres"]


                                    foto_codificada = respuesta["foto"]
                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                        



                                    imagen_fondo = Image.open(f'./ANTJUD/certificado_pj1.jpg')

                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni1}.jpg')


                                    nuevo_tamano = (450,600)
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)
                                    posicion = (300, 1200)
                                    imagen_fondo.paste(imagen_superpuesta, posicion)
    
                                    dibujar = ImageDraw.Draw(imagen_fondo)

                                    texto1 = f"{apePaterno}"
                                    ubicacion1 = (900, 1880)

                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 70)

                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #APELLDIO MATERNO

                                    texto1 = f"{apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2550, 1880)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #APELLDIO MATERNO

                                    texto1 = f"{preNombres}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1600, 2230)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #DNI

                                    texto1 = f"{nuDni}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1550, 2500)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 70)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    
                                    # Obtener la fecha actual
                                    fecha_actual = datetime.now()

                                    # Extraer el día, mes y año
                                    dia_actual = fecha_actual.day
                                    mes_actual = fecha_actual.month
                                    año_actual = fecha_actual.year
                                    
                                    texto1 = f"{dia_actual}/{mes_actual}/{año_actual}"
                                    ubicacion1 = (810, 4775)

                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 50)

                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)







                                    imagen_fondo.save(f'./ANTJUD/{dni1}.jpg')




                                    img = Image.open(f'./ANTJUD/{dni1}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./ANTJUD/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./ANTJUD/{dni1}.jpg', 0, 0)

                                    # Guardar el archivo PDF
                                    pdf.save()



                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon
                                    Servicio = "RENIEC"
                                    Comando = "/antjud"
                                    
                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    #thumbnail sirve enviar el pdf con foto 

                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./ANTJUD/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] FICHA JUDICIAL </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)


                                    ruta_imagen0 = f"./FOTOS_RE/{dni2}.jpg"
                                    ruta_imagen4 = f"./ANTJUD/{dni1}.jpg"
                                    ruta_imagen5 = f"./ANTJUD/{dni1}.pdf"

                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen4)
                                        os.remove(ruta_imagen5)                                                                                  
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")



                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                # Mensaje de error
                                error_message = f"📢 ¡Ups! El servicio de RENIEC no está disponible en este momento. Por favor, intenta nuevamente más tarde o prueba otro comando  con /cmd.⚠️ "

                                                        # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/antjud] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/antjud 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"                    
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")


                


        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["antpen"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/antpen 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        print(nombre_archivo)
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/antjud"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return


            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [ANTIJUF] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"https://sseeker.org/api/reniec?token=acYrJNje9faCXv8I&dni={dni1}"


                            headers = {
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "accept-language": "es-419,es;q=0.9",
                            "cache-control": "max-age=0",
                            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": "\"Windows\"",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "none",
                            "sec-fetch-user": "?1",
                            "upgrade-insecure-requests": "1"
                            }
                            print("hacienod l consulta ")


                            response = requests.get(url, headers=headers)
                            print(response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")   
                                

                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")



                                else:
                                    respuesta = data['Respuesta'][0]
                        
                                    nuDni = respuesta["nuDni"]
                                    apePaterno = respuesta["apePaterno"]
                                    apeMaterno = respuesta["apeMaterno"]
                                    preNombres = respuesta["preNombres"]


                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/{dni2}.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))



                                    # Abre ambas imágenes
                                    imagen_fondo = Image.open(f'./ANTPEN/BASE.png')
                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni1}.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (366,494) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                    # Pega la imagen superpuesta sobre la imagen de fondo
                                    posicion = (1985, 350)    
                                    imagen_fondo.paste(imagen_superpuesta, posicion)

                                    # Guarda la nueva imagen
                        



    
                                    "inicio de plan de nombres"


                                    # Abre la imagen
                        

                                    "fila 1"
                                    # Crea un objeto ImageDraw para dibujar sobre la imagen
                                    dibujar = ImageDraw.Draw(imagen_fondo)


                                    #PRIMER NOMBRE

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{nuDni}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (600, 1392)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    "fila 2"

                                    #PRIMER APELLIDO


                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apePaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (250, 1180)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 45)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    "fila 3"

                                    #SEGUNDO  APELLIDO

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (855, 1180)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 45)

                                    #  Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    "fila 4"
    
                                    #prenombres
        
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{preNombres}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1470, 1180)
    
                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 45)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)
    


                                    "fila 5"

                                    #SPLICITU PARA 

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"TRAMITE ADMINISTRATIVO"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (1200, 1392)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 45)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

    
                                    "SEGUNDA PARTE "

                                    "SEGUNDO 1"

                                    #SPLICITU PARA 

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"388903"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (450, 3095)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 45)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)
    
                                    "SEGUNDO 2"

                                    #OPERADOR DE CONSULTA PARA 
    
                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"USRPCAP"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2050, 3095)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    "SEGUNDO 3"




                                    # Obtener la fecha actual
                                    fecha_actual = datetime.now()
    
                                    # Obtener el día, mes y año
                                    dia = fecha_actual.day
                                    mes = fecha_actual.month
                                    anio = fecha_actual.year

                                    # Imprimir la fecha en formato "dd/mm/aaaa"
                                    print(f"{dia}/{mes}/{anio}")
                                    #FECHA DE PAGO 

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{dia}/{mes}/{anio}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (450, 3200)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    "SEGUNDO 4"





                                    # Obtener la fecha actual
                                    fecha_actual = datetime.now()

                                    # Obtener la fecha del día siguiente
                                    fecha_siguiente = fecha_actual + dt.timedelta(days=30)

                                    # Obtener el día, mes y año
                                    dia = fecha_siguiente.day
                                    mes = fecha_siguiente.month
                                    anio = fecha_siguiente.year
                                    #FECHA DE PAGO 

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{dia}/{mes}/{anio}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2050, 3200)
    
                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    "SEGUNDO 5 HORA"

    


                                    # Obtener la hora actual
                                    hora_actual = datetime.now().time()

                                    # Obtener las horas, minutos y segundos
                                    horas = hora_actual.hour
                                    minutos = hora_actual.minute
                                    segundos = hora_actual.second

                                    # Imprimir la hora en formato "hh:mm:ss"
                                    print(f"{horas}:{minutos}:{segundos}")

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{horas}:{minutos}:{segundos}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (450, 3305)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)
    


                                    "SEGUNDO 6 HORA"




                                    # Obtener la hora actual
                                    hora_actual = datetime.now().time()

                                    # Obtener las horas, minutos y segundos
                                    horas = hora_actual.hour
                                    minutos = hora_actual.minute
                                    segundos = hora_actual.second

                                    # Imprimir la hora en formato "hh:mm:ss"
                                    print(f"{horas}:{minutos}:{segundos}")

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{horas}:{minutos}:{segundos}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2050, 3305)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    "SEGUNDO  VALOR"


                                    texto1 = f"S/.52.80"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (450, 3415)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)
        


                                    "SEGUNDO  TERMINA"
    


                                    # Obtener la fecha actual
                                    fecha_actual = datetime.now()

                                    # Obtener la fecha del día siguiente
                                    fecha_siguiente = fecha_actual + dt.timedelta(days=90)

                                    # Obtener el día, mes y año
                                    dia = fecha_siguiente.day
                                    mes = fecha_siguiente.month
                                    anio = fecha_siguiente.year
                                    #FECHA DE PAGO 

                                    # Define la ubicación y el texto a agregar
                                    texto1 = f"{dia}/{mes}/{anio}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (2050, 3415)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arial.ttf", 40)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    print("guardado0")

                        
                                    # Guarda la imagen con el texto agregado
                                    imagen_fondo_rgb = imagen_fondo.convert("RGB")

                                    # Save the image as a JPEG file
                                    imagen_fondo_rgb.save(f"./ANTPEN/{dni1}.jpg")



                                    img = Image.open(f'./ANTPEN/{dni1}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./ANTPEN/{dni1}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./ANTPEN/{dni1}.jpg', 0, 0)
    
                                    # Guardar el archivo PDF
                                    pdf.save()
                                    
                        

                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    #thumbnail sirve enviar el pdf con foto 
                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon
                                    Servicio = "RENIEC"
                                    Comando = "/antpen"
                                   


                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./ANTPEN/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] FICHA ANTPENALES </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)


                                    ruta_imagen0 = f"./FOTOS_RE/{dni1}.jpg"
                                    ruta_imagen4 = f"./ANTPEN/{dni1}.jpg"
                                    ruta_imagen5 = f"./ANTPEN/{dni1}.pdf"

                                    if os.path.exists(ruta_imagen0):
                                        # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                        os.remove(ruta_imagen4)
                                        os.remove(ruta_imagen5)                                                                                  
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")


                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                # Mensaje de error
                                error_message = f"📢 ¡Ups! El servicio de RENIEC no está disponible en este momento. Por favor, intenta nuevamente más tarde o prueba otro comando  con /cmd.⚠️ "

                                                        # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/antpen] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/antpen 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

                


        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


comandos_ag = {}
@bot.message_handler(commands=["ag","AG"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])



    user_id = message.from_user.id
    print(user_id)
    comandos_ag[user_id] = "/ag"


    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/ag 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):


            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return


            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/ag"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango GOLD, HAXER o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [C4C] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 6

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        print("No tienes suficientes créditos para la consulta.")

                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1")
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")
                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f" GENERANDO ARBOL ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"http://sseeker.org/api/darbol?token=acYrJNje9faCXv8I"
                           
                            params = {
                                "token": "acYrJNje9faCXv8I",
                                "dni" : dni1
                            }


                            print("hacienod l consulta ")


                            try:
                                response = requests.get(url, params=params,timeout=20)
                                print(response)
                                status = response.status_code
                        

                                if response.status_code == 200:
                                    data = response.json()
                                    datos = data.get("Resultados", [])
                                    # Divide los diccionarios en lotes de 10
                                    lotes_de_diccionarios = [datos[i:i + 10] for i in range(0, len(datos), 10)]

                                    # Imprime el número de páginas
                                    numero_de_paginas = len(lotes_de_diccionarios)
                                    print(f"El número total de páginas es: {numero_de_paginas}")
                                    print("La respuesta en formato JSON es:")

                                    # Leer el JSON desde el archivo (CREDITOS)


                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                    
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "RENIEC ARBOL"
                                    Comando = "/ag"
                                   


                                    if datos:

                                        #print(data)

                                        mensaje= ""
                                        contadores = 0
                                        contador_paginas = 0
                                


                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        dnis = []

                                        contadores = 0
                                        keyboard = InlineKeyboardMarkup(row_width=2)
                                        buttons = []
                                        for persona in datos:
                                            dni = persona.get('nuDni')
                                            dnis.append(dni)
                                            digitoVerificacion = persona.get('digitoVerificacion')
                                            Apellidos = persona.get('Apellidos')



                                            nombres = persona.get('preNombres')
                                            genero = persona.get('sexo')
                                            edad = persona.get('nuEdad')
                                            tipo = persona.get('tipo')
                                            verificacion = persona.get('verificacion')

                            
                                    
                                            print(f"- DNI : {dni} -> NUMERO : {tipo}")  
                                            

                                            mensaje +=f"<b>•DOCUMENTO →</b> <code>{dni} -{digitoVerificacion}</code>\n"
                                            mensaje +=f"<b>•APELLIDOS →</b> <code>{Apellidos}</code>\n"
                                            mensaje +=f"<b>•NOMBRES →</b> <code>{nombres}</code>\n"                                  
                                            mensaje +=f"<b>•GENERO →</b> <code>{genero}</code>\n"
                                            mensaje +=f"<b>•EDAD →</b> <code>{edad}</code>\n"
                                            mensaje +=f"<b>•TIPO →</b> <code>{tipo}</code>\n"
                                            mensaje +=f"<b>•VERIFICACION RELACION→</b> <code>{verificacion}</code>\n\n"



                                            contadores += 1


                                            button = InlineKeyboardButton(dni, callback_data=f"arbol_dni_{dni}")
                                            buttons.append(button)


                                            if contadores % 10== 0 or contadores == len(datos):

                                                contador_paginas += 1
                                                ## Dividir los botones en filas de dos
                                                for i in range(0, len(buttons), 3):
                                                    keyboard.row(*buttons[i:i + 3])
                                            

                                                bot.reply_to(message, f"<b>[#DataGold🌩] → ARBOL GENEALOGICO</b>\n\n[{contador_paginas}/{numero_de_paginas}]\n\n{mensaje} ↞ Puedes visualizar la foto de una coincidencia gratuitamente antes de usar /dni \n\n💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html", reply_markup=keyboard)

                                                mensaje = ""
                                                # Reiniciar teclado para los próximos 10 botones
                                                keyboard = InlineKeyboardMarkup(row_width=2)
                                                buttons = []


                                        if len(mensaje) > 0:
                                            contador_paginas += 1

                                            bot.reply_to(message, f"<b>[#DataGold🌩] → ARBOL GENEALOGICO</b>\n\n[{contador_paginas}/{numero_de_paginas}]\n\n{mensaje} ↞ Puedes visualizar la foto de una coincidencia gratuitamente antes de usar /dni \n\n💰 Credits : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html", reply_markup=keyboard)
                                    else:
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        bot.reply_to(message,f"[⚠️] No se encontro Informacion", parse_mode="html")




                                        
                                else:
                                    error = response.json()
                                    
                                    respuesta  = error.get("error")

                                    if  respuesta == f"No hay informacion":
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        bot.reply_to(message,f"[⚠️] No hay informacion", parse_mode="html")

                                    elif respuesta == f"Error en la consulta a la API":
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        bot.reply_to(message,f"[⚠️] EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                    else:



                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        # Mensaje de error
                                        error_message = f"[📢] ¡Ups! El servicio de RENIEC no está disponible"

                                        # Enviar mensaje de error al chat de Telegram
                                        bot.send_message(message.chat.id, error_message, parse_mode="html")



                            except requests.Timeout:
                                print("La solicitud ha superado el tiempo de espera.")
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                bot.reply_to(message,f"[⚠️] No se encontro informacion", parse_mode="html")
                                




                        else:
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/ag] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/ag 44444444]", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")




        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


# Manejar las interacciones con los botones
@bot.callback_query_handler(func=lambda call: call.data.startswith("arbol_dni_"))
def handle_callback_query(call):
    # Obtener el ID del usuario que realizó la consulta
    user_id = call.from_user.id


    message_id = call.message.message_id
    # Verificar si el usuario ha ejecutado el comando "/hogar" antes de permitir la interacción con los botones
    if user_id in comandos_ag and comandos_ag[user_id] == "/ag":
        # El usuario ejecutó el comando "/hogar", permitir la interacción con los botones
        dni = call.data.split("_")[2]
        #bot.reply_to(call.message, f"Este es el DNI seleccionado: {dni}")






        url = f"https://sseeker.org/api/reniec_buscar?token=acYrJNje9faCXv8I&dni={dni}"


        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        print("hacienod l consulta ")


        response = requests.get(url, headers=headers)
        print(response)
        

        if response.status_code == 200:
            data = response.json()
    
            respuesta = data['Respuesta'][0]

            if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
            
                bot.reply_to(call.message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

            elif respuesta == f"Reniec OFF":
            
                bot.reply_to(call.message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

            elif respuesta == f"ERROR EN LA RESPUESTA":
            
                bot.reply_to(call.message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

            elif respuesta == f"ERRO DEL SERVIDOR":
            
                bot.reply_to(call.message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


            elif respuesta == "dni cancelado":
            
                bot.reply_to(call.message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")

            else:
                respuesta = data['Respuesta'][0]



                foto_codificada = respuesta["foto"]



                # Guardar la imagen en un archivo con ruta dinámica
                dni2 = f"{dni}"  # Valor de ejemplo para dni1
                ruta_archivo = f"./FOTOS_RE/foto1.jpg"  # Ruta y nombre de archivo con variable dni1
                with open(ruta_archivo, "wb") as archivo:
                    archivo.write(base64.b64decode(foto_codificada))







                nuDni = dni



                foto = open(f'./FOTOS_RE/foto1.jpg', 'rb')


                #QUITA CREDITOS
                bot.send_chat_action(call.message.chat.id, "upload_photo")

                bot.send_photo(call.message.chat.id, foto,f"<b>DNI:</b> <code>{nuDni}</code>\n\n",parse_mode="html", reply_to_message_id=message_id)
                
                ruta_imagen0 = f"./FOTOS_RE/foto1.jpg"

                if os.path.exists(ruta_imagen0):
                    # Eliminar el archivo

                    os.remove(ruta_imagen0)
                
                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")

                else:
                    print(f"El archivo {ruta_imagen0} no existe.")





    else:
        print(f"alvertencia {user_id}")
        # El usuario no ha ejecutado el comando "/hogar", informar que no tiene permiso para interactuar con los botones
        bot.answer_callback_query(call.id, text='No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)





@bot.message_handler(commands=["claro","CLARO"])
def cmd_dni(message):









    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/claro 45393644</code>\n'
        texto +=f'<code>/claro 984334973</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:


                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [CLARO] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1")
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 or contador == 9:
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/api_claro"


                            params = {
                                "numero" : dni1,
                            }


                            response = requests.get(url, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                


                                
                                

                                respuesta = data.get('Resultados', [])
                                total_resultados = len(respuesta)
                                print("RESULTAODS :",total_resultados)


                                mensaje =""

                                for primer_resultado in  respuesta:
                                    dni = primer_resultado.get('dni','')
                                    titular = primer_resultado.get('titular' ,'')
                                    operador = "Claro"
                                    telefono = primer_resultado.get('numero','')
                                    plan = primer_resultado.get('plan','')

                                    print(f"- DNI : {dni} -> NUMERO : {telefono}")  
                                            
                                    mensaje +=f"<b>1. Número de Teléfono: </b>\n\n"
                                    mensaje +=f"<b>• DOCUMENTO →</b> <code>{dni}</code>\n"
                                    mensaje +=f"<b>• TITULAR →</b> <code>{titular}</code>\n"
                                    mensaje +=f"<b>• TELEFONO →</b> <code>{telefono}</code>\n"                                      
                                    mensaje +=f"<b>• OPERADOR →</b> <code>{operador}</code>\n"
                                    mensaje +=f"<b>• PLAN →</b> <code>{plan}</code>\n\n"




                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)

                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon


                                Servicio = "Numero_claro"
                                Comando = "/claro"
                               
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                

                                bot.reply_to(message, f"<b>[#DataGold🌩] - CLARO ONLINE </b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                            else:

                                data = response.json()


                                respuesta = data['error']


                                if  respuesta == f"ELEMENTO NO VALIDO":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] DNI INVALIDO", parse_mode="html")

                                elif respuesta == "No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontró la informacion[claro].", parse_mode="html")


                                elif respuesta == "Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]  uops. Ocurrio un erro interno prueve /fono o /celx\n\n", parse_mode="html")








                                else:


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/claro] seguido de un número de DNI de 8 dígitos o numero 9 dígitos\n\n➜ EJEMPLO: [/claro 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["bitel","BITEL"])
def cmd_dni(message):

    dni1 = "".join(message.text.split()[1:2])
    



    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/bitel 984334973</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:


                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [bitel] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        markup1.add(a1)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 or contador == 9:
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")

                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/api_bitel"


                            params = {
                                "token" : "O7gBHY9MapZEBH" ,
                                "numero" : dni1,
                            }


                            response = requests.get(url, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                #data = json.loads(data_dict) 


                                
                                

                                respuesta = data.get('Resultados')
                                total_resultados = len(respuesta)
                                print("RESULTAODS :",total_resultados)


                                mensaje =""

                                primer_resultado =  respuesta[0]



                                dni = primer_resultado.get('dni','')
                                titular = primer_resultado.get('titular' ,'')
                                operador = "Bitel"
                                telefono = primer_resultado.get('numero','')
                                plan = primer_resultado.get('plan','')

                                print(f"- DNI : {dni} -> NUMERO : {telefono}")  
                                            
                                mensaje +=f"<b>1. Número de Teléfono: </b>\n\n"
                                mensaje +=f"<b>• DOCUMENTO →</b> <code>{dni}</code>\n"
                                mensaje +=f"<b>• TITULAR →</b> <code>{titular}</code>\n"
                                mensaje +=f"<b>• TELEFONO →</b> <code>{telefono}</code>\n"                                      
                                mensaje +=f"<b>• OPERADOR →</b> <code>{operador}</code>\n"
                                mensaje +=f"<b>• PLAN →</b> <code>{plan}</code>\n\n"




                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)

                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon

                                Servicio = "Numero_bitel"
                                Comando = "/bitel"
                               
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                

                                bot.reply_to(message, f"<b>[#DataGold🌩] - BITEL ONLINE</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")



                            else:

                                data = response.json()


                                respuesta = data['error']


                                if  respuesta == f"ELEMENTO NO VALIDO":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] DNI INVALIDO", parse_mode="html")

                                elif respuesta == "No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontró la informacion[bitel].", parse_mode="html")


                                elif respuesta == "Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]  uops. Ocurrio un erro interno prueve /fono o /celx\n\n", parse_mode="html")








                                else:


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/bitel] seguido de un número de  Numero 9 dígitos\n\n➜ EJEMPLO: [/bitel 444444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["movistarxd","MOVISTARxd"])
def cmd_dni(message):

    dni1 = "".join(message.text.split()[1:2])
    



    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/movistar 984334973</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:


                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [movistar] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 4
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 9:
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/api_movistar"


                            params = {
                                "numero" : dni1,
                            }


                            response = requests.get(url, params=params)

                            if response.status_code == 200:
                                data = response.json()
                                #data = json.loads(data_dict) 


                                
                                

                                respuesta = data.get('Resultados')
                                total_resultados = len(respuesta)
                                print("RESULTAODS :",total_resultados)


                                mensaje =""

                                

                                primer_resultado = respuesta[0]


                                dni = primer_resultado.get('dni','')
                                titular = primer_resultado.get('titular' ,'')
                                operador = "Movistar"
                                telefono = primer_resultado.get('numeros','')
                                plan = primer_resultado.get('plan','')
                                fecha = primer_resultado.get('fechaActivacion','')

                                print(f"- DNI : {dni} -> NUMERO : {telefono}")  
                                            
                                mensaje +=f"<b>1. Número de Teléfono: </b>\n\n"
                                mensaje +=f"<b>• DOCUMENTO →</b> <code>{dni}</code>\n"
                                mensaje +=f"<b>• TITULAR →</b> <code>{titular}</code>\n"
                                mensaje +=f"<b>• TELEFONO →</b> <code>{telefono}</code>\n"                                      
                                mensaje +=f"<b>• OPERADOR →</b> <code>{operador}</code>\n"
                                mensaje +=f"<b>• PLAN →</b> <code>{plan}</code>\n\n"
                                mensaje +=f"<b>• FECHA ACTIVACION →</b> <code>{fecha}</code>\n\n"



                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)

                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon

                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                

                                bot.reply_to(message, f"<b>[#DataGold🌩] - TELEFONIA ONLINE º4</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")



                            else:

                                data = response.json()


                                respuesta = data['error']


                                if  respuesta == f"ELEMENTO NO VALIDO":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] DNI INVALIDO", parse_mode="html")

                                elif respuesta == "No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontró la informacion[bitel].", parse_mode="html")


                                elif respuesta == "Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]  uops. Ocurrio un erro interno prueve /fono o /celx\n\n", parse_mode="html")








                                else:


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/bitel] seguido de un número de  Numero 9 dígitos\n\n➜ EJEMPLO: [/bitel 444444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")





@bot.message_handler(commands=["telp","TELP"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/telp 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [telp] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 or contador == 9 :



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"https://sseeker.org/api/fonos?token=acYrJNje9faCXv8I&dni={dni1}"


                            response = requests.get(url)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                if respuesta:

                                    
                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "opsitel"
                                    Comando = "/telp"
                                    
                                    mensaje =""

                                    contadores = 0
                                    valor_x = 0


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
        
                                    
                                    for lote in respuesta:
                
                                            
                                        dni = lote['dni']
                                        try:
                                            titular = lote['titular']
                                        except KeyError:
                                            titular = ""
                                    
                                
                                        
                                        año1 = lote['fecha']
                                        operador = lote['operador']
                                        plan = lote['plan'] 
                                        mayusculas = operador.upper()
                                        telefono = lote['numero']

                                        try:


                                            Marcas = lote['marcar']
                                            Modelo = lote['modelo']
                                        except KeyError:
                                            Marcas = " "
                                            Modelo = " "
                                        imei = lote['imei']
                                        color = lote['color']


                                        valor_x +=1






                                        print(f"- DNI : {dni} -> NUMERO : {telefono}")  
                                            
                                        mensaje +=f"<b>{valor_x}. Número de Teléfono: </b>\n\n"
                                        
                                        mensaje +=f"<b>[ ☑️ ] TITULAR DE - {dni} -</b>\n"
                                        mensaje +=f"<b>⌞TELEFONO →</b> <code>{telefono}</code>\n"                                      
                                        mensaje +=f"<b>⌞OPERADOR →</b> <code>{mayusculas}</code>\n"
                                        mensaje +=f"<b>⌞ COLOR: →</b> <code>{color}</code>\n"                                        
                                        mensaje +=f"<b>⌞PLAN →</b> <code>{plan}</code>\n"
                                        mensaje +=f"<b>⌞FECHA →</b> <code>{año1}</code>\n"
                                        mensaje +=f"<b>⌞MARCA →</b> <code>{Marcas}</code>\n"
                                        mensaje +=f"<b>⌞MODELO →</b> <code>{Modelo}</code>\n"
                                        mensaje +=f"<b>⌞IMEI → </b>{imei}\n\n"



                                        contadores += 1
                                        if contadores % 10== 0 or contadores == len(respuesta):

                                            

                                            bot.reply_to(message, f"<b>[#DataGold🌩] - TELEFONIA Nº2</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                                            mensaje = ""

                                    if len(mensaje) > 0:

                                        bot.reply_to(message, f"<b>[#DataGold🌩] - TELEFONIA Nº2</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No se encontró la información":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"no contiene 9 dijitos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] no contiene 9 dijitos", parse_mode="html")

                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tel] seguido de un número de DNI de 8 dígitos o numero 9 dígitos\n\n➜ EJEMPLO: [/tel 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["dnivel","DNIVEL"])
def cmd_dni(message):











    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/dnivel 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/dnivel"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [dnivel] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 :



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            curl = "http://sseeker.org/api/dni/electronic"
                            params = {
                                "dni": dni1,
                            }
                            response = requests.get(curl, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                diccionario_respuesta = respuesta[0]
                                pdf_sexo = diccionario_respuesta.get('pdf_dni_electronico')
                                # Decodificar la cadena Base64
                                datos_binarios = base64.b64decode(pdf_sexo)

                                # Escribir los datos binarios en un archivo PDF
                                with open(f"./PDF_ELEC/{dni1}.pdf", "wb") as archivo_pdf:
                                    archivo_pdf.write(datos_binarios)

                                print("Archivo PDF creado correctamente.")


                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)



                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon

                                Servicio = "DNI ELECTRONICO"
                                Comando = "/dnivel"
                              

                                #thumbnail sirve enviar el pdf con foto 

                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./PDF_ELEC/{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] DNI ELECTRONICO </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./PDF_ELEC/{dni1}.pdf"




                                if os.path.exists(ruta_imagen0):
                                    # Eliminar el archivo
                                    os.remove(ruta_imagen0)
                                                                                
                                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")



                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No se encontro el dni en planilla":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"El servicio de reniec esta en mantenimiento":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] El servicio de reniec esta en mantenimiento", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado o datos incompletos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado el servidor no responde":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"DNI Cancelado en RENIEC":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] DNI Cancelado en RENIEC", parse_mode="html")
                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Reniec</b> no está disponible en este momento", parse_mode="html")




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tel] seguido de un número de DNI de 8 dígitos o numero 9 dígitos\n\n➜ EJEMPLO: [/tel 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")











@bot.message_handler(commands=["actn","ACTN"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/actn 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/actn"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [dniama] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 :



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            curl = "http://sseeker.org/api/acta_nacmiento"
                            params = {
                                "token" : "O7gBHY9MapZEBH" ,
                                "dni": dni1,
                            }
                            response = requests.get(curl, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                resultados = data.get('Resultados',[])

                                primer_resultado = resultados[0]



                                Tipo_Acta = primer_resultado.get('Tipo_Acta','')                          
                                Fecha_Registro = primer_resultado.get('Fecha_Registro','')
                                N_Acta = primer_resultado.get('N_Acta','')
                                apePaterno = primer_resultado.get('apePaterno','')
                                apeMaterno = primer_resultado.get('apeMaterno','')
                                nuDni = primer_resultado.get('nuDni','')
                                preNombres = primer_resultado.get('preNombres','')
                                imagenActaAnverso = primer_resultado.get('imagenActaAnverso')
                                imagenActaReverso = primer_resultado.get('imagenActaReverso')




                                # Guardar la imagen en un archivo con ruta dinámica
                                dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                ruta_archivo = f"./ACTAN/imagen1.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(imagenActaAnverso))




                                # Guardar la imagen en un archivo con ruta dinámica
                                dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                ruta_archivo = f"./ACTAN/imagen2.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(imagenActaReverso))








                                imagen1 = "./ACTAN/imagen1.jpg"
                                imagen2 = "./ACTAN/imagen2.jpg"

                                # Cargar las imágenes
                                img1 = Image.open(imagen1)
                                img2 = Image.open(imagen2)

                                # Crear el archivo PDF
                                pdf = canvas.Canvas(f"./ACTAN/{dni1}.pdf", pagesize=img1.size)

                                # Añadir la primera imagen a la primera página del archivo PDF
                                pdf.drawImage(imagen1, 0, 0)

                                # Añadir una nueva página para la segunda imagen
                                pdf.showPage()

                                # Añadir la segunda imagen a la segunda página del archivo PDF
                                pdf.drawImage(imagen2, 0, 0)

                                # Guardar el archivo PDF
                                pdf.save()





















                                print("Archivo PDF creado correctamente.")


                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)



                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon

                                Servicio = "actas reniec"
                                Comando = "/actn"
                               


                                #thumbnail sirve enviar el pdf con foto 

                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./ACTAN/{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] ACTA NACMIENTO </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./ACTAN/{dni1}.pdf"
                                ruta_imagen1 = f"./ACTAN/imagen1.jpg"
                                ruta_imagen2 = f"./ACTAN/imagen2.jpg"


                                if os.path.exists(ruta_imagen0):
                                    # Eliminar el archivo
                                    os.remove(ruta_imagen0)
                                    os.remove(ruta_imagen1)
                                    os.remove(ruta_imagen2)
                                                                                
                                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")



                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"El servicio de reniec esta en mantenimiento":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] El servicio de reniec esta en mantenimiento", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado o datos incompletos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado el servidor no responde":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"DNI Cancelado en RENIEC":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] DNI Cancelado en RENIEC", parse_mode="html")


                                elif respuesta == f"DNI tiene mas de 18 años":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] El DNI tiene mas de 18 años", parse_mode="html")





                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Reniec</b> no está disponible en este momento", parse_mode="html")




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/actn] seguido de un número de DNI de 8 dígitos \n\n➜ EJEMPLO: [/actn 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")




@bot.message_handler(commands=["actadef","ACTADEF"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/actadef 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/actn"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [actadef] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 :



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            curl = "http://161.132.48.93:5000/api/acta_defuncion"
                            params = {
                                "token" : "O7gBHY9MapZEBH" ,
                                "dni": dni1,
                            }
                            response = requests.get(curl, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                resultados = data.get('Resultados',[])

                                primer_resultado = resultados[0]



                                Tipo_Acta = primer_resultado.get('Tipo_Acta','')                          
                                Fecha_Registro = primer_resultado.get('Fecha_Registro','')
                                N_Acta = primer_resultado.get('N_Acta','')
                                apePaterno = primer_resultado.get('apePaterno','')
                                apeMaterno = primer_resultado.get('apeMaterno','')
                                nuDni = primer_resultado.get('nuDni','')
                                preNombres = primer_resultado.get('preNombres','')
                                imagenActaAnverso = primer_resultado.get('imagenActaAnverso')
                                imagenActaReverso = primer_resultado.get('imagenActaReverso')




                                # Guardar la imagen en un archivo con ruta dinámica
                                dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                ruta_archivo = f"./ACTADEF/imagen1.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(imagenActaAnverso))




                                # Guardar la imagen en un archivo con ruta dinámica
                                dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                ruta_archivo = f"./ACTADEF/imagen2.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(imagenActaReverso))








                                imagen1 = "./ACTADEF/imagen1.jpg"
                                imagen2 = "./ACTADEF/imagen2.jpg"

                                # Cargar las imágenes
                                img1 = Image.open(imagen1)
                                img2 = Image.open(imagen2)

                                # Crear el archivo PDF
                                pdf = canvas.Canvas(f"./ACTADEF/{dni1}.pdf", pagesize=img1.size)

                                # Añadir la primera imagen a la primera página del archivo PDF
                                pdf.drawImage(imagen1, 0, 0)

                                # Añadir una nueva página para la segunda imagen
                                pdf.showPage()

                                # Añadir la segunda imagen a la segunda página del archivo PDF
                                pdf.drawImage(imagen2, 0, 0)

                                # Guardar el archivo PDF
                                pdf.save()





















                                print("Archivo PDF creado correctamente.")


                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)



                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon
                                Servicio = "RENIEC"
                                Comando = "/actadef"
                           
                                #thumbnail sirve enviar el pdf con foto 

                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./ACTADEF/{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] ACTA DEFUNCION </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./ACTADEF/{dni1}.pdf"
                                ruta_imagen1 = f"./ACTADEF/imagen1.jpg"
                                ruta_imagen2 = f"./ACTADEF/imagen2.jpg"


                                if os.path.exists(ruta_imagen0):
                                    # Eliminar el archivo
                                    os.remove(ruta_imagen0)
                                    os.remove(ruta_imagen1)
                                    os.remove(ruta_imagen2)
                                                                                
                                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")



                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"El servicio de reniec esta en mantenimiento":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] El servicio de reniec esta en mantenimiento", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado o datos incompletos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado el servidor no responde":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"DNI Cancelado en RENIEC":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] DNI Cancelado en RENIEC", parse_mode="html")


                                elif respuesta == f"DNI tiene mas de 18 años":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] El DNI tiene mas de 18 años", parse_mode="html")





                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Reniec</b> no está disponible en este momento", parse_mode="html")




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/actadef] seguido de un número de DNI de 8 dígitos \n\n➜ EJEMPLO: [/actadef 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")


@bot.message_handler(commands=["actamatri","ACTAMATRI"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/actamatri 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/actn"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [actadef] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 :



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            curl = "http://161.132.48.93:5000//api/acta_matrimonio"
                            params = {
                                "token" : "O7gBHY9MapZEBH" ,
                                "dni": dni1,
                            }
                            response = requests.get(curl, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                resultados = data.get('Resultados',[])

                                primer_resultado = resultados[0]



                                Tipo_Acta = primer_resultado.get('Tipo_Acta','')                          
                                Fecha_Registro = primer_resultado.get('Fecha_Registro','')
                                N_Acta = primer_resultado.get('N_Acta','')
                                apePaterno = primer_resultado.get('apePaterno','')
                                apeMaterno = primer_resultado.get('apeMaterno','')
                                nuDni = primer_resultado.get('nuDni','')
                                preNombres = primer_resultado.get('preNombres','')
                                imagenActaAnverso = primer_resultado.get('imagenActaAnverso')
                                imagenActaReverso = primer_resultado.get('imagenActaReverso')




                                # Guardar la imagen en un archivo con ruta dinámica
                                dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                ruta_archivo = f"./ACTAMATRI/imagen1.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(imagenActaAnverso))




                                # Guardar la imagen en un archivo con ruta dinámica
                                dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                ruta_archivo = f"./ACTAMATRI/imagen2.jpg"  # Ruta y nombre de archivo con variable dni1
                                with open(ruta_archivo, "wb") as archivo:
                                    archivo.write(base64.b64decode(imagenActaReverso))








                                imagen1 = "./ACTAMATRI/imagen1.jpg"
                                imagen2 = "./ACTAMATRI/imagen2.jpg"

                                # Cargar las imágenes
                                img1 = Image.open(imagen1)
                                img2 = Image.open(imagen2)

                                # Crear el archivo PDF
                                pdf = canvas.Canvas(f"./ACTAMATRI/{dni1}.pdf", pagesize=img1.size)

                                # Añadir la primera imagen a la primera página del archivo PDF
                                pdf.drawImage(imagen1, 0, 0)

                                # Añadir una nueva página para la segunda imagen
                                pdf.showPage()

                                # Añadir la segunda imagen a la segunda página del archivo PDF
                                pdf.drawImage(imagen2, 0, 0)

                                # Guardar el archivo PDF
                                pdf.save()








                                print("Archivo PDF creado correctamente.")


                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)



                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon


                                Servicio = "ACTA MATRIMONIO"
                                Comando = "/actam"
                                



                                #thumbnail sirve enviar el pdf con foto 

                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./ACTAMATRI/{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] ACTA MATRIMONIO </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./ACTAMATRI/{dni1}.pdf"
                                ruta_imagen1 = f"./ACTAMATRI/imagen1.jpg"
                                ruta_imagen2 = f"./ACTAMATRI/imagen2.jpg"


                                if os.path.exists(ruta_imagen0):
                                    # Eliminar el archivo
                                    os.remove(ruta_imagen0)
                                    os.remove(ruta_imagen1)
                                    os.remove(ruta_imagen2)
                                                                                
                                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")



                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"El servicio de reniec esta en mantenimiento":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] El servicio de reniec esta en mantenimiento", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado o datos incompletos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado el servidor no responde":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"DNI Cancelado en RENIEC":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] DNI Cancelado en RENIEC", parse_mode="html")


                                elif respuesta == f"DNI tiene mas de 18 años":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] El DNI tiene mas de 18 años", parse_mode="html")





                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Reniec</b> no está disponible en este momento", parse_mode="html")




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/actamatri] seguido de un número de DNI de 8 dígitos \n\n➜ EJEMPLO: [/actamatri 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")











@bot.message_handler(commands=["notas","NOTAS"])
def cmd_dni(message):





    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/notas 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/dnivel"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [NOTAS] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 :



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            curl = "http://161.132.48.93:5000/buscar/minedu"
                            token = "acYrJNje9faCXv8I"
                            params = {
                                "token": token,
                                "dni": dni1,
                            }
                            response = requests.get(curl, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                diccionario_respuesta = respuesta[0]







                                codigoModular = diccionario_respuesta.get('codigoModular')
                                descripcionGrado = diccionario_respuesta.get('descripcionGrado')
                                documento = diccionario_respuesta.get('documento')
                                idAnio = diccionario_respuesta.get('idAnio')
                                nivelColegio = diccionario_respuesta.get('nivelColegio')
                                nombreIE = diccionario_respuesta.get('nombreIE')

                                pdf_sexo = diccionario_respuesta.get('pdf64')







                                # Decodificar la cadena Base64
                                datos_binarios = base64.b64decode(pdf_sexo)

                                # Escribir los datos binarios en un archivo PDF
                                with open(f"./NOTAS/{dni1}.pdf", "wb") as archivo_pdf:
                                    archivo_pdf.write(datos_binarios)

                                print("Archivo PDF creado correctamente.")


                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)



                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon



                                Servicio = "MINEDU"
                                Comando = "/notas"
                               



                                #thumbnail sirve enviar el pdf con foto 

                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./NOTAS/{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] CONTANCIA APRENDIZAJE </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>CODIGO</b> ➟ <code> {codigoModular}</code>\n"
                                                                                                    f"<b>COLEGIO</b> ➟ <code>{nombreIE}</code>\n"
                                                                                                    f"<b>AÑO</b> ➟ <code> {idAnio}</code>\n"
                                                                                                    f"<b>NIVEL</b> ➟ <code> {nivelColegio}</code>\n"
                                                                                                    f"<b>GRADO</b> ➟ <code> {descripcionGrado}</code>\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./NOTAS/{dni1}.pdf"




                                if os.path.exists(ruta_imagen0):
                                    # Eliminar el archivo
                                    os.remove(ruta_imagen0)
                                                                                
                                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")



                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"Los datos ingresados NO corresponden a una persona de 16 años a más, deberá solicitar la constancia mediante la opción “Apoderado”.":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información, deberá solicitar la constancia mediante la opción “Apoderado”.", parse_mode="html")

                                elif respuesta == f"El servicio de reniec esta en mantenimiento":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] El servicio de reniec esta en mantenimiento", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado o datos incompletos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado el servidor no responde":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"DNI Cancelado en RENIEC":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] DNI Cancelado en RENIEC", parse_mode="html")
                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Reniec</b> no está disponible en este momento", parse_mode="html")




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tel] seguido de un número de DNI de 8 dígitos o numero 9 dígitos\n\n➜ EJEMPLO: [/tel 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")







@bot.message_handler(commands=["placab","PLACAB"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/placab ARU579</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/dnivel"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰",url="https://t.me/BlassRR" )
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [dnivel] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥" ,url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 6:



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            curl = "https://api.deathdata.net/api/placas/sunarp?placa={placa_para_api}&usuario=ghost-1b2a3a9a3b8c"
                            params = {
                                "token" : "O7gBHY9MapZEBH" ,
                                "placa": dni1,
                            }
                            response = requests.get(curl, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                diccionario_respuesta = respuesta[0]
                                pdf_sexo = diccionario_respuesta.get('PDF')
                                # Decodificar la cadena Base64
                                datos_binarios = base64.b64decode(pdf_sexo)

                                # Escribir los datos binarios en un archivo PDF
                                with open(f"./TIVE_PDF/{dni1}.pdf", "wb") as archivo_pdf:
                                    archivo_pdf.write(datos_binarios)

                                print("Archivo PDF creado correctamente.")


                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)



                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon

                                Servicio = "bolte infromativa"
                                Comando = "/placab"
                               

                                #thumbnail sirve enviar el pdf con foto 

                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./TIVE_PDF/{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[##DataGold] BOLETA INFORMATIVA </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./TIVE_PDF/{dni1}.pdf"




                                if os.path.exists(ruta_imagen0):
                                    # Eliminar el archivo
                                    os.remove(ruta_imagen0)
                                                                                
                                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")



                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No se encontro el dni en planilla":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"El servicio de reniec esta en mantenimiento":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] El servicio de reniec esta en mantenimiento", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado o datos incompletos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado el servidor no responde":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"DNI Cancelado en RENIEC":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] DNI Cancelado en RENIEC", parse_mode="html")
                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Reniec</b> no está disponible en este momento", parse_mode="html")




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/placab] seguido de un número de un nmerode tu placa evite - para que la busqueda filtre\n\n➜ EJEMPLO: [/placab ARU579]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")










@bot.message_handler(commands=["placav","PLACAV"])
def cmd_dni(message):












    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/placav ARU579</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/dnivel"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [placav] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥" ,url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 6:



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            curl = "https://api.deathdata.net/api/placas/sunarp?placa={placa_para_api}&usuario=ghost-1b2a3a9a3b8c"
                            params = {
                                "token" : "O7gBHY9MapZEBH" ,
                                "placa": dni1,
                            }
                            response = requests.get(curl, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                diccionario_respuesta = respuesta[0]
                                documento = diccionario_respuesta.get('documento')
                                propietario = diccionario_respuesta.get('propietario')
                                pdf_sexo = diccionario_respuesta.get('PDF')
                                # Decodificar la cadena Base64
                                datos_binarios = base64.b64decode(pdf_sexo)

                                # Escribir los datos binarios en un archivo PDF
                                with open(f"./TARJETA_V/{dni1}.pdf", "wb") as archivo_pdf:
                                    archivo_pdf.write(datos_binarios)

                                print("Archivo PDF creado correctamente.")


                                # Leer el JSON desde el archivo (CREDITOS)
                                with open(f"./Registros/{recipient_id}.json","r") as file:
                                    mi_json = json.load(file)
                
                                mi_json["CRD"] = drgon


                                # Guardar los cambios en el mismo archivo
                                with open(f'./Registros/{huserid}.json', 'w') as file:
                                    json.dump(mi_json, file, indent=2)



                                hfirst_name=message.from_user.first_name
                                huserid=message.from_user.id
                                usernombre= f"{hfirst_name}"
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                if 5000 <= drgon <= 50000:
                                    valor_cred = "♾"

                                else:
                                    valor_cred = drgon

                                Servicio = "TARJETA"
                                Comando = "/placaV"
                               

                                #thumbnail sirve enviar el pdf con foto 

                                thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                thumbnail = open(thumbnail_path, 'rb')
                                document = open(f'./TARJETA_V/{dni1}.pdf', 'rb')
                                bot.send_document(message.chat.id , document=document ,caption=f"<b>[] TARJETA PROPIEDA </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{documento}</code>\n"
                                                                                                    f"<b>PROPIETARIO</b> ➟ <code>{propietario}</code>\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
                                


                                ruta_imagen0 = f"./TARJETA_V/{dni1}.pdf"




                                if os.path.exists(ruta_imagen0):
                                    # Eliminar el archivo
                                    os.remove(ruta_imagen0)
                                                                                
                                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                else:
                                    print(f"El archivo {ruta_imagen0} no existe.")



                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No se encontro el dni en planilla":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"El servicio de reniec esta en mantenimiento":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] El servicio de reniec esta en mantenimiento", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado o datos incompletos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"Ocurrió un error inesperado el servidor no responde":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Ocurrió un error inesperado el servidor no responde", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"DNI Cancelado en RENIEC":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ ⚠️ ] DNI Cancelado en RENIEC", parse_mode="html")
                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Reniec</b> no está disponible en este momento", parse_mode="html")




                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/placav] seguido de un número de un nmerode tu placa evite - para que la busqueda filtre\n\n➜ EJEMPLO: [/placav ARU579]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")















@bot.message_handler(commands=["celxss","CELXsss"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/celx 907676088</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [telp] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if  contador == 9:



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/api_entel"
                            token = "acYrJNje9faCXv8I"

                            params ={

                                "numero": dni1
                            }
                            
                            



                            response = requests.get(url, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                print(data)
                                respuesta = data
                                if respuesta:

                                    
                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "Numero_celx"
                                    Comando = "/celx"

                                    mensaje =""

                                    contadores = 0
                                    valor_x = 0


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                    primer_elemento = respuesta
                
                                    try:

                                        documento = primer_elemento['documento']
                                    except KeyError:
                                        documento = primer_elemento['dni']

                                    try:
                                        titular = primer_elemento['Nombre']
                                    except KeyError:
                                        titular = primer_elemento['nombres']

                                    telefono = dni1




                                    valor_x +=1






                                    print(f"- DNI : {documento} -> NUMERO : {telefono}")  
                                            
                                    mensaje +=f"<b>{valor_x}. Número de Teléfono: </b>\n\n"
                                    mensaje +=f"<b>• DOCUMENTO →</b> <code>{documento}</code>\n"
                                    mensaje +=f"<b>• TITULAR →</b> <code>{titular}</code>\n"
                                    mensaje +=f"<b>• TELEFONO →</b> <code>{telefono}</code>\n\n"                                      





                                    #contadores += 1
                                    #if contadores % 10== 0 or contadores == len(respuesta):

                                            

                                    bot.reply_to(message, f"<b>[#DataGold🌩] - HISTORIAL DEL TITULAR Nº2</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                                        #mensaje = ""

                                    #if len(mensaje) > 0:

                                        #bot.reply_to(message, f"<b>[#𝔹𝕃𝔸𝕂_𝔻𝔸𝕋𝔸_𝕏🌩] - HISTORIAL DEL TITULAR Nº2</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"Error el numero no contiene 9 o 8 dijitos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/celx] seguido de un número   9 dígitos\n\n➜ EJEMPLO: [/celx 975155013]", parse_mode="html")

                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/celx] seguido de un número de DNI  9 dígitos\n\n➜ EJEMPLO: [/celx 975155013]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")







@bot.message_handler(commands=["tel","TEL"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/tel 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id

        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [telp] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/+6LVDDgEHWStlMTQx" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 or contador == 9:



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"https://sseeker.org/api/fono.s?token=acYrJNje9faCXv8I&dni={dni1}"

                            
                            params = {
                                "token": "O7gBHY9MapZEBH" ,
                                "dni": dni1 ,
                            }
                            
                            



                            response = requests.get(url, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                if respuesta:

                                    
                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "API NUMEROS"
                                    Comando = "/tel"
                                    
                                    mensaje =""

                                    contadores = 0
                                    valor_x = 0


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
        
                                    
                                    for lote in respuesta:
                
                                            
                                        dni = lote['DOCUMENTO']
                                        try:
                                            titular = lote['TITULAR']
                                        except KeyError:
                                            titular = ""
                                    
                                
                                        
                                        año1 = lote['ACTIVACION']
                                        operador = lote['OPERADOR']
                                        plan = lote['PLAN'] 
                                        mayusculas = operador.upper()
                                        telefono = lote['NUMERO']




                                        valor_x +=1






                                        print(f"- DNI : {dni} -> NUMERO : {telefono}")  
                                            
                                        mensaje +=f"<b>{valor_x}. Número de Teléfono: </b>\n\n"
                                        mensaje +=f"<b>• DOCUMENTO →</b> <code>{dni}</code>\n"
                                        mensaje +=f"<b>• TITULAR →</b> <code>{titular}</code>\n"
                                        mensaje +=f"<b>• TELEFONO →</b> <code>{telefono}</code>\n"                                      
                                        mensaje +=f"<b>• OPERADOR →</b> <code>{mayusculas}</code>\n"                                      
                                        mensaje +=f"<b>• PLAN →</b> <code>{plan}</code>\n"
                                        mensaje +=f"<b>• FECHA →</b> <code>{año1}</code>\n\n"




                                        contadores += 1
                                        if contadores % 10== 0 or contadores == len(respuesta):

                                            

                                            bot.reply_to(message, f"<b>[#DataGold🌩] - TELEFONIA Nº1</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                                            mensaje = ""

                                    if len(mensaje) > 0:

                                        bot.reply_to(message, f"<b>[#DataGold🌩] - TELEFONIA Nº1</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No se pudo obtener datos en la consulta":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"Error el numero no contiene 9 o 8 dijitos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tel] seguido de un número de DNI 8 o NUMERO  o 9 dígitos\n\n➜ EJEMPLO: [/tel 44444444]\n➜ EJEMPLO: [/tel 975155013]", parse_mode="html")

                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tel] seguido de un número de DNI de 8 dígitos o numero 9 dígitos\n\n➜ EJEMPLO: [/tel 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")









@bot.message_handler(commands=["opsitel","OPSITEL"])
def cmd_dni(message):

















    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/opsitel 74123918</code>\n'


        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):


            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/celx"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [opsitel] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8 or contador == 9:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)

                            url = f"https://sseeker.org/api/opsitel?token=acYrJNje9faCXv8I&dni=45123918"
                            

                            params ={
                                "token": "acYrJNje9faCXv8I" ,
                                "dni": dni1 ,
                            }
                            
                            



                            response = requests.get(url, params=params)
                            status = response.status_code
                            print(response.content)

                        
                            if response.status_code == 200:
                                data = response.json()
                                print(data)
                                respuesta = data['Resultados']
                                if respuesta:
                                    primer_resultado = respuesta[0]

                                    dni_consuta_por_numero = primer_resultado['DOCUMENTO']
                                    print("ELDNI ES ",      dni_consuta_por_numero)

                                    #print("repuestas1",respuesta)

                                    
                                    # Inicializar listas y contador para guardar datos cada tres elementos
                                    datos_cada_tres = []
                                    temp_data = {}
                                    contador = 0

                                    for elemento in respuesta:
                                        # Hacer algo con los datos aquí, como los pasos que ya tienes
    
                                        # Supongamos que los valores ya están asignados
    



                                        # Guardar los valores en un diccionario con un contador
                                        temp_data[f'dni{contador }'] = elemento['DOCUMENTO']
                                        temp_data[f'plan{contador }'] = elemento['PLAN']
                                        temp_data[f'operador{contador}'] = elemento['OPERADOR'].upper()
                                        temp_data[f'telefono{contador}'] = elemento['NUMERO']
                                        temp_data[f'fecha{contador}'] = elemento['ACTIVACION']

                                        contador += 1

                                        # Cada tres elementos, guarda los datos en una lista y reinicia el diccionario temporal y el contador
                                        if contador % 3 == 0:
                                            datos_cada_tres.append(temp_data)
                                            temp_data = {}
                                            contador = 0
                                        elif contador == len(respuesta):  # Si es el último elemento y no es múltiplo de tres, agrégalo a datos_cada_tres
                                            datos_cada_tres.append(temp_data)


                                    # Convertir la lista de diccionarios a formato JSON
                                    datos_json = json.dumps(datos_cada_tres)

                                    # Imprimir o hacer algo con los datos JSON
                                    #print(datos_json)

                                    #FALT RENIEC
                                    
                                    url = f"http://161.132.48.93:5000/api/reniec_buscar?dni={dni_consuta_por_numero}"
    

                                    headers = {
                                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                        "accept-language": "es-419,es;q=0.9",
                                        "cache-control": "max-age=0",
                                        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                                        "sec-ch-ua-mobile": "?0",
                                        "sec-ch-ua-platform": "\"Windows\"",
                                        "sec-fetch-dest": "document",
                                        "sec-fetch-mode": "navigate",
                                        "sec-fetch-site": "none",
                                        "sec-fetch-user": "?1",
                                        "upgrade-insecure-requests": "1"
                                    }
                                    print("HACIENDO CONSULTA EN OPSITEL")


                                    response = requests.get(url, headers=headers)
                                    #print(response)
                        
    
                                    if response.status_code == 200:
                                        data = response.json()
    
                                        respuesta = data['Respuesta'][0]

                                        if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                            bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                        elif respuesta == f"Reniec OFF":
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                            bot.reply_to(message,f"⚠️ EL SERVICIO DE OPSITEL ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                        elif respuesta == f"ERROR EN LA RESPUESTA":
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                            bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                        elif respuesta == f"ERRO DEL SERVIDOR":
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                            bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 

                                        elif respuesta == "dni cancelado":
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                            bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")

                                        else:
                                        
    
                                    
                                            respuesta = data['Respuesta'][0]
                        
                                            nuDni = respuesta["nuDni"]
                                            apePaterno = respuesta["apePaterno"]
                                            apeMaterno = respuesta["apeMaterno"]
                                            preNombres = respuesta["preNombres"]



                                            foto_codificada = respuesta["foto"]



                                            # Guardar la imagen en un archivo con ruta dinámica
                                            dni2 = f"{dni1}"  # Valor de ejemplo para dni1
                                            ruta_archivo = f"./FOTOS_RE/{dni1}.jpg"  # Ruta y nombre de archivo con variable dni1
                                            with open(ruta_archivo, "wb") as archivo:
                                                archivo.write(base64.b64decode(foto_codificada))




                                            # Convertir JSON a Python
                                            parsed_data = json.loads(datos_json)

                                            data = parsed_data[0]


                                            



                                            numero01 = data["telefono0"]
                                            operador01 = data["operador0"]
                                            fecha01 = data["fecha0"]
                                            fech01 = fecha01
                                            hora01 = ""
                                            plan01 = data["plan0"]

                                            print(data)



                                            try:
                                                numero02 = data["telefono1"]
                                                operador02 = data["operador1"]
                                                fecha02 = data["fecha1"]
                                                fech02 = fecha02
                                                hora02 = ""
                                                plan02 = data["plan1"]
                                            except KeyError:
                                                numero02 = "sin informacion"
                                                operador02 = "sin informacion"
                                                fecha02 = "sin informacion"
                                                fech02 = "sin informacion"
                                                hora02 = "sin informacion"
                                                plan02 = "sin informacion"



                                            try:
                                                numero03 = data["telefono2"]
                                                operador03 = data["operador2"]
                                                fecha03 = data["fecha2"]
                                                fech03 = fecha03
                                                hora03 = ""
                                                plan03 = data["plan2"]
                                            except KeyError:
                                                numero03 = "sin informacion"
                                                operador03 = "sin informacion"
                                                fecha03 = "sin informacion"
                                                fech03 = "sin informacion"
                                                hora03 = "sin informacion"
                                                plan03 = "sin informacion"






                                            # Abre ambas imágenes
                                            imagen_fondo = Image.open(f'./FICHAS_OPSITEL/ficha_opsitel.jpg')
                                            imagen_superpuesta = Image.open(f'./FOTOS_RE/{dni1}.jpg')

                                            # Ajusta el tamaño de la imagen superpuesta
                                            nuevo_tamano = (193,210) # especifica el tamaño deseado
                                            imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)

                                            # Pega la imagen superpuesta sobre la imagen de fondo
                                            posicion = (665, 185) # especifica la posición donde se pegará la imagen superpuesta
                                            imagen_fondo.paste(imagen_superpuesta, posicion)




                                            # Crea un objeto ImageDraw para dibujar sobre la imagen
                                            dibujar = ImageDraw.Draw(imagen_fondo)

                                            #dni
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{nuDni}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 140)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 30)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{preNombres} {apePaterno} {apeMaterno}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (150, 190)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)


                                            #comienza los numeros 


                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{numero01}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 390)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)

                                            #OPERADORA1
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{operador01}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 430)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                            #PLAN1
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{plan01}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 470)#160

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)


                                            #FECHA DE ACTIVACION1
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{fech01}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 508)#220

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                            #HORA DE ACTIVACION1
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{hora01}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 543)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)






                                            #PARTE2


                                            #NUMERO2
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{numero02}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 639)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)


                                            #OPERADORA2
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{operador02}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 679)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)


                                            #PLAN2
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{plan02}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 719)#160

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)







                                            #FECHA DE ACTIVACION2
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{fech02}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 755)#220

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                            #HORA DE ACTIVACION2
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{hora02}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 790)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)







                                            #PARTE 3


                                            #NUMERO3
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{numero03}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 887)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)





                                            #OPERADORA3
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{operador03}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 925)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                            #PLAN3
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{plan03}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 965)#160

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                            #FECHA DE ACTIVACION3
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{fech03}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 1001)#220

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)



                                            #HORA DE ACTIVACION3
                                            # Define la ubicación y el texto a agregar
                                            texto1 = f"{hora03}"
                                            #y=costado ,x arriba pa abajo
                                            ubicacion1 = (240, 1037)

                                            # Define la fuente del texto
                                            fuente1 = ImageFont.truetype("./letras/arial.ttf", 20)

                                            # Agrega el texto a la imagen
                                            dibujar.text(ubicacion1, texto1, fill=(255, 255, 255), font=fuente1)




                                            # Guarda la imagen con el texto agregado
                                            imagen_fondo.save(f'./FICHAS_OPSITEL/{dni1}.jpg')

                                    
                                            "segundo"
                                            # Cargamos la imagen

                    

                                            # Cargar la imagen
                                            img = Image.open(f'./FICHAS_OPSITEL/{dni1}.jpg')

                                            # Crear el archivo PDF
                                            pdf = canvas.Canvas(f"./FICHAS_OPSITEL/{dni1}.pdf", pagesize=img.size)

                                            # Añadir la imagen al archivo PDF
                                            pdf.drawImage(f'./FICHAS_OPSITEL/{dni1}.jpg', 0, 0)
        
                                            # Guardar el archivo PDF
                                            pdf.save()





                                            # Leer el JSON desde el archivo (CREDITOS)


                                            with open(f"./Registros/{recipient_id}.json","r") as file:
                                                mi_json = json.load(file)
                    
                                            mi_json["CRD"] = drgon


                                            # Guardar los cambios en el mismo archivo
                                            with open(f'./Registros/{huserid}.json', 'w') as file:
                                                json.dump(mi_json, file, indent=2)



                                            if 5000 <= drgon <= 50000:
                                                valor_cred = "♾"

                                            else:
                                                valor_cred = drgon



                                            Servicio = "FICHA TELEFONICA"
                                            Comando = "/opsitel"
                                            
 



                                            hfirst_name=message.from_user.first_name
                                            huserid=message.from_user.id
                                            usernombre= f"{hfirst_name}"
                                            bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)


                                            #thumbnail sirve enviar el pdf con foto 

                                            thumbnail_path = f'./FICHAS_OPSITEL/{dni1}.jpg'
                                            thumbnail = open(thumbnail_path, 'rb')
                                            document = open(f'./FICHAS_OPSITEL/{dni1}.pdf', 'rb')
                                            bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] FICHA TELEFONICA </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)


                                            ruta_imagen0 = f"./FOTOS_RE/{dni1}.jpg"
                                            ruta_imagen1 = f"./FICHAS_OPSITEL/{dni1}.jpg"
                                            ruta_imagen2 = f"./FICHAS_OPSITEL/{dni1}.pdf"

        
                                            if os.path.exists(ruta_imagen0):
                                                # Eliminar el archivo
                                                os.remove(ruta_imagen0)
                                                os.remove(ruta_imagen1)
                                                os.remove(ruta_imagen2)                                                                                
                                                print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                            else:
                                                print(f"El archivo {ruta_imagen0} no existe.")
                                    



                            else:
                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No se pudo obtener datos en la consulta":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"Error el numero no contiene 9 o 8 dijitos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tel] seguido de un número de DNI 8 o NUMERO  o 9 dígitos\n\n➜ EJEMPLO: [/tel 44444444]\n➜ EJEMPLO: [/tel 975155013]", parse_mode="html")

                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")
                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/opsitel] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/optiel 44444444]", parse_mode="html")

                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")













@bot.message_handler(commands=["mtc","MTC"])
def cmd_dni(message):











    mtc = "".join(message.text.split()[1:2])
    

        

    if not mtc:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/mtc 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/mtc"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [mtc] {mtc}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{mtc}"

                        contador = len(numero)

                        if contador == 8 :
                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {mtc}", parse_mode="html")




                        

                            url = f"http://161.132.48.93:5000/api/mtc"

                            params = {
                                "token" : "O7gBHY9MapZEBH" ,
                                "dni": mtc ,
                            }






                        


                            response = requests.get(url, params=params)
                            status = response.status_code
                            print(response)
                    

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados'][0]

                                Nro_licencia = respuesta.get('Nro_licencia')


                                Categoria_licencia = " ".join(respuesta.get('Categoria_licencia', []))

                                categoria_dividida = Categoria_licencia.split(' ')

                                if len(categoria_dividida) == 2:
                                    categoria_principal = categoria_dividida[0]
                                    categoria_secundaria = categoria_dividida[1]
                                else:
                                    categoria_principal = Categoria_licencia
                                    categoria_secundaria = None



                                FechaExpedicion = respuesta.get('FechaExpedicion')
                                FechaRevalidacion = respuesta.get('FechaRevalidacion')

                                TIPO_dni = "DNI"





                                Servicio =  respuesta.get('Correlato')



                                Nro_documento = mtc


                                restricciones = respuesta.get('Restricciones')


                                grupo_sanginio = respuesta.get('GrupoSanguineo')

                                dona_organos = respuesta.get('DonacionOrganos')

                                print(grupo_sanginio)




                                url = f"http://161.132.48.93:5000/api/reniec_buscar"

                                params = {
                                    "dni": mtc
                                }




                                print("hacienod l consulta ")


                                response = requests.get(url, params=params)
                                print(response)
                        

                                
                                data = response.json()
    
                                respuesta = data['Respuesta'][0]

                                if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

                                elif respuesta == f"Reniec OFF":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

                                elif respuesta == f"ERROR EN LA RESPUESTA":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

                                elif respuesta == f"ERRO DEL SERVIDOR":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


                                elif respuesta == "dni cancelado":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")
                                else:

                                    print(data)
                    
                                    apePaterno = respuesta["apePaterno"]
                                    apeMaterno = respuesta["apeMaterno"]
                                    preNombres = respuesta["preNombres"]
                                    fecha_nacimiento = respuesta["feNacimiento"]

                                    direcion = respuesta["desDireccion"]
                        
                        

                                    foto_codificada = respuesta["foto"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{mtc}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/fotos0.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))

                                    foto_codificada = respuesta["firma"]

                                    # Guardar la imagen en un archivo con ruta dinámica
                                    dni2 = f"{mtc}"  # Valor de ejemplo para dni1
                                    ruta_archivo = f"./FOTOS_RE/fotos1.jpg"  # Ruta y nombre de archivo con variable dni1
                                    with open(ruta_archivo, "wb") as archivo:
                                        archivo.write(base64.b64decode(foto_codificada))











                                    # Abre ambas imágenes
                                    imagen_fondo = Image.open(f'./MTC/Licencia.jpg')
                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/fotos0.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (635,822) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)


                                    posicion = (1850, 1029)
                                    imagen_fondo.paste(imagen_superpuesta, posicion)
        

                                    #firma

                                    imagen_superpuesta = Image.open(f'./FOTOS_RE/fotos1.jpg')

                                    # Ajusta el tamaño de la imagen superpuesta
                                    nuevo_tamano = (600,250) # especifica el tamaño deseado
                                    imagen_superpuesta = imagen_superpuesta.resize(nuevo_tamano)


                                    posicion = (1900, 1860)
                                    imagen_fondo.paste(imagen_superpuesta, posicion)



                                    dibujar = ImageDraw.Draw(imagen_fondo)


                                    #LICENCIA

                                    texto1 = f"{Nro_licencia}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 650)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #CLASE

                                    texto1 = f"{categoria_principal}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 810)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #CATEGORIA

                                    texto1 = f"{categoria_secundaria}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (855, 810)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #FECHA EXPEDICION

                                    texto1 = f"{FechaExpedicion}"
                            
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 970)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)







                                    #FECHA REVELACION

                                    texto1 = f"{FechaRevalidacion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 1130)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)





                                    #apellidos
                                    texto1 = f"{apePaterno} {apeMaterno}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 1500)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 55)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #NOMBRES

                                    texto1 = f"{preNombres}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 1660)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 55)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #DNI

                                    texto1 = f"{TIPO_dni} {Nro_documento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 1830)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #servicio

                                    texto1 = f"{Servicio}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 1980)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #numero primegenico

                                    texto1 = f"{Nro_documento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (590, 1980)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #FECHA NACMIENTO 

                                    texto1 = f"{fecha_nacimiento}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 2140)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #DIRECION 

                                    texto1 = f"{direcion}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 2300)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 50)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                    #RESTRINCION 

                                    texto1 = f"{restricciones}"
                                    #y=costado ,x arriba pa abajo
                                    ubicacion1 = (260, 2550)

                                    # Define la fuente del texto
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)




                                    #GRUPO SANGINIO

                                    texto1 = f"{grupo_sanginio}"
                    
                                    ubicacion1 = (260, 2780)

                    
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                    #DONACION DE ORGANO

                                    texto1 = f"{dona_organos}"
                    
                                    ubicacion1 = (260, 2950)

                    
                                    fuente1 = ImageFont.truetype("./letras/arialbd.ttf", 60)

                                    # Agrega el texto a la imagen
                                    dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                    imagen_fondo.save(f'./MTC/{mtc}.jpg')




                                    # Cargar la imagen
                                    img = Image.open(f'./MTC/{mtc}.jpg')

                                    # Crear el archivo PDF
                                    pdf = canvas.Canvas(f"./MTC/{mtc}.pdf", pagesize=img.size)

                                    # Añadir la imagen al archivo PDF
                                    pdf.drawImage(f'./MTC/{mtc}.jpg', 0, 0)

                                    # Guardar el archivo PDF
                                    pdf.save()



                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    hfirst_name=message.from_user.first_name
                                    huserid=message.from_user.id
                                    usernombre= f"{hfirst_name}"
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon


                                    Servicio = "MTC LICENCIA"
                                    Comando = "/mtc"
                                    dni1 = mtc
                                    


                                    #thumbnail sirve enviar el pdf con foto 

                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./MTC/{mtc}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] LICENCIA MTC </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{mtc}</code>\n"
                                                                                                    f"<b>NOMBRES</b> ➟ <code>{preNombres}</code>\n"
                                                                                                    f"<b>AP PATERNO</b> ➟ <code>{apePaterno}</code>\n"
                                                                                                    f"<b>AP MATERNO</b> ➟ <code>{apeMaterno}</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)



                                    ruta_imagen1 = f"./MTC/{mtc}.jpg"
                                    ruta_imagen2 = f"./MTC/{mtc}.pdf"



                                    if os.path.exists(ruta_imagen1):
                                        # Eliminar el archivo

                                        os.remove(ruta_imagen1)
                                        os.remove(ruta_imagen2)
                                                                                
                                        print(f"Archivo {ruta_imagen1} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen1} no existe.")





                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")

                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/mtc] seguido de un número de DNI de 8 dígitos \n\n➜ EJEMPLO: [/mtc 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")





@bot.message_handler(commands=["papeletas","PAPELETAS"])
def cmd_dni(message):














    dni1 = "".join(message.text.split()[1:2])
    

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/papeletas 74123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return





            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [PAPELETAS] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥", url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8 or contador == 9:



                            message0 = bot.reply_to(message , f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/api/mtc_papeletas"

                            
                            params = {
                                "token": "O7gBHY9MapZEBH",
                                "dni": dni1
                            }
                            
                            



                            response = requests.get(url, params=params)
                            status = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                if respuesta:

                                    
                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon


                                    mensaje =""

                                    contadores = 0
                                    valor_x = 0



                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
        
                                    
                                    for lote in respuesta:
                
                                            
                                        cod_administrado = lote['cod_administrado']
                                        cod_entidad = lote['cod_entidad']
                                        dat_fecha_firme = lote['dat_fecha_firme']
                                        entidad = lote['entidad']
                                        estado = lote['estado']
                                        falta = lote['falta']
                                        fec_infraccion = lote['fec_infraccion']
                                        num_infraccion = lote['cod_administrado']
                                        p_proceso = lote['cod_administrado']
                                        papeleta = lote['cod_administrado']

                                        puntos_firmes = lote['cod_administrado']
                                        tipopit = lote['cod_administrado']










                                        #print(f"- DNI : {dni} -> NUMERO : {telefono}")  
                                            
                                        mensaje +=f"<b>🚦 Infracción Reportada</b>\n\n"
                                        mensaje +=f"<b>📋 Datos de la Infracción:</b>\n\n"
                                        mensaje +=f"<b>• Código Administrado: </b> <code>{cod_administrado}</code>\n"
                                        mensaje +=f"<b>• Número de Infracción: </b> <code>{num_infraccion}</code>\n"
                                        mensaje +=f"<b>• Código de Entidad: </b> <code>{cod_entidad}</code>\n"                                      
                                        mensaje +=f"<b>• Entidad: </b> <code>{entidad}</code>\n"                                      
                                        mensaje +=f"<b>• Papeleta: </b> <code>{papeleta}</code>\n"
                                        mensaje +=f"<b>• Fecha de Infracción: </b> <code>{fec_infraccion}</code>\n\n"
                                        mensaje +=f"<b>• Estado: </b> <code>{estado}</code>\n\n"

                                        mensaje +=f"<b>• ℹ️ Detalles Adicionales:</b>\n\n"
                                        mensaje +=f"<b>• Falta →</b> <code>{falta}</code>\n"
                                        mensaje +=f"<b>• Puntos →</b> <code>{puntos_firmes}</code>\n"
                                        mensaje +=f"<b>• Proceso →</b> <code>{p_proceso}</code>\n"
                                        mensaje +=f"<b>• Tipo de PIT →</b> <code>{tipopit}</code>\n\n"





                                        contadores += 1
                                        if contadores % 1== 0 or contadores == len(respuesta):

                                            

                                            bot.reply_to(message, f"<b>[#DataGold🌩] - PAPELTEAS MTC Nº1</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                                            mensaje = ""

                                    if len(mensaje) > 0:

                                        bot.reply_to(message, f"<b>[#DataGold🌩] - PAPELTEAS MTC Nº1</b>\n\n{mensaje}💰 Creditos : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")


                            else:


                                data = response.json()
                                respuesta = data['error']

                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")

                                elif respuesta == f"Error el numero no contiene 9 o 8 dijitos":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tel] seguido de un número de DNI 8 o NUMERO  o 9 dígitos\n\n➜ EJEMPLO: [/tel 44444444]\n➜ EJEMPLO: [/tel 975155013]", parse_mode="html")

                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/papeletas] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/papeletas 44444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")









@bot.message_handler(commands=["tra"])
def cmd_dni(message):








    dni1 = "".join(message.text.split()[1:2])


    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/tra 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/sbs"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return


            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [tra] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥", url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/buscar/trabjos"

                            params = {
                                "dni" : dni1
                            }

                            

                            response = requests.get(url, params=params)

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                if respuesta:

                                    
                                    # Divide los diccionarios en lotes de 10
                                    lotes_de_diccionarios = [respuesta[i:i + 10] for i in range(0, len(respuesta), 10)]


                                    # Imprime el número de páginas
                                    numero_de_paginas = len(lotes_de_diccionarios)
                                    print(f"El número total de páginas es: {numero_de_paginas}")
                                    print("La respuesta en formato JSON es:")

                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                    # Leer el JSON desde el archivo (CREDITOS)


                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                    
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon


                                    guardar =""
                                    contadores = 0
                                    contador_paginas = 0
                                    for elemento in respuesta:
                                        rut = elemento['ruc']
                                        trabajo = elemento['nombre_empresa']
                                        estado = elemento['situacion']
                                        mensualida = elemento['sueldo']
                                        fecha = elemento['fecha']
                                        contadores += 1

                                        guardar += f"<b>DENOMINACION:</b> <code>{trabajo}</code>\n<b>• RUC:</b> <code>{rut}</code>\n<b>• SUELDO:</b> <code>S/.{mensualida}</code>\n<b>• PERIODO:</b> <code>{estado}</code>\n<b>• Fecha:</b> <code>{fecha}</code>\n\n"

                                        
                                        if contadores % 10== 0 or contadores == len(respuesta):
                                            contador_paginas += 1
                                            bot.reply_to(message,f"<b>[#DataGold🌩] ➣ HISTORIAL DE TRABAJOS</b>\n\n[{contador_paginas}/{numero_de_paginas}]\n\n{guardar}💰 Credits : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")
                                            guardar =""

                                    
                                    if len(guardar) > 0:
                                        contador_paginas += 1
                                        bot.reply_to(message,f"<b>[#DataGold🌩] ➣ HISTORIAL DE TRABAJOS</b>\n\n[{contador_paginas}/{numero_de_paginas}]\n\n{guardar}💰 Credits : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")
                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                            else:
                                data = response.json()
                                respuesta = data['error']


                                if  respuesta == f"No se encontro el informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")
                                else:


                                    bot.reply_to(message,f"[❗️] No hay informacion [Trabajo]", parse_mode="html")



                        else:

                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/tra] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/tra 44444444]", parse_mode="html")

                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")





@bot.message_handler(commands=["sbs"])
def cmd_dni(message):








    dni1 = "".join(message.text.split()[1:2])


    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/sbs 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/sbs"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return


            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [sbs] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥", url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/buscar/sbs"

                            params = {
                                "tokem" : "O7gBHY9MapZEBH",
                                "dni" : dni1
                            }

                            

                            response = requests.get(url, params=params)

                            if response.status_code == 200:
                                data = response.json()
                                respuesta = data['Resultados']
                                if respuesta:

                                    
                                    # Divide los diccionarios en lotes de 10
                                    lotes_de_diccionarios = [respuesta[i:i + 10] for i in range(0, len(respuesta), 10)]


                                    # Imprime el número de páginas
                                    numero_de_paginas = len(lotes_de_diccionarios)
                                    print(f"El número total de páginas es: {numero_de_paginas}")
                                    print("La respuesta en formato JSON es:")

                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                    # Leer el JSON desde el archivo (CREDITOS)


                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                    
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon


                                    guardar =""
                                    contadores = 0
                                    contador_paginas = 0
                                    for elemento in respuesta:
                                        codigo = elemento['codigo']
                                        entidad = elemento['entidad']
                                        saldo = elemento['saldo']
                                        tipo = elemento['tc']
                                        tipocuenta = elemento['tipocuenta']
                                        descripcion = elemento['descripcion']

                                        contadores += 1

                                        guardar += f"<b>CODIGO SBS:</b> <code>{codigo}</code>\n"
                                        guardar += f"<b>• ENTIDAD:</b> <code>{entidad}</code>\n"
                                        guardar += f"<b>• SUELDO:</b> <code>S/.{saldo}</code>\n"
                                        guardar += f"<b>• TIPO:</b> <code>{tipo}</code>\n"
                                        guardar += f"<b>• TIPO DE CUENTA:</b> <code>{tipocuenta}</code>\n"
                                        guardar += f"<b>• DESCRIPCION:</b> <code>{descripcion}</code>\n\n"

                                        
                                        if contadores % 10== 0 or contadores == len(respuesta):
                                            contador_paginas += 1
                                            bot.reply_to(message,f"<b>[#DataGold🌩] ➣ SBS</b>\n\n[{contador_paginas}/{numero_de_paginas}]\n\n{guardar}💰 Credits : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")
                                            guardar =""

                                    
                                    if len(guardar) > 0:
                                        contador_paginas += 1
                                        bot.reply_to(message,f"<b>[#DataGold🌩] ➣ SBS</b>\n\n[{contador_paginas}/{numero_de_paginas}]\n\n{guardar}💰 Credits : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")
                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                            else:
                                data = response.json()
                                respuesta = data['error']


                                if  respuesta == f"No se encontro el informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                elif respuesta == f"Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")
                                else:


                                    bot.reply_to(message,f"[❗️] No hay informacion [Trabajo]", parse_mode="html")



                        else:

                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/sbs] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/sbs 44444444]", parse_mode="html")

                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")



@bot.message_handler(commands=["seeker"])
def cmd_dni(message):








    dni1 = "".join(message.text.split()[1:2])


    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/seeker 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/sbs"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return


            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [SEEKER] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥", url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.55.126:6900/api/sisweb/dni/{dni1}"


                            try:

                                response = requests.get(url, timeout=10)

                                if response.status_code == 200:
                                    data = response.json()

                                    if 'archivopdf' in data and data['archivopdf']:
                                        respuesta = data['archivopdf']
                                        datos_binarios = base64.b64decode(respuesta)
                                


                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                        # Leer el JSON desde el archivo (CREDITOS)


                                        with open(f"./Registros/{recipient_id}.json","r") as file:
                                            mi_json = json.load(file)
                    
                                        mi_json["CRD"] = drgon


                                        # Guardar los cambios en el mismo archivo
                                        with open(f'./Registros/{huserid}.json', 'w') as file:
                                            json.dump(mi_json, file, indent=2)

                                        if 5000 <= drgon <= 50000:
                                            valor_cred = "♾"

                                        else:
                                            valor_cred = drgon
















                                        with open(f"./seeker/{dni1}.pdf", "wb") as archivo_pdf:
                                            archivo_pdf.write(datos_binarios)





                                        thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                        thumbnail = open(thumbnail_path, 'rb')
                                        document = open(f'./seeker/{dni1}.pdf', 'rb')
                                        bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] SEEKER PDF </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
    
                                        ruta_imagen0 = f"./seeker/{dni1}.pdf"

    
                                        if os.path.exists(ruta_imagen0):
                                            # Eliminar el archivo
                                            os.remove(ruta_imagen0)
                                                                                    
                                            print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                        else:
                                            print(f"El archivo {ruta_imagen0} no existe.")







                                    else:
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                else:
                                    data = response.json()
                                    respuesta = data['error']


                                    if  respuesta == f"No se encontro el informacion":
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")

                                    elif respuesta == f"Error en la consulta a la API":
                                        bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                        bot.reply_to(message,f"⚠️ Error en la consulta a la API", parse_mode="html")
                                    else:


                                        bot.reply_to(message,f"[❗️] No hay informacion [SEEKER]", parse_mode="html")

                            except requests.Timeout:
                                bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")


                        else:

                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/SEEKER] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/SEEKER 44444444]", parse_mode="html")

                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")







@bot.message_handler(commands=["cedula"])
def cmd_dni(message):











    dni1 = "".join(message.text.split()[1:2])

        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/cedula 005434695</code>\n'


        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/sbs"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return

            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [cedula] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥", url="https://t.me/BlassRR")
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 9:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            url = f"http://161.132.48.93:5000/venecos"
                            params ={
                                "celula":dni1
                            }



                            response = requests.get(url, params=params)

                            if response.status_code == 200:

                                data = response.json()
                                respuesta = data['Respuesta'][0]


                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro Informacion de la cedula", parse_mode="html")

                                else:

                                    metadatos = ""


                                    Centro =respuesta.get("Centro","")
                                    Cédula =respuesta.get("Cédula","")
                                    Dirección =respuesta.get("Dirección","")
                                    Estado =respuesta.get("Estado","")
                                    Municipio =respuesta.get("Municipio","")
                                    Nombre =respuesta.get("Nombre","")
                                    Parroquia =respuesta.get("Parroquia","")

                                    metadatos += f"<b>[📝] 𝗜𝗡𝗙𝗢</b>\n\n"
                                    metadatos += f"• <b>CEDULA:</b> {Cédula}\n"
                                    metadatos += f"• <b>NOMBRES:</b> {Nombre}\n"
                                    metadatos += f"• <b>NACIONALIDAD:</b> VENEZOLANA\n"
                                    metadatos += f"• <b>ESTADO:</b> {Estado}\n\n"

                                    metadatos += f"[📍] 𝗨𝗕𝗜𝗖𝗔𝗖𝗜𝗢𝗡:\n\n"

                                    metadatos += f"• <b>MUNICIPIO:</b> {Municipio}\n"
                                    metadatos += f"• <b>PARROQUIA:</b> {Parroquia}\n"                                    
                                    metadatos += f"• <b>CENTRO:</b> {Centro}\n"
                                    metadatos += f"• <b>DIRECCION:</b> {Dirección}\n\n"





                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                    
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)




                                    bot.reply_to(message,f"<b>[#DataGold] -  CEDULA VENEZOLANA 🇻🇪 </b>\n\n{metadatos}💰 Credits : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html")














                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/cedula] seguido de un número de cedula de 9 dígitos\n\n➜ EJEMPLO: [/cedula 004444444]", parse_mode="html")

                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")











comandos_ejecutados1 = {}
@bot.message_handler(commands=["hogar"])
def cmd_dni(message):













    dni1 = "".join(message.text.split()[1:2])
    user_id = message.from_user.id
    comandos_ejecutados1[user_id] = "/hogar"
        

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/hogar 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/hogar"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return


            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [hogar] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 3

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        print("No tienes suficientes créditos para la consulta.")
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios." , parse_mode="html")
                    
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"⏳Consultando ... {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"http://sseeker.org/buscarhogar"

                            token = "acYrJNje9faCXv8I"
                            params = {
                                "token": token,
                                "dni" : dni1
                            }


 


                            response = requests.get(url, params=params)
                            print("estatus ", response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
                                #print(data)
                                
                                
    
                                respuesta = data['Respuesta'][0]
                                

                                if  respuesta == f"No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontro información [HG]", parse_mode="html")

                                else:


                                    respuesta = data['Respuesta'][0]
                                    #print(respuesta)

                                    dnis = []
                                    

                                    dni_base =""
                                    guardar = ""
                                    contador = 0
                                    for elemento in respuesta:
                                        dni = elemento['dni']
                                        dnis.append(dni)
                                        aPaterno = elemento['apPat']
                                        aMaterno = elemento['apMat']
                                        nombres = elemento ['Nombres']
                                        sexo = elemento ['Sexo']
                                        edad = elemento ['Edad']
                                        Fecha_Nac = elemento ['Fecha_Nac']
                                        contador += 1


                                        # Construimos una cadena con los datos del familiar actual.
                                        familiar_str = f"🏠 <b>FAMILIAR {contador}</b>\n"
                                        familiar_str += f"- <b>Nombre:</b> {nombres} {aPaterno} {aMaterno}\n"
                                        familiar_str += f"- <b>DNI:</b> {dni}\n"
                                        familiar_str += f"- <b>Edad:</b> {edad} años\n"
                                        familiar_str += f"- <b>Sexo:</b> {sexo}\n"
                                        familiar_str += f"- <b>Fecha_Nacimiento:</b> {Fecha_Nac}\n\n"

                                        # Agregamos la cadena del familiar actual a la variable 'guardar'.
                                        guardar += familiar_str

                                        dni_base += dni



                                    keyboard = InlineKeyboardMarkup(row_width=2)
                                    buttons = []
                                    for dni in dnis:
                                        button = InlineKeyboardButton(dni, callback_data=f"ver_dni_{dni}")
                                        buttons.append(button)


                                    # Dividir los botones en filas de dos
                                    for i in range(0, len(buttons), 2):
                                        keyboard.row(*buttons[i:i + 2])


                                    usernombre = message.from_user.first_name
                                    user_id = message.from_user.id
                                    hfirst_name=message.from_user.first_name
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)





                                    # Leer el JSON desde el archivo (CREDITOS)


                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                    
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)




                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "hogar"
                                    Comando = "/HOGAR"

                                    
                                    contador = guardar.count("FAMILIAR")




                                    bot.reply_to(message,f"<b>FORYX_DATA → META | HOGAR </b>\n\n<code>Se encontro {contador} resultados.</code>\n\n{guardar}💰 Credits : {valor_cred}\n🎖 Solicitado Por: <a href='tg://user?id={user_id}'>{usernombre}</a>", parse_mode="html",reply_markup=keyboard)
                                    


                                        

                                



                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                # Mensaje de error
                                error_message = f"📢 ¡Ups! ubo un problema interno porfavor utilize otro comando /cmd.⚠️ "
                                bot.send_message(message.chat.id, error_message, parse_mode="html")
                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/hogar] seguido de un número de DNI de 8 dígitos\n\n➜ EJEMPLO: [/hogar 44444444]", parse_mode="html")

                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")
                


        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")

# Manejar las interacciones con los botones /hogar
@bot.callback_query_handler(func=lambda call: call.data.startswith("ver_dni_"))
def handle_callback_query(call):
    # Obtener el ID del usuario que realizó la consulta
    user_id = call.from_user.id

    chat_id = call.from_user.id
    message_id = call.message.message_id
    # Verificar si el usuario ha ejecutado el comando "/hogar" antes de permitir la interacción con los botones
    if user_id in comandos_ejecutados1 and comandos_ejecutados1[user_id] == "/hogar":
        # El usuario ejecutó el comando "/hogar", permitir la interacción con los botones
        dni = call.data.split("_")[2]
        #bot.reply_to(call.message, f"Este es el DNI seleccionado: {dni}")




        url = f"http://161.132.48.93:5000/api/reniec_buscar?dni={dni}"


        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        print("hacienod l consulta ")


        response = requests.get(url, headers=headers)
        print(response)
                        

        if response.status_code == 200:
            data = response.json()
    
            respuesta = data['Respuesta'][0]

            if  respuesta == f"no se encuentra registrado en la Base de Datos de Reniec":
                
                bot.reply_to(call.message,f"[⚠️] No se encontro el dni en planilla", parse_mode="html")

            elif respuesta == f"Reniec OFF":
                                    
                bot.reply_to(call.message,f"⚠️ EL SERVICIO DE RENIEC ESTÁ EN MANTENIMIENTO", parse_mode="html")

            elif respuesta == f"ERROR EN LA RESPUESTA":
                
                bot.reply_to(call.message,f"[ 💢 ] Ocurrió un error inesperado o datos incompletos", parse_mode="html")

            elif respuesta == f"ERRO DEL SERVIDOR":
                
                bot.reply_to(call.message,f"[ 💢 ] Ocurrió un error inesperado el servidor no responde", parse_mode="html") 


            elif respuesta == "dni cancelado":
                
                bot.reply_to(call.message,f"[⚠️] DNI Cancelado en RENIEC ", parse_mode="html")

            else:
                respuesta = data['Respuesta'][0]



                foto_codificada = respuesta["foto"]



                # Guardar la imagen en un archivo con ruta dinámica
                dni2 = f"{dni}"  # Valor de ejemplo para dni1
                ruta_archivo = f"./FOTOS_RE/foto1.jpg"  # Ruta y nombre de archivo con variable dni1
                with open(ruta_archivo, "wb") as archivo:
                    archivo.write(base64.b64decode(foto_codificada))







                nuDni = dni



                foto = open(f'./FOTOS_RE/foto1.jpg', 'rb')


                #QUITA CREDITOS
                bot.send_chat_action(call.message.chat.id, "upload_photo")

                bot.send_photo(call.message.chat.id, foto,f"<b>DNI:</b> <code>{nuDni}</code>\n\n",parse_mode="html", reply_to_message_id=message_id)
                
                ruta_imagen0 = f"./FOTOS_RE/foto1.jpg"

                if os.path.exists(ruta_imagen0):
                    # Eliminar el archivo

                    os.remove(ruta_imagen0)
                
                    print(f"Archivo {ruta_imagen0} eliminado con éxito.")

                else:
                    print(f"El archivo {ruta_imagen0} no existe.")



    else:
        print(f"alvertencia {user_id}")
        # El usuario no ha ejecutado el comando "/hogar", informar que no tiene permiso para interactuar con los botones
        bot.answer_callback_query(call.id, text=f'No puedes usar esta opcion porque tu no ejecutastes este comando.', show_alert=True)









@bot.message_handler(commands=["mpfn"," MPFN"])
def cmd_dni(message):



















    dni1 = "".join(message.text.split()[1:2])

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/mpfn 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ USTED ESTA BANEADO")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/fis"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [bitel] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥", url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                                


                            
                            url = f"http://161.132.48.93:5000/mpfn?token=O7gBHY9MapZEBH&dni={dni1}"



                            print("hacienod l consulta ")


                            response = requests.get(url)
                            print(response)



                            if response.status_code == 200:

                                print("")

                                data = response.json()


                            
    
                                respuesta = data.get('mpfn_pdf', [])

                                if respuesta:

                                    respuestav1 = respuesta[0]
                                    datos_binarios = base64.b64decode(respuestav1)
                                


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)

                                    # Leer el JSON desde el archivo (CREDITOS)


                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                    
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon
















                                    with open(f"./FISCALIA/{dni1}.pdf", "wb") as archivo_pdf:
                                        archivo_pdf.write(datos_binarios)





                                    thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                    thumbnail = open(thumbnail_path, 'rb')
                                    document = open(f'./FISCALIA/{dni1}.pdf', 'rb')
                                    bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold] FISCALIA PDF </b>\n\n"
                                                                                                    f"<b>DNI</b> ➟ <code>{dni1}</code>\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code> EXITOSAMENTE</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)
    
                                    ruta_imagen0 = f"./FISCALIA/{dni1}.pdf"

    
                                    if os.path.exists(ruta_imagen0):
                                            # Eliminar el archivo
                                        os.remove(ruta_imagen0)
                                                                                    
                                        print(f"Archivo {ruta_imagen0} eliminado con éxito.")
                                    else:
                                        print(f"El archivo {ruta_imagen0} no existe.")







                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️]No se encontró la información", parse_mode="html")




                                    

                            else:
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                # Mensaje de error
                                error_message = f"[📢] ¡Ups! El servicio de FISCALIA no está disponible en este momento O  esta en manteminiento"

                                                        # Enviar mensaje de error al chat de Telegram
                                bot.send_message(message.chat.id, error_message, parse_mode="html")

                        else:
                                bot.reply_to(message,f"[❗️]DnI INVALIDO", parse_mode="html")
                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")
                

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")






@bot.message_handler(commands=["detddd"])
def cmd_dni(message):

















    dni1 = "".join(message.text.split()[1:2])

    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/def 74123918</code>'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:


        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ USTED ESTA BANEADO")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/fis"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:

                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [def] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥", url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    
                    else:



                        numero = f"{dni1}"

                        contador = len(numero)
                        
                    

                        if contador == 8:
                        
                            message0 = bot.send_message(message.chat.id,f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html")
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"


                            url = f"http://161.132.41.56:8080/denuncias?dni={dni1}"



                            print("hacienod l consulta ")


                            response = requests.get(url)
                            print(response)
                            status = response.status_code
                        

                            if response.status_code == 200:
                                data = response.json()
    
                                respuesta = data['mensaje']

                                if  respuesta == f"El DNI NO EXISTE":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] Dni incorrecto", parse_mode="html")

                                elif respuesta == "No hay informacion":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠] No hay informacion [Det] ", parse_mode="html")


                                else:

                                    respuesta = data['listaAni']

                                    print(respuesta)



                                    contador = 0

                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)





                                    # Leer el JSON desde el archivo (CREDITOS)
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)



                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    Servicio = "denuncia"
                                    Comando = "/det"
                                    





                                    for denuncias in respuesta:
                                        dni = denuncias['dni']
                                        nombres = denuncias['nombres']
                                        fecha_REGISTRO = denuncias['fecha']
                                        delito = denuncias['delito']
                                        lugar = denuncias['lugar']

                                        valores = nombres.split(",")

                                        # Asignar los valores a dos variables
                                        valor_uno = valores[0]
                                        valor_dos = valores[1]


                                        contador += 1




                                        imagen_fondo = Image.open(f'./SIPOL/ficha_sipol.jpeg')


                                        dibujar = ImageDraw.Draw(imagen_fondo)

                                        #NUMERO
                                        numero_al_azar = random.randint(10000000, 99999999)

                                        texto1 = f"{numero_al_azar}"
                                        ubicacion1 = (200, 255)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                        #REGION POLICIAL
                                        texto1 = f"{lugar}"
                                        ubicacion1 = (200, 275)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                        #COMISARIA
                                        texto1 = f"-"
                                        ubicacion1 = (200, 295)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                        #TIPO
                                        texto1 = f"DENUNCIA"
                                        ubicacion1 = (200, 314)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                        #=============================================================================
                                        #FECHA Y HORA DEL ECHO
                                        texto1 = f"{fecha_REGISTRO} 00:00:00 Hrs."
                                        ubicacion1 = (620, 255)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                        fecha_hora_actual = datetime.now()

  
                                        
                                        # Formatear la fecha en el formato deseado (dd/mm/yyyy)
                                        fecha_formateada = fecha_hora_actual.strftime("%d/%m/%Y")

                                        # Obtener la hora actual
                                        hora_actual = fecha_hora_actual.time()


                                        






                                        #FECHA Y HORA DEL REGISTRO
                                        texto1 = f"{fecha_REGISTRO} {hora_actual} Hrs."
                                        ubicacion1 = (620, 275)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)







                                        #COMISARIA
                                        texto1 = f"{fecha_formateada} {hora_actual} Hrs."
                                        ubicacion1 = (620, 295)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)


                                        #=============================================================================

                                        #NOMBRES
                                        texto1 = f"{valor_uno} {valor_dos}"
                                        ubicacion1 = (53, 610)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                        #DNI
                                        texto1 = f"{dni}"
                                        ubicacion1 = (360, 610)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                        #FECHA NACMIENTO
                                        texto1 = f"-"
                                        ubicacion1 = (505, 610)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

                                        #SITUCION
                                        texto1 = f"DENUNCIADO"
                                        ubicacion1 = (667, 610)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)



                                        #=============================================================================


                                        texto1 = f"SIENDO LA HORA Y FECHA ANOTADAS.SE DENUNCIA A {valor_uno} {valor_dos} , CON DNI {dni} POR EL DELITO DE {delito}"

                                        longitud_linea = 110  # Define la longitud deseada de la línea
                                        
                                        lineas = []
                                        palabras = texto1.split()
                                        linea_actual = ""

                                        for palabra in palabras:
                                            if len(linea_actual) + len(palabra) + 1 <= longitud_linea:
                                                if linea_actual:
                                                    linea_actual += " "
                                                linea_actual += palabra
                                            else:
                                                lineas.append(linea_actual)
                                                linea_actual = palabra

                                        if linea_actual:
                                            lineas.append(linea_actual)

                                        texto_formateado = "\n".join(lineas)
                                        print(texto_formateado)





                                        #DELITOS
                                        texto1 = f"{texto_formateado}"
                                        ubicacion1 = (53, 680)#x = alcostado  Y= arriba abajo
                                        fuente1 = ImageFont.truetype("./letras/arial.ttf", 11)
                                        dibujar.text(ubicacion1, texto1, fill=(0, 0, 0), font=fuente1)

















                                        # Guarda la nueva imagen
                                        imagen_fondo.save(f"./SIPOL/{dni1}.jpg")

                                    
                                


                                        # Cargar la imagen
                                        img = Image.open(f'./SIPOL/{dni1}.jpg')

                                        # Crear el archivo PDF
                                        pdf = canvas.Canvas(f"./SIPOL/{dni1}.pdf", pagesize=img.size)

                                        # Añadir la imagen al archivo PDF
                                        pdf.drawImage(f'./SIPOL/{dni1}.jpg', 0, 0)

                                        # Guardar el archivo PDF
                                        pdf.save()

                                        thumbnail_path = './FOTOS_INICIO/miniatura.jpg'
                                        thumbnail = open(thumbnail_path, 'rb')
                                        document = open(f'./SIPOL/{dni1}.pdf', 'rb')
                                        bot.send_document(message.chat.id , document=document ,caption=f"<b>[#DataGold🌩] FICHA SIPOL </b>\n\n"
                                                                                                    f"<b>GENERADO</b> ➟ <code>CORRECTO</code>\n\n"
                                                                                                    f"<b>💰 Creditos :</b>  <code>{valor_cred}</code>\n"
                                                                                                    f"<b>🎖 Solicitado Por :</b> <a href='tg://user?id={huserid}'>{usernombre}</a>", 
                                                                                            parse_mode="html",reply_to_message_id=message.message_id,thumb=thumbnail)







                                        ruta_imagen1 = f"./SIPOL/{dni1}.jpg"
                                        ruta_imagen2 = F"./SIPOL/{dni1}.pdf"


                                        if os.path.exists(ruta_imagen1):
                                            # Eliminar el archivo
                                            os.remove(ruta_imagen1)

                                            os.remove(ruta_imagen2)

                                            print(f"Archivo {ruta_imagen1} eliminado con éxito.")
                                        else:
                                            print(f"El archivo {ruta_imagen1} no existe.")







                else:
                    huserid=message.from_user.id
                    hfirst_name=message.from_user.first_name
                    huserid=message.from_user.id
                    usernombre= f"{hfirst_name}"
                    bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No cuenta con CRÉDITOS o MEMBRESIA activa, use /buy para conocer nuestros planes y precios.", parse_mode="html")

        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")







@bot.message_handler(commands=["pre","PRE"])
def cmd_dni(message):

    dni1 = "".join(message.text.split()[1:2])
    



    if not dni1:
        texto = '<b>[❗️]  Formatos Válidos :</b>\n\n'
        texto +=f'<code>/pre 45123918</code>\n'

        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, texto, parse_mode="html")

    else:

        #paso dos validar
        huserid = message.from_user.id
        nombre_archivo = f"./Registros/{huserid}.json"
        if os.path.exists(nombre_archivo):

            user_id = message.from_user.id

            datos_ids = cargar_datos_desde_json()
            # ID a verificar
            id_a_verificar = f"{user_id}"

            # Verificar si el ID está en los datos cargados desde el archivo JSON
            if id_a_verificar in datos_ids:
                bot.reply_to(message, "❰👺❱ Lamentamos informarle que su acceso ha sido restringido. Por favor, comuníquese con el administrador del grupo para obtener más detalles.")
                return
    

            # VALIDADOR DE COMANDOS
            recipient_id = message.from_user.id
            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

            comand = "/telp"
            validar =  validador_comdnos(plan,comand,fecha_final)
            val = validar


            if not val:


                markup1 = types.InlineKeyboardMarkup(row_width= 3)
                a1= InlineKeyboardButton("💰Comprar creditos aqui💰" ,url="https://t.me/BlassRR")
                markup1.add(a1)
                bot.reply_to(message, f"[⚠] Debes tener almenos rango <b>GOLD</b>, <b>HAXER</b> o superior para usar este comando.", reply_markup=markup1 , parse_mode="html")
                return






            #print("pase")

            recipient_id = message.from_user.id

            base = determinar_plan_tiempo(recipient_id)
            plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                

        
            global ultima_vez

            # Obtener el ID del usuario que envió el mensaje
            user_id = message.from_user.id
    
            # Obtener el tiempo actual en segundos desde la época de Unix
            tiempo_actual = time.time()
    
            # Verificar si ha pasado suficiente tiempo desde la última vez que se usó el comando
            if user_id in ultima_vez and tiempo_actual - ultima_vez[user_id] < TIEMPO_MINIMO:
                # Aún no ha pasado suficiente tiempo
                segundos_restantes = int(TIEMPO_MINIMO - (tiempo_actual - ultima_vez[user_id]))
                bot.reply_to(message, f"❰⏳❱ ANTI-SPAM - INTENTA DESPUES DE {segundos_restantes} SEGUNDOS.")
            else:

                # Actualizar la última vez que se usó el comando para este usuario
                ultima_vez[user_id] = tiempo_actual
                print(f"comenzando servidor [PROPIETARIO] {dni1}")


                huserid=message.from_user.id
                hfirst_name=message.from_user.first_name
                huserid=message.from_user.id
                usernombre= f"{hfirst_name}"


            
                ids=f"{huserid}"
        
                filename = f"./Registros/{huserid}.json"
                #print(filename)
                creditos_disponibles = True

                if os.path.isfile(filename):

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base
                    creditos = str(creditos)
                    if creditos == "0" or creditos.startswith("-"):

                        creditos_disponibles = False



                if creditos_disponibles:

                    base = determinar_plan_tiempo(recipient_id)
                    plan, TIEMPO_MINIMO, creditos, hora_registro,fecha_inic,fecha_final = base

                    drgon = int(creditos) - 5
                    

                    if drgon < 0:
                        # Si no hay suficientes créditos
                        markup1 = InlineKeyboardMarkup(row_width= 3)
                        a1= InlineKeyboardButton("🔥Comprar aqui🔥",url="https://t.me/BlassRR" )
                        a2= InlineKeyboardButton("Unete a nuestro grupo publico 🔥",url="https://t.me/BlassV1" )
                        markup1.add(a1).row(a2)
                        bot.reply_to(message,f"[ ❌ ] Estimado <a href='tg://user?id={huserid}'>{usernombre}</a>, No tienes suficientes créditos para la consulta., use /buy para conocer nuestros planes y precios.", reply_markup=markup1 , parse_mode="html")
                    
                    
                    else:
                        numero = f"{dni1}"

                        contador = len(numero)

                        if contador == 8:
                            foto = open(f'./FOTOS_INICIO/consultando.jpg', 'rb')
                            bot.send_chat_action(message.chat.id, "upload_photo")


                            message0 = bot.send_photo(message.chat.id,photo=foto,caption=f"❰🤖❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗡𝗗𝗢 ➟ {dni1}", parse_mode="html",reply_to_message_id=message.message_id)
                            huserid=message.from_user.id
                            hfirst_name=message.from_user.first_name
                            huserid=message.from_user.id
                            usernombre= f"{hfirst_name}"



                            num = f"{dni1}"
                            walter = len(num)

                            walter1 = f"{walter}"
                            print(walter1)


                        
                    
                            url = f"http://161.132.48.93:5000/buscar/sunarp/{dni1}"




                            response = requests.get(url)
                            status  = response.status_code

                            if response.status_code == 200:
                                data = response.json()
                                
                                bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                validador = data["Resultados"]
                                if  validador:
                                    with open(f"./Registros/{recipient_id}.json","r") as file:
                                        mi_json = json.load(file)
                    
                                    mi_json["CRD"] = drgon


                                    # Guardar los cambios en el mismo archivo
                                    with open(f'./Registros/{huserid}.json', 'w') as file:
                                        json.dump(mi_json, file, indent=2)

                                    if 5000 <= drgon <= 50000:
                                        valor_cred = "♾"

                                    else:
                                        valor_cred = drgon

                                    
                                    Servicio = "propiedades"
                                    Comando = "/pre"

                                    

                                    guardar = ""
                                    contador = 0
                                    for elemento in data["Resultados"]:
                                        documento = elemento.get('Documento')
                                        libros = elemento.get('Libros')
                                        Nombres = elemento.get('Nombres')
                                        apPaterno = elemento.get('apPaterno')
                                        apMaterno = elemento.get('apMaterno')
                                        Numero = elemento.get('Numero')
                                        Registro = elemento.get('Registro')
                                        direccion = elemento.get('direccion')
                                        estado = elemento.get('estado')
                                        numeroPartida = elemento.get('numeroPartida')
                                        numeroPlaca = elemento.get('numeroPlaca')
                                        zona = elemento.get('zona')
                                        contador += 1
                                        guardar += f"📍𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧𝗢 ➟ <code>{documento}</code>\n𝗔𝗣𝗘𝗟𝗟𝗜𝗗𝗢𝗦 ➟ <code>{apPaterno} {apMaterno}</code>\n𝗡𝗢𝗠𝗕𝗥𝗘𝗦 ➟ <code>{Nombres}</code>\n\n🗂 <b>CATEGORIAS</b>\n\n<b>Registro 1: </b> <code>{libros}</code>\n\n<b>• Placa:</b> <code>{numeroPlaca}</code>\n<b>• Zona Registral:</b> <code>{zona}</code>\n\nRegistro 2: <code>{Registro}</code>\n\n• Dirección: <code>{direccion}</code>\n• Estado: <code>{estado}</code>\n\n"

                                        if contador == 5:
                                        
                                            bot.reply_to(message, f"<b>[#DataGold🌩] - Datos Sunarp [VIP]</b>\n\n{guardar}\n<b>Credits :</b> <code>{valor_cred}</code>\nWanted for : <a href='tg://user?id={huserid}'>{usernombre}</a>", parse_mode="html")
                                            contador = 0
                                            guardar = ""
                                    if contador > 0:
                                        bot.reply_to(message, f"<b>[#DataGold🌩] - Datos Sunarp [VIP]</b>\n\n{guardar}\n<b>Credits :</b> <code>{valor_cred}</code>\nWanted for : <a href='tg://user?id={huserid}'>{usernombre}</a>", parse_mode="html")
                                else:
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontró la informacion.", parse_mode="html")


                            else:

                                data = response.json()


                                respuesta = data['error']


                                if  respuesta == f"ELEMENTO NO VALIDO":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[❗️] DNI INVALIDO", parse_mode="html")

                                elif respuesta == "Error en la consulta a la API":
                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                    bot.reply_to(message,f"[⚠️] No se encontró la informacion.", parse_mode="html")



                                else:


                                    bot.delete_message(chat_id=message.chat.id, message_id=message0.message_id)
                                
                                    # Enviar mensaje de error al chat de Telegra
                                    bot.reply_to(message,f"[❗️] <b>Opsitel</b> no está disponible en este momento", parse_mode="html")


                        else:
                            
                            bot.reply_to(message,f"[❗️] Uso incorrecto, utiliza [/pre] seguido de un número de  Numero 8 dígitos\n\n➜ EJEMPLO: [/pre 444444444]", parse_mode="html")
        else:
            bot.reply_to(message,"𝗡𝗼 𝘀𝗲 𝗲𝗻𝗰𝘂𝗲𝗻𝘁𝗿𝗮 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗱𝗼, 𝗨𝘀𝗲 /register 𝗽𝗮𝗿𝗮 𝗽𝗼𝗱𝗲𝗿 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝗿𝘀𝗲.🔥.",parse_mode="html")















if __name__ == '__main__':
    global huserid


    


    # Diccionario para almacenar la última vez que se usó el comando para cada usuario
    ultima_vez = {}

    try:
        print("______________BOT INICIADO__________")
        bot.infinity_polling()
        


        
        
        #Esto hace que el bot esté siempre activo y escuchando actualizaciones de Telegram
    except Exception as e:
        print("Ha ocurrido un error:", e)





