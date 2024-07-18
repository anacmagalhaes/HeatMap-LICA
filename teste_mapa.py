import folium
from folium.plugins import HeatMap
import streamlit as st
from conexao import buscar_localizacoes, buscar_ovi

# Função para criar o mapa de calor
def create_heatmap(locais, ovos):
    centro_mapa = [-16.7187, -43.8556]
    mapa = folium.Map(location=centro_mapa, zoom_start=12)

    # Normalizar os dados entre 0 e 1 para usar o gradient
    if ovos:
        max_val = max(ovos)
        ovos_normalized = [float(o) / max_val for o in ovos]

        # Criar lista de tuplas para HeatMap com locais e ovos_normalized
        data_heatmap = []
        for local, valor in zip(locais, ovos_normalized):
            data_heatmap.append((*local, valor))

        HeatMap(locais, radius=14).add_to(mapa)  # Desativar gradient para evitar cores misturadas
        HeatMap(data_heatmap, radius=14).add_to(mapa)
    else:
        st.write("Erro: lista de ovos está vazia.")

    return mapa

# Obter dados do banco de dados
dados_localizacoes = buscar_localizacoes()
dados_ovi = buscar_ovi()

# Verificar se os dados foram carregados corretamente
if not dados_localizacoes or not dados_ovi:
    st.error("Erro ao carregar os dados do banco de dados.")
else:
    # Preparar localizações para HeatMap
    locais = [[localizacao[0], localizacao[1]] for localizacao in dados_localizacoes]

    # Interface do Streamlit
    st.title('Mapa de Calor de Ovos por Semana')

    # Selecionar a semana
    semana_opcoes = ['Semana 3', 'Semana 5', 'Semana 7', 'Semana 9', 'Semana 11', 'Semana 15', 'Semana 17', 'Semana 19', 'Semana 21', 'Semana 23', 'Semana 25', 'Semana 27']
    semana = st.selectbox('Selecione a semana', semana_opcoes)

    # Index da semana selecionada
    semana_index = semana_opcoes.index(semana)

    # Verificar se os índices estão corretos
    if len(dados_ovi[0]) <= semana_index:
        st.error(f"A semana {semana} não está presente nos dados.")
    else:
        # Preparar dados da semana selecionada
        ovos = [ovo[semana_index] for ovo in dados_ovi]

        # Criar o mapa de calor
        mapa = create_heatmap(locais, ovos)

        # Exibir o mapa no Streamlit
        st.components.v1.html(mapa._repr_html_(), width=700, height=500)
