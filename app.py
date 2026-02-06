# 3. BIBLIOTECA DE IMAGENS DINÂMICAS (Corrigido para não quebrar)
# Removemos a lista fixa e usamos um gerador baseado em palavras-chave
def get_img_sincronizada(titulo, indice_randomico):
    t = titulo.lower()
    
    # Define as palavras-chave baseadas no contexto
    if any(w in t for w in ["risco", "alerta", "emergência", "perigo", "rompimento"]):
        keywords = "siren,danger,fire"
    elif any(w in t for w in ["resolução", "norma", "portaria", "lei", "anm", "oficial"]):
        keywords = "document,law,court"
    elif any(w in t for w in ["fiscalização", "vistoria", "técnico", "inspeção", "obra"]):
        keywords = "engineer,construction,hardhat"
    else:
        keywords = "dam,river,water,hydroelectric"
    
    # Adiciona um número aleatório no final para que as imagens não sejam todas iguais
    return f"https://loremflickr.com/600/400/{keywords}?random={indice_randomico}"

@st.cache_data(ttl=1800)
def coletar():
    termos = ["Segurança de Barragens", "Resolução ANM Barragens", "Fiscalização de Barragens"]
    noticias = []
    
    # Contador para garantir imagens diferentes
    contador_img = 1
    
    for termo in termos:
        # Tenta pegar o feed; se falhar, não quebra o app
        try:
            feed = feedparser.parse(f"https://news.google.com/rss/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
            
            for entry in feed.entries[:6]: # Limita a 6 por termo para não poluir
                dt = parse_date(entry.published) if hasattr(entry, 'published') else datetime.now()
                titulo = entry.title.lower()
                
                if any(word in titulo for word in ["resolução", "norma", "portaria", "lei"]):
                    cat = "LEGISLAÇÃO"
                elif any(word in titulo for word in ["risco", "alerta", "emergência", "perigo"]):
                    cat = "ALERTAS"
                else:
                    cat = "GERAL"
                
                # Gera URL da imagem
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
