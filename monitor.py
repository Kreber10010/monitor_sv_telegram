import telegram
import requests
import time
import logging
from telegram.ext import Application, CommandHandler, ContextTypes
import ping3
import socket
import os
from dotenv import load_dotenv

# Ative o logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TARGET_IP = os.getenv("SV_TARGET_IP")
TARGET_PORT = os.getenv("SV_TARGET_PORT")

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
    failure_reason = ""

    # ping
    if ping3.ping(TARGET_IP):
        print("Ping OK!")

        # Verifica a porta
        if check_port(TARGET_IP, TARGET_PORT):
            print(f"Porta {TARGET_PORT} OK!")
            current_status = True
        else:
            failure_reason = f"Porta {TARGET_PORT} OFFLINE!"
            print(failure_reason)
    else:
        failure_reason = "Ping FALHOU!"
        print(failure_reason)

    if current_status != target_online:
        target_online = current_status
        if not target_online:
            await context.bot.send_message(chat_id=CHAT_ID, text=f"🚨 ALERTA: O alvo em {TARGET_IP} está OFFLINE! \nMotivo: {failure_reason}")
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text=f"✅ O alvo em {TARGET_IP} voltou a ficar ONLINE!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    job_queue = application.job_queue
    job_queue.run_repeating(check_target_status, interval=10, first=1)
    
    print("O agente local está rodando e verificando o alvo...")
    application.run_polling()

if __name__ == "__main__":
    main()