import streamlit as st
import feedparser
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Segurança de Barragens - Monitor IA", page_icon="🏗️", layout="wide")

# CSS: DESIGN AZUL ESCURO COM BLUR (GLASSMORPHISM)
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
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }

    .main-banner h1 {
        font-weight: 900;
        font-size: 3rem;
        color: #ffffff !important;
        margin: 0;
        text-transform: uppercase;
    }

    .news-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        overflow: hidden;
        height: 460px;
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }
    .news-card:hover { transform: translateY(-5px); border-color: #3b82f6; }

    .news-image { width: 100%; height: 200px; object-fit: cover; background: #1e293b; }

    .news-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; text-align: center; }

    .news-tag { color: #3b82f6; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 10px; }

    .news-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; line-height: 1.3; margin-bottom: 15px; min-height: 60px; }

    .news-meta { color: #94a3b8; font-size: 0.85rem; margin-top: auto; }

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
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        width: auto !important;
        padding: 5px 25px !important;
        margin: 0 auto !important;
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
    termos = ["Segurança de Barragens", "Barragens no Brasil"]
    noticias = []
    # Usando imagens do Unsplash Source que são mais estáveis para hotlinking
    imgs = [
        "https://images.unsplash.com/photo-1574790332569-48380c10952c?w=500&q=80",
        "https://images.unsplash.com/photo-1585914966076-9600193696ad?w=500&q=80",
        "https://images.unsplash.com/photo-1473163928189-3f4b2c713e1c?w=500&q=80"
    ]
    for i, termo in enumerate(termos):
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for j, e in enumerate(feed.entries[:12]):
            dt = parse_date(e.published) if hasattr(e, 'published') else datetime.now()
            noticias.append({
                't': e.title, 'l': e.link, 'f': e.source.title if hasattr(e, 'source') else 'Portal',
                'dt_obj': dt, 'dt_s': dt.strftime('%d/%m/%Y'), 'hr_s': dt.strftime('%H:%M'),
                'cat': "SEGURANÇA" if "Segurança" in termo else "BRASIL",
                'img': imgs[(i + j) % len(imgs)]
            })
    return sorted(noticias, key=lambda x: x['dt_obj'], reverse=True)

st.markdown('<div class="main-banner"><h1>SEGURANÇA DE BARRAGENS</h1><p style="color:#94a3b8; margin-top:10px;">Monitoramento Autônomo via Agente de IA</p></div>', unsafe_allow_html=True)

noticias = coletar()

col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
with col_c2:
    busca = st.text_input("", placeholder="🔍 Digite aqui para pesquisar...")
    if st.button("🔄 Atualizar Portal"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

filtradas = [n for n in noticias if busca.lower() in n['t'].lower()]
if filtradas:
    for i in range(0, len(filtradas), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtradas):
                n = filtradas[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="news-card">
                        <img src="{n['img']}" class="news-image">
                        <div class="news-content">
                            <span class="news-tag">{n['cat']}</span>
                            <div class="news-title">{n['t']}</div>
                            <div class="news-meta">🕒 {n['dt_s']} | {n['hr_s']}</div>
                            <div style="font-size: 0.7rem; color: #64748b; margin-top: 5px;">Fonte: {n['f']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("ABRIR NOTÍCIA", n['l'], use_container_width=True)

st.markdown("<br><br><div style='text-align: center; color: #64748b; font-size: 0.8rem; padding-bottom: 50px;'>© 2024 Segurança de Barragens - Monitoramento IA</div>", unsafe_allow_html=True)
