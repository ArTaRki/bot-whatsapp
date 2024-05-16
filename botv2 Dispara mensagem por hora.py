import json
import requests
import time
import random
from datetime import datetime, timedelta

print(f"########################################")
print(f"######### Robô TuZziK ##########")
print(f"########################################")

url = "http://93.127.212.111:8080/message/sendText/fortune"
api_key = "31f6f4a2d9a624260b0727d8bf02598b"

# ID do grupo para o qual você quer enviar mensagens
grupo_id = "120363298096694487@g.us"

# Dados do cabeçalho (headers)
headers = {
    "Content-Type": "application/json",
    "apikey": api_key
}

# Função para enviar mensagem com o texto fornecido
def enviar_mensagem(mensagem):
    try:
        # Dados do corpo da requisição para a mensagem
        postData = {
            "number": grupo_id,
            "textMessage": {
                "text": mensagem
            }
        }

        # Converte os dados da mensagem em JSON
        postDataJson = json.dumps(postData)

        # Define as opções da requisição
        headers["Content-Length"] = str(len(postDataJson))

        # Executa a requisição e obtém a resposta
        response = requests.post(url, data=postDataJson, headers=headers)
        response.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

def gerar_horarios():
    horario_atual = datetime.now()

    # Se estiver no minuto 57, avança para o próximo horário cheio
    if horario_atual.minute == 57:
        proxima_hora_cheia = horario_atual.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        # Se não estiver no minuto 57, mantém o horário atual e avança para o próximo minuto 57
        proxima_hora_cheia = horario_atual.replace(minute=57, second=0, microsecond=0)

    # Calcula o número de intervalos de 3 a 8 minutos que cabem até 55 minutos
    num_intervalos = 6  # Pois 60 minutos dividido por 10 é igual a 6

    # Gera os horários com minutos ajustados
    horarios = []
    horario_envio = proxima_hora_cheia  # Começa a partir do próximo minuto 57
    for _ in range(10):
        minutos = random.randint(3, 8)
        if minutos > num_intervalos * 8:  # Verifica se o minuto gerado ultrapassa 55
            minutos = num_intervalos * 8
        horarios.append(horario_envio.strftime("%H:%M"))
        horario_envio += timedelta(minutes=minutos)

    return horarios


# Variável para armazenar o horário da última mensagem enviada
ultimo_envio = None

# Envia a mensagem apenas quando o horário completo é :57
def enviar_mensagens():
    global ultimo_envio  # Precisamos indicar que estamos utilizando a variável global dentro da função
    while True:
        hora_atual = datetime.now().hour
        minuto_atual = datetime.now().minute
        if minuto_atual == 57 and (ultimo_envio is None or ultimo_envio.hour != hora_atual):
            horarios = gerar_horarios()
            
            # Gera números aleatórios para Normal e Turbo
            normal_aleatorio = random.randint(11, 13)
            turbo_aleatorio = random.randint(5, 10)
            
            mensagem = f"""💰 *OPORTUNIDADE ENCONTRADA* 💰
⏰ Encontramos horários pagantes

🐯 *FORTUNE TIGER*

🔥 *{normal_aleatorio}X* Normal
🔄  Intercalado
⚡ *{turbo_aleatorio}x* Turbo

➡️ *Cadastre-se aqui:* https://go.aff.donald.bet/2gam3jb4 

"""

            mensagem += "\n".join([f"⏰ {horario} ✅" for horario in horarios])

            enviar_mensagem(mensagem)
            ultimo_envio = datetime.now()  # Atualiza o horário do último envio
            # Aguarda até o próximo minuto
            while datetime.now().minute == 57:
                time.sleep(1)
        else:
            time.sleep(10)  # Verifica a cada 10 segundos

# Inicia o envio de mensagens
enviar_mensagens()

