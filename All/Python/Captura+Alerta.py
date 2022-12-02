from statistics import mean
import time
import psutil
import numpy
import datetime
import pyodbc
import textwrap
import mysql.connector
from mysql.connector import errorcode
from errno import errorcode
import subprocess
import requests

# Bloco pegar serial id
byte_SerialIdAtual = subprocess.check_output(
    '''sudo dmidecode -s system-serial-number''', shell=True)
str_SerialIdAtual = byte_SerialIdAtual.decode('UTF-8')
global strip_SerialIdAtual
strip_SerialIdAtual = str_SerialIdAtual.strip('\n')

# Bloco pegar sistema operacional
byte_OsAtual = subprocess.check_output('''lsb_release -d''', shell=True)
str_OsAtual = byte_OsAtual.decode('UTF-8')
strip_OsAtual = str_OsAtual.strip('Description:')
strip2_OsAtual = strip_OsAtual.strip('\t')
global strip3_OsAtual
strip3_OsAtual = strip2_OsAtual.strip('\n')

# Bloco pegar modelo maquina
byte_MaquinaAtual = subprocess.check_output(
    '''sudo dmidecode -t 1 | grep 'Product Name' | uniq''', shell=True)
str_MaquinaAtual = byte_MaquinaAtual.decode('UTF-8')
strip_MaquinaAtual = str_MaquinaAtual.strip('\tProduct')
strip2_MaquinaAtual = strip_MaquinaAtual.strip(' Name: ')
global strip3_MaquinaAtual
strip3_MaquinaAtual = strip2_MaquinaAtual.strip('\n')

# Bloco pegar processador
byte_ProcessadorAtual = subprocess.check_output(
    '''lscpu | grep 'Model name:' | uniq''', shell=True)
str_ProcessadorAtual = byte_ProcessadorAtual.decode('UTF-8')
strip_ProcessadorAtual = str_ProcessadorAtual.strip('Model name:')
global strip2_ProcessadorAtual
strip2_ProcessadorAtual = strip_ProcessadorAtual.strip('\n')

# Bloco pegar disco
byte_DiscoAtual = subprocess.check_output(
    '''sudo lshw -class disk -class storage | grep -B1 'vendor' | head -1''', shell=True)
str_DiscoAtual = byte_DiscoAtual.decode('UTF-8')
strip_DiscoAtual = str_DiscoAtual.strip('\tproduct: ')
global strip2_DiscoAtual
strip2_DiscoAtual = strip_DiscoAtual.strip('\n')

# Bloco pegar velocidade da ram
byte_RamAtual = subprocess.check_output(
    '''sudo dmidecode --type memory | grep -B1 'Type Detail: ' | head -1''', shell=True)
str_RamAtual = byte_RamAtual.decode('UTF-8')
strip_RamAtual = str_RamAtual.strip('\tType: ')
global strip2_RamAtual
strip2_RamAtual = strip_RamAtual.strip('\n')


global v_login
v_login = False


# receber o login do cliente
def Login(conectado):

    if conectado == 1 or conectado == 3:
        print("Bem vindo ao Grenn Light!")
        print("Login")
        u_email = input('Seu e-mail: ')
        u_senha = input('Sua senha: ')
        ValidarLogin(u_email, u_senha)
    elif conectado == 0:
        print("Sem conexão com a internet.")


# estabelecer conexao com Azure
def ConectarBancoAzure(nmr, login):

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
        global conectado
        conectado = nmr

    except pyodbc.Error as ex:
        print("Conexão com a Azure perdida")
        print(ex)
        conectado = 0

    if conectado == 0:
        ConectarBancoLocal(login)
    elif conectado == 3 and login == True:
        BuscarComponentes(idTorre)
    elif conectado == 3 and login == False:
        Login(conectado)


# Estabelecer conexao com banco de dados local no docker
def ConectarBancoLocal(login):

    if login:
        try:
            conn = mysql.connector.connect(
                host='172.17.0.2',
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
    else:
        print("Login ainda não efetuado")


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


# Validar login do cliente
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
        print(f'Bem vindo {u_usuario[0]}!')
        global fkEmpresa
        fkEmpresa = u_usuario[1]
        global v_login
        v_login = True
        BuscarTorres(fkEmpresa)
        

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))
        print("Falha ao realizar login por favor tente novamente")
        v_login = False


