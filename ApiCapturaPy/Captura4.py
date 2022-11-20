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



# Bloco pegar serial id
byte_SerialIdAtual = "c26d"
global strip_SerialIdAtual
strip_SerialIdAtual = byte_SerialIdAtual

# Bloco pegar sistema operacional
byte_OsAtual = "Ubuntu 20.04"
global strip3_OsAtual
strip3_OsAtual = byte_OsAtual

# Bloco pegar modelo maquina
byte_MaquinaAtual = "docker"
global strip3_MaquinaAtual
strip3_MaquinaAtual = byte_MaquinaAtual

# Bloco pegar processador
byte_ProcessadorAtual = "Quad.Core"
global strip2_ProcessadorAtual
strip2_ProcessadorAtual = byte_ProcessadorAtual

# Bloco pegar disco
byte_DiscoAtual = 1000000
global strip2_DiscoAtual
strip2_DiscoAtual = byte_DiscoAtual

# Bloco pegar velocidade da ram
byte_RamAtual = 1000
global strip2_RamAtual
strip2_RamAtual = byte_RamAtual


conectado = 1


def Login():
    if conectado == 1:
        print("Bem vindo ao Grenn Light!")
        print("Login")
        u_email = input('Seu e-mail: ')
        u_senha = input('Sua senha: ')
        ValidarLogin(u_email, u_senha)
    elif conectado == 0:
        print("Sem conexão com a internet.")


# estabelecer conexao com Azure

def ConectarBancoAzure(nmr):

    try:
        # variaveis de conexao
        driver = '{ODBC Driver 18 for SQL Server}'
        server_name = 'montioll'
        database_name = 'Monitoll'
        server = '{server_name}.database.windows.net,1433'.format(
            server_name=server_name)
        username = 'Monitoll'
        password = 'Grupo7@123'
        # definindo banco url
        connection_string = textwrap.dedent('''
        Driver={driver};
        Server={server};
        Database={database};
        Uid={username};
        Pwd={password};
        Encrypt=yes;
        TrustedServerCertificate=no;
        Connection Timeout=10;
        '''.format(
            driver=driver,
            server=server,
            database=database_name,
            username=username,
            password=password
        ))

        cnxn: pyodbc.Connection = pyodbc.connect(connection_string)
        global crsr
        crsr = cnxn.cursor()
        print("Conectado ao banco de dados da Nuvem")
        conectado = nmr

    except pyodbc.Error as ex:
        print("Conexão com a Azure perdida")
        print(ex)
        conectado = 0

    if conectado == 3:
        BuscarComponentes(idTorre)
    elif conectado == 0:
        ConectarBancoLocal()



# Estabelecer conexao com banco de dados local no docker
def ConectarBancoLocal():
    try:
        conn = mysql.connector.connect(
            host='172.17.0.3',
            user='root',
            password='123',
            database='MoniToll'
        )
        print("Conexão com o Banco de Dados MySQL efetuada com sucesso!")
        LeituraLocal(conn)

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


# Inserir leituras Banco local
def LeituraLocal(conn):
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

    cursor = conn.cursor()

    cursor.execute("INSERT INTO Leitura (dataHora, cpuPercent, ramTotal, ramUso, ramUsoPercent, discoTotal, discoUso, discoLivre, discoPercent, pacoEnv, pacoRec ,pacoPerd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (datahora, PorcentCPU, RamTotal, RamUso, PorcentUsoRam, DiscoRTotal, UsoDiscoR, LivreDiscoR,
                    PorcentDiscoR, PacotesEnv, PacotesRec, PorcPctperdidos))
    conn.commit()

    print("Inserindo leitura no banco de dados local!")


