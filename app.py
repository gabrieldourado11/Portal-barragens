import streamlit as st
import feedparser
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Monitor de Segurança de Barragens IA",
    page_icon="🏗️",
    layout="wide"
)

# CSS para estilização
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap' );
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    .main-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .news-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .news-tag {
        background: #dbeafe;
        color: #1e40af;
        font-size: 0.7rem;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 10px;
    }
    .news-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Agente de Coleta
@st.cache_data(ttl=3600)
def coletar():
    noticias = []
    for termo in ["Segurança de Barragens", "Barragens no Brasil"]:
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+' )}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for e in feed.entries[:9]:
            noticias.append({
                'titulo': e.title,
                'link': e.link,
                'fonte': e.source.title if hasattr(e, 'source') else 'News',
                'termo': termo
            })
    return noticias

# Interface
st.markdown('<div class="main-banner"><h1>🏗️ Monitor de Segurança de Barragens</h1><p>Agente de IA para Monitoramento Autônomo</p></div>', unsafe_allow_html=True)

noticias = coletar()

# Busca e Filtro
col1, col2 = st.columns([3, 1])
with col1:
    busca = st.text_input("🔍 Pesquisar notícias...", placeholder="Digite aqui...")
with col2:
    if st.button("🔄 Atualizar"):
        st.cache_data.clear()
        st.rerun()

# Filtragem
filtradas = [n for n in noticias if busca.lower() in n['titulo'].lower()]

# Exibição em Grid
if filtradas:
    for i in range(0, len(filtradas), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtradas):
                n = filtradas[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="news-card">
                        <div>
                            <span class="news-tag">{n['termo']}</span>
                            <div class="news-title">{n['titulo'][:85]}...</div>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b;">🏢 {n['fonte']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("Ler Notícia", n['link'], use_container_width=True)
else:
    st.info("Nenhuma notícia encontrada.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #94a3b8;'>Portal Gerado por Agente de IA • 2024</div>", unsafe_allow_html=True)