# Buscar as torres cadastradas na empresa do cliente
def BuscarTorres(fkEmpresa):

    try:
        crsr.execute('''
    SELECT idTorre FROM Torre WHERE fkEmpresa = ?
    ''', fkEmpresa)
        # Executando comando SQL)
        idTorres = crsr.fetchall()
        BuscarNomeEmp(fkEmpresa)
        BuscarMetricas(2,fkEmpresa)
        BuscarMetricas(5,fkEmpresa)
        BuscarMetricas(9,fkEmpresa)
        BuscarMetricas(12,fkEmpresa)
        EscolherTorres(idTorres)

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))


def BuscarNomeEmp(fkEmpresa):
    try:
        crsr.execute('''
    SELECT Nome FROM Empresa WHERE idEmpresa = ?
    ''', fkEmpresa)
        # Executando comando SQL)
        global nomeEmp
        nomeEmp = crsr.fetchone()

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))

m_cpu = []
m_ram = []
m_disco = []
m_net = []
# Buscar as metricas de cada componente
def BuscarMetricas(idComponente, idEmpresa):
    try:
        crsr.execute('''
        select Normall,Atencao,Critico from  luigi_Metricas where fkComponente = ? and fkEmpresa = ?
        ''',idComponente, idEmpresa)
        Metricas = crsr.fetchall()

        if idComponente == 2:
            for x in Metricas:
                m_cpu.append(x)
        elif idComponente == 5:
            for x in Metricas:
                m_ram.append(x)
        elif idComponente == 9:
            for x in Metricas:
                m_disco.append(x)                
        elif idComponente == 12:
            for x in Metricas:
                m_net.append(x)
        print(f'Metricas do componente {idComponente} recebidas do banco')

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))



# Mostrar as torres para o cliente e pedir para ele escolher qual é essa
def EscolherTorres(idTorres):
    for x in idTorres:
        print('Maquina:', x[0])
    global idTorre
    idTorre = input('Qual é esta maquina? ')
    VerificarDadosMaquina(idTorre)


# Validar se as maquinas possuen seus dados (serialID, SO, Nome, Velicidade da RAM, Marca do Disco) já cadastrados
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
        global v_login
        ConectarBancoAzure(3, v_login)
    else:
        print("A torre não possui dados")
        InserirDadosMaquina(strip_SerialIdAtual, strip3_OsAtual, strip3_MaquinaAtual,
                            strip2_ProcessadorAtual, strip2_DiscoAtual, strip2_RamAtual)


# Cadastrar os dados (serialID, SO, Nome, Velicidade da RAM, Marca do Disco) da maquina
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


# Buscar os componentes q devem ser monitorados desta torre
def BuscarComponentes(idTorre):

    # PEGAR fkCOMPONENTE
    try:
        print("Buscando os componentes da torre...")
        crsr.execute('''
        SELECT fkComponente FROM Torre_Componente WHERE Torre_Componente.fkTorre = ?
        ''', idTorre)
        fkComponente = crsr.fetchall()
        for x in fkComponente:
            idComponente = x[0]
            print("Componente:", idComponente)
            try:
                crsr.execute('''
                    SELECT Codigo, Nome FROM Componente WHERE Componente.idComponente = ?
                    ''', idComponente)
                # Executing the SQL command
                Codigo = crsr.fetchone()
                if idComponente > 12:
                    print(f'O componente {idComponente} é em outra API!')
                else:
                    InserirLeitura(Codigo[0], Codigo[1], idComponente, idTorre)
                

            except pyodbc.Error as err:
                print("Something went wrong: {}".format(err))

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))



