from email import message
from pickletools import read_int4
import telebot
from time import sleep
from src.Conn import Conn
from datetime import datetime
import json

class Telebot:
    
    @staticmethod
    def send_signal(self, liga, categoria, estrategia, config, hora, minutos, mediaGeral, estrategia_dif):
        if str(liga).strip() == "Euro Cup" : liga = "EURO"
        if str(liga).strip() == "Premier League" : liga = "PREMIER"
        if str(liga).strip() == "Copa do Mundo" : liga = "COPA"
        if str(liga).strip() == "Superleague" : liga = "SUPER"
        with open("mensagem.txt", encoding='utf8') as mensagemFile:
            mensagem = mensagemFile.read()
            mensagemFile.close()   
        list_id_group = Conn.get_groups(Conn)
        bot = telebot.TeleBot(config['telegram']['token'])
        messagens_enviadas = []
        _minutos = []
        if hora < 10 : hora = f"0{hora}" 
        for minuto in minutos:
            if minuto < 10 : minuto = f"0{minuto}"
            _minutos.append(minuto)
        minutos = _minutos
        for i, grupo in enumerate(list_id_group):
            try:                
                mensagem = str(mensagem).replace('{categoria}', categoria)
                mensagem = str(mensagem).replace('{liga}', liga)
                mensagem = str(mensagem).replace('{estrategia}', estrategia)
                mensagem = str(mensagem).replace('{hora}', str(hora))
                mensagem = str(mensagem).replace('{t1}', str(minutos[0]))
                mensagem = str(mensagem).replace('{t2}', str(minutos[1]))
                mensagem = str(mensagem).replace('{t3}', str(minutos[2]))
                mensagem = str(mensagem).replace('{t4}', str(minutos[3]))
                messageInfo = (bot.send_message(grupo[0], mensagem))
                messagens_enviadas.append([grupo[0], messageInfo.message_id])
                if i == 0:
                    mediaGeral = round(mediaGeral,2)
                    if estrategia_dif == '5H' : estrategia = estrategia_dif
                    messageInfo = (bot.send_message(grupo[0], "⚽ Padrão: ({estrategia}) ⚽\nPorcentagem: {mediaGeral}".replace('{mediaGeral}', str(mediaGeral)).replace('{estrategia}', estrategia)))
                   
            except Exception as err:
                print(str(err))
                continue
            sleep(0.5)
        return [messagens_enviadas, mensagem]


    def update_signal(self, resultado, mensagem, minuto, list_message, config, result_boolean, tentativa, ultima, main):
        bot = telebot.TeleBot(config['telegram']['token'])
        if minuto < 10 : minuto = f"0{minuto}"
        if result_boolean:
            tentativa+=1 
            if tentativa == 1 : tentativa = "1⃣"
            if tentativa == 2 : tentativa = "2⃣"
            if tentativa == 3 : tentativa = "3⃣"
            if tentativa == 4 : tentativa = "4⃣"
            mensagem += f"\n{resultado} {tentativa} ({ultima})"
        else:
            mensagem += f"\n{resultado}"
        for grupo in list_message:
            try:
                bot.edit_message_text(chat_id=grupo[0],message_id=grupo[1], text=mensagem)
            except Exception as err:
                print(err)
                continue

    @staticmethod
    def send_score(self, main):
        list_id_group = Conn.get_groups(Conn)
        bot = telebot.TeleBot(main.config['telegram']['token'])
        for i, grupo in enumerate(list_id_group):
            try:                
                if i == 0:
                    messageInfo = (bot.send_message(grupo[0], main.get_score(main)))
            except Exception as err:
                print(str(err))
                continue