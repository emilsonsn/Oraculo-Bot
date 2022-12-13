import mysql.connector
import json
from datetime import date
class Conn:

    def start(self):
        with open("config.json") as configFile:
            config = (json.load(configFile))['conn']
            configFile.close()
        self.conn = mysql.connector.connect(user=config['user'], password=config['pass'], host=config['host'], database=config['database'])
    
    def get_groups(self):
         #liga, res_casa, res_fora, hora, minuto, nome casa, nome fora
        self.start(self)
        sql_select_Query ="SELECT telegram_id FROM `tb_grupos` WHERE ativado = 1"
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return records
    
    def get_estrategias(self, cod):
         #liga, res_casa, res_fora, hora, minuto, nome casa, nome fora
        self.start(self)
        sql_select_Query ="SELECT id FROM `tb_estrategias` WHERE cod = '%s' and ativada = 1". replace('%s', cod)
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return len(records) > 0
    
    def insertResult(self, resultado, estrategia, tiro, categoria):
        self.start(self)
        sql = "INSERT INTO tb_resultados (resultado, estrategia, tiro, categoria) VALUES (%s, %s, %s, %s)"
        val = (resultado, estrategia, tiro, categoria)
        cursor = self.conn.cursor()
        cursor.execute(sql, val)
        self.conn.commit()
        self.conn.close()
        
    def get_resultado_geral(self):
         #liga, res_casa, res_fora, hora, minuto, nome casa, nome fora
        self.start(self)
        sql_select_Query = """Select ROUND((SELECT count(*) FROM tb_resultados where resultado='gain' and cast(data as date) = cast(now() as date)) /
        ((SELECT count(*) FROM tb_resultados where resultado='gain' and cast(data as date) = cast(now() as date)) +
        (SELECT count(*) FROM tb_resultados where resultado='loss' and cast(data as date) = cast(now() as date))) * 100)"""
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return str((records[0][0])) + '%'

    def get_resultado_tiro(self, tiro):
         #liga, res_casa, res_fora, hora, minuto, nome casa, nome fora
        self.start(self)
        sql_select_Query = """Select ROUND((SELECT count(*) FROM tb_resultados where resultado='gain' and tiro={tiro} and cast(data as date) = cast(now() as date))
        /((SELECT count(*) FROM tb_resultados where resultado='gain' and tiro={tiro} and cast(data as date) = cast(now() as date))
        +(SELECT count(*) FROM tb_resultados where resultado='loss' and tiro={tiro} and cast(data as date) = cast(now() as date)))*100, 2)""".replace('{tiro}', str(tiro))
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return str((records[0][0])) + '%'

    def get_ambas(self):
         #liga, res_casa, res_fora, hora, minuto, nome casa, nome fora
        self.start(self)
        sql_select_Query = """Select ROUND((SELECT count(*) FROM tb_resultados where resultado='gain' and categoria='AMBAS MARCAM' and cast(data as date) = cast(now() as date)) /
        ((SELECT count(*) FROM tb_resultados where resultado='gain' and categoria='AMBAS MARCAM' and cast(data as date) = cast(now() as date)) +
        (SELECT count(*) FROM tb_resultados where resultado='loss' and categoria='AMBAS MARCAM' and cast(data as date) = cast(now() as date))) * 100)  as 'ambas'"""
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return str((records[0][0])) + '%'

    def get_2_5(self):
         #liga, res_casa, res_fora, hora, minuto, nome casa, nome fora
        self.start(self)
        sql_select_Query = """Select ROUND((SELECT count(*) FROM tb_resultados where resultado='gain' and categoria='2.5' and cast(data as date) = cast(now() as date)) /
        ((SELECT count(*) FROM tb_resultados where resultado='gain' and categoria='2.5' and cast(data as date) = cast(now() as date)) +
        (SELECT count(*) FROM tb_resultados where resultado='loss' and categoria='2.5' and cast(data as date) = cast(now() as date))) * 100) as '2_5'"""
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return str((records[0][0])) + '%'

    def get_3_5_ambas(self):
         #liga, res_casa, res_fora, hora, minuto, nome casa, nome fora
        self.start(self)
        sql_select_Query = """Select ROUND((SELECT count(*) FROM tb_resultados where resultado='gain' and categoria='AMBAS MARCAM 3.5' and cast(data as date) = cast(now() as date)) /
        ((SELECT count(*) FROM tb_resultados where resultado='gain' and categoria='AMBAS MARCAM 3.5' and cast(data as date) = cast(now() as date)) +
        (SELECT count(*) FROM tb_resultados where resultado='loss' and categoria='AMBAS MARCAM 3.5' and cast(data as date) = cast(now() as date))) * 100)  as '3_5_ambas'"""
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return str((records[0][0])) + '%'

    def sequenciaMes(self):
        self.start(self)
        sql_select_Query = "SELECT sequencia_mes FROM tb_resultados_mes where month(now()) = month(data);"
        cursor = self.conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.conn.close()
        return records[0][0]


