import mysql.connector
import json
from datetime import datetime, timedelta

class Conn:
    def start(self):
        with open("config.json") as configFile:
            config = (json.load(configFile))['conn']
            configFile.close()
        self.conn = mysql.connector.connect(user=config['user'], password=config['pass'], host=config['host'], database=config['database'])

    @staticmethod
    def notificacao(self, arrayData):
        self.start(self)
        if self.existeNoficacao(self, arrayData):
            return 0
        else:
            dataSinal = datetime.strptime(arrayData[2], "%Y-%m-%d %H:%M:%S")
            hoje = int(datetime.today().hour)+4
            if hoje > 23:
                hoje = 24-hoje
            minuto = datetime.today().minute
            if dataSinal.hour >= hoje or ( dataSinal.hour >= hoje and dataSinal.minute > minuto):
                self.salvarNoticicacao(self, arrayData)
        
    def salvarNoticicacao(self, arrayData):
        mycursor = self.conn.cursor()
        sql = """INSERT INTO tb_eventos
        (liga, regra, horaNotificar, min_1, min_2, min_3, min_4, enviado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (arrayData[0], arrayData[1],arrayData[2], arrayData[3], arrayData[4], arrayData[5], arrayData[6], arrayData[7])
        mycursor.execute(sql, val)
        self.conn.commit()

    def updateNotificacao(self, data):
        self.start(self)
        sql_select_Query = "UPDATE tb_eventos SET enviado = 1 WHERE id = {id}".replace("{id}", str(data[0]))
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        self.conn.commit()

    def existeNoficacao(self,arrayData):
        self.start(self)
        sql_select_Query ="select id from tb_eventos where liga=%s and regra=%s and horaNotificar=%s"
        val = (arrayData[0], arrayData[1], arrayData[2])
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query, val)
        records = cursor.fetchall()
        return (len(records)>0)
    
    def getSinal(self, data):
        hora = data.hour+4
        if hora >=24 :
            hora = hora-24
        data = f"{data.year}-{data.month}-{data.day} {hora}:{data.minute}:00"
        self.start(self)
        sql_select_Query = "select id, liga, HOUR(horaNotificar), regra, min_1, min_2, min_3, min_4 from tb_eventos where enviado = 0 and horaNotificar = '{date}' ORDER BY horaNotificar asc LIMIT 1".replace("{date}", data)
        val = (data)
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query, val)
        records = cursor.fetchall()
        return records
    
    def resultadoNotificacao(self, id, resultado):
        #Conn, id_noti, resultado
        self.start(self)
        sql_select_Query = "UPDATE tb_eventos SET resultado = '{resultado}' WHERE id = {id}".replace("{resultado}", resultado).replace("{id}", str(id))
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        self.conn.commit()
    
    def getListId(self):
        self.start(self)
        sql_select_Query = "select id_grupo from tb_grupos where ativado = 1"
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        return records