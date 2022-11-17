from statistics import mean
import subprocess
import time
import psutil
import numpy
import datetime
import functools
import operator
import pyodbc 
from pyodbc import Error
import textwrap
import mysql.connector
from mysql.connector import errorcode
from asyncio import sleep
from errno import errorcode
from json import loads

def Conexao2(cont, conn):
    while True:
        CpuPercent = psutil.cpu_percent(interval=1, percpu=True)
        QtdProcessadores = psutil.cpu_count(logical=True)
        RamTotal = round((psutil.virtual_memory()[0] / 10**9), 4)
        RamUso = round((psutil.virtual_memory()[3] / 10**9), 4)
        PorcentUsoRam = round((psutil.virtual_memory()[2]), 1)
        vmem = round((psutil.virtual_memory()[1] / 1024/1024/1024), 3)
        DiscoRTotal = round((psutil.disk_usage('/')[0] / 10**12), 3)
        UsoDiscoR = round((psutil.disk_usage('/')[1] / 10**12), 3)
        LivreDiscoR = round((psutil.disk_usage('/')[2] / 10**12), 3)
        PorcentDiscoR = psutil.disk_usage('/')[3]
        BytesRec = round(psutil.net_io_counters()[1] / 10**6, 2)
        BytesEnv = round(psutil.net_io_counters()[0] / 10**6, 2)
        PacotesEnv = round((psutil.net_io_counters(
            pernic=False, nowrap=True)[2] / 1024), 2)
        PacotesRec = round((psutil.net_io_counters(
            pernic=False, nowrap=True)[3] / 1024), 2)
        contador = 0
        for x in CpuPercent:
            contador = contador + x
            PorcentCPU = (round(contador/QtdProcessadores, 1))
        vetor = [PorcentCPU, QtdProcessadores, RamTotal, RamUso, PorcentUsoRam,
                 DiscoRTotal, UsoDiscoR, LivreDiscoR, PorcentDiscoR, PacotesEnv, PacotesRec, vmem, BytesRec, BytesEnv]
        PorcPctperdidos = round((((vetor[10] - vetor[9])/vetor[10])*100), 1)
        datahora = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        t = time.sleep(5)

        def leitura(conn):
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Leitura (dataHora, cpuPercent, ramTotal, ramUso, ramUsoPercent, discoTotal, discoUso, discoLivre, discoPercent, pacoEnv, pacoRec ,pacoPerd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (datahora,PorcentCPU, RamTotal, RamUso, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR,
                            PorcentDiscoR, PacotesEnv, PacotesRec, PorcPctperdidos))
            conn.commit()

            print("Inserindo dados no banco de dados!")

        if cont > cont: # Este contador realiza apenas 4 leitura e para, não sendo necessário dar ctrl+c para para o serviço de captura
            break
        else:
            cont += 1

        leitura(conn)

try:
    conn = mysql.connector.connect(
        host='172.17.0.2',
        user='root',
        password='123',
        database='MoniToll'
    )
    print("Conexão com o Banco de Dados MySQL efetuada com sucesso!")

    cont = 0

# Validações de Erro:
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Algo está errado com o Usuário do Banco ou a Senha.")
        time.sleep(10)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("O banco de dados direcionado não existe.")
        time.sleep(10)
    else:
        print(err)
        time.sleep(10)