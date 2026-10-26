import requests
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from shapely.geometry import Polygon
import pyproj

# Configuração da Página
st.set_page_config(
    page_title="Vitória Veloso Arquitetura - Dimensionamento Solar", 
    layout="wide", 
    page_icon="☀️"
)

# Estilo CSS limpo e corrigido para exibir a barra lateral e os elementos visuais
st.markdown("""
    <style>
        @font-face {
            font-family: 'HeligoDemo';
            src: url('HeligoDemo-Bold-BF6adf19d58943d.otf') format('opentype');
            font-weight: bold;
            font-style: normal;
        }

        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

        /* Esconde o botão de fechar a barra lateral */
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Fundo Geral da Aplicação */
        .stApp {
            background-color: #FFC0CB !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #000000 !important;
        }
        
        /* Barra Lateral com Verde Sálvia e Scroll Liberado */
        [data-testid="stSidebar"] {
            background-color: #8EA860 !important;
            border-right: 3px solid #000000 !important;
            z-index: 100 !important;
        }

        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: #000000 !important;
            font-family: 'HeligoDemo', sans-serif !important;
            font-weight: bold !important;
        }
        
        /* Títulos Principais usando a fonte HeligoDemo */
        h1, h2, h3 {
            font-family: 'HeligoDemo', sans-serif !important;
            color: #000000 !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            letter-spacing: -1px !important;
        }
        
        /* Textos Gerais */
        p, span, .stMarkdown {
            color: #000000 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
        }

        /* Cartões de Métricas */
        .stMetric {
            background-color: #F7E9B7 !important;
            padding: 20px !important;
            border-radius: 16px !important;
            border: 2px solid #000000 !important;
            box-shadow: 4px 4px 0px #000000 !important;
        }
        
        /* Botões Arredondados em Preto */
        .stButton > button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 50px !important;
            padding: 0.85rem 2.5rem !important;
            font-size: 16px !important;
            font-weight: bold !important;
            font-family: 'HeligoDemo', sans-serif !important;
            border: 2px solid #000000 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            width: 100% !important;
        }
        .stButton > button:hover {
            background-color: #8EA860 !important;
            color: #000000 !important;
        }
        
        /* Caixas de Alerta e Sucesso */
        .stAlert {
            border-radius: 16px !important;
            border: 2px solid #000000 !important;
            background-color: #FFFFFF !important;
            color: #000000 !important;
            box-shadow: 4px 4px 0px #000000 !important;
        }

        /* Moldura do Mapa */
        iframe {
            border-radius: 16px !important;
            border: 2px solid #000000 !important;
            box-shadow: 4px 4px 0px #000000 !important;
            width: 100% !important;
            background-color: #F7E9B7 !important;
        }

        /* Botão do Instagram fixo no canto inferior esquerdo */
        .instagram-footer {
            position: fixed !important;
            bottom: 20px !important;
            left: 20px !important;
            background-color: #000000 !important;
            color: #FFFFFF !important;
            padding: 12px 22px !important;
            border-radius: 30px !important;
            font-family: 'HeligoDemo', sans-serif !important;
            font-size: 15px !important;
            font-weight: bold !important;
            z-index: 999999 !important;
            border: 2px solid #F7E9B7 !important;
            box-shadow: 4px 4px 0px #8EA860 !important;
            text-decoration: none !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 6px !important;
        }
        .instagram-footer:hover {
            background-color: #1C241E !important;
            color: #FFFFFF !important;
        }

        /* Flores Decorativas de Fundo com Animação */
        .flower-bg-top {
            position: fixed;
            top: -30px;
            right: -30px;
            width: 270px;
            z-index: 0;
            pointer-events: none;
            opacity: 0.9;
            animation: float1 6s ease-in-out infinite;
        }
        .flower-bg-bottom {
            position: fixed;
            bottom: -30px;
            right: -10px;
            width: 250px;
            z-index: 0;
            pointer-events: none;
            opacity: 0.9;
            animation: float2 8s ease-in-out infinite;
        }
        .flower-bg-left {
            position: fixed;
            bottom: 50px;
            left: -40px;
            width: 210px;
            z-index: 0;
            pointer-events: none;
            opacity: 0.85;
            animation: float1 7s ease-in-out infinite;
        }

        @keyframes float1 {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-12px) rotate(6deg); }
        }
        @keyframes float2 {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(12px) rotate(-6deg); }
        }
    </style>
    
    <!-- Link Direto Clicável para o Instagram -->
    <a href="https://www.instagram.com/vihve_" target="_blank" class="instagram-footer">
        📸 @vihve_
    </a>
    
    <!-- Flores Decorativas Animadas no Fundo -->
    <svg class="flower-bg-top" viewBox="0 0 100 100">
      <path d="M50 20 C60 10, 75 15, 80 30 C90 35, 95 50, 85 60 C90 75, 75 85, 60 80 C50 90, 35 85, 30 75 C15 80, 5 65, 15 55 C5 40, 15 25, 30 30 C35 15, 50 10, 50 20 Z" fill="#FFB7C5" stroke="#000000" stroke-width="2.5"/>
    </svg>

    <svg class="flower-bg-bottom" viewBox="0 0 100 100">
      <path d="M50 20 C60 10, 75 15, 80 30 C90 35, 95 50, 85 60 C90 75, 75 85, 60 80 C50 90, 35 85, 30 75 C15 80, 5 65, 15 55 C5 40, 15 25, 30 30 C35 15, 50 10, 50 20 Z" fill="#D8B4E2" stroke="#000000" stroke-width="2.5"/>
      <circle cx="50" cy="50" r="15" fill="#8EA860" stroke="#000000" stroke-width="2"/>
    </svg>

    <svg class="flower-bg-left" viewBox="0 0 100 100">
      <path d="M50 20 C60 10, 75 15, 80 30 C90 35, 95 50, 85 60 C90 75, 75 85, 60 80 C50 90, 35 85, 30 75 C15 80, 5 65, 15 55 C5 40, 15 25, 30 30 C35 15, 50 10, 50 20 Z" fill="#B4E2CE" stroke="#000000" stroke-width="2.5"/>
      <circle cx="50" cy="50" r="15" fill="#FFB7C5" stroke="#000000" stroke-width="2"/>
    </svg>
""", unsafe_allow_html=True)

