import ping3

while True:
    resposta = ping3.ping("192.168.1.175")

    if resposta is not None:
        print("Blz, passou! Tempo de resposta:", resposta, "s")
    else:
        print("Deu erro!")