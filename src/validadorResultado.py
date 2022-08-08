from tkinter import E
from tkinter.tix import Tree
from bs4 import BeautifulSoup
from pytz import HOUR
from src.Telebot import Telebot

class Validador:
    def resultadoOver3_5(self, sinal,arrayTabelas ,time):
        try:
            #id, liga, HOUR(horaNotificar), regra, min_1, min_2, min_3, min_4
            LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
            protecao = []
            arrayTabelas = arrayTabelas[LigasNome.index(sinal[1])]
            minutoArray = []
            for y, minuto in enumerate(time['minutos'][LigasNome.index(sinal[1])]):
                minutoArray.append(int(minuto.text))
            arrayEntradas = [minutoArray.index(sinal[4]), minutoArray.index(sinal[5]), minutoArray.index(sinal[6]), minutoArray.index(sinal[7]) ]
            if int(arrayTabelas[0][arrayEntradas[0]-1].split("x")[0]) + int(arrayTabelas[0][arrayEntradas[0]-1].split("x")[1]) > 3.5:
                return ["abortada", 0, protecao]
            arraySinal = [sinal[4], sinal[5],sinal[6],sinal[7]]
            outraLinha = []
            for i,array in enumerate(arraySinal):
                if int(array) == 2 or int(array) == 0 or int(array) == 1 :
                    outraLinha.append(i)
            hour = 0
            primeira = True
            for c,entrada in enumerate(arrayEntradas):
                if len(outraLinha) > 0 and len(arrayTabelas[hour]) < 4 and primeira:
                    hour = 1
                if len(outraLinha) > 0 and int(c) == int(outraLinha[0]):
                    hour = 0
                    primeira = False
                if int(arrayTabelas[hour][entrada].split("x")[0])+ int(arrayTabelas[hour][entrada].split("x")[1]) > 3.5:
                    return ["win", sinal[c+4], protecao]
                elif int(arrayTabelas[hour][entrada].split("x")[0]) > 0 and int(arrayTabelas[hour][entrada].split("x")[1]) > 0:
                    for i in protecao: 
                        if(i == sinal[c+4]) : 
                            break
                    protecao.append(sinal[c+4])
            if len(protecao) > 0:
                return ['protecao', 0, protecao]
            return ['lose', 0, protecao]
        except Exception as err:
            return []
        #if  

    def resultadoAmbas(self, sinal, arrayTabelas, time):
        try:
            LigasNome = ["Euro", "Copa", "Premier", "Superliga"]
            arrayTabelas = arrayTabelas[LigasNome.index(sinal[1])]
            minutoArray = []
            for y, minuto in enumerate(time['minutos'][LigasNome.index(sinal[1])]):
                minutoArray.append(int(minuto.text))
            arrayEntradas = [minutoArray.index(sinal[4]), minutoArray.index(sinal[5]), minutoArray.index(sinal[6]), minutoArray.index(sinal[7]) ]
            #if int(arrayTabelas[0][arrayEntradas[0]-1].split("x")[0]) > 0 and int(arrayTabelas[0][arrayEntradas[0]-1].split("x")[1]) > 0:
            #    return "abortada"
            arraySinal = [sinal[4], sinal[5],sinal[6],sinal[7]]
            outraLinha = []
            for i,array in enumerate(arraySinal):
                if int(array) == 2 or int(array) == 0 or int(array) == 1 :
                    outraLinha.append(i)
            hour = 0
            primeira = True
            for c,entrada in enumerate(arrayEntradas):
                if len(outraLinha) > 0 and len(arrayTabelas[hour]) < 4 and primeira:
                    hour = 1
                if len(outraLinha) > 0 and int(c) == int(outraLinha[0]):
                    hour = 0
                    primeira = False
                if int(arrayTabelas[hour][entrada].split("x")[0]) >0 and int(arrayTabelas[hour][entrada].split("x")[1]) > 0:
                    return ["win", sinal[c+4], []]
            return ["lose",0,[]]
        except Exception as err:
            return []
    #def resultadoOver3_5(self, sinal, driver):
