import telegram
import requests
import time
import logging
from telegram.ext import Application, CommandHandler, ContextTypes
import ping3
import socket

# Ative o logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

BOT_TOKEN = "8431098641:AAFHkabBirjMG6MINm9xz5M5WxLuETrb3iM"
CHAT_ID = "-4984490758"
TARGET_URL = "192.168.1.175"
TARGET_PORT = 22

target_online = False

def check_port(host, port, timeout=1):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

async def check_target_status(context: ContextTypes.DEFAULT_TYPE):
    global target_online

    current_status = False

    # ping    
    if ping3.ping(TARGET_URL):
        
        # Verifica a porta
        if check_port(TARGET_URL, TARGET_PORT):
            current_status = True

    if current_status != target_online:
        target_online = current_status
        if not target_online:
            await context.bot.send_message(chat_id=CHAT_ID, text=f"🚨 ALERTA: O alvo em {TARGET_URL} está OFFLINE!")
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text=f"✅ O alvo em {TARGET_URL} voltou a ficar ONLINE!")

"""
async def check_target_status(context: ContextTypes.DEFAULT_TYPE):
    global target_online

    current_status = False
    try:
        # Pings the target and gets the result
        ping_result = ping3.ping(TARGET_URL, timeout=1)

        # --- Adicione esta linha para ver o resultado ---
        print(f"Resultado do ping para {TARGET_URL}: {ping_result}")
        # -----------------------------------------------

        # If ping_result is not False (e.g., a number), it means the ping was successful.
        if ping_result is not False:
            current_status = True
        else:
            current_status = False

    except Exception as e:
        print(f"Erro no ping: {e}")
        current_status = False

    if current_status != target_online:
        target_online = current_status
        if not target_online:
            await context.bot.send_message(chat_id=CHAT_ID, text=f"🚨 ALERTA: O alvo em {TARGET_URL} está OFFLINE!")
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text=f"✅ O alvo em {TARGET_URL} voltou a ficar ONLINE!")
"""

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    job_queue = application.job_queue
    job_queue.run_repeating(check_target_status, interval=10, first=1)
    
    print("O agente local está rodando e verificando o alvo...")
    application.run_polling()

if __name__ == "__main__":
    main()