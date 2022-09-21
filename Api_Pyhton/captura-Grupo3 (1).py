# Grupo 3
# Henrique Oliveira, Arthur Simão, Kaique Siqueira, Júlia Araripe, Mateus do Carmo e Marco Antonio

from datetime import datetime
import psutil
import mysql.connector
import time 
from mysql.connector import errorcode

while True:

    try:
        db_connection = mysql.connector.connect(
            host='localhost', user='root', password='siqueira300', database='MoniToll')
        print("Conectei no banco!")
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
             print("Não encontrei o banco")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
           print("Credenciais erradas")
        else:
           print(error) 
    


    
    frequencia_cpu1 = (psutil.cpu_freq()[0])  
    frequencia_cpu2 = frequencia_cpu1 * 1.25     
    frequencia_cpu3 = frequencia_cpu2 * 0.90     
   
    porcentagem_cpu1 = psutil.cpu_percent()
    porcentagem_cpu2 = porcentagem_cpu1 * 1.10   
    porcentagem_cpu3 = porcentagem_cpu2 * 1.05 

    ram = (psutil.virtual_memory()) 
    ramEmUsoGB1 = float("%0.2f" % (ram [3] * (10**-9)))
    ramEmUsoGB2 = float(ramEmUsoGB1 * 1.05)
    ramEmUsoGB3 = float(ramEmUsoGB2 * 0.80)
    
    ramPercent1 = ram.percent 
    ramPercent2 = ramPercent1 * 1.15 
    ramPercent3 = ramPercent2 * 1.05

    disk = psutil.disk_usage('C:\\')
    diskPercent1 = disk.percent
    diskPercent2 = diskPercent1 * 0.95
    diskPercent3 = diskPercent2 * 3 
    
    diskEmUsoGB1 = float("%0.2f" % (disk [1] * (10**-9)))
    diskEmUsoGB2 = float(diskEmUsoGB1 * 1.05)
    diskEmUsoGB3 = float(diskEmUsoGB2 * 0.90)

    dataHora = datetime.now()
    formatoh = dataHora.strftime("%d/%m/%Y %H:%M:%S")

    cursor = db_connection.cursor()
    fkMaquina = 100
    sql = "INSERT INTO dadosMedidas (freqCpu, cpuPercent, ramPercent, ramEmUsoGB, diskPercent, diskEmUsoGB, dataHora, fkMaquina) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = [frequencia_cpu1, porcentagem_cpu1, ramPercent1, ramEmUsoGB1, diskPercent1, diskEmUsoGB1, dataHora, fkMaquina]
    cursor.execute(sql, values)

    fkMaquina = 101
    sql = "INSERT INTO dadosMedidas (freqCpu, cpuPercent, ramPercent, ramEmUsoGB, diskPercent, diskEmUsoGB, dataHora, fkMaquina) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = [frequencia_cpu2, porcentagem_cpu2, ramPercent2, ramEmUsoGB2, diskPercent2, diskEmUsoGB2, dataHora, fkMaquina]
    cursor.execute(sql, values)

    fkMaquina = 102
    sql = "INSERT INTO dadosMedidas (freqCpu, cpuPercent, ramPercent, ramEmUsoGB, diskPercent, diskEmUsoGB, dataHora, fkMaquina) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = [frequencia_cpu3, porcentagem_cpu3, ramPercent3, ramEmUsoGB3 ,diskPercent3, diskEmUsoGB3, dataHora, fkMaquina]
    cursor.execute(sql, values)

    
    print("\n")
    print(cursor.rowcount, "Inserindo no banco.")

    db_connection.commit()
    db_connection.close()    
    time.sleep(30.0)

   