import streamlit as st
import feedparser
from datetime import datetime
import random
import time

# 1. Configuração da Página (Deve ser o primeiro comando)
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
    
    # Nota: Em f-strings com CSS, usamos {{ para CSS real e { para variáveis Python
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
            text-transform
