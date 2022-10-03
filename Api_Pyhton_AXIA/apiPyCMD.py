import time
# Biblioteca para discretirização (definir o intervalo entre capturas)
import subprocess
# Biblioteca para execução de comando no CMD
import psutil
# Biblioteca para captura dos dados dos hardwares
import datetime
# Biblioteca para captura da data e hora da leitura
import mysql.connector
# Biblioteca de coneção com o banco de dados local


i=0
# estrutura de repetição infinita
while True:
    # CAPTURA MODELO PC CMD

    direct_output = subprocess.check_output(
        'wmic computersystem get model', shell=True)
    modeloPC = direct_output.decode('UTF-8')
    trim1ModeloPC = modeloPC.strip()
    def func(value):
        return ''.join(value.splitlines())
    trim2ModeloPC = func(trim1ModeloPC)
    trim3ModeloPC = trim2ModeloPC.strip("Model") 
    trim4ModeloPC = trim3ModeloPC.strip()


    # CAPTURA SERIALID PC CMD
    
    direct_output2 = subprocess.check_output(
        'wmic bios get serialnumber', shell=True)
    SerialID = direct_output2.decode('UTF-8')
    trim1SerialID = SerialID.strip()
    def func(value):
        return ''.join(value.splitlines())
    trim2SerialID = func(trim1SerialID)
    trim3SerialID = trim2SerialID.strip("SerialNumber") 
    trim4SerialID = trim3SerialID.strip()


    # CAPTURA MODELO PROCESSADOR PC CMD
    
    direct_output3 = subprocess.check_output(
        'wmic cpu get name', shell=True)
    ModeloCPU = direct_output3.decode('UTF-8')
    trim1ModeloCPU = ModeloCPU.strip()
    def func(value):
        return ''.join(value.splitlines())
    trim2ModeloCPU = func(trim1ModeloCPU)
    trim3ModeloCPU = trim2ModeloCPU.strip("SerialNumber") 
    trim4ModeloCPU = trim3ModeloCPU.strip()


    # CAPTURA MODELO DISCO R PC CMD
    
    direct_output4 = subprocess.check_output(
        'wmic diskdrive get model', shell=True)
    ModeloDR = direct_output4.decode('UTF-8')
    trim1ModeloDR = ModeloDR.strip()
    def func(value):
        return ''.join(value.splitlines())
    trim2ModeloDR = func(trim1ModeloDR)
    trim3ModeloDR = trim2ModeloDR.strip("Model") 
    trim4ModeloDR = trim3ModeloDR.strip()


    # CAPTURA RAM SPEED PC CMD
    
    direct_output5 = subprocess.check_output(
        'wmic memorychip get speed', shell=True)
    ramSpeed = direct_output5.decode('UTF-8')
    trim1ramSpeed = ramSpeed.strip()
    def func(value):
        return ''.join(value.splitlines())
    trim2ramSpeed = func(trim1ramSpeed)
    trim3ramSpeed = trim2ramSpeed.strip("Speed") 
    trim4ramSpeed = trim3ramSpeed.strip()

    # CAPTURA OS NOME PC CMD
    
    direct_output6 = subprocess.check_output(
        'wmic os get Caption', shell=True)
    OSnome = direct_output6.decode('UTF-8')
    trim1OSnome = OSnome.strip()
    def func(value):
        return ''.join(value.splitlines())
    trim2OSnome = func(trim1OSnome)
    trim3OSnome = trim2OSnome.strip("Caption") 
    trim4OSnome = trim3OSnome.strip()


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
    null = None
    trim3SerialIDfake = "BY9DQM3"
    trim4SerialIDfake = trim3SerialIDfake.strip()
    def criarTabela():
        # print("Leitura", i)
        # print()
        # print("SerialID:", trim4SerialID)
        # print("Modelo PC:",trim4ModeloPC)
        # print("Modelo CPU:",trim4ModeloCPU)
        # print("Modelo Disco Rigido:",trim4ModeloDR)
        # print("Velocidade RAM:",trim4ramSpeed)
        # print("OS nome:",trim4OSnome)



        config = {
            'user': 'root',
            'password': '#Gf15533155708',
            'host': 'localhost',
            'database': 'argos',
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

        query = ("SELECT `idTorre` FROM Torre " 
                "WHERE SerialID like %s;")
        try:
            # Executing the SQL command
            cursor.execute(query, (trim4SerialID,))
            print("fez o select")

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

        idTorre = cursor.fetchone()

        if idTorre is not None:
            print("tem id")
            idTorreStrip = "".join(map(str, idTorre))

            sql = ("INSERT INTO Leitura (DataHora, PorcentCPU, QtdProcesadores, RamTotal, RamUsada, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR, PercentDiscoR, PacotesEnv, PacotesRec,  PorcentPerd, fkTorre) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            values = (datahora, PorcentCPU, QtdProcesadores, RamTotal, RamUso, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR, PorcentDiscoR, PacotesEnv, PacotesRec,  PorcPctperdidos, idTorreStrip)


            try:
                # Executando comando SQL   
                cursor.execute(sql, values)

                # Commit de mudanças no banco de dados
                cnx.commit()

                print("Foi insert da leitura")

            except mysql.connector.Error as err:
                cnx.rollback()
                print("Something went wrong: {}".format(err))
    

        else:
            print("não tem id")
            sql = ("INSERT INTO Torre (idTorre ,SerialID, ModeloTorre, ModeloProcessador, ModeloDiscoR, VelocidadeRam, SO, fkEmpresa) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
            values = (null, trim4SerialID, trim4ModeloPC, trim4ModeloCPU, trim4ModeloDR, trim4ramSpeed, trim4OSnome, 1)

            try:
                # Executando comando SQL
                cursor.execute(sql, values)

                # Commit de mudanças no banco de dados
                cnx.commit()

                print("inseriu nova torre no banco")

            except mysql.connector.Error as err:
                cnx.rollback()
                print("Something went wrong: {}".format(err))

            try:
                # Executando comando SQL
                cursor.execute(query, (trim4SerialID,))
                print("fez o select de sem id")
                idTorre = cursor.fetchone()


            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                
            print(idTorre)
        


        # Encerrando a conexão
        cnx.close()

        time.sleep(1)

    criarTabela()
