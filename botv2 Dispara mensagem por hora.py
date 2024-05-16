
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

