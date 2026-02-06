import streamlit as st
import feedparser

# 1. Configuração da Página
st.set_page_config(page_title="CNN Brasil - Monitor", page_icon="🔴", layout="wide")

# 2. Estilo Visual (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap' );
    * { font-family: 'Roboto', sans-serif; }
    .stApp { background-color: #ffffff; }
    .h { background-color: #cc0000; padding: 20px; text-align: center; color: white; border-bottom: 5px solid #990000; }
    .h h1 { font-weight: 900; font-size: 2.5rem; margin: 0; color: white !important; }
    .sh { background-color: #222222; color: white; padding: 10px; text-align: center; font-weight: 700; text-transform: uppercase; font-size: 14px; margin-bottom: 20px; }
    .card { border-bottom: 3px solid #cc0000; padding: 20px; height: 250px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .tag { color: #cc0000; font-weight: 900; font-size: 12px; text-transform: uppercase; }
    .t { font-size: 18px; font-weight: 700; margin: 15px 0; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; color: #222; }
    .stTextInput input { border: 2px solid #eee !important; border-radius: 0px !important; text-align: center !important; }
    .stButton>button { border-radius: 0px !important; background-color: #222 !important; color: white !important; font-weight: 700 !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

# 3. Cabeçalho
st.markdown('<div class="h"><h1>CNN BRASIL</h1></div><div class="sh">Monitor de Segurança de Barragens | Agente de IA</div>', unsafe_allow_html=True)

# 4. Agente de Coleta
@st.cache_data(ttl=3600)
def coletar():
    noticias = []
    for termo in ["Segurança de Barragens", "Barragens no Brasil"]:
        f = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+' )}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for e in f.entries[:9]:
            noticias.append({'t': e.title, 'l': e.link, 'f': e.source.title if hasattr(e, 'source') else 'CNN', 'cat': "SEGURANÇA" if "Segurança" in termo else "BRASIL"})
    return noticias

# 5. Interface e Filtros
noticias = coletar()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    busca = st.text_input("", placeholder="🔍 PESQUISAR NO PORTAL...")
    if st.button("ATUALIZAR NOTÍCIAS"):
        st.cache_data.clear()
        st.rerun()

st.markdown("  
", unsafe_allow_html=True)
filtradas = [n for n in noticias if busca.lower() in n['t'].lower()]

# 6. Grid de Notícias
if filtradas:
    for i in range(0, len(filtradas), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtradas):
                n = filtradas[i + j]
                with cols[j]:
                    st.markdown(f'<div class="card"><span class="tag">{n["cat"]}</span><div class="t">{n["t"]}</div><div style="font-size:12px;color:#666">Fonte: {n["f"]}</div></div>', unsafe_allow_html=True)
                    st.link_button("LEIA MAIS", n['l'], use_container_width=True)

st.markdown("  
  
<hr><div style='text-align:center;color:#666;font-size:12px;padding-bottom:50px;'>© 2024 CNN Brasil - Monitoramento Autônomo via Agente de IA</div>", unsafe_allow_html=True)
