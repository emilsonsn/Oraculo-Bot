from cgitb import reset
from codecs import utf_8_encode
from encodings import utf_8
import gc
from signal import signal
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from src.conn import Conn
from selenium.webdriver.common.by import By
from time import sleep
from datetime import date
from datetime import datetime
from src.Telebot import Telebot
from src.validadorResultado import Validador
import json

class Bot:

    def config(self):
        with open("config.json") as config:
            self.config = json.load(config)
            self.user = self.config['user']
            self.password = self.config['pass']
        self.dataHoje = date.today()

    def start(self):
        self.options = webdriver.ChromeOptions()
        self.temporizador = 0
        self.options.add_argument("--start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        #self.options.add_argument('headless')
        self.tabelaVazia = False
        self.driver = webdriver.Chrome(service=Service("./chromedriver.exe"),chrome_options=self.options)
        
    def logar(self):
        self.driver.get("https://oraculo.mentoriabet.com.br/")
        while len(self.driver.find_elements(By.CSS_SELECTOR, "#email")) < 1:
            sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "#email").send_keys(self.user)
        self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
        while len(self.driver.find_elements(By.CSS_SELECTOR, "td")) < 1:
            sleep(1)
        self.page = self.driver.page_source

    def tratarDados(self):
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.time = {
            "horas" :self.soup.select("th")[44:69],
            "minutos":[
                self.soup.select("th")[23:43],
                self.soup.select("th")[136:156],
                self.soup.select("th")[249:269],
                self.soup.select("th")[362:382]           
                ]
            }
        self.results = self.soup.select('.card-body')    
        array = []
        arrayGeral = []
        arrayTabelas = []
        for i, result in enumerate(self.results):
            if i == 0:
                continue
            result = result.select('#matchResult')  
            blocosPreenchidos = (500-len(result))
            if blocosPreenchidos > 20 :
                blocosPreenchidos-=20
                self.tabelaVazia = True
            primeiraLista = 20 - blocosPreenchidos
            if len(arrayTabelas) == 0:
                primeiraLista+=1
            for x, res in enumerate(result):
                if x == primeiraLista or len(array) == 20:
                    arrayGeral.append(array)
                    array = []        
                array.append(res.text)
            arrayTabelas.append(arrayGeral[0:6])
            array = []
            arrayGeral = []
            primeiraLista = 0
        self.arrayTabelas = arrayTabelas
                
    def calcularSinal2x2(self):
        timeHora = self.time['horas']
        if self.tabelaVazia:
            timeHora = self.time['horas'][1::]
        LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
        for i,ligas in enumerate(self.arrayTabelas):
            for x,linha in enumerate(ligas):
                if x == 2:
                    break
                for y, coluna in enumerate(linha):
                    if coluna == "2x2" : 
                        hora = timeHora[x].text
                        minuto = int(self.time['minutos'][i][y].text)
                        if int(hora) > 23:
                            hora = hora-24
                        if int(minuto) > 59:
                            minuto= (minuto-59)
                        if minuto < 0:
                            minuto = 24 - minuto 
                        minutos = [int(minuto)-2, int(minuto), int(minuto)+3, int(minuto)+6, int(minuto)+9]
                        for iM, min in enumerate(minutos):
                            if min > 59: minutos[iM] = min-60
                        for iM, min in enumerate(minutos):
                            if min < 0: minutos[iM] = 24-min
                        if hora == '23':
                            hora = "-1"   
                        Conn.notificacao(Conn, [LigasNome[i], "2x2", f"{date.today()} {int(hora)+1}:{int(minutos[0])}:00", minutos[1],minutos[2],minutos[3],minutos[4], 0])

    def calcularSinal2x0(self):
        timeHora = self.time['horas']
        if self.tabelaVazia:
           timeHora = self.time['horas'][1::]
        LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
        for i,ligas in enumerate(self.arrayTabelas):
            for x,linha in enumerate(ligas):
                if x == 1:
                    break
                for y, coluna in enumerate(linha):
                    if coluna == "2x0" and y+1 < len(linha):
                        if int(linha[y+1].split("x")[0])>0 and int(linha[y+1].split("x")[1])>0:
                            hora = timeHora[x].text
                            minuto = self.time['minutos'][i][y].text
                            if int(hora) > 23:
                                hora = hora-24
                            if int(minuto) > 59:
                                minuto= minuto-59
                            minutos = [int(minuto)+7, int(minuto)+9, int(minuto)+12, int(minuto)+15, int(minuto)+18]
                            for iM, min in enumerate(minutos):
                                if min > 59: minutos[iM] = min-60
                            for iM, min in enumerate(minutos):
                                if min < 0: minutos[iM] = 24-min
                                Conn.notificacao(Conn, [LigasNome[i], "2x0", f"{date.today()} {int(hora)}:{int(minutos[0])}:00", minutos[1],minutos[2],minutos[3],minutos[4], 0])
        
    def calcularSinal1x1_1x0(self):
        timeHora = self.time['horas']
        if self.tabelaVazia:
            timeHora = self.time['horas'][1::]
        LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
        for i,ligas in enumerate(self.arrayTabelas):
            for x,linha in enumerate(ligas):
                if x == 1:
                    break
                for y, coluna in enumerate(linha):
                    if coluna == "1x1" and y+1 < len(linha):
                        if linha[y+1] == "1x0":                           
                            hora = timeHora[x].text
                            minuto = self.time['minutos'][i][y].text
                            if int(hora) > 23:
                                hora = hora-24
                            if int(minuto) > 59:
                                minuto= minuto-59
                            minutos = [int(minuto)+7, int(minuto)+9, int(minuto)+12, int(minuto)+15, int(minuto)+18]
                            for iM, min in enumerate(minutos):
                                if min > 59: minutos[iM] = min-60
                            for iM, min in enumerate(minutos):
                                if min < 0: minutos[iM] = 24-min
                            Conn.notificacao(Conn, [LigasNome[i], "1x1_1x0", f"{date.today()} {int(hora)}:{int(minutos[0])}:00", minutos[1],minutos[2],minutos[3],minutos[4], 0])


    def calcularSinal2x0_1x0(self):
        timeHora = self.time['horas']
        if self.tabelaVazia:
            timeHora = self.time['horas'][1::]
        LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
        for i,ligas in enumerate(self.arrayTabelas):
            for x,linha in enumerate(ligas):
                if x == 1:
                    break
                for y, coluna in enumerate(linha):
                    if coluna == "2x0" and y+1 < len(linha):
                        if linha[y+1] == "1x0":               
                            hora = timeHora[x].text
                            minuto = self.time['minutos'][i][y].text
                            if int(hora) > 23:
                                hora = hora-24
                            if int(minuto) > 59:
                                minuto= minuto-59
                            minutos = [int(minuto)+7, int(minuto)+9, int(minuto)+12, int(minuto)+15, int(minuto)+18]
                            for iM, min in enumerate(minutos):
                                if min > 59: minutos[iM] = min-60
                            for iM, min in enumerate(minutos):
                                if min < 0: minutos[iM] = 24-min
                            Conn.notificacao(Conn, [LigasNome[i], "2x0_1x0", f"{date.today()} {int(hora)}:{int(minutos[0])}:00", minutos[1],minutos[2],minutos[3],minutos[4], 0])

    def calcularSinal5_mais(self):
        timeHora = self.time['horas']
        if self.tabelaVazia:
            timeHora = self.time['horas'][1::]
        LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
        for i,ligas in enumerate(self.arrayTabelas):
            for x,linha in enumerate(ligas):
                if x == 1:
                    break
                for y, coluna in enumerate(linha):
                    if int(coluna.split("x")[0])+int(coluna.split("x")[1]) >= 5:             
                        hora = timeHora[x].text
                        minuto = self.time['minutos'][i][y].text
                        if int(hora) > 23:
                            hora = hora-24
                        if int(minuto) > 59:
                            minuto= minuto-59
                        minutos = [int(minuto)+4, int(minuto)+6, int(minuto)+9, int(minuto)+12, int(minuto)+15]
                        for iM, min in enumerate(minutos):
                            if min > 59: minutos[iM] = min-60
                        for iM, min in enumerate(minutos):
                            if min < 0: minutos[iM] = 24-min
                        Conn.notificacao(Conn, [LigasNome[i], "5_mais", f"{date.today()} {int(hora)}:{int(minutos[0])}:00", minutos[1],minutos[2],minutos[3],minutos[4], 0])

    def calcularSinal1x1(self):
        timeHora = self.time['horas']
        if self.tabelaVazia:
            timeHora = self.time['horas'][1::]
        LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
        for i,ligas in enumerate(self.arrayTabelas):
            for x,linha in enumerate(ligas):
                if x == 1:
                    break
                for y, coluna in enumerate(linha):
                    if coluna == "1x1" and y+1 < len(linha):
                        if int(linha[y+1].split("x")[0])>0 and int(linha[y+1].split("x")[1])>0:              
                            hora = timeHora[x].text
                            minuto = self.time['minutos'][i][y].text
                            if int(hora) > 23:
                                hora = hora-24
                            if int(minuto) > 59:
                                minuto= minuto-59
                            minutos = [int(minuto)+7, int(minuto)+9, int(minuto)+12, int(minuto)+15, int(minuto)+18]
                            for iM, min in enumerate(minutos):
                                if min > 59: minutos[iM] = min-60
                            for iM, min in enumerate(minutos):
                                if min < 0: minutos[iM] = 24-min
                            Conn.notificacao(Conn, [LigasNome[i], "1x1", f"{date.today()} {hora}:{int(minutos[0])}:00", minutos[1],minutos[2],minutos[3],minutos[4], 0])
    
    def verificarSinal(self):
        signals = Conn.getSinal(Conn,datetime.today())
        if len(signals) > 0:
            for sinal in signals:
                #id, liga, HOUR(horaNotificar), regra, min_1, min_2, min_3, min_4
                infoMessage = Telebot.send_signal(Telebot,sinal,self.config) 
                Conn.updateNotificacao(Conn, sinal)
                if sinal[3] == "2x2" : 
                    while True:
                        self.tratarDados(self)
                        validacao = Validador.resultadoOver3_5(Validador, sinal, self.arrayTabelas ,self.time)
                        if len(validacao) > 0:
                            # id, mensagem, resultado, config
                            Telebot.update_signal(Telebot,infoMessage[0],sinal[0], infoMessage[1], validacao[0],validacao[1],validacao[2], self.config)
                            self.reset(self)
                            break
                        sleep(10)
                else:
                    while True:
                        self.tratarDados(self)
                        validacao = Validador.resultadoAmbas(Validador, sinal, self.arrayTabelas ,self.time)
                        if len(validacao) > 0:
                            Telebot.update_signal(Telebot,infoMessage[0], sinal[0], infoMessage[1],validacao[0],validacao[1],validacao[2], self.config)
                            self.reset(self)
                            break
                        sleep(10)
     
    def reset(self):
        self.driver.quit()
        gc.collect()
        self.start(self)
        self.logar(self)
        return 0

    def zerarPlacar(self):
        with open("result.json", 'w', encoding='UTF-8') as resultFile:
            result = json.load(resultFile) 
            result["resultado"]["envios"] = 0
            result["resultado"]["win"] = 0
            result["resultado"]["lose"] = 0
            result = json.dumps(result, indent = 2) 
            resultFile.write(str(result))
            resultFile.close()

    @staticmethod
    def main(self):
        while True:
            self.verificarSinal(self)
            self.tratarDados(self)
            self.calcularSinal2x2(self)
            self.calcularSinal2x0(self)
            self.calcularSinal1x1(self)
            self.calcularSinal5_mais(self)
            self.calcularSinal2x0_1x0(self)
            self.calcularSinal1x1_1x0(self)
            self.verificarSinal(self)
            self.temporizador+=1
            if self.dataHoje !=date.today():
                self.zerarPlacar(self)

Bot.config(Bot)
Bot.start(Bot)
Bot.logar(Bot)
Bot.main(Bot)
#self.id = Telebot.send_signal(Telebot, entradas,self.config) 