# Cabeçalho da Marca
st.title("☀️ VITÓRIA VELOSO ARQUITETURA")
st.subheader("DIMENSIONAMENTO SOLAR FOTOVOLTAICO")
st.markdown("Ferramenta interativa de precisão integrando dados climáticos reais da **NASA POWER API** e análise espacial de cobertura de telhado.")

# Configurações na Barra Lateral
st.sidebar.header("⚙️ PARÂMETROS DO PROJETO")
num_pessoas = st.sidebar.number_input("Número de Pessoas", value=6, min_value=1)
consumo_por_pessoa = st.sidebar.number_input("Consumo por Pessoa (kWh/mês)", value=150.0, min_value=0.0)
consumo_total_mes = num_pessoas * consumo_por_pessoa

potencia_painel = st.sidebar.number_input("Potência do Painel (Wp)", value=550.0)
eficiencia_sistema = st.sidebar.number_input("Eficiência do Sistema (PR)", value=0.8, min_value=0.1, max_value=1.0, step=0.05)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Consumo Total Estimado:** `{consumo_total_mes:.1f} kWh/mês`")

# Interface do Mapa
st.subheader("1. LOCALIZAÇÃO E DELIMITAÇÃO DO TELHADO")
st.markdown("Navegue pelo mapa de satélite em HD, localize o projeto e utilize a ferramenta de **polígono ou retângulo** para delimitar a área do telhado.")

# Coordenadas iniciais (Maringá / PR)
lat_centro, lon_centro = -23.4205, -51.9333

# Mapa base com imagens de satélite em alta definição
m = folium.Map(location=[lat_centro, lon_centro], zoom_start=18, max_zoom=20)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri & — Source: Esri, Maxar, GeoEye, Earthstar Geographics, CNES/Airbus DS, USDA, USGS, AeroGRID, IGN, and the GIS User Community',
    name='Satélite (HD)',
    max_zoom=20,
    max_native_zoom=18,
    overlay=False,
    control=True
).add_to(m)

folium.TileLayer('openstreetmap', name='OpenStreetMap', control=True).add_to(m)

folium.TileLayer(
    tiles='https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    attr='Esri Boundaries and Places',
    name='Fronteiras e Cidades',
    overlay=True,
    control=True
).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

draw = Draw(
    export=False,
    draw_options={
        'polyline': False,
        'marker': True,
        'circle': False,
        'rectangle': True,
        'polygon': True,
        'circlemarker': False
    },
    edit_options={'edit': True}
)
draw.add_to(m)

output = st_folium(m, use_container_width=True, height=500)

