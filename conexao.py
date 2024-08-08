import mysql.connector

# Configuração do banco de dados
def conectar():
    config = {
        'user': 'root',
        'host': '127.0.0.1',
        'database': 'ovitrampas',
        'port': '3306',
        'raise_on_warnings': True,
    }

    try:
        conexao = mysql.connector.connect(**config)
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None

# Buscar localizações (latitude e longitude) da tabela "ovitrampas"
def buscar_localizacoes():
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT latitude, longitude FROM ovitrampas")
        localizacoes = cursor.fetchall()
        cursor.close()
        conexao.close()
        return localizacoes
    else:
        return None
    
# Buscar semanas disponíveis na tabela "relatorio"
def buscar_semanas():
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT semana FROM relatorio ORDER BY semana")
        semanas = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [semana[0] for semana in semanas]  # Retorna uma lista de semanas disponíveis
    else:
        return None

# Buscar quantidade de ovos por semana específica da tabela "relatorio"
def buscar_ovi(semana):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        query = "SELECT quant_ovos FROM relatorio WHERE semana = %s"
        cursor.execute(query, (semana,))
        ovos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [ovo[0] for ovo in ovos]  # Retorna uma lista com as quantidades de ovos
    else:
        return None
