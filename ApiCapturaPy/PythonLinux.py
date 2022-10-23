import os
import subprocess
import datetime

# Bloco verificar bibliotecas instaladas
verificacao_psutil_byte = subprocess.check_output('''pip list | grep 'psutil' | uniq''', shell=True)
verificacao_psutil_str = verificacao_psutil_byte.decode('UTF-8')
verificacao_pyodbc_byte = subprocess.check_output('''pip list | grep 'pyodbc' | uniq''', shell=True)
verificacao_pyodbc_str = verificacao_pyodbc_byte.decode('UTF-8')
verificacao_numpy_byte = subprocess.check_output('''pip list | grep 'numpy' | uniq''', shell=True)
verificacao_numpy_str = verificacao_numpy_byte.decode('UTF-8')
verificacao_textwrap3_byte = subprocess.check_output('''pip list | grep 'textwrap3' | uniq''', shell=True)
verificacao_textwrap3_str = verificacao_textwrap3_byte.decode('UTF-8')


verificacao_psutil = False
verificacao_pyodbc = False
verificacao_numpy = False
verificacao_textwrap3 = False



# Bloco setar  Boolean da bibliotecas
if (verificacao_psutil_str == ''):
    verificacao_psutil = True
if (verificacao_pyodbc_str == ''):
    verificacao_pyodbc = True
if (verificacao_numpy_str == ''):
    verificacao_numpy = True
if (verificacao_textwrap3_str == ''):
    verificacao_textwrap3 = True


def Bibliotecas(psutil, pyodbc, numpy, textwrap3):
        if psutil:
             subprocess.run('pip install psutil', shell=True)
        if pyodbc:
            subprocess.run('pip install pyodbc', shell=True)
        if numpy:
            subprocess.run('pip install numpy', shell=True)
        if textwrap3:
            subprocess.run('pip install -U textwrap3', shell=True)
        

Bibliotecas(verificacao_psutil, verificacao_pyodbc, verificacao_numpy, verificacao_textwrap3)
