import time
import subprocess
import psutil
import datetime
import mysql.connector

i=0
while True:
    # CPTURA DADOS MAQUINA
    cpu_percent = psutil.cpu_percent(interval = 1, percpu = True)
    QtdProcesadores = psutil.cpu_count(logical=True)
    RamTotal = round((psutil.virtual_memory() [0] / 10**9), 4)
    RamUso = round((psutil.virtual_memory() [3] / 10**9), 4)
    PorcentUsoRam = round((psutil.virtual_memory() [2]), 1)
    DiscoRTotal = round((psutil.disk_usage("C:\\")[0] / 10**12), 3)
    UsoDiscoR = round((psutil.disk_usage("C:\\")[1] / 10**12), 3)
    LivreDiscoR = round((psutil.disk_usage("C:\\")[2] / 10**12), 3)
    PorcentDiscoR = psutil.disk_usage("C:\\")[3]
    PacotesEnv = round((psutil.net_io_counters(pernic=False, nowrap=True) [2] / 1024), 2)
    PacotesRec = round((psutil.net_io_counters(pernic=False, nowrap=True) [3] / 1024), 2)
    soma = 0
    for x in cpu_percent:
            soma = soma + x
            PorcentCPU = (round(soma/8, 1))
    vetor = [PacotesEnv, PacotesRec]
    PorcPctperdidos = round((((vetor[1] - vetor[0])/vetor[1])*100), 1)
    datahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    i+=1

    def criarTabela():

        config = {
            'user': 'MoniToll',
            'password':'123',
            'host': 'localhost',
            'database': 'MoniToll',
            'raise_on_warnings': True
        }

        cnx = mysql.connector.connect(**config)

        if cnx.is_connected():
            db_info = cnx.get_server_info()
            print('conectado', db_info)
            cursor = cnx.cursor()
            cursor.execute("select database();")
            linha = cursor.fetchone()
            print("Conectado ao banco de dados:", linha)

        cursor = cnx.cursor() 
            
        try:
            sql = ("INSERT INTO Leitura VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)")
            values = (PorcentCPU, RamTotal, RamUso, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR, PorcentDiscoR, PacotesEnv, PacotesRec, PorcPctperdidos)

                # Executing the SQL command
            cursor.execute(sql, values)

                # Commit your changes in the database
            cnx.commit()

            print("Foi insert da leitura")

        except mysql.connector.Error as err:
            cnx.rollback()
            print("Something went wrong: {}".format(err))
    
    


        # Closing the connection
        cnx.close()

        time.sleep(1)

    criarTabela()