# Inserir os dados da leitura de cada componente
def InserirLeitura(Codigo,Nome, idComponente, idTorre):
        datahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        exec(Nome + " = " + Codigo, globals())
        var_leitura = globals()[Nome]
        if Nome == 'processadores_nucleo_porcentagem':
            
            var_leitura2 = mean(var_leitura)
        elif Nome == 'pacotes_perdidos_porcentagem':
            print('caiu no elif 1')
            var_leitura2 = round((((pacotes_perdidos_porcentagem[1] - pacotes_perdidos_porcentagem[0])/pacotes_perdidos_porcentagem[1])*100), 1)
        elif Nome == 'processadores_nucleo_porcentagem':
            var_leitura2 = numpy.mean(var_leitura) 
        else:
            var_leitura2 = var_leitura

        
        try:
            # Executando comando SQL   
            crsr.execute('''
            INSERT INTO Leitura (Leitura, DataHora, fkTorre, fkComponente) VALUES (?, ?, ?, ?)
            ''',var_leitura2, datahora, idTorre , idComponente)
            # Commit de mudanças no banco de dados
            crsr.commit()
            

        except pyodbc.Error as err:
            crsr.rollback()
            print("Something went wrong: {}".format(err))
        print(f"Leitura componente {idComponente} inserida no banco as {datahora}")
        VerificarMetricas(var_leitura2, idComponente, idTorre)



#
def VerificarMetricas(Leitura,idComponente,idTorre):
    alertar = False
    frase = ''
    componente = ''
    if idComponente == 2:
        componente = 'CPU'
        if Leitura > int(m_cpu[0][0]) and Leitura < int(m_cpu[0][1]):
            frase = 'Alerta'
            alertar = True
        elif Leitura > int(m_cpu[0][1]) and Leitura < int(m_cpu[0][2]):
            frase = 'Perigo'
            alertar = True
        elif Leitura > int(m_cpu[0][2]):
            frase = 'Crítico'
            alertar = True
        else:
            print('Nenhum alerta emitido')
    if idComponente == 5:
        componente = 'RAM'
        if Leitura > int(m_ram[0][0]) and Leitura < int(m_ram[0][1]):
            frase = 'Alerta'
            alertar = True
        elif Leitura > int(m_ram[0][1]) and Leitura < int(m_ram[0][2]):
            frase = 'Perigo'
            componente = 'RAM'
            alertar = True
        elif Leitura > int(m_ram[0][2]):
            frase = 'Crítico'
            alertar = True
        else:
            print('Nenhum alerta emitido')
    if idComponente == 9:
        componente = 'Disco'
        if Leitura > int(m_disco[0][0]) and Leitura < int(m_disco[0][1]):
            frase = 'Alerta'
            alertar = True
        elif Leitura > int(m_disco[0][1]) and Leitura < int(m_disco[0][2]):
            frase = 'Perigo'
            alertar = True
        elif Leitura > int(m_disco[0][2]):
            frase = 'Crítico'
            alertar = True
        else:
            print('Nenhum alerta emitido')
    if idComponente == 12:
        componente = 'Pacotes'
        if Leitura > int(m_net[0][0]) and Leitura < int(m_net[0][1]):
            frase = 'Alerta'
            alertar = True
        elif Leitura > int(m_net[0][1]) and Leitura < int(m_net[0][2]):
            frase = 'Perigo'
            alertar = True
        elif Leitura > int(m_net[0][2]):
            frase = 'Crítico'
            alertar = True
        else:
            print('Nenhum alerta emitido')
    alertas(frase,componente,Leitura,idTorre,alertar)

def alertas(frase,componente,Leitura,idTorre,alertar):
    if alertar:
    #     url = "https://api.pipefy.com/graphql"

    #     payload = {"query": "{"mutation { createCard(input: { pipe_id:\"302621694\" fields_attributes:[ {field_id: "nome_da_empresa", field_value: "${nomeEmp}"},{field_id: "descri_o_do_alerta", field_value: "${componente}"},{field_id: "m_tricas", field_value: " ${frase}: ${metrica}"}]})}"}
    #     headers = {
    #         "Authorizarion": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjp7ImlkIjozMDIwOTE4NzAsImVtYWlsIjoicmVuYXRvLnRpZXJub0BzcHRlY2guc2Nob29sIiwiYXBwbGljYXRpb24iOjMwMDIwMDc5OX19.u1OD3vfD6im7FYV9owyD6kVPdstkeU3_1tX-WJdZz0Pf5VM8QZ2VEO6vEye9ht82VD7t2bnBqMwtuWywW0rjEg"
    #         "Content-Type": "application/json"
    #     }

    # response = requests.post(url, json=payload, headers=headers)

    # print(response.text)
    
        



# Conexão incial e estrutura de repeticão
ConectarBancoAzure(1, v_login)
Login(conectado)
while True:
    ConectarBancoAzure(3,v_login)
    time.sleep(2)
