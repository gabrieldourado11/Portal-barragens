import streamlit as st
import feedparser
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Portal de Notícias - Segurança de Barragens",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para deixar a interface moderna
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #3B82F6 0%, #1E3A8A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .news-card {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .news-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .news-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .news-meta {
        color: #64748B;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .news-source {
        color: #3B82F6;
        font-weight: 600;
    }
    .stat-box {
        background: linear-gradient(135deg, #3B82F6 0%, #1E3A8A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


# Função do Agente de Coleta de Notícias
@st.cache_data(ttl=3600)  # Cache por 1 hora
def coletar_noticias():
    """
    Agente de IA que coleta notícias automaticamente do Google News RSS
    sobre Segurança de Barragens e Barragens no Brasil
    """
    termos_busca = [
        "Segurança de Barragens",
        "Barragens no Brasil"
    ]
    
    todas_noticias = []
    
    for termo in termos_busca:
        # URL do RSS do Google News
        url_rss = f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        
        try:
            # Faz o parsing do feed RSS
            feed = feedparser.parse(url_rss)
            
            # Processa cada notícia
            for entrada in feed.entries:
                noticia = {
                    'titulo': entrada.title,
                    'link': entrada.link,
                    'data': entrada.published if hasattr(entrada, 'published') else 'Data não disponível',
                    'fonte': entrada.source.title if hasattr(entrada, 'source') else 'Google News',
                    'termo_busca': termo
                }
                todas_noticias.append(noticia)
        
        except Exception as e:
            st.error(f"Erro ao coletar notícias para '{termo}': {str(e)}")
    
    # Remove duplicatas baseado no título
    noticias_unicas = []
    titulos_vistos = set()
    
    for noticia in todas_noticias:
        if noticia['titulo'] not in titulos_vistos:
            noticias_unicas.append(noticia)
            titulos_vistos.add(noticia['titulo'])
    
    # Ordena por data (mais recentes primeiro)
    return noticias_unicas


# Função para formatar data
def formatar_data(data_str):
    """Formata a data para exibição"""
    try:
        # Tenta parsear diferentes formatos de data
        for fmt in ['%a, %d %b %Y %H:%M:%S %Z', '%a, %d %b %Y %H:%M:%S %z']:
            try:
                data_obj = datetime.strptime(data_str, fmt)
                return data_obj.strftime('%d/%m/%Y às %H:%M')
            except:
                continue
        return data_str
    except:
        return data_str


# Interface Principal
def main():
    # Cabeçalho
    st.markdown('<h1 class="main-header">🏗️ Portal de Notícias: Segurança de Barragens</h1>', unsafe_allow_html=True)
    st.markdown("### 🤖 Alimentado por Agente de IA Autônomo")
    st.markdown("---")
    
    # Barra Lateral com Estatísticas
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2920/2920277.png", width=100)
        st.title("📊 Estatísticas")
        
        # Botão de atualização
        if st.button("🔄 Atualizar Notícias", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Coleta as notícias
        with st.spinner("🔍 Agente coletando notícias..."):
            noticias = coletar_noticias()
        
        # Estatísticas
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(noticias)}</div>
            <div class="stat-label">Notícias Encontradas</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Contagem por termo
        termos_count = {}
        for noticia in noticias:
            termo = noticia['termo_busca']
            termos_count[termo] = termos_count.get(termo, 0) + 1
        
        st.markdown("### 🔍 Por Termo de Busca")
        for termo, count in termos_count.items():
            st.metric(termo, count)
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.info("""
        Este portal é alimentado por um **Agente de IA** que coleta automaticamente 
        notícias sobre Segurança de Barragens no Brasil através do Google News RSS.
        
        **Atualização:** A cada 1 hora
        """)
        
        st.markdown("---")
        st.markdown("### 🛠️ Tecnologias")
        st.markdown("""
        - **Python** 🐍
        - **Streamlit** 🎈
        - **Feedparser** 📰
        - **Google News RSS** 📡
        """)
    
    # Área Principal - Exibição das Notícias
    if len(noticias) == 0:
        st.warning("⚠️ Nenhuma notícia encontrada no momento. Tente atualizar em alguns instantes.")
    else:
        # Filtros
        col1, col2 = st.columns([3, 1])
        with col1:
            termo_filtro = st.selectbox(
                "🔍 Filtrar por termo de busca:",
                ["Todas"] + list(set([n['termo_busca'] for n in noticias]))
            )
        with col2:
            st.metric("Total Exibido", len([n for n in noticias if termo_filtro == "Todas" or n['termo_busca'] == termo_filtro]))
        
        st.markdown("---")
        
        # Exibe as notícias
        noticias_filtradas = [n for n in noticias if termo_filtro == "Todas" or n['termo_busca'] == termo_filtro]
        
        for idx, noticia in enumerate(noticias_filtradas, 1):
            st.markdown(f"""
            <div class="news-card">
                <div class="news-title">📰 {noticia['titulo']}</div>
                <div class="news-meta">
                    📅 {formatar_data(noticia['data'])} | 
                    <span class="news-source">🔗 {noticia['fonte']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([6, 1])
            with col2:
                st.link_button("Ler Notícia", noticia['link'], use_container_width=True)
            
            if idx < len(noticias_filtradas):
                st.markdown("<br>", unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #64748B; padding: 2rem;'>
        <p><strong>Portal de Notícias - Segurança de Barragens</strong></p>
        <p>Desenvolvido com ❤️ usando Python e Streamlit</p>
        <p>🤖 Agente de IA Autônomo | 📰 Dados do Google News RSS</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
