import folium 
from folium.plugins import HeatMap
from conexao import buscar_localizacoes, buscar_ovi

# Obter dados do banco de dados
dados_localizacoes = buscar_localizacoes()
dados_ovi = buscar_ovi()

# Criar o mapa
centro_mapa = [-16.7187, -43.8556]
mapa = folium.Map(location=centro_mapa, zoom_start=12)

# Preparar localizações para HeatMap
locais = []
for localizacao in dados_localizacoes:
    latitude, longitude, *_ = localizacao
    locais.append([latitude, longitude])

# Preparar dados da coluna "semana_3" da tabela "semana" para HeatMap
ovos = []
for ovo in dados_ovi:
    semana_3 = ovo[-1]  # Supondo que semana_3 é o último elemento da tupla ovo
    ovos.append(semana_3)

# Normalizar os dados entre 0 e 1 para usar o gradient
if ovos:  
    max_val = max(ovos)
    ovos_normalized = [float(o) / max_val for o in ovos]

    # Criar lista de tuplas para HeatMap com locais e ovos_normalizados
    data_heatmap = []
    for local, valor in zip(locais, ovos_normalized):
        data_heatmap.append((*local, valor))


    HeatMap(locais, radius=14).add_to(mapa)  # Desativar gradient para evitar cores misturadas

    # Adicionar mapa de calor de dados da coluna "semana_3" com gradiente personalizado
    HeatMap(data_heatmap, radius=14).add_to(mapa)

    # Salvar mapa
    mapa.save('testemc.html')
else:
    print("Erro: lista de ovos está vazia.")
