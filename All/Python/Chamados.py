from statistics import mean
import subprocess
import time
import psutil
import numpy
import datetime
import functools
import operator
import pyodbc 
import textwrap

def Conexao():

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
        print("Conectado ao banco de dados: MoniToll")

def teste():

        #datahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        try:
        # Executando comando SQL 
            crsr.execute('''
    SELECT componente ,COUNT(componente) AS Quantidade FROM [dbo].[AlertaRenato] WHERE fkTorre = 167 GROUP BY componente
                ''')
                
       
        # Commit de mudanças no banco de dados
            result = crsr.fetchall()

               
            comp = result[0][0]
            print(comp)
            comp2 = result[1][0]
            print(comp2)
            comp3 = result[2][0]
            print(comp3)
            comp4 = result[3][0]
            print(comp4)
            comp5 = result[4][0]
            print(comp5)
            comp6 = result[5][0]
            print(comp6)

            count = result[0][1]
            count2 = result[1][1]
            count3 = result[2][1]
            count4 = result[3][1]
            count5 = result [4][1]
            count6 = result[5][1]

            
            crsr.execute('''
        INSERT INTO [dbo].[Chamado_Comp] (componente, qntCHC) VALUES (?,?)
        ''', comp, count)
            crsr.execute('''
        INSERT INTO [dbo].[Chamado_Comp] (componente, qntCHC) VALUES (?,?)
        ''', comp2, count2)
            crsr.execute('''
        INSERT INTO [dbo].[Chamado_Comp] (componente, qntCHC) VALUES (?,?)
        ''', comp3, count3)
            crsr.execute('''
        INSERT INTO [dbo].[Chamado_Comp] (componente, qntCHC) VALUES (?,?)
        ''', comp4, count4)
            crsr.execute('''
        INSERT INTO [dbo].[Chamado_Comp] (componente, qntCHC) VALUES (?,?)
        ''', comp5, count5)
            crsr.execute('''
        INSERT INTO [dbo].[Chamado_Comp] (componente, qntCHC) VALUES (?,?)
        ''', comp6, count6)
            crsr.commit()


        except pyodbc.Error as err:
            crsr.roolback()
            print("Something went wrong: {}".format(err))
            
Conexao()
while True:
    teste()
    time.sleep(5)


