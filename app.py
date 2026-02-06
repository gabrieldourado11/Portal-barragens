import streamlit as st
import feedparser
from datetime import datetime
import time

# Configuração da página
st.set_page_config(page_title="CNN Brasil - Monitor de Barragens", page_icon="🔴", layout="wide")

# CSS ESTILO CNN BRASIL AVANÇADO
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');
    * { font-family: 'Roboto', sans-serif; }
    .stApp { background-color: #ffffff; color: #222222; }
    
    /* Header CNN */
    .cnn-header { background-color: #cc0000; padding: 1.5rem; text-align: center; color: white; border-bottom: 5px solid #990000; }
    .cnn-header h1 { font-weight: 900; font-size: 2.8rem; margin: 0; color: white !important; }
    .cnn-subheader { background-color: #222222; color: #ffffff; padding: 0.5rem; text-align: center; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 2rem; }
    
    /* Barra de Pesquisa */
    .stTextInput input { border: 2px solid #eeeeee !important; border-radius: 0px !important; text-align: center !important; height: 50px !important; }
    
    /* Card de Notícia Estilo CNN */
    .news-card {
        background: #ffffff;
        margin-bottom: 30px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .news-card:hover { transform: translateY(-5px); }
    
    .news-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        background-color: #f0f0f0;
    }
    
    .news-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; text-align: left; }
    
    .news-category { color: #cc0000; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px; }
    
    .news-title { font-size: 1.25rem; font-weight: 900; color: #222222; line-height: 1.2; margin-bottom: 15px; min-height: 60px; }
    
    .news-meta { display: flex; align-items: center; color: #666666; font-size: 0.85rem; margin-top: auto; }
    .news-meta i { margin-right: 5px; }
    
    /* Botão */
    .stButton>button { border-radius: 0px !important; background-color: #222222 !important; color: white !important; font-weight: 700 !important; text-transform: uppercase; width: 100%; height: 45px; border: none; }
    .stButton>button:hover { background-color: #cc0000 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# Função para converter data do RSS para objeto datetime
def parse_date(date_str):
    try:
        # Formato comum em RSS: "Fri, 06 Feb 2026 14:12:00 GMT"
        return datetime.strptime(date_str[:-4], '%a, %d %b %Y %H:%M:%S')
    except:
        return datetime.now()

# Agente de Coleta com Ordenação
@st.cache_data(ttl=300) # Atualiza a cada 5 minutos para ser "tempo real"
def coletar_noticias():
    termos = ["Segurança de Barragens", "Barragens no Brasil"]
    todas_noticias = []
    
    # Imagens padrão para o tema (caso o RSS não forneça)
    imagens_tema = [
        "https://images.unsplash.com/photo-1584463651400-90363984306d?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1590098573390-340888d2983b?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1473163928189-3f4b2c713e1c?auto=format&fit=crop&q=80&w=800"
    ]
    
    for i, termo in enumerate(termos):
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
        for j, e in enumerate(feed.entries[:10]):
            dt = parse_date(e.published) if hasattr(e, 'published') else datetime.now()
            todas_noticias.append({
                'titulo': e.title,
                'link': e.link,
                'fonte': e.source.title if hasattr(e, 'source') else 'CNN Brasil',
                'data_obj': dt,
                'data_str': dt.strftime('%d/%m/%Y'),
                'hora_str': dt.strftime('%H:%M'),
                'categoria': "SEGURANÇA" if "Segurança" in termo else "BRASIL",
                'imagem': imagens_tema[(i + j) % len(imagens_tema)]
            })
    
    # Ordenar por data (mais recentes primeiro)
    return sorted(todas_noticias, key=lambda x: x['data_obj'], reverse=True)

# --- INTERFACE ---

st.markdown('<div class="cnn-header"><h1>CNN BRASIL</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="cnn-subheader">Monitor de Segurança de Barragens | Alertas em Tempo Real</div>', unsafe_allow_html=True)

noticias = coletar_noticias()

# Barra de Pesquisa
col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
with col_c2:
    busca = st.text_input("", placeholder="🔍 PESQUISAR NOTÍCIAS E ALERTAS...")
    if st.button("🔄 ATUALIZAR PORTAL AGORA"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Filtragem
filtradas = [n for n in noticias if busca.lower() in n['titulo'].lower()]

# Grid de Notícias
if filtradas:
    for i in range(0, len(filtradas), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtradas):
                n = filtradas[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="news-card">
                        <img src="{n['imagem']}" class="news-image">
                        <div class="news-content">
                            <span class="news-category">{n['categoria']}</span>
                            <div class="news-title">{n['titulo']}</div>
                            <div class="news-meta">
                                🕒 {n['data_str']} | {n['hora_str']}
                            </div>
                            <div style="font-size: 0.8rem; color: #999; margin-top: 5px;">Fonte: {n['fonte']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button("LEIA MAIS", n['link'], use_container_width=True)
else:
    st.markdown("<h3 style='text-align: center;'>Nenhum alerta encontrado para sua busca.</h3>", unsafe_allow_html=True)

st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color: #666666; font-size: 0.8rem; padding-bottom: 50px;'>© {datetime.now().year} CNN Brasil - Monitoramento Autônomo via Agente de IA</div>", unsafe_allow_html=True)
