import datetime
from datetime import date
from distutils.command.config import config
from pyodbc import Error
from this import d
import requests
import json
import urllib.parse
from urllib.parse import quote
import textwrap
import pyodbc
import time
import numpy

accuweatherAPIKey = "yEXfpNKSOMfMVf69A3msVe4g9XGUAmAq"
mapboxToken = "pk.eyJ1IjoiYXJvbm5pIiwiYSI6ImNsYTczOGZxejBqbnczdmxkNjNuN3Q1bTIifQ.0tBJGc81IZLQopZnQ--cPg"
# my_date = datetime.today() # if date is 01/01/2018
# year, week_num, day_of_week = my_date.isocalendar()
# print("Week #" + str(week_num) + " of year " + str(year))
listOfDays = []
base = datetime.datetime.today()
for x in range(0, 5):
    nextDay = base + datetime.timedelta(days=x)
    listOfDays.append(f"{nextDay.year}/{nextDay.month}/{nextDay.day}")

print(listOfDays[1])


dias_semana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

def pegarCoordenadas():
    r = requests.get('http://www.geoplugin.net/json.gp')
    #verificação de localização, baseado na numeração de erro 200
    if(r.status_code != 200):
        print('Não foi possivel obter a localização.')
        return None
    else:
        try:
            #print(r.text) - dados da requisição http
            localizacao = json.loads(r.text)
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long'] = localizacao['geoplugin_longitude']
            print('coordenadas ok')
            return coordenadas
        except:
            return None 
           
            

def pegarCodigoLocal(lat,long):
    LocationAPIUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=" + accuweatherAPIKey + "&q=" + lat + "%2C" + long + "&language=pt-br"

    r = requests.get(LocationAPIUrl)
    if(r.status_code == 401):
        print('Não autorizado.')
    elif(r.status_code != 200):
        print('Não foi possível obter a localização.')
        return None
    else:
        try:
            locationResponse = json.loads(r.text)
            infoLocal = {}
            infoLocal['nomeLocal'] = locationResponse['LocalizedName'] + "," + locationResponse['AdministrativeArea']['LocalizedName'] + "." + locationResponse['Country']['LocalizedName']
            infoLocal['codigoLocal'] = locationResponse['Key']
            return infoLocal
        except:
            return None

def pegarTempoAgora(codigoLocal, nomeLocal):
    CurrentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" + codigoLocal + "?apikey=" + accuweatherAPIKey + "&language=pt-br"

    r = requests.get(CurrentConditionsAPIUrl)
    if(r.status_code != 200):
        print('Não foi possivel obter o clima atual')
        return None
    else:
        try:
            CurrentConditionsResponse = json.loads(r.text)
            global infoClima
            infoClima = {}
            infoClima['textoClima'] = CurrentConditionsResponse[0]['WeatherText']
            infoClima['temperatura'] = CurrentConditionsResponse[0]['Temperature']['Metric']['Value'] 
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None

def pegarPrevisao5Dias(codigoLocal):
    DailyAPIUrl = " http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + codigoLocal + "?apikey=" + accuweatherAPIKey + "&language=pt-br&metric=true"

    r = requests.get(DailyAPIUrl)
    if(r.status_code != 200):
        print('Não foi possivel obter o clima atual.')
        return None
    else:
        try:
            DailyResponse = json.loads(r.text)
            global climaDia
            infoClima5Dias = []
            for i, dia in enumerate(DailyResponse['DailyForecasts']):
                climaDia = {}
                climaDia['max']=dia['Temperature']['Maximum']['Value']
                climaDia['min']=dia['Temperature']['Maximum']['Value']
                climaDia['clima']=dia['Day']['IconPhrase']
                diaSemana = int(date.fromtimestamp(dia['EpochDate']).strftime("%w"))
                climaDia['diaSemana']=dias_semana[diaSemana]
                climaDia['diaMes']= listOfDays[i]
                infoClima5Dias.append(climaDia)
            return infoClima5Dias
        except:
            return None

    ##Inicio do cod