area_telhado = 0.0

if output and output.get("last_active_drawing"):
    drawing = output["last_active_drawing"]
    geometry = drawing.get("geometry")
    
    if geometry and geometry.get("type") == "Polygon":
        coords = geometry["coordinates"][0] 
        poly_coords = [(c[0], c[1]) for c in coords]
        poly = Polygon(poly_coords)
        
        geom_area = pyproj.Geod(ellps='WGS84').geometry_area_perimeter(poly)
        area_telhado = abs(geom_area[0])
        
        centroid = poly.centroid
        lon_centro, lat_centro = centroid.x, centroid.y
        
        st.success(f"✅ Telhado mapeado com sucesso! Área útil estimada: {area_telhado:.2f} m² | Coordenadas: Lat {lat_centro:.4f}, Lon {lon_centro:.4f}")

if area_telhado == 0:
    st.warning("⚠️ Nenhum telhado desenhado no mapa acima. Desenhe o polígono no mapa ou defina a área manualmente abaixo:")
    area_telhado = st.number_input("Área do telhado manual (m²):", value=50.0, min_value=1.0)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 PROCESSAR DIMENSIONAMENTO ENERGÉTICO", type="primary"):
    with st.spinner("Consultando dados climáticos em tempo real da NASA POWER API..."):
        
        url = f"https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={lon_centro}&latitude={lat_centro}&start=2023&end=2023&format=JSON"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            monthly_data = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
            
            months_pt = {
                '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
                '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto',
                '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
            }
            
            df_solar = pd.DataFrame(list(monthly_data.items()), columns=['Mes_Ano', 'Irradiacao_Diaria'])
            df_solar['Mes'] = df_solar['Mes_Ano'].str[4:]
            df_solar = df_solar[df_solar['Mes'] != '13'] 
            df_solar['Nome_Mes'] = df_solar['Mes'].map(months_pt)
            df_solar['Dias'] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            df_solar['Irradiacao_Mensal'] = df_solar['Irradiacao_Diaria'] * df_solar['Dias']
            
            media_irradiacao_diaria = df_solar['Irradiacao_Diaria'].mean() 
            consumo_diario = consumo_total_mes / 30.0
            
            potencia_necessaria_kwp = consumo_diario / (media_irradiacao_diaria * eficiencia_sistema)
            
            potencia_painel_kw = potencia_painel / 1000.0
            num_paineis = int(round(potencia_necessaria_kwp / potencia_painel_kw))
            if num_paineis < 1: 
                num_paineis = 1
            
            area_por_painel = 2.4 
            area_necessaria_paineis = num_paineis * area_por_painel
            
            st.markdown("---")
            st.subheader("📊 RELATÓRIO DE DESEMPENHO E VIABILIDADE")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Consumo Mensal", f"{consumo_total_mes:.1f} kWh")
            col2.metric("Potência do Sistema", f"{potencia_necessaria_kwp:.2f} kWp")
            col3.metric("Painéis (550 Wp)", f"{num_paineis} unid.")
            col4.metric("Área Ocupada", f"{area_necessaria_paineis:.1f} m²")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if area_telhado >= area_necessaria_paineis:
                st.success(f"✅ **Projeto Viável:** O telhado selecionado ({area_telhado:.1f} m²) comporta confortavelmente os painéis necessários ({area_necessaria_paineis:.1f} m²).")
            else:
                st.error(f"❌ **Atenção:** O telhado possui {area_telhado:.1f} m², mas o arranjo fotovoltaico requer {area_necessaria_paineis:.1f} m².")

            st.markdown("---")
            st.subheader("📈 HISTÓRICO DE IRRADIAÇÃO SOLAR (JANEIRO A DEZEMBRO)")
            
            col_tabela, col_grafico = st.columns([1, 1])
            with col_tabela:
                st.dataframe(df_solar[['Nome_Mes', 'Irradiacao_Diaria', 'Irradiacao_Mensal']].rename(
                    columns={
                        'Nome_Mes': 'Mês', 
                        'Irradiacao_Diaria': 'Média Diária (kWh/m²/dia)', 
                        'Irradiacao_Mensal': 'Acumulado Mensal (kWh/m²/mês)'
                    }
                ), use_container_width=True, hide_index=True)
            
            with col_grafico:
                st.line_chart(df_solar.set_index('Nome_Mes')['Irradiacao_Diaria'])
            
        except Exception as e:
            st.error(f"Erro ao conectar com a API da NASA POWER: {e}")
