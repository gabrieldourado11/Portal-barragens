import streamlit as st
import feedparser
from datetime import datetime
import re

# 1. Configuração da Página
st.set_page_config(page_title="Segurança de Barragens - Hub IA", page_icon="🏗️", layout="wide")

# 2. FUNÇÃO PARA INJETAR O TEMA E DESIGN MINIMALISTA
def inject_theme(theme_name):
    themes = {
        "GERAL": {
            "bg": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)",
            "primary": "#3b82f6",
            "accent": "rgba(59, 130, 246, 0.2)"
        },
        "ALERTAS": {
            "bg": "linear-gradient(135deg, #450a0a 0%, #991b1b 100%)",
            "primary": "#ef4444",
            "accent": "rgba(239, 68, 68, 0.2)"
        },
        "LEGISLACAO": {
            "bg": "linear-gradient(135deg, #451a03 0%, #92400e 100%)",
            "primary": "#f59e0b",
            "accent": "rgba(245, 158, 11, 0.2)"
        }
    }
    t = themes[theme_name]
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        * {{ font-family: 'Inter', sans-serif; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .stApp {{
            background: {t['bg']} !important;
            background-attachment: fixed !important;
            transition: background 0.8s ease-in-out !important;
            color: white;
        }}
        
        .main-banner {{
            background: transparent;
            padding: 2rem 1rem;
            text-align: center;
            margin-bottom: 1rem;
            animation: fadeIn 0.8s ease-out;
        }}

        .main-banner h1 {{
            font-weight: 900;
            font-size: clamp(1.8rem, 6vw, 3rem);
            color: #ffffff !important;
            margin: 0;
            letter-spacing: -1px;
        }}

        /* Estilização Minimalista do Seletor (Abas Clean) */
        .stRadio > div {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            justify-content: center !important;
            gap: 30px !important;
            margin-bottom: 3rem !important;
        }}

        .stRadio [data-testid="stWidgetLabel"] {{ display: none; }}

        /* Estilo do texto das categorias */
        .stRadio div[role="radiogroup"] label {{
            background: transparent !important;
            border: none !important;
            padding: 10px 0 !important;
            color: rgba(255,255,255,0.6) !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            border-bottom: 3px solid transparent !important;
        }}

        /* Traçado embaixo quando selecionado */
        .stRadio div[role="radiogroup"] label[data-baseweb="radio"] {{
            border-bottom: 3px solid transparent !important;
        }}
        
        /* Simulação do traçado dinâmico via CSS para o item selecionado */
        .stRadio div[role="radiogroup"] > div:has(input:checked) label {{
            color: white !important;
            border-bottom: 3px solid {t['primary']} !important;
        }}

        /* Cards Clean */
        .news-card {{
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            overflow: hidden;
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            transition: all 0.4s ease;
            height: 450px;
            animation: fadeIn 0.6s ease-out;
        }}
        
        .news-card:hover {{
            transform: translateY(-10px);
            background: rgba(255, 255, 255, 0.08);
            border-color: {t['primary']};
        }}

        .news-tag {{ color: {t['primary']}; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 10px; }}
        .news-image {{ width: 100%; height: 190px; object-fit: cover; filter: grayscale(20%); transition: 0.5s; }}
        .news-card:hover .news-image {{ filter: grayscale(0%); transform: scale(1.05); }}
        .news-content {{ padding: 20px; flex-grow: 1; display: flex; flex-direction: column; text-align: center; }}
        .news-title {{ font-size: 1.15rem; font-weight: 700; color: #ffffff; line-height: 1.4; margin-bottom: 15px; }}
        .news-meta {{ color: #94a3b8; font-size: 0.85rem; margin-top: auto; }}
        .card-link {{ text-decoration: none; color: inherit; display: block; }}
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
            
            img_url = backup_imgs[(i + j) % 3]
            if hasattr(e, 'summary'):
                match = re.search(r'src="([^"]+)"', e.summary)
                if match: img_url = match.group(1)
            
            if any(word in titulo for word in ["resolução", "norma", "portaria", "lei"]):
                cat = "LEGISLAÇÃO"
            elif any(word in titulo for word in ["risco", "alerta", "emergência", "perigo"]):
                cat = "ALERTAS"
            else:
                cat = "GERAL"
                
            noticias.append({
                't': e.title, 'l': e.link, 'f': e.source.title if hasattr(e, 'source') else 'Portal',
                'dt_obj': dt, 'dt_s': dt.strftime('%d/%m/%Y'), 'hr_s': dt.strftime('%H:%M'),
                'cat': cat, 'img': img_url
            })
    return sorted(noticias, key=lambda x: x['dt_obj'], reverse=True)

# --- INTERFACE ---
st.markdown('<div class="main-banner"><h1>SEGURANÇA DE BARRAGENS</h1><p style="color:rgba(255,255,255,0.5); font-size:0.9rem; font-weight:500; letter-spacing:1px;">HUB DE MONITORAMENTO INTELIGENTE</p></div>', unsafe_allow_html=True)

noticias = coletar()

# Seletor de Categorias Minimalista e Centralizado
escolha = st.radio("", ["PANORAMA GERAL", "ALERTAS URGENTES", "LEGISLAÇÃO TÉCNICA"], horizontal=True)

if "GERAL" in escolha:
    inject_theme("GERAL")
    lista_exibir = noticias
elif "ALERTAS" in escolha:
    inject_theme("ALERTAS")
    lista_exibir = [n for n in noticias if n['cat'] == "ALERTAS"]
else:
    inject_theme("LEGISLAÇÃO")
    lista_exibir = [n for n in noticias if n['cat'] == "LEGISLAÇÃO"]

st.markdown("<br>", unsafe_allow_html=True)

def render_grid(lista):
    if not lista:
        st.info("Nenhuma notícia encontrada nesta categoria.")
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
                                <div style="font-size: 0.7rem; color: rgba(255,255,255,0.4);">Fonte: {n['f']}</div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

render_grid(lista_exibir)

st.markdown("<br><br><div style='text-align: center; color: rgba(255,255,255,0.3); font-size: 0.7rem; padding-bottom: 40px; font-weight:600; letter-spacing:1px;'>© 2024 SEGURANÇA DE BARRAGENS - AGENTE DE IA</div>", unsafe_allow_html=True)
