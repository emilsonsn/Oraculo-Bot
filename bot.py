import json
import re
from unittest import result
import requests
from time import sleep
from src.Conn import Conn
from src.Telebot import Telebot
from src.Validator import Validator
from datetime import datetime

class Bot:
    def start(self):
        with open("config.json") as configFile:
            self.config = json.load(configFile)
            configFile.close()      
        self.lista_message_id = []
        self.user = self.config['user_api']['user']
        self.password = self.config['user_api']['password']
        self.ligas = ['Copa do Mundo', 'Euro Cup', 'Premier League']
        self.url = 'https://betvirtualapi.com.br/api/'
        self.get_token(self)
        self.carregarValores(self)
        self.horas = ['07', '13', '19', '01']
        self.hora_score = 0
    
    def carregarValores(self):
        self.maior_sequencia = 0

        self.sequencia = 0
    
    def resetar_sequencia(self):
        if self.sequencia > self.maior_sequencia :
            self.maior_sequencia = self.sequencia
        self.sequencia = 0           

    def get_token(self):
        url = self.url+'login?user='+self.user+'&password='+self.password
        response = requests.get(url)
        self.token = json.loads(response.text)['token']

    def get_score(self):
        placar="✴️ MENTORIA - BOT"
        placar+="\n\n✅ {assertividade} DE ASSERTIVIDADE no dia até o momento"
        placar+="\n\n✅ Ambas /yes: {ambas}"
        placar+="\n\n✅ Ambas marcam com 3.5: {3_5}"
        placar+="\n\n✅ OVER 2.5: {2_5}"
        placar+="\n\n🔥 {sequencia} GREENS seguidos atualmente"
        placar+="\n\n🚀 {sequencia_mes} GREENS seguidos é a maior sequência do mês"
        placar+="\n\n⚠️ Gestão e meta sempre ⚠️"
        placar = str(placar).replace('{sequencia}', str(self.maior_sequencia))
        placar = str(placar).replace('{sequencia_mes}', str(Conn.sequenciaMes(Conn)))
        placar = str(placar).replace('{assertividade}', str(Conn.get_resultado_geral(Conn)))
        placar = str(placar).replace('{ambas}', str(Conn.get_ambas(Conn)))
        placar = str(placar).replace('{2_5}', str(Conn.get_2_5(Conn)))
        placar = str(placar).replace('{3_5}', str(Conn.get_3_5_ambas(Conn)))

        return placar
        
    def get_last_result(self, liga):
        url = self.url+str(liga)+'/results/1'
        response = requests.post(url, data={'token': self.token})
        response = json.loads(response.text)
        self.minuto = response['result'][0]['minuto']
        self.hora = response['result'][0]['hora']
        self.liga = response['result'][0]['liga']
        casa = response['result'][0]['res_casa']
        fora = response['result'][0]['res_fora']
        return f"{casa}x{fora}"

    def get_results(self, liga, numero):
        url = self.url+str(liga)+'/results/'+str(numero)
        response = requests.post(url, data={'token': self.token})
        response = json.loads(response.text)
        try:
            if response['status'] == 'success': response = response['result']
        except:
            pass                
        return response
    
    def calc_hour(self, hora, intervalo):
        hora = int(hora)-intervalo
        if hora < 0:
            hora = 24 + hora
        return hora
    
    def calc_minute(self, minute, sinal, intervalo):
        if sinal == "+":
            minute = int(minute)+intervalo
        else:
            minute = int(minute)-intervalo
        if minute > 59:
            minute = minute-60
        if minute < 0:
            minute = 60 + minute
        return minute
            
    def get_result(self, liga, hora, minuto):
        url = self.url+str(liga)+'/result/hour/'+str(hora)+'/minute/'+str(minuto)
        response = requests.post(url, data={'token': self.token})
        response = json.loads(response.text)
        casa = response['result']['res_casa']
        fora = response['result']['res_fora']
        return f"{casa}x{fora}"
    
    def get_maxima(self, liga):
        resultados  = self.get_results(self, liga, 4)
        for resultado in resultados:
            if int(resultado['res_casa']) < 1 or int(resultado['res_fora']) < 1:
                return True
        return False
    
    def get_atracao(self, liga):
        resultados  = self.get_results(self, liga, 2)
        for resultado in resultados:
            if int(resultado['res_casa']) > 0 and int(resultado['res_fora']) > 0:
                return True
        return False
    
    def get_ocorrencias_padrao(self, liga,casa, fora, hora_intervalo):
        url = self.url+str(liga)+'/casa/'+str(casa)+'/fora/'+str(fora)+'/intervalo/'+str(hora_intervalo)
        response = requests.post(url, data={'token': self.token})
        return json.loads(response.text)
    
    def get_resultado_ocorrencia(self, liga, id, intervalo):
        url = self.url+str(liga)+'/'+str(id)+'/'+str(intervalo)
        response = requests.post(url, data={'token': self.token})
        response = json.loads(response.text)
        try:
            for res in response['result']:
                if int(res['res_casa']) > 0 and int(res['res_fora']) > 0:
                    return True
            return False
        except:
            return False
        
    def calcular_media_assertividade(self, liga, intervalo_hora, sinal_minuto, intervalo_minuto, estrategia):
        horas_intervalo = [12, 24, 48]
        media = [[0,0], [0,0], [0,0]]
        estrategia = estrategia.split('x')
        for i, hora_intervalo in enumerate(horas_intervalo):
            ocorrencias = self.get_ocorrencias_padrao(self, liga, estrategia[0], estrategia[1], hora_intervalo)
            for ocorrencia in ocorrencias['result']:
                if sinal_minuto == "-" : intervalo = intervalo_hora*20 + int(intervalo_minuto)/3
                if sinal_minuto == "+" : intervalo = int(intervalo_hora)*20 - int(intervalo_minuto)/3          
                intervalo = int(intervalo)
                if self.get_resultado_ocorrencia(self, liga, ocorrencia['id'], intervalo):
                    media[i][0]+=1
                else:
                    media[i][1]+=1
        try:
            media1 = media[0][0] / (media[0][0]+media[0][1]) * 100
            media2 = media[1][0] / (media[1][0]+media[1][1]) * 100
            media3 = media[2][0] / (media[2][0]+media[2][1]) * 100
            self.mediaGeral = ((media1+media2+media3)/3)
            if self.mediaGeral >= 94:
                return True
            return False
        except:
            return False                
                    
    def get_minutos(self, minuto):
        minutos = []
        for i in range(0, 4):
            minutos.append(self.calc_minute(self, minuto, '+', (i*3)))
        return minutos
        
    def get_signal(self, liga, intervalo_hora, sinal_minuto, intervalo_minuto, estrategia, entrada):
        # [liga, sinal_hora, intervalo_hora, sinal_minuto, intervalo_minuto, resultado, entrada]
        try:
            self.get_last_result(self, liga)
            hora = self.calc_hour(self, self.hora, intervalo_hora)
            minuto = self.calc_minute(self, self.minuto, sinal_minuto, intervalo_minuto)
            result = self.get_result(self, liga=liga, hora=hora, minuto=minuto)
            minuto_da_frente = self.calc_minute(self, self.minuto, "+", 6)
            if result == estrategia and int(str(datetime.today())[11:13]) < minuto_da_frente and self.get_maxima(self, liga) and self.calcular_media_assertividade(self, liga, intervalo_hora, sinal_minuto, intervalo_minuto, estrategia) and self.get_atracao(self, liga=liga):
                # liga, categoria, estrategia, config, mensagem, hora, minuto
                estrategia_dif = ''
                if intervalo_hora == 5 : estrategia_dif = '5H'
                resposta_telegram = Telebot.send_signal(Telebot, liga, entrada, estrategia, self.config, self.hora, self.get_minutos(self, int(self.minuto)+6), self.mediaGeral, estrategia_dif)
                self.lista_message_id = resposta_telegram[0]
                self.mensagem = resposta_telegram[1]
                # self,list_message, mensagem, minuto, main,
                if entrada == "AMBAS MARCAM e OVER 3.5":
                    Validator.resultadoAmbas_3_5(Validator, self.liga, self.lista_message_id, self.mensagem, self.minuto, self, self.config, estrategia, "AMBAS MARCAM 3.5")        
                if entrada == "OVER 2.5":
                    Validator.resultado2_5(Validator, self.liga, self.lista_message_id, self.mensagem, self.minuto, self, self.config, estrategia, "2.5")
                if entrada == "AMBAS MARCAM":
                    Validator.resultadoAmbas(Validator, self.liga, self.lista_message_id, self.mensagem, self.minuto, self, self.config, estrategia, "AMBAS MARCAM")
                        
        except Exception as err:
            print(err)
            return 0
        
    def main(self):
        # [liga, intervalo_hora, sinal_minuto, intervalo_minuto, resultado, entrada]
        while True:
            self.start(self)
            while True:
                for liga in self.ligas:                        
                    self.liga = liga
                    self.get_token(self)            
                    if Conn.get_estrategias(Conn, '3x3'):
                        self.get_signal(self, liga, 4, '+', 12, '3x3', "OVER 2.5")
                    if Conn.get_estrategias(Conn, '2x3'):
                        self.get_signal(self, liga, 4, '+', 12, '2x3', "OVER 2.5")
                    if Conn.get_estrategias(Conn, '2x2'):
                        self.get_signal(self, liga, 3, '-', 3, '2x2', "AMBAS MARCAM e OVER 3.5")
                    if Conn.get_estrategias(Conn, '1x1'):
                        self.get_signal(self, liga, 1, '+', 9, '1x1', "AMBAS MARCAM")
                    if Conn.get_estrategias(Conn, '1x2'):
                        self.get_signal(self, liga, 2, '+', 9, '1x2', "AMBAS MARCAM")
                    if Conn.get_estrategias(Conn, '0x2'):
                        self.get_signal(self, liga, 2, '-', 0, '0x2', "AMBAS MARCAM")
                    if Conn.get_estrategias(Conn, '0x1'):
                        self.get_signal(self, liga, 3, '+', 3, '0x1', "AMBAS MARCAM")
                    if Conn.get_estrategias(Conn, '0x4'):                            
                        self.get_signal(self, liga, 0, '+', 3, '0x4', "AMBAS MARCAM")
                    if Conn.get_estrategias(Conn, '3x2'):
                        self.get_signal(self, liga, 4, '+', 12, '3x2', "AMBAS MARCAM")
                    self.get_signal(self, liga, 5, '+', 6, '1x4', "AMBAS MARCAM")
                    self.get_signal(self, liga, 5, '+', 6, '10x10', "AMBAS MARCAM")
                    self.get_signal(self, liga, 5, '+', 6, '4x1', "AMBAS MARCAM")
                    self.get_signal(self, liga, 5, '+', 6, '5x0', "AMBAS MARCAM")
                    self.get_signal(self, liga, 5, '+', 6, '3x2', "AMBAS MARCAM")
                    self.get_signal(self, liga, 5, '+', 6, '2x3', "AMBAS MARCAM")    
                sleep( 10 )
                
Bot.main(Bot)