##Conexão com o banco
def Login(conectado):

    if conectado == 1 or conectado == 3:
        print("Bem vindo ao Grenn Light!")
        print("Login")
        u_email = input('Seu e-mail: ')
        u_senha = input('Sua senha: ')
        ValidarLogin(u_email, u_senha)
    elif conectado == 0:
        print("Sem conexão com a internet.")

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




def pesquisarLocal(local):
    _local = urllib.parse.quote(local)
    mapboxGeocodeUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + _local +".json?access_token=" + mapboxToken
    r = requests.get(mapboxGeocodeUrl)
    if(r.status_code != 200):
        print('Não foi possivel obter o clima atual.')
        return None
    else:
        try:
            MapboxResponse = json.loads(r.text)
            coordenadas = {}
            coordenadas['lat'] = str(MapboxResponse['features'][0]['geometry']['coordinates'][1])
            coordenadas['long'] = str(MapboxResponse['features'][0]['geometry']['coordinates'][0])
            return coordenadas
        except:
            print('Erro na pesquisa de local.')

global v_login
v_login = False


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
        EscolherTorres(idTorres)

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))

def BuscarNomeEmp(fkEmpresa):
    try:
        crsr.execute('''
    SELECT Nome FROM Empresa WHERE idEmpresa = ?
    ''', fkEmpresa)
        # Executando comando SQL)
        nomeEmpFetch = crsr.fetchone()
        global nomeEmp
        nomeEmp = nomeEmpFetch[0]

    except pyodbc.Error as err:
        print("Something went wrong: {}".format(err))

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


def EscolherTorre():
    try:
            crsr.execute('''
            SELECT idTorre, localização FROM torre where idTorre = ?
            ''', idTorre)
            global resultado
            resultado = crsr.fetchall()
            print(resultado)
    except pyodbc.Error as err:
                    print(err)
                    print('erro no envio')

def tempLocal():
    try:
        for data in resultado:
            print("Cidade: ", data[1])
            coord = pesquisarLocal(data[1])
            print(coord)
            print(pegarCodigoLocal(coord['lat'],coord['long']))
            local = pegarCodigoLocal(coord['lat'],coord['long'])
            climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
            print(climaAtual)
            try:
                tc = infoClima['textoClima']
                temp = infoClima['temperatura']
                dt = data[0]
                crsr.execute('''
                INSERT INTO TempLocal(textoClima,temperatura,fkTorre) VALUES(?,?,?)
                ''',tc,temp,dt)
                crsr.commit()
                print('Dados enviados')
            except pyodbc.Error as err:
                print(err)
                print('erro no envio')
    except pyodbc.Error as err:
                print(err)
                print('erro no envio')

def tempSemana():
    try:
        for id in resultado:
            coord = pesquisarLocal(id[1])
            local = pegarCodigoLocal(coord['lat'],coord['long'])
            semana = pegarPrevisao5Dias(local['codigoLocal'])
            print(id)
            try:
                for i, data in enumerate(semana):
                    print(i, data)
                    dm = data['diaMes']
                    ds = data['diaSemana']
                    max = data['max']
                    min = data['min']
                    c = data['clima']
                    crsr.execute('''
                    INSERT INTO TempSemana(diaMes, diaSemana, climaMax, climaMin, climaTexto, fkTorre) VALUES(?,?,?,?,?,?)
                    ''',dm,ds,max,min,c,idTorre)
                    crsr.commit()
            except pyodbc.Error as err:
                print(err)
                print('erro no envio')
    except pyodbc.Error as err:
                print(err)
                print('erro no envio')

ConectarBancoAzure(1, v_login)
Login(conectado)
while(True):
    ConectarBancoAzure(3,v_login)
    EscolherTorre()
    tempLocal()
    time.sleep(10)
    tempSemana()