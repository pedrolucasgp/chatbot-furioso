from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def iniciar_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-webgl')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-features=WebRtcHideLocalIpsWithMdns')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(options=options)
    return driver

def buscar_noticias_furia(driver, url):
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    xpath = "//a[contains(@href, 'noticia') and contains(@class, 'a-block') and contains(@class, 'standard-box') and contains(@class, 'news-item') and contains(@class, 'wide-article')]"

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )

    noticias = []
    links = driver.find_elements(By.XPATH, xpath)
    
    print(f"Analisando o link {url}...")
    for link in links:
        try:
            href = link.get_attribute("href")
            if href:
                link_text = link.text.lower()
                if 'furia' in link_text:
                    print(f"Notícia relacionada à FURIA encontrada: {href}")
                    noticias.append(href)
        except Exception as e:
            print(f"Erro ao processar link: {e}")
    
    return noticias

def verificar_conteudo_furia(driver, link):
    try:
        driver.get(link)
        time.sleep(2)
        return 'furia' in driver.page_source.lower()
    except Exception as e:
        print(f"Erro ao verificar conteúdo de {link}: {e}")
        return False

def extrair_conteudo_noticia(driver, link):
    try:
        driver.get(link)
        time.sleep(2)
    
        titulo_elem = driver.find_elements(By.TAG_NAME, 'h1')
        titulo = titulo_elem[0].text.strip() if titulo_elem else 'Título não encontrado'
        
        data_elem = driver.find_elements(By.CSS_SELECTOR, 'span[data-format*="de"]') or driver.find_elements(By.TAG_NAME, 'time')
        data = data_elem[0].text.strip() if data_elem else 'Data não encontrada'
        
        conteudo = ""
        conteudo_div = driver.find_elements(By.CSS_SELECTOR, 'div.news-content') or driver.find_elements(By.TAG_NAME, 'article')
        if conteudo_div:
            paragrafos = conteudo_div[0].find_elements(By.TAG_NAME, 'p')
            conteudo = '\n'.join(p.text.strip() for p in paragrafos if p.text.strip())
        else:
            paragrafos = driver.find_elements(By.CSS_SELECTOR, 'p.paragraph')
            conteudo = '\n'.join(p.text.strip() for p in paragrafos if p.text.strip())
        
        print(f"A notícia: {titulo} é válida!")
        return {'titulo': titulo, 'data': data, 'conteudo': conteudo, 'link': link}
    except Exception as e:
        print(f"Erro ao processar {link}: {e}")
        return None

def carregar_noticias_salvas():
    if not os.path.exists("furia_datalog.md"):
        return set(), None

    with open("furia_datalog.md", "r", encoding="utf-8") as f:
        conteudo = f.read()

    links_salvos = set()
    primeira_url = None

    linhas = conteudo.split('\n')
    for linha in linhas:
        if linha.startswith("[Fonte]("):
            link = linha.split("(")[1].split(")")[0]
            links_salvos.add(link)
            if not primeira_url:
                primeira_url = link

    return links_salvos, primeira_url

def processar_novas_noticias(driver, links, links_salvos, primeira_url_salva):
    novas_noticias = []

    for link in links:
        if link in links_salvos:
            print(f"Notícia já existente: {link}")
            if link == primeira_url_salva:
                print("Chegamos à notícia mais recente. Parando busca.")
                return novas_noticias, True
            continue

        if verificar_conteudo_furia(driver, link):
            noticia = extrair_conteudo_noticia(driver, link)
            if noticia:
                novas_noticias.append(noticia)
                links_salvos.add(link)

    return novas_noticias, False

def atualizar_arquivo_markdown(novas_noticias):
    if not novas_noticias:
        print("Nenhuma notícia nova para adicionar.")
        return

    conteudo_existente = ""
    if os.path.exists("furia_datalog.md"):
        with open("furia_datalog.md", "r", encoding="utf-8") as f:
            conteudo_existente = f.read()

    novo_conteudo = "# Notícias sobre a FURIA – Dust2.com.br\n\n"
    for noticia in novas_noticias:
        novo_conteudo += f"## {noticia['titulo']}\n"
        novo_conteudo += f"*Publicado em: {noticia['data']}*\n\n"
        novo_conteudo += f"{noticia['conteudo']}\n\n"
        novo_conteudo += f"[Fonte]({noticia['link']})\n\n"
        novo_conteudo += "---\n\n"

    markdown = novo_conteudo + conteudo_existente

    with open("furia_datalog.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Adicionadas {len(novas_noticias)} novas notícias ao arquivo.")

if __name__ == "__main__":
    arquivo_existe = os.path.exists("furia_datalog.md")
    links_salvos, primeira_url_salva = carregar_noticias_salvas()
    
    if primeira_url_salva:
        print(f"Notícia mais recente: {primeira_url_salva}")

    driver = iniciar_driver()
    todas_novas_noticias = []

    try:
        for offset in range(0, 601, 30):
            url = f"https://www.dust2.com.br/arquivo?offset={offset}"
            print(f"\nBuscando em: {url}")

            links_pagina = buscar_noticias_furia(driver, url)
            novas_noticias, encontrou_primeira = processar_novas_noticias(driver, links_pagina, links_salvos, primeira_url_salva)

            todas_novas_noticias.extend(novas_noticias)
            if encontrou_primeira:
                break

            time.sleep(2)
    finally:
        driver.quit()

    atualizar_arquivo_markdown(todas_novas_noticias)
