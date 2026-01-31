import streamlit as st
import feedparser
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="CNN Brasil - Monitor de Barragens",
    page_icon="🔴",
    layout="wide"
)

# CSS INSPIRADO NA CNN BRASIL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&display=swap' );
    
    * { font-family: 'Roboto', sans-serif; }

    /* Fundo do Portal */
    .stApp {
        background-color: #ffffff;
        color: #222222;
    }

    /* Header Estilo CNN */
    .cnn-header {
        background-color: #cc0000; /* Vermelho CNN */
        padding: 1.5rem;
        text-align: center;
        color: white;
        margin-bottom: 0;
        border-bottom: 5px solid #990000;
    }

    .cnn-header h1 {
        font-weight: 900;
        font-size: 2.8rem;
        letter-spacing: -1px;
        margin: 0;
        color: white !important;
    }

    .cnn-subheader {
        background-color: #222222;
        color: #ffffff;
        padding: 0.5rem;
        text-align: center;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* Barra de Pesquisa Estilizada */
    .stTextInput input {
        border: 2px solid #eeeeee !important;
        border-radius: 0px !important;
        padding: 12px !important;
        font-size: 1.1rem !important;
        text-align: center !important;
        color: #222222 !important;
    }

    /* Cards de Notícias Estilo Portal */
    .news-card {
        background: #ffffff;
        border-bottom: 3px solid #cc0000;
        padding: 2rem;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: background 0.3s;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .news-card:hover {
        background: #f9f9f9;
    }

    .news-tag {
        color: #cc0000;
        font-weight: 900;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: block;
    }

    .news-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #222222;
        line-height: 1.2;
        margin-bottom: 15px;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .news-source {
        font-size: 0.85rem;
        color: #666666;
        font-weight: 400;
    }

    /* Botão de Ação */
    .stButton>button {
        border-radius: 0px !important;
        background-color: #222222 !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #cc0000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Agente de Coleta
@st.cache_data(ttl=3600)
def coletar():
    noticias = []
    termos = ["Segurança de Barragens", "Barragens no Brasil"]
    for termo in termos:
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+' )}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for e in feed.entries[:12]:
            noticias.append({
                'titulo': e.title,
                'link': e.link,
                'fonte': e.source.title if hasattr(e, 'source') else 'CNN Brasil Feed',
                'termo': "SEGURANÇA" if "Segurança" in termo else "BRASIL"
            })
    return noticias

# --- INTERFACE ---

st.markdown('<div class="cnn-header"><h1>CNN BRASIL</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="cnn-subheader">Monitor de Segurança de Barragens | Agente de IA</div>', unsafe_allow_html=True)

noticias = coletar()

# Barra de Pesquisa
col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
with col_c2:
    busca = st.text_input("", placeholder="🔍 PESQUISAR NO PORTAL...")
    if st.button("ATUALIZAR NOTÍCIAS"):
        st.cache_data.clear()
        st.rerun()

st.markdown("  
", unsafe_allow_html=True)

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
                        <div class="news-title">{n['titulo']}</div>
                        <div class="news-source">Fonte: {n['fonte']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("LEIA MAIS", n['link'], use_container_width=True)
else:
    st.markdown("<h3 style='text-align: center;'>Nenhuma notícia encontrada.</h3>", unsafe_allow_html=True)

st.markdown("  
  
<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666666; font-size: 0.8rem; padding-bottom: 50px;'>© 2024 CNN Brasil - Monitoramento Autônomo via Agente de IA</div>", unsafe_allow_html=True)
