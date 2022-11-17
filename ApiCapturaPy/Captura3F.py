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


def Conexao1():

    try:
        # variaveis de conexao
        driver ='{ODBC Driver 18 for SQL Server}'
        server_name = 'montioll'
        database_name = 'Monitoll'
        server = '{server_name}.database.windows.net,1433'.format(server_name=server_name)
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

        cnxn:pyodbc.Connection = pyodbc.connect(connection_string) 

        global crsr
        crsr = cnxn.cursor()
        print("Conectado ao banco de dados da Nuvem:")
        try:
                crsr.execute('''
            SELECT * FROM Torre
            ''')                    
                # Executando comando SQL)
        except pyodbc.Error as err:
            print("Something went wrong: {}".format(err))

        cnxn.close()
        ValidacaoLogin()
        VerificarDadosMaquina(idTorre)

    except pyodbc.Error as ex:
        print("{c} não conexão com o banco".format(c=connection_string))    
        Conexao2(cont, conn)


def ValidacaoLogin():

    records = u_email = input('Seu e-mail: ')
    records2 = u_senha = input('Sua senha: ')
                    
    try:
        crsr.execute('''
    SELECT Nome FROM Usuario WHERE Email = ? and Senha = ?
    ''',records, records2)
        # Executando comando SQL
        print("Fazendo login...")
        global usuario
        usuario = crsr.fetchone()

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))
    
    if usuario is not None:
        def convertTuple(tup):
            str = ''
            for item in tup:
                str = str + item
            return str
        str_usuario = convertTuple(usuario)
        print('Olá,',str_usuario,'!')
                    
        try:
            crsr.execute('''
        SELECT fkEmpresa FROM Usuario WHERE Email = ? and Senha = ?
        ''',u_email, u_senha)
            # Executando comando SQL
            global fkEmpresa
            fkEmpresa = crsr.fetchone()
            global int_fkEmpresa
            int_fkEmpresa = sum(fkEmpresa)
            print('fkEmpresa:', fkEmpresa)

        except pyodbc.Error as err:
            print("Something went wrong: {}".format(err))

        SelectIdTorres(fkEmpresa)

    else:
        print('Email ou senha incoretos')
        ValidacaoLogin()


def EscolherTorres(idTorres):
    maquinas = numpy.asarray(idTorres)
    print('Maquinas:', maquinas)
    global idTorre
    idTorre = input('Qual é esta maquina?')

def SelectIdTorres(fkEmpresa):

    try:
        crsr.execute('''
    SELECT idTorre FROM Torre WHERE fkEmpresa = ?
    ''',fkEmpresa)                    
        # Executando comando SQL)
        idTorres = crsr.fetchall()
        print(idTorres)
        

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))
    
    EscolherTorres(idTorres)


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



def teste():
        print("Inserindo leitura no banco...")
        datahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        print(datahora)
        exec(strNome + " = " + strCodigo, globals())
        var_leitura = globals()[strNome]
        if strNome == 'processadores_nucleo_porcentagem':
            
            print(var_leitura)
            var_leitura2 = mean(var_leitura)
            print(var_leitura2)
        elif strNome == 'pacotes_perdidos_porcentagem':
            print('caiu no elif 1')
            var_leitura2 = round((((pacotes_perdidos_porcentagem[1] - pacotes_perdidos_porcentagem[0])/pacotes_perdidos_porcentagem[1])*100), 1)
        elif strNome == 'processadores_nucleo_porcentagem':
            print('caiu no elif 2')
            var_leitura2 = numpy.mean(var_leitura) 
        else:
            print('caiu no else')
            var_leitura2 = var_leitura
        print(var_leitura2)

        
        try:
            # Executando comando SQL   
            crsr.execute('''
        INSERT INTO Leitura (Leitura, DataHora, fkTorre, fkComponente) VALUES (?, ?, ?, ?)
        ''',var_leitura2, datahora, idTorre , y)
            # Commit de mudanças no banco de dados
            crsr.commit()
            print("Leitura inserida no banco")

        except pyodbc.Error as err:
            cnxn.rollback()
            print("Something went wrong: {}".format(err))


            

def InserindoLeitura():
    # PEGAR fkCOMPONENTE

            try:
                crsr.execute('''
            SELECT fkComponente FROM Torre_Componente WHERE Torre_Componente.fkTorre = ?
            ''', idTorre)
                # Executing the SQL command
                print("Pegando os componentes da torre...")

            except pyodbc.Error as err:
                print("Something went wrong: {}".format(err))
                print('teste exept')

            fkComponente= crsr.fetchall()
            print(fkComponente)
            vet_fkComponente = numpy.asarray(fkComponente)
            print("Componentes da maquina:", vet_fkComponente)
            
            for x in vet_fkComponente:
                print(x)
                global y
                y = int(x[0])
                print(y)

                # PEGAR CODIGO COMPONENTE
                
                try:
                    crsr.execute('''
                SELECT Codigo FROM Componente WHERE Componente.idComponente = ?
                ''', y)
                    # Executing the SQL command
                    print("Pegando codigo do componente ", y,'...')

                except pyodbc.Error as err:
                    print("Something went wrong: {}".format(err))

                Codigo = crsr.fetchone()
                print("Codigo do componente ",y,":", Codigo)

                def convertTuple(tup):
                    str = functools.reduce(operator.add, (tup))
                    return str

                global strCodigo
                strCodigo = convertTuple(Codigo)            

                # PREGAR NOME COMPONENTE

                try:
                    crsr.execute('''
                SELECT Nome FROM Componente WHERE Componente.idComponente = ?
                ''',y)
                    # Executing the SQL command
                    print("Pegando nome do componente", y)

                except pyodbc.Error as err:
                    print("Something went wrong: {}".format(err))

                Nome= crsr.fetchone()
                global strNome
                strNome = convertTuple(Nome)
                print("Nome componente ",y,":", strNome)
                print(strNome + " = " + strCodigo)
                teste()



def VerificarDadosMaquina(idTorre):
                    
    try:
        crsr.execute('''
    SELECT SerialID FROM Torre WHERE idTorre = ?
    ''',idTorre)
        # Executando comando SQL
        print("Verificando dados da torre...")
        SerialIdBanco = crsr.fetchone()

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))
    
    if SerialIdBanco[0] != '':
        print("A torre possui dados cadastrados")
        print("Cadastrando leituras...")
        InserindoLeitura()
    else:
        print("A torre não possui dados")
        InserirDadosMaquina(strip_SerialIdAtual, strip3_OsAtual, strip3_MaquinaAtual, strip2_ProcessadorAtual, strip2_DiscoAtual, strip2_RamAtual)




def InserirDadosMaquina(SerialID, OS, Maquina, Processador, Disco, RamSpeed):
    
    try:
        crsr.execute('''
    UPDATE Torre  SET SerialID = ?,  SO = ?, Maquina = ?, Processador = ?, Disco = ?, Ram = ?,  fkEmpresa = ? WHERE idTorre = ?
    ''', SerialID, OS, Maquina, Processador, Disco, RamSpeed, int_fkEmpresa, idTorre)
    # Executando comando SQL
    # Commit de mudanças no banco de dados
        crsr.commit()
        print("Inserindo dados...")

    except pyodbc.Error as err:
        crsr.rollback()
        print("Something went wrong: {}".format(err))            

while True:
    Conexao1()
    ValidacaoLogin()
    time.sleep(5)