import streamlit as st
import feedparser
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Segurança de Barragens - Hub IA", page_icon="🏗️", layout="wide")

# 2. CSS: CARDS CLICÁVEIS COM ANIMAÇÃO E GLASSMORPHISM
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
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .main-banner h1 {
        font-weight: 900;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        color: #ffffff !important;
        margin: 0;
        text-transform: uppercase;
    }

    /* Estilização do Link Invisível que cobre o Card */
    .card-link {
        text-decoration: none;
        color: inherit;
        display: block;
    }

    .news-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
    }
    
    /* Animação de Hover */
    .news-card:hover {
        transform: translateY(-10px) scale(1.02);
        background: rgba(255, 255, 255, 0.08);
        border-color: #3b82f6;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
    }

    @media (min-width: 768px) {
        .news-card { height: 380px; }
    }

    .news-header-visual {
        width: 100%;
        height: 140px;
        background: linear-gradient(45deg, rgba(30, 58, 138, 0.8), rgba(59, 130, 246, 0.8));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
    }

    .news-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; text-align: center; }
    .news-tag { color: #3b82f6; font-weight: 800; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 10px; }
    .news-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; line-height: 1.4; margin-bottom: 15px; }
    .news-meta { color: #94a3b8; font-size: 0.8rem; margin-top: auto; }

    /* Esconder o botão padrão do Streamlit e usar o card como link */
    .stButton { display: none; }
    
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
        text-align: center !important;
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
    termos = ["Segurança de Barragens", "Resolução ANM Barragens", "Fiscalização de Barragens"]
    noticias = []
    icons = ["🏗️", "🌊", "📜", "📊", "🛡️"]
    
    for i, termo in enumerate(termos):
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for j, e in enumerate(feed.entries[:8]):
            dt = parse_date(e.published) if hasattr(e, 'published') else datetime.now()
            titulo = e.title.lower()
            
            if any(word in titulo for word in ["resolução", "norma", "portaria", "lei"]):
                cat = "📜 LEGISLAÇÃO"
            elif any(word in titulo for word in ["risco", "alerta", "emergência", "perigo"]):
                cat = "🚨 ALERTAS"
            else:
                cat = "🇧🇷 PANORAMA BRASIL"
                
            noticias.append({
                't': e.title, 'l': e.link, 'f': e.source.title if hasattr(e, 'source') else 'Portal',
                'dt_obj': dt, 'dt_s': dt.strftime('%d/%m/%Y'), 'hr_s': dt.strftime('%H:%M'),
                'cat': cat, 'icon': icons[(i + j) % len(icons)]
            })
    return sorted(noticias, key=lambda x: x['dt_obj'], reverse=True)

# --- INTERFACE ---
st.markdown('<div class="main-banner"><h1>SEGURANÇA DE BARRAGENS</h1><p style="color:#94a3b8; font-size:0.9rem;">Monitoramento Inteligente via Agente de IA</p></div>', unsafe_allow_html=True)

noticias = coletar()

col_c1, col_c2, col_c3 = st.columns([1, 4, 1])
with col_c2:
    busca = st.text_input("", placeholder="🔍 Pesquisar no Hub...")
    # Botão de atualização discreto
    if st.button("🔄 Sincronizar"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

tab_geral, tab_alertas, tab_normas = st.tabs(["🌐 Todas", "🚨 Alertas", "📜 Legislação"])

def render_grid(lista):
    if not lista:
        st.info("Nenhuma notícia encontrada.")
        return
    for i in range(0, len(lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(lista):
                n = lista[i + j]
                with cols[j]:
                    # Card Clicável usando HTML <a> envolvendo o conteúdo
                    st.markdown(f"""
                    <a href="{n['l']}" target="_blank" class="card-link">
                        <div class="news-card">
                            <div class="news-header-visual">{n['icon']}</div>
                            <div class="news-content">
                                <span class="news-tag">{n['cat']}</span>
                                <div class="news-title">{n['t']}</div>
                                <div class="news-meta">🕒 {n['dt_s']} | {n['hr_s']}</div>
                                <div style="font-size: 0.7rem; color: #64748b;">Fonte: {n['f']}</div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

filtradas = [n for n in noticias if busca.lower() in n['t'].lower()]

with tab_geral: render_grid(filtradas)
with tab_alertas: render_grid([n for n in filtradas if "ALERTAS" in n['cat']])
with tab_normas: render_grid([n for n in filtradas if "LEGISLAÇÃO" in n['cat']])

st.markdown("<br><br><div style='text-align: center; color: #64748b; font-size: 0.7rem; padding-bottom: 40px;'>© 2024 Segurança de Barragens - Monitoramento IA</div>", unsafe_allow_html=True)
