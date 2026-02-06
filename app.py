import streamlit as st
import feedparser
from datetime import datetime
import re

# 1. Configuração da Página
st.set_page_config(page_title="Segurança de Barragens - Hub IA", page_icon="🏗️", layout="wide")

# 2. CSS: DESIGN GLASSMORPHISM RESPONSIVO
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

    .card-link { text-decoration: none; color: inherit; display: block; }

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
    }
    
    .news-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.08);
        border-color: #3b82f6;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
    }

    @media (min-width: 768px) { .news-card { height: 440px; } }

    .news-image {
        width: 100%;
        height: 180px;
        object-fit: cover;
        background: #1e293b;
    }

    .news-content { padding: 15px; flex-grow: 1; display: flex; flex-direction: column; text-align: center; }
    .news-tag { color: #3b82f6; font-weight: 800; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 8px; }
    .news-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; line-height: 1.3; margin-bottom: 12px; }
    .news-meta { color: #94a3b8; font-size: 0.8rem; margin-top: auto; padding-bottom: 10px; }

    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
        text-align: center !important;
    }

    .stButton>button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #94a3b8 !important;
        border-radius: 20px !important;
        width: 100% !important;
        max-width: 200px;
        margin: 0 auto;
        display: block;
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
    # Imagens de backup caso o Google não forneça
    backup_imgs = [
        "https://images.unsplash.com/photo-1584463651400-90363984306d?w=600&q=80",
        "https://images.unsplash.com/photo-1590098573390-340888d2983b?w=600&q=80",
        "https://images.unsplash.com/photo-1473163928189-3f4b2c713e1c?w=600&q=80"
    ]
    
    for i, termo in enumerate(termos):
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for j, e in enumerate(feed.entries[:10]):
            dt = parse_date(e.published) if hasattr(e, 'published') else datetime.now()
            titulo = e.title.lower()
            
            # Extração de Imagem do Feed (Google News Thumbnail)
            img_url = backup_imgs[(i + j) % 3]
            if hasattr(e, 'summary'):
                match = re.search(r'src="([^"]+)"', e.summary)
                if match:
                    img_url = match.group(1)
            
            if any(word in titulo for word in ["resolução", "norma", "portaria", "lei"]):
                cat = "📜 LEGISLAÇÃO"
            elif any(word in titulo for word in ["risco", "alerta", "emergência", "perigo"]):
                cat = "🚨 ALERTAS"
            else:
                cat = "🇧🇷 PANORAMA BRASIL"
                
            noticias.append({
                't': e.title, 'l': e.link, 'f': e.source.title if hasattr(e, 'source') else 'Portal',
                'dt_obj': dt, 'dt_s': dt.strftime('%d/%m/%Y'), 'hr_s': dt.strftime('%H:%M'),
                'cat': cat, 'img': img_url
            })
    return sorted(noticias, key=lambda x: x['dt_obj'], reverse=True)

# --- INTERFACE ---
st.markdown('<div class="main-banner"><h1>SEGURANÇA DE BARRAGENS</h1><p style="color:#94a3b8; font-size:0.9rem;">Monitoramento Inteligente via Agente de IA</p></div>', unsafe_allow_html=True)

noticias = coletar()

col_c1, col_c2, col_c3 = st.columns([1, 4, 1])
with col_c2:
    busca = st.text_input("", placeholder="🔍 Pesquisar no Hub...")
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
                    st.markdown(f"""
                    <a href="{n['l']}" target="_blank" class="card-link">
                        <div class="news-card">
                            <img src="{n['img']}" class="news-image">
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
