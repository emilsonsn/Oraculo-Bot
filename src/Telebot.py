import telebot
from time import sleep
from src.conn import Conn
import json

class Telebot:
    @staticmethod
    def send_signal(self, dados, config):
        if dados[3] == "2x2":
            categoria = "OVER 3.5\n| ❗️SE BATER UMA ANTES ABORTAR |\n| PROTEGER EM AMBAS MARCAM |"
        else:
            categoria  = "Ambas Marcam"
        with open("notificacao.txt", "r" , encoding='UTF-8') as notiFile:
            noti = notiFile.read()
            notiFile.close()
        noti = noti.replace(r'{liga}', str(dados[1]))
        noti = noti.replace(r'{hora}', str(dados[2]))
        if int(dados[4]) <= 9 :
            noti = f"{noti.replace(r'{t1}', f'0{str(dados[4])}')}" 
        else:
            noti = noti.replace(r'{t1}', str(dados[4]))
        if int(dados[5]) <= 9 :
            noti = f"{noti.replace(r'{t2}', f'0{str(dados[5])}')}" 
        else:
            noti = noti.replace(r'{t2}', str(dados[5]))
        if int(dados[6]) <= 9 :
            noti = f"{noti.replace(r'{t3}', f'0{str(dados[6])}')}" 
        else:
            noti = noti.replace(r'{t3}', str(dados[6]))
        if int(dados[7]) <= 9 :
            noti = f"{noti.replace(r'{t4}', f'0{str(dados[7])}')}" 
        else:
             noti = noti.replace(r'{t4}', str(dados[7]))

        noti = noti.replace(r'{categoria}', categoria)
        bot = telebot.TeleBot(config['telegram']['token'], parse_mode=None)
        list_id_group = Conn.getListId(Conn)
        messagens_enviadas = []
        for id in list_id_group:
            messageInfo = (bot.send_message(id[0], noti))
            messagens_enviadas.append(messageInfo.message_id)
            sleep(0.5)
        return [messagens_enviadas, noti]

    def update_signal(self, messages_sent, id_noti, mensagem, resultado, entrada, protecao, config):
        bot = telebot.TeleBot(config['telegram']['token'], parse_mode=None)
        if resultado == "win":
            if entrada <= 9 : entrada = f"0{entrada}"
            mensagem = mensagem.replace(f"⏳{entrada}", f"{entrada}✅")
            mensagem+=" ====== ✅ GAIN ✅ ======"
        elif resultado == "lose":
            mensagem+=" ====== ❌ LOSS ❌ ======"
        elif resultado == "abortada":
            mensagem+=" ====== ⚠️ ABORTADA ⚠️ ======"
        elif resultado == "protecao":
            mensagem+=" ======  PROTEÇÃO  ======"
        mensagem = self.montarPlacar(self, resultado, mensagem)
        for prot in protecao:
            mensagem = mensagem.replace(f"⏳{prot}", f"{prot}☑️")

        list_id_group = Conn.getListId(Conn)
        for i,grupo in enumerate(list_id_group):
            id_message = messages_sent[i]
            bot.edit_message_text(chat_id=grupo,message_id=id_message, text=mensagem)
        Conn.resultadoNotificacao(Conn, id_noti, resultado)
    
    def montarPlacar(self, resultado,mensagem):
        with open("result.json", "r") as resultFile:
            result = json.load(resultFile) 
            result["resultado"]["envios"] = int(result["resultado"]["envios"])+1
            win = int(result["resultado"]["win"])
            abortadas  = int(result["resultado"]["abortadas"])
            lose  = int(result["resultado"]["lose"])
            envios  = int(result["resultado"]["envios"])+1
        if resultado == "win":
            win = int(result["resultado"]["win"])+1
            result["resultado"]["win"] = int(result["resultado"]["win"])+1        
        elif resultado == "lose":
            lose  = int(result["resultado"]["lose"])+1
            result["resultado"]["lose"] = int(result["resultado"]["lose"])+1
        elif resultado == "abortadas":
            abortadas =  int(result["resultado"]["abortadas"])+1
            result["resultado"]["abortadas"] = int(result["resultado"]["abortadas"])+1

        with open("result.json", "w") as resultFile:
            result = json.dumps(result, indent = 2) 
            resultFile.write(str(result))
            resultFile.close()

        placar =f"""\nEnvios: {envios}\n✅Gain: {win}\n⛔️lose: {lose}\nAbortadas: {abortadas}"""
        placar +=f"\nAssertividade: {round((int(win)*100)/(int(lose)+int(win)), 2)}%"
        return (mensagem+placar)


