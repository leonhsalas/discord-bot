import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carga las variables del archivo .env
load_dotenv()

# --- Configuración de la API de Gemini ---
# Asegúrate de que la clave de API de Gemini esté en tu archivo .env
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# ➡️ Cambia el modelo de 'gemini-flash' a 'gemini-pro'
model = genai.GenerativeModel('gemini-1.5-flash-latest')
# --- Configuración del bot de Discord ---
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# ID del canal donde el bot publicará el mensaje
CANAL_ID = 995882267236892702  # Reemplaza con tu ID de canal

# La instrucción (prompt) para Gemini. Puedes cambiar esto.
PROMPT_DE_GEMINI = "generate me a short technology curiosity no more than 30 words that's not a question like Did you know that IBM’s first hard drive (1956) weighed over one ton and could only store 5 MB of data? Today, you can fit that same amount into a single photo taken with your smartphone 📸💾."

@client.event
async def on_ready():
    """Este evento se ejecuta cuando el bot se conecta a Discord."""
    print(f'El bot ha iniciado sesión como {client.user}')
    # Inicia la tarea de publicación programada.
    publicar_mensaje.start()

@tasks.loop(hours=12)
async def publicar_mensaje():
    """Esta tarea se ejecuta cada 12 horas, genera un texto con Gemini y lo envía."""
    print("Intentando generar y publicar mensaje con Gemini...")
    try:
        # Genera el texto usando la API de Gemini
        response = model.generate_content(PROMPT_DE_GEMINI)
        # Extrae el texto generado de la respuesta
        mensaje_generado = response.parts[0].text

        canal = client.get_channel(CANAL_ID)
        if canal:
            await canal.send(mensaje_generado)
            print("Mensaje generado y publicado exitosamente.")
        else:
            print(f"No se encontró el canal con el ID {CANAL_ID}")
    except Exception as e:
        print(f"Ocurrió un error al usar la API de Gemini: {e}")
        # En caso de error, puedes enviar un mensaje predeterminado
        canal = client.get_channel(CANAL_ID)
        if canal:
            await canal.send("Lo siento, no pude generar el mensaje en este momento. Inténtalo de nuevo más tarde.")

# Ejecuta el bot con el token de la variable de entorno
client.run(os.getenv('DISCORD_TOKEN'))