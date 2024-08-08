import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
from conexao import buscar_localizacoes, buscar_ovi, buscar_semanas

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

# Interface do Streamlit
st.title('Mapa de Calor de Ovos por Semana')

# Dados do banco de dados
dados_localizacoes = buscar_localizacoes()
semanas_disponiveis = buscar_semanas()

# Verifica se as semanas foram carregadas corretamente
if not semanas_disponiveis:
    st.error("Erro ao carregar as semanas do banco de dados.")
else:
    # Selecionar a semana
    semana = st.selectbox('Selecione a semana:', semanas_disponiveis)

    # Busca os dados da semana selecionada
    dados_ovi = buscar_ovi(semana)

    # Verifica se os dados foram carregados corretamente
    if not dados_localizacoes or not dados_ovi:
        st.error("Erro ao carregar os dados do banco de dados.")
    else:
        # Prepara as localizações para HeatMap
        locais = [[localizacao[0], localizacao[1]] for localizacao in dados_localizacoes]

        # Verifica se a lista de ovos está vazia
        if not dados_ovi:
            st.error(f"Não há dados de ovos para a semana {semana}.")
        # Verifica se todos os valores na lista de ovos são zero
        elif all(o == 0 for o in dados_ovi):
            st.error(f"Todos os valores de ovos na semana {semana} são zero.")
        else:
            # Cria o mapa de calor
            mapa = create_heatmap(locais, dados_ovi)

            # Exibe o mapa no Streamlit
            folium_static(mapa)
