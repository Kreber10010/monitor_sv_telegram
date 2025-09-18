import ping3
import os
from dotenv import load_dotenv

load_dotenv()
TARGET_IP = os.getenv("SV_TARGET_IP")

while True:
    resposta = ping3.ping(TARGET_IP)

    if resposta is not None:
        print("Blz, passou! Tempo de resposta:", resposta, "s")
    else:
        print("Deu erro!")