def ValidarLogin(email, senha):
    try:
        crsr.execute('''
        SELECT Nome,fkEmpresa FROM Usuario WHERE Email = ? and Senha = ?
        ''', email, senha)
        # Executando comando SQL
        print("Fazendo login...")
        global usuario
        usuario = crsr.fetchall()
        print("Login efetuado com sucesso")
        u_usuario = usuario[0]
        print(u_usuario)
        global fkEmpresa
        fkEmpresa = u_usuario[1]
        BuscarTorres(fkEmpresa)

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))
        print("Falha ao realizar login por favor tente novamente")


def BuscarTorres(fkEmpresa):

    try:
        crsr.execute('''
    SELECT idTorre FROM Torre WHERE fkEmpresa = ?
    ''', fkEmpresa)
        # Executando comando SQL)
        idTorres = crsr.fetchall()
        EscolherTorres(idTorres)

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))


def EscolherTorres(idTorres):
    for x in idTorres:
        print('Maquina:', x[0])
    global idTorre
    idTorre = input('Qual é esta maquina? ')
    VerificarDadosMaquina(idTorre)


def VerificarDadosMaquina(idTorre):

    try:
        crsr.execute('''
        SELECT SerialID FROM Torre WHERE idTorre = ?
        ''', idTorre)
        # Executando comando SQL
        print("Verificando dados da torre...")
        SerialIdBanco = crsr.fetchone()

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))

    if SerialIdBanco[0] != '':
        print("A torre possui dados cadastrados")
        ConectarBancoAzure(3)
    else:
        print("A torre não possui dados")
        InserirDadosMaquina(strip_SerialIdAtual, strip3_OsAtual, strip3_MaquinaAtual,
                            strip2_ProcessadorAtual, strip2_DiscoAtual, strip2_RamAtual)


def InserirDadosMaquina(SerialID, OS, Maquina, Processador, Disco, RamSpeed):

    try:
        crsr.execute('''
        UPDATE Torre  SET SerialID = ?,  SO = ?, Maquina = ?, Processador = ?, Disco = ?, Ram = ?,  fkEmpresa = ? WHERE idTorre = ?
        ''', SerialID, OS, Maquina, Processador, Disco, RamSpeed, fkEmpresa, idTorre)
        # Executando comando SQL
        # Commit de mudanças no banco de dados
        crsr.commit()
        print("Inserindo dados...")

    except pyodbc.Error as err:
        crsr.rollback()
        print("Something went wrong: {}".format(err))


def BuscarComponentes(idTorre):

    # PEGAR fkCOMPONENTE
    try:
        print("Buscando os componentes da torre...")
        crsr.execute('''
        SELECT fkComponente FROM Torre_Componente WHERE Torre_Componente.fkTorre = ?
        ''', idTorre)
        fkComponente = crsr.fetchall()
        for x in fkComponente:
            global idComponente
            idComponente = x[0]
            print("Componente:",idComponente)
            try:
                crsr.execute('''
                    SELECT Codigo, Nome FROM Componente WHERE Componente.idComponente = ?
                    ''', idComponente)
                # Executing the SQL command
                print("Pegando codigo do componente ",idComponente,'.........')
                Codigo = crsr.fetchone()
                print(Codigo)
                print("Codigo do componente ", idComponente,":",Codigo[0])

            except pyodbc.Error as err:
                print("Something went wrong: {}".format(err))




            # global strCodigo
            # strCodigo = convertTuple(Codigo)

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))



        # PEGAR CODIGO COMPONENTE



        # PREGAR NOME COMPONENTE

        # try:
        #     crsr.execute('''
        #         SELECT Nome FROM Componente WHERE Componente.idComponente = ?
        #         ''', y)
        #     # Executing the SQL command
        #     print("Pegando nome do componente", y)

        # except pyodbc.Error as err:
        #     print("Something went wrong: {}".format(err))

        # Nome = crsr.fetchone()
        # global strNome
        # strNome = convertTuple(Nome)
        # print("Nome componente ", y, ":", strNome)
        # print(strNome + " = " + strCodigo)
        # teste()





ConectarBancoAzure(1)
Login()
while True:
    ConectarBancoAzure(3)
    time.sleep(10)
