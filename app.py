import streamlit as st
import feedparser
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Monitor IA - Segurança de Barragens",
    page_icon="🏗️",
    layout="wide"
)

# CSS AVANÇADO: GLASSMORPHISM & CENTRALIZAÇÃO
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }

    /* Fundo com Gradiente Azul Escuro */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        background-attachment: fixed;
        color: white;
    }

    /* Banner Principal Glassmorphism */
    .main-banner {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 3.5rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }

    .main-banner h1 {
        font-weight: 900;
        font-size: 3.5rem;
        letter-spacing: -1px;
        color: #f8fafc !important;
        margin-bottom: 10px;
    }

    .main-banner p {
        font-size: 1.2rem;
        color: #94a3b8;
    }

    /* Cards de Notícias Centralizados */
    .news-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 20px;
    }

    .news-card:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.08);
        border-color: #3b82f6;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
    }

    .news-tag {
        background: #3b82f6;
        color: white;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 5px 15px;
        border-radius: 50px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    .news-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.3;
        margin-bottom: 15px;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .news-source {
        font-size: 0.9rem;
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 5px;
    }

    /* Customização da Barra de Pesquisa */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-size: 1.1rem !important;
        text-align: center !important;
    }

    /* Botões Estilizados */
    .stButton>button {
        border-radius: 15px !important;
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        padding: 10px 25px !important;
        font-weight: 700 !important;
        transition: 0.3s !important;
    }

    .stButton>button:hover {
        background: #2563eb !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Agente de Coleta
@st.cache_data(ttl=3600)
def coletar():
    noticias = []
    termos = ["Segurança de Barragens", "Barragens no Brasil"]
    for termo in termos:
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for e in feed.entries[:12]:
            noticias.append({
                'titulo': e.title,
                'link': e.link,
                'fonte': e.source.title if hasattr(e, 'source') else 'Portal de Notícias',
                'termo': "Segurança" if "Segurança" in termo else "Brasil"
            })
    return noticias

# --- INTERFACE ---

st.markdown('<div class="main-banner"><h1>🏗️ MONITOR DE BARRAGENS</h1><p>Agente de Inteligência Artificial • Monitoramento em Tempo Real</p></div>', unsafe_allow_html=True)

noticias = coletar()

# Barra de Pesquisa Centralizada
col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
with col_c2:
    busca = st.text_input("", placeholder="🔍 Digite aqui para pesquisar no portal...")
    if st.button("🔄 ATUALIZAR AGENTE AGORA", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("<br><br>", unsafe_allow_html=True)

# Filtragem
filtradas = [n for n in noticias if busca.lower() in n['titulo'].lower()]

# Grid de Notícias
if filtradas:
    for i in range(0, len(filtradas), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtradas):
                n = filtradas[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="news-card">
                        <span class="news-tag">{n['termo']}</span>
                        <div class="news-source">🏢 {n['fonte']}</div>
                        <div class="news-title">{n['titulo']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("🔗 ABRIR PREVISUALIZAÇÃO", n['link'], use_container_width=True)
else:
    st.markdown("<h3 style='text-align: center;'>Nenhuma notícia encontrada para sua busca.</h3>", unsafe_allow_html=True)

st.markdown("<br><br><hr style='opacity: 0.1;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #64748b; padding-bottom: 50px;'>Desenvolvido por Agente de IA Autônomo • 2024</div>", unsafe_allow_html=True)
