import streamlit as st
import feedparser
from datetime import datetime
import random

# 1. Configuração da Página
st.set_page_config(page_title="Segurança de Barragens - Hub IA", page_icon="🏗️", layout="wide")

# 2. FUNÇÃO PARA INJETAR O TEMA E DESIGN MINIMALISTA
def inject_theme(theme_name):
    theme_key = "LEGISLACAO" if "LEGIS" in theme_name.upper() else theme_name.upper()
    if "GERAL" in theme_key: theme_key = "GERAL"
    if "ALERTA" in theme_key: theme_key = "ALERTAS"

    themes = {
        "GERAL": {
            "bg": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)",
            "primary": "#3b82f6",
            "accent": "rgba(59, 130, 246, 0.3)"
        },
        "ALERTAS": {
            "bg": "linear-gradient(135deg, #450a0a 0%, #991b1b 100%)",
            "primary": "#ef4444",
            "accent": "rgba(239, 68, 68, 0.3)"
        },
        "LEGISLACAO": {
            "bg": "linear-gradient(135deg, #451a03 0%, #92400e 100%)",
            "primary": "#f59e0b",
            "accent": "rgba(245, 158, 11, 0.3)"
        }
    }
    
    t = themes.get(theme_key, themes["GERAL"])
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        * {{ font-family: 'Inter', sans-serif; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
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
            margin-bottom: 0.5rem;
            animation: fadeIn 0.8s ease-out;
        }}

        .main-banner h1 {{
            font-weight: 900;
            font-size: 3rem;
            color: #ffffff !important;
            margin: 0;
            letter-spacing: -1px;
            text-transform: uppercase;
        }}

        .stRadio > div {{
            background: transparent !important;
            border: none !important;
            justify-content: center !important;
            gap: 40px !important;
            margin-bottom: 2rem !important;
        }}

        .stRadio [data-testid="stWidgetLabel"] {{ display: none; }}

        .stRadio div[role="radiogroup"] label {{
            background: transparent !important;
            border: none !important;
            padding: 8px 0 !important;
            color: rgba(255,255,255,0.5) !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }}

        .stRadio div[role="radiogroup"] div[data-testid="stRadioButtonCustomObject"] {{
            display: none !important;
        }}

        .stRadio div[role="radiogroup"] > div:has(input:checked) label {{
            color: white !important;
            border-bottom: 3px solid {t['primary']} !important;
        }}

        .news-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            overflow: hidden;
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            height: 450px;
            animation: fadeIn 0.6s ease-out;
        }}
        
        .news-card:hover {{
            transform: translateY(-15px) scale(1.02);
            background: rgba(255, 255, 255, 0.12);
            border-color: {t['primary']};
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        }}

        .news-tag {{ color: {t['primary']}; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 10px; }}
        .news-image {{ width: 100%; height: 190px; object-fit: cover; transition: 0.5s; }}
        .news-card:hover .news-image {{ transform: scale(1.08); }}
        .news-content {{ padding: 20px; flex-grow: 1; display: flex; flex-direction: column; text-align: center; }}
        .news-title {{ font-size: 1.15rem; font-weight: 700; color: #ffffff; line-height: 1.4; margin-bottom: 15px; }}
        .news-meta {{ color: #94a3b8; font-size: 0.85rem; margin-top: auto; }}
        .card-link {{ text-decoration: none; color: inherit; display: block; }}
    </style>
    <script>
        setTimeout(function() {
            window.location.reload();
        }, 1800000); // 1800000 ms = 30 minutos
    </script>
    """, unsafe_allow_html=True)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str[:-4], '%a, %d %b %Y %H:%M:%S')
    except:
        return datetime.now()

# 3. BIBLIOTECA DE IMAGENS SINCRONIZADAS POR CONTEXTO
IMGS_CONTEXTO = {
    "BARRAGEM": [
        "https://images.unsplash.com/photo-1584463651400-90363984306d?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1590098573390-340888d2983b?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1473163928189-3f4b2c713e1c?auto=format&fit=crop&w=600&q=80"
    ],
    "ALERTA": [
        "https://images.unsplash.com/photo-1590105577767-e217ec73b2d3?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=600&q=80"
    ],
    "FISCALIZACAO": [
        "https://images.unsplash.com/photo-1581094288338-2314dddb7ecc?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=600&q=80"
    ],
    "LEGISLACAO": [
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&w=600&q=80"
    ]
}

def get_img_sincronizada(titulo):
    t = titulo.lower()
    if any(w in t for w in ["risco", "alerta", "emergência", "perigo"]):
        return random.choice(IMGS_CONTEXTO["ALERTA"])
    if any(w in t for w in ["resolução", "norma", "portaria", "lei", "anm"]):
        return random.choice(IMGS_CONTEXTO["LEGISLACAO"])
    if any(w in t for w in ["fiscalização", "vistoria", "técnico", "inspeção"]):
        return random.choice(IMGS_CONTEXTO["FISCALIZACAO"])
    return random.choice(IMGS_CONTEXTO["BARRAGEM"])

@st.cache_data(ttl=1800)
def coletar():
    termos = ["Segurança de Barragens", "Resolução ANM Barragens", "Fiscalização de Barragens"]
    noticias = []
    
    for i, termo in enumerate(termos):
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for j, e in enumerate(feed.entries[:10]):
            dt = parse_date(e.published) if hasattr(e, 'published') else datetime.now()
            titulo = e.title.lower()
            
            # Sincronização de imagem baseada no título
            img_url = get_img_sincronizada(e.title)
            
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
st.markdown('<div class="main-banner"><h1>SEGURANÇA DE BARRAGENS</h1><p style="color:rgba(255,255,255,0.4); font-size:0.8rem; font-weight:600; letter-spacing:2px;">HUB DE MONITORAMENTO INTELIGENTE</p></div>', unsafe_allow_html=True)

noticias = coletar()

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
                                <div style="font-size: 0.7rem; color: rgba(255,255,255,0.3);">Fonte: {n['f']}</div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

render_grid(lista_exibir)

st.markdown("<br><br><div style='text-align: center; color: rgba(255,255,255,0.2); font-size: 0.7rem; padding-bottom: 40px; font-weight:600; letter-spacing:1px;'>© 2024 SEGURANÇA DE BARRAGENS - AGENTE DE IA</div>", unsafe_allow_html=True)
