import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static 
from conexao import buscar_localizacoes, buscar_ovi

# Cria o mapa de calor
def create_heatmap(locais, ovos):
    centro_mapa = [-16.7187, -43.8556]
    mapa = folium.Map(location=centro_mapa, zoom_start=12, min_zoom=12)

    if ovos:
        max_val = max(ovos)
        if max_val == 0:
            st.error("Erro: todos os valores na lista de ovos são zero.")
            return mapa  # Retorna o mapa sem heatmap
        
        ovos_normalized = [float(o) / max_val for o in ovos]

        data_heatmap = []
        for local, valor in zip(locais, ovos_normalized):
            data_heatmap.append((*local, valor))

        HeatMap(data_heatmap, radius=14).add_to(mapa)
    else:
        st.error("Erro: lista de ovos está vazia.")

    return mapa

# Dados do banco de dados
dados_localizacoes = buscar_localizacoes()
dados_ovi = buscar_ovi()

# Verifica se os dados foram carregados corretamente
if not dados_localizacoes or not dados_ovi:
    st.error("Erro ao carregar os dados do banco de dados.")
else:
    # Prepara as localizações para HeatMap
    locais = [[localizacao[0], localizacao[1]] for localizacao in dados_localizacoes]

    # Interface do Streamlit
    st.title('Mapa de Calor de Ovos por Semana')

    # Selecionar a semana
    semana_opcoes = ['Semana 3', 'Semana 5', 'Semana 7', 'Semana 9', 'Semana 11', 'Semana 15', 'Semana 17', 'Semana 19', 'Semana 21', 'Semana 23', 'Semana 25', 'Semana 27']
    semana = st.selectbox('Selecione a semana:', semana_opcoes)

    # Index da semana selecionada
    semana_index = semana_opcoes.index(semana)

    # Verifica os índices
    if len(dados_ovi[0]) <= semana_index:
        st.error(f"A semana {semana} não está presente nos dados.")
    else:
        # Prepara os dados da semana selecionada
        ovos = [ovo[semana_index] for ovo in dados_ovi]
        #st.write(f"Dados para a semana {semana}: {ovos}")  # Debug: Exibir os dados da semana selecionada

        # Verifica se a lista de ovos está vazia
        if not ovos:
            st.error(f"Não há dados de ovos para a {semana}.")
        # Verifica se todos os valores na lista de ovos são zero
        elif all(o == 0 for o in ovos):
            st.error(f"Todos os valores de ovos na {semana} são zero.")
        else:
            # Cria o mapa de calor
            mapa = create_heatmap(locais, ovos)

            # Exibi o mapa no Streamlit
            folium_static(mapa)
