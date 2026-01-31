import streamlit as st
import feedparser
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Monitor de Segurança de Barragens IA",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS AVANÇADO PARA PERSONALIZAÇÃO TOTAL
st.markdown("""
<style>
    /* Importando fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap' );
    
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo da página */
    .stApp {
        background-color: #f4f7f9;
    }

    /* Banner Principal */
    .main-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.2);
    }

    .main-banner h1 {
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: white !important;
    }

    /* Cards de Notícias */
    .news-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 250px;
    }

    .news-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.08);
        border-color: #3b82f6;
    }

    .news-tag {
        background: #dbeafe;
        color: #1e40af;
        font-size: 0.7rem;
        font-weight: bold;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        display: inline-block;
    }

    .news-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.4;
        margin-bottom: 1rem;
    }

    .news-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.8rem;
        color: #64748b;
        border-top: 1px solid #f1f5f9;
        padding-top: 0.8rem;
    }

    /* Sidebar Estilizada */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    .stat-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }

    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background-color: #3b82f6;
        color: white;
        border: none;
        transition: all 0.2s;
    }

    .stButton>button:hover {
        background-color: #1e40af;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Função do Agente de Coleta
@st.cache_data(ttl=3600)
def coletar_noticias():
    termos = ["Segurança de Barragens", "Barragens no Brasil"]
    noticias = []
    for termo in termos:
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+' )}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for entry in feed.entries[:12]: 
            noticias.append({
                'titulo': entry.title,
                'link': entry.link,
                'data': entry.published if hasattr(entry, 'published') else 'Recente',
                'fonte': entry.source.title if hasattr(entry, 'source') else 'Google News',
                'termo': termo
            })
    
    vistos = set()
    unicas = []
    for n in noticias:
        if n['titulo'] not in vistos:
            unicas.append(n)
            vistos.add(n['titulo'])
    return unicas

# --- INTERFACE ---

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920277.png", width=80 )
    st.title("Painel de Controle")
    
    if st.button("🔄 Sincronizar Agente"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Status do Agente")
    noticias = coletar_noticias()
    
    st.markdown(f"""
    <div class="stat-card">
        <small>Notícias Coletadas</small>  

        <strong>{len(noticias)} itens encontrados</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Configurações")
    st.info("O Agente de IA verifica novas fontes a cada 60 minutos automaticamente.")

# Área Principal
st.markdown("""
<div class="main-banner">
    <h1>🏗️ Monitor de Segurança de Barragens</h1>
    <p>Agente de Inteligência Artificial para Monitoramento Autônomo de Notícias</p>
</div>
""", unsafe_allow_html=True)

# Filtros em linha
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    busca = st.text_input("🔍 Pesquisar no portal...", placeholder="Ex: Brumadinho, Fiscalização...")
with col_f2:
    filtro_termo = st.selectbox("Filtrar por Categoria", ["Todas", "Segurança", "Brasil"])

st.markdown("  
", unsafe_allow_html=True)

# Filtragem lógica
noticias_filtradas = [n for n in noticias if busca.lower() in n['titulo'].lower()]
if filtro_termo != "Todas":
    noticias_filtradas = [n for n in noticias_filtradas if (filtro_termo in n['termo'])]

# Grid de Notícias (3 colunas)
if not noticias_filtradas:
    st.warning("Nenhuma notícia encontrada para os filtros selecionados.")
else:
    for i in range(0, len(noticias_filtradas), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(noticias_filtradas):
                n = noticias_filtradas[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="news-card">
                        <div>
                            <span class="news-tag">{n['termo']}</span>
                            <div class="news-title">{n['titulo'][:80]}...</div>
                        </div>
                        <div class="news-footer">
                            <span>🏢 {n['fonte']}</span>
                            <span>📅 {n['data'][:16]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("Ver Notícia Completa", n['link'], use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.8rem; padding: 1rem;'>
    Portal Gerado Autonomamente por Agente de IA • 2024  

    Tecnologias: Python, Streamlit, Feedparser
</div>
""", unsafe_allow_html=True)
