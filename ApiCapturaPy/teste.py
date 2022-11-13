import psutil
import mysql.connector
from mysql.connector import Error


def Conexao2():

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='MoniToll',
                                            user='MoniToll',
                                            password='123')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            global cursor
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            InserirLocal()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


cpuPercent = psutil.cpu_percent(interval = 1, percpu = True)
ramTotal = round((psutil.virtual_memory() [0] / 10**9), 4)
ramUso = round((psutil.virtual_memory() [3] / 10**9), 4)
ramUsoPercent = round((psutil.virtual_memory() [2]), 1)
discoTotal = round((psutil.disk_usage("/")[0] / 10**12), 3)
discoUso = round((psutil.disk_usage("/")[1] / 10**12), 3)
discoLivre = round((psutil.disk_usage("/")[2] / 10**12), 3)
discoPercent = psutil.disk_usage("/")[3]
pacoEnv = round((psutil.net_io_counters(pernic=False, nowrap=True) [2] / 1024), 2)
pacoRec = round((psutil.net_io_counters(pernic=False, nowrap=True) [3] / 1024), 2)
pacoPerd = [pacoEnv, pacoRec]

def InserirLocal():

    try: 
        sql = ("INSERT INTO Leitura VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        values = (cpuPercent, ramTotal, ramUso, ramUsoPercent, discoTotal, discoUso, discoLivre, discoPercent, pacoEnv, pacoRec ,pacoPerd)
        cursor.execute(sql, values)
        cursor.commit()
        print("Inserindo")
    except Error as e:
        cursor.rollback()
        print("Error while connecting to MySQL", e)

         
Conexao2()

   