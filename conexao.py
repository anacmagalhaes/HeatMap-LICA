import mysql.connector

def conectar():
    config = {
        'user': 'root',
        'host': '127.0.0.1',
        'database': 'teste_ovi',
        'port': '3306',
        'raise_on_warnings': True,
    }

    try:
        conexao = mysql.connector.connect(**config)
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None

def buscar_localizacoes():
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT latitude, longitude FROM endereco")
        localizacoes = cursor.fetchall()
        cursor.close()
        conexao.close()
        return localizacoes
    else:
        return None
    
def buscar_ovi(semana=None):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        if semana:
            cursor.execute(f"SELECT semana_3, semana_5, semana_7, semana_9, semana_11, semana_15, semana_17, semana_19, semana_21, semana_25, semana_27 FROM semanas")
        else:
            cursor.execute("SELECT semana_3, semana_5, semana_7, semana_9, semana_11, semana_15, semana_17, semana_19, semana_21, semana_25, semana_27 FROM semanas")
        ovos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return ovos
    else:
        return None
