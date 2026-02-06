import streamlit as st
import feedparser
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Hub de Notícias - Segurança de Barragens", page_icon="🏗️", layout="wide")

# 2. CSS: DESIGN HUB GLASSMORPHISM
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        background-attachment: fixed;
        color: white;
    }

    .main-banner {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }

    .main-banner h1 {
        font-weight: 900;
        font-size: 2.5rem;
        color: #ffffff !important;
        margin: 0;
        text-transform: uppercase;
    }

    /* Estilização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px 10px 0 0 !important;
        color: #94a3b8 !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }

    .news-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        overflow: hidden;
        height: 420px;
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }
    .news-card:hover { transform: translateY(-5px); border-color: #3b82f6; }

    .news-header-gradient {
        width: 100%;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
    }

    .news-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; text-align: center; }
    .news-tag { color: #3b82f6; font-weight: 800; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 8px; }
    .news-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; line-height: 1.3; margin-bottom: 12px; min-height: 60px; }
    .news-meta { color: #94a3b8; font-size: 0.8rem; margin-top: auto; }

    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
        text-align: center !important;
    }

    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #94a3b8 !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        padding: 5px 25px !important;
    }
</style>
""", unsafe_allow_html=True)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str[:-4], '%a, %d %b %Y %H:%M:%S')
    except:
        return datetime.now()

@st.cache_data(ttl=300)
def coletar():
    termos = ["Segurança de Barragens", "Barragens no Brasil", "Fiscalização de Barragens"]
    noticias = []
    gradients = ["linear-gradient(45deg, #1e3a8a, #3b82f6)", "linear-gradient(45deg, #0f172a, #1e40af)", "linear-gradient(45deg, #1e40af, #60a5fa)"]
    icons = ["🏗️", "🌊", "📊"]
    
    for i, termo in enumerate(termos):
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for j, e in enumerate(feed.entries[:10]):
            dt = parse_date(e.published) if hasattr(e, 'published') else datetime.now()
            titulo = e.title.lower()
            
            # Lógica de Categorização
            if any(word in titulo for word in ["risco", "alerta", "emergência", "urgente", "perigo"]):
                cat = "🚨 ALERTAS"
            elif any(word in titulo for word in ["fiscalização", "anm", "vistoria", "lei", "obras"]):
                cat = "🏗️ FISCALIZAÇÃO"
            else:
                cat = "🇧🇷 PANORAMA BRASIL"
                
            idx = (i + j) % 3
            noticias.append({
                't': e.title, 'l': e.link, 'f': e.source.title if hasattr(e, 'source') else 'Portal',
                'dt_obj': dt, 'dt_s': dt.strftime('%d/%m/%Y'), 'hr_s': dt.strftime('%H:%M'),
                'cat': cat, 'grad': gradients[idx], 'icon': icons[idx]
            })
    return sorted(noticias, key=lambda x: x['dt_obj'], reverse=True)

# --- INTERFACE ---
st.markdown('<div class="main-banner"><h1>HUB DE NOTÍCIAS</h1><p style="color:#94a3b8; margin-top:10px;">Segurança de Barragens | Monitoramento Inteligente</p></div>', unsafe_allow_html=True)

noticias = coletar()

col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
with col_c2:
    busca = st.text_input("", placeholder="🔍 Pesquisar no Hub...")
    if st.button("🔄 Sincronizar Agente"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Organização por Abas (Categorias)
tab_geral, tab_alertas, tab_fiscal = st.tabs(["🌐 Todas as Notícias", "🚨 Alertas e Riscos", "🏗️ Fiscalização e Obras"])

def render_grid(lista_noticias):
    if not lista_noticias:
        st.info("Nenhuma notícia encontrada nesta categoria.")
        return
    for i in range(0, len(lista_noticias), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(lista_noticias):
                n = lista_noticias[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="news-card">
                        <div class="news-header-gradient" style="background: {n['grad']};">{n['icon']}</div>
                        <div class="news-content">
                            <span class="news-tag">{n['cat']}</span>
                            <div class="news-title">{n['t']}</div>
                            <div class="news-meta">🕒 {n['dt_s']} | {n['hr_s']}</div>
                            <div style="font-size: 0.7rem; color: #64748b; margin-top: 5px;">Fonte: {n['f']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("ABRIR NO HUB", n['l'], use_container_width=True)

# Filtragem por busca
noticias_filtradas = [n for n in noticias if busca.lower() in n['t'].lower()]

with tab_geral:
    render_grid(noticias_filtradas)

with tab_alertas:
    alertas = [n for n in noticias_filtradas if "ALERTAS" in n['cat']]
    render_grid(alertas)

with tab_fiscal:
    fiscal = [n for n in noticias_filtradas if "FISCALIZAÇÃO" in n['cat']]
    render_grid(fiscal)

st.markdown("<br><br><div style='text-align: center; color: #64748b; font-size: 0.8rem; padding-bottom: 50px;'>© 2024 Hub de Notícias - Segurança de Barragens</div>", unsafe_allow_html=True)
