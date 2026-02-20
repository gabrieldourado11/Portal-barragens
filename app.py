import streamlit as st
import feedparser
from datetime import datetime
import random
import time

# 1. Configuração da Página (Deve ser o primeiro comando Streamlit)
st.set_page_config(page_title="Segurança de Barragens - Hub IA", page_icon="🏗️", layout="wide")

# 2. FUNÇÃO PARA INJETAR O TEMA E DESIGN
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

        .partner-banner {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px 20px;
            margin-bottom: 30px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}
        .partner-banner:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: {t['primary']};
        }}
        .partner-banner h3 {{
            color: white;
            font-size: 1.2rem;
            margin-bottom: 10px;
        }}
        .partner-banner a {{
            display: inline-block;
            background: {t['primary']};
            color: white;
            padding: 8px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 700;
            transition: background 0.3s ease;
        }}
        .partner-banner a:hover {{
            background: #fff;
            color: {t['primary']};
        }}

        .consultoria-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: {t['primary']};
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        .consultoria-btn:hover {{
            background: #fff;
            color: {t['primary']};
            transform: translateY(-5px);
        }}

        .newsletter-form {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-top: 50px;
            margin-bottom: 50px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .newsletter-form h3 {{
            color: white;
            font-size: 1.5rem;
            margin-bottom: 15px;
        }}
        .newsletter-form p {{
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 20px;
        }}
        .newsletter-form input[type="email"] {{
            width: 70%;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            margin-right: 10px;
            font-size: 1rem;
        }}
        .newsletter-form input[type="email"]::placeholder {{
            color: rgba(255, 255, 255, 0.5);
        }}
        .newsletter-form button {{
            background: {t['primary']};
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            border: none;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.3s ease;
            font-size: 1rem;
        }}
        .newsletter-form button:hover {{
            background: #fff;
            color: {t["primary"]};
        }}

        .courses-events-section {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-top: 50px;
            margin-bottom: 50px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .courses-events-section h3 {{
            color: white;
            font-size: 1.5rem;
            margin-bottom: 15px;
        }}
        .courses-events-section p {{
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 20px;
        }}
        .courses-events-section .course-card {{
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 15px;
            margin: 10px auto;
            max-width: 400px;
            text-align: left;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}
        .courses-events-section .course-card:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: {t["primary"]};
        }}
        .courses-events-section .course-card h4 {{
            color: white;
            margin-bottom: 5px;
        }}
        .courses-events-section .course-card span {{
            color: {t["primary"]};
            font-weight: 700;
            font-size: 0.9rem;
        }}
        .courses-events-section .course-card a {{
            display: block;
            background: {t["primary"]};
            color: white;
            padding: 8px 15px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 700;
            margin-top: 10px;
            transition: background 0.3s ease;
            text-align: center;
        }}
        .courses-events-section .course-card a:hover {{
            background: #fff;
            color: {t["primary"]};
        }}

    </style>
    <script>
        setTimeout(function() {{
            window.location.reload();
        }}, 1800000); 
    </script>
    """, unsafe_allow_html=True)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str[:-4], '%a, %d %b %Y %H:%M:%S')
    except:
        return datetime.now()

# 3. BIBLIOTECA DE IMAGENS DINÂMICAS E COLETA (Atualizado)
def get_img_sincronizada(titulo, indice_randomico):
    t = titulo.lower()
    
    # Define as palavras-chave baseadas no contexto
    if any(w in t for w in ["risco", "alerta", "emergência", "perigo", "rompimento", "evacuação"]):
        keywords = "siren,danger,fire,emergency"
    elif any(w in t for w in ["resolução", "norma", "portaria", "lei", "anm", "oficial", "decreto"]):
        keywords = "document,law,court,paper"
    elif any(w in t for w in ["fiscalização", "vistoria", "técnico", "inspeção", "obra", "engenharia"]):
        keywords = "engineer,construction,hardhat,inspection"
    else:
        keywords = "dam,river,water,hydroelectric,concrete"
    
    # Adiciona um número aleatório no final para que as imagens não sejam todas iguais
    return f"https://loremflickr.com/600/400/{keywords}?random={indice_randomico}"

@st.cache_data(ttl=1800)
def coletar():
    termos = ["Segurança de Barragens", "Resolução ANM Barragens", "Fiscalização de Barragens"]
    noticias = []
    
    # Contador para garantir imagens diferentes
    contador_img = 1
    
    for termo in termos:
        try:
            feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
            
            # Limita a 6 notícias por termo para não poluir
            for entry in feed.entries[:6]: 
                dt = parse_date(entry.published) if hasattr(entry, 'published') else datetime.now()
                titulo = entry.title.lower()
                
                if any(word in titulo for word in ["resolução", "norma", "portaria", "lei"]):
                    cat = "LEGISLAÇÃO"
                elif any(word in titulo for word in ["risco", "alerta", "emergência", "perigo"]):
                    cat = "ALERTAS"
                else:
                    cat = "GERAL"
                
                # Gera URL da imagem usando a nova função
                img_url = get_img_sincronizada(titulo, contador_img)
                contador_img += 1
                
                noticias.append({
                    't': entry.title, 
                    'l': entry.link, 
                    'f': entry.source.title if hasattr(entry, 'source') else 'Portal',
                    'dt_obj': dt, 
                    'dt_s': dt.strftime('%d/%m/%Y'), 
                    'hr_s': dt.strftime('%H:%M'),
                    'cat': cat, 
                    'img': img_url
                })
        except Exception as e:
            continue # Se der erro em um feed, pula para o próximo
            
    # Remove duplicatas baseadas no título
    seen_titles = set()
    unique_noticias = []
    for n in noticias:
        if n['t'] not in seen_titles:
            unique_noticias.append(n)
            seen_titles.add(n['t'])
            
    return sorted(unique_noticias, key=lambda x: x['dt_obj'], reverse=True)

# --- INTERFACE ---
st.markdown('<div class="main-banner"><h1>LUISA DOURADO</h1><p style="color:rgba(255,255,255,0.4); font-size:0.8rem; font-weight:600; letter-spacing:2px;">HUB DE MONITORAMENTO INTELIGENTE</p></div>', unsafe_allow_html=True)

# Banner de Parceiro
st.markdown(f"""
<div class="partner-banner">
    <h3>Seja um Parceiro Oficial do Hub de Segurança de Barragens!</h3>
    <p style="color:rgba(255,255,255,0.7);">Destaque sua empresa para milhares de profissionais do setor.</p>
    <a href="#" target="_blank">Anuncie Conosco</a>
</div>
""", unsafe_allow_html=True)

# Coleta de dados
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

# Seção de Cursos e Eventos
st.markdown(f"""
<div class="courses-events-section">
    <h3>Capacite-se e Mantenha-se Atualizado!</h3>
    <p>Confira os principais cursos, treinamentos e eventos sobre segurança de barragens.</p>
    <div class="course-card">
        <h4>Curso: Gestão de Segurança de Barragens</h4>
        <span>Online | 40h | Certificado</span>
        <a href="#" target="_blank">Saiba Mais</a>
    </div>
    <div class="course-card">
        <h4>Webinar: Novas Regulamentações da ANM</h4>
        <span>Ao Vivo | Gratuito | Inscrições Abertas</span>
        <a href="#" target="_blank">Inscreva-se</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Formulário de Newsletter
st.markdown(f"""
<div class="newsletter-form">
    <h3>Receba Alertas e Análises Exclusivas!</h3>
    <p>Assine nossa newsletter e mantenha-se à frente com informações estratégicas sobre segurança de barragens.</p>
    <form action="#" method="post">
        <input type="email" placeholder="Seu melhor e-mail" required>
        <button type="submit">Assinar Agora</button>
    </form>
</div>
""", unsafe_allow_html=True)

# Botão de Consultoria Flutuante
st.markdown(f"""
<a href="#" target="_blank" class="consultoria-btn">
    Solicitar Consultoria Técnica
</a>
""", unsafe_allow_html=True)

st.markdown("<br><br><div style='text-align: center; color: rgba(255,255,255,0.2); font-size: 0.7rem; padding-bottom: 40px; font-weight:600; letter-spacing:1px;'>© 2024 SEGURANÇA DE BARRAGENS - AGENTE DE IA</div>", unsafe_allow_html=True)
