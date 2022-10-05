import datetime
import psutil
import time
import mysql.connector

while True:
    CpuPercent = psutil.cpu_percent(interval = 1, percpu = True)
    QtdProcesadores = psutil.cpu_count(logical=True)
    RamTotal = round((psutil.virtual_memory() [0] / 10**9), 4)
    RamUso = round((psutil.virtual_memory() [3] / 10**9), 4)
    PorcentUsoRam = round((psutil.virtual_memory() [2]), 1)
    DiscoRTotal = round((psutil.disk_usage('/')[0] / 10**12), 3)
    UsoDiscoR = round((psutil.disk_usage('/')[1] / 10**12), 3)
    LivreDiscoR = round((psutil.disk_usage('/')[2] / 10**12), 3)
    PorcentDiscoR = psutil.disk_usage('/')[3]
    PacotesEnv = round((psutil.net_io_counters(pernic=False, nowrap=True) [2] / 1024), 2)
    PacotesRec = round((psutil.net_io_counters(pernic=False, nowrap=True) [3] / 1024), 2)
    contador = 0
    for x in CpuPercent:
            contador = contador + x
            PorcentCPU = (round(contador/QtdProcesadores, 1))
    vetor = [PorcentCPU, QtdProcesadores, RamTotal, RamUso, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR, PorcentDiscoR, PacotesEnv, PacotesRec]
    PorcPctperdidos = round((((vetor[10] - vetor[9])/vetor[10])*100), 1)
    datahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')


    def criarTabela():

        

        config = {
            'user': 'root',
            'password': 'Urubu100',
            'host': 'localhost',
            'database': 'Argos',
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
        sql = ("INSERT INTO Leitura (DataHora, PorcentCPU, QtdProcesadores, RamTotal, RamUsada, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR, PercentDiscoR, PacotesEnv, PacotesRec,  PorcentPerd, fkTorre) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        values = (datahora, PorcentCPU, QtdProcesadores, RamTotal, RamUso, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR, PorcentDiscoR, PacotesEnv, PacotesRec,  PorcPctperdidos, 1)


        try:
            # Executing the SQL command
            cursor.execute(sql, values)

            # Commit your changes in the database
            cnx.commit()

            print("Dados Inseridos com sucesso")

        except mysql.connector.Error as err:
            cnx.rollback()
            print("Something went wrong: {}".format(err))
    
        # Closing the connection
        cnx.close()
    
        time.sleep(3)

    criarTabela()
