from time import sleep
from unittest import result
from src.Telebot import Telebot
from src.Conn import Conn
class  Validator:
    def resultadoAmbas_3_5(self,liga, list_message, mensagem, minuto, main, config, estrategia, categoria):
        tentativa =0
        ultimaSaida = ''
        pular = 0
        while True:
            if tentativa >3:
                break
            ultima = main.get_last_result(main, liga)
            ultimo_resultado = ultima.split('x')
            if int(minuto) == int(main.minuto):
                sleep( 10 )
                continue
            if pular == 0:
                minuto = main.minuto
                pular = 1
                continue
            if int(ultimo_resultado[0])+int(ultimo_resultado[1]) > 3.5 or (int(ultimo_resultado[0]) > 0 and int(ultimo_resultado[1])> 0):
                Telebot.update_signal(Telebot, "✅✅ ", mensagem , main.minuto, list_message, config, True, tentativa, ultima, main)
                Conn.insertResult(Conn, 'gain', estrategia, tentativa+1, categoria)
                return
            else:
                minuto = main.minuto
                tentativa+=1
                sleep( 10 )
        Telebot.update_signal(Telebot, "❌ ❌", mensagem, main.minuto, list_message, config, False, tentativa, ultima, main)
        Conn.insertResult(Conn, 'loss', estrategia, tentativa+1, categoria)
        

    def resultado2_5(self, liga, list_message, mensagem, minuto, main, config, estrategia, categoria):
        tentativa = 0
        ultimaSaida = ''
        pular = 0
        while True:
            if tentativa >3:
                break
            ultima = main.get_last_result(main, liga)
            ultimo_resultado = ultima.split('x')
            if int(minuto) == int(main.minuto):
                sleep( 10 )
                continue
            if pular == 0:
                minuto = main.minuto
                pular = 1
                continue
            if int(ultimo_resultado[0])+int(ultimo_resultado[1]) > 2:
                Telebot.update_signal(Telebot, "✅✅ ", mensagem , main.minuto, list_message, config, True, tentativa, ultima, main)
                Conn.insertResult(Conn, 'gain', estrategia, tentativa+1, categoria)
                return
            else:
                minuto = main.minuto
                tentativa+=1
                sleep( 10 )
        Telebot.update_signal(Telebot, "❌ ❌", mensagem, main.minuto, list_message, config, False, tentativa, ultima, main)
        Conn.insertResult(Conn, 'loss', estrategia, tentativa+1, categoria)

    def resultadoAmbas(self,liga, list_message, mensagem, minuto, main, config, estrategia, categoria):
        tentativa =0
        ultimaSaida = ''
        pular = 0
        while True:
            if tentativa >3:
                break
            ultima = main.get_last_result(main, liga)
            ultimo_resultado = ultima.split('x')
            if int(minuto) == int(main.minuto):
                sleep( 10 )
                continue
            if pular == 0:
                minuto = main.minuto
                pular = 1
                continue
            if int(ultimo_resultado[0]) > 0 and int(ultimo_resultado[1]) > 0:
                Telebot.update_signal(Telebot, "✅✅ ", mensagem , main.minuto, list_message, config, True, tentativa, ultima, main)
                Conn.insertResult(Conn, 'gain', estrategia, tentativa+1, categoria)
                return
            else:
                minuto = main.minuto
                tentativa+=1
                sleep( 10 )
        Telebot.update_signal(Telebot, "❌ ❌", mensagem, main.minuto, list_message, config, False, tentativa, ultima, main)
        Conn.insertResult(Conn, 'loss', estrategia, tentativa+1, categoria)
