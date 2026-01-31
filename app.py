import streamlit as st
import feedparser

# 1. Configuração
st.set_page_config(page_title="CNN Brasil - Monitor", page_icon="🔴", layout="wide")

# 2. Estilo (Versão Curta)
st.markdown("<style>.stApp{background:#fff}.h{background:#c00;padding:20px;text-align:center;color:#fff;border-bottom:5px solid #900}.h h1{font-weight:900;margin:0;color:#fff!important}.sh{background:#222;color:#fff;padding:10px;text-align:center;font-weight:700;text-transform:uppercase;font-size:14px;margin-bottom:20px}.card{border-bottom:3px solid #c00;padding:20px;height:250px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,.05);margin-bottom:10px}.tag{color:#c00;font-weight:900;font-size:12px;text-transform:uppercase}.t{font-size:18px;font-weight:700;margin:15px 0;overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical}</style>", unsafe_allow_html=True)

# 3. Cabeçalho
st.markdown('<div class="h"><h1>CNN BRASIL</h1></div><div class="sh">Monitor de Segurança de Barragens</div>', unsafe_allow_html=True)

# 4. Agente
@st.cache_data(ttl=3600)
def coletar():
    noticias = []
    for termo in ["Segurança de Barragens", "Barragens no Brasil"]:
        f = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+' )}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for e in f.entries[:9]:
            noticias.append({'t': e.title, 'l': e.link, 'f': e.source.title if hasattr(e, 'source') else 'CNN', 'cat': "SEGURANÇA" if "Segurança" in termo else "BRASIL"})
    return noticias

# 5. Busca e Grid
noticias = coletar()
busca = st.text_input("", placeholder="🔍 PESQUISAR...")
filtradas = [n for n in noticias if busca.lower() in n['t'].lower()]

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
<hr><div style='text-align:center;color:#666;font-size:12px'>© 2024 CNN Brasil - Agente de IA</div>", unsafe_allow_html=True)
