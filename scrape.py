from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'noticia')]"))
    )

    noticias = set()
    links = driver.find_elements(By.XPATH, "//a[contains(@href, 'noticia')]")
    
    print(f"Analisando o link {url}...")
    for link in links:
        try:
            href = link.get_attribute("href")
            if href and href not in noticias:
                link_text = link.text.lower()
                if 'furia' in link_text:
                    print(f"Notícia relacionada à FURIA encontrada: {href}")
                    noticias.add(href)
        except Exception as e:
            print(f"Erro ao processar link: {e}")
    
    return list(noticias)

def verificar_conteudo_furia(driver, link):
    try:
        driver.get(link)
        time.sleep(2)
        
        page_content = driver.page_source.lower()
        
        if 'furia' in page_content:
            return True
            
        return False
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
        
        conteudo_div = driver.find_elements(By.CSS_SELECTOR, 'div.news-content')
        if conteudo_div:
            paragrafos = conteudo_div[0].find_elements(By.TAG_NAME, 'p')
            conteudo = '\n'.join(p.text.strip() for p in paragrafos if p.text.strip())
        else:
            article = driver.find_elements(By.TAG_NAME, 'article')
            if article:
                paragrafos = article[0].find_elements(By.TAG_NAME, 'p')
                conteudo = '\n'.join(p.text.strip() for p in paragrafos if p.text.strip())
            else:
                paragrafos = driver.find_elements(By.CSS_SELECTOR, 'p.paragraph')
                conteudo = '\n'.join(p.text.strip() for p in paragrafos if p.text.strip())
        
        print(f"A notícia: {titulo} é valida!")
        return titulo, data, conteudo
    except Exception as e:
        print(f"Erro ao processar {link}: {e}")
        return None

def montar_markdown(driver, links):
    markdown = "# Notícias sobre a FURIA – Dust2.com.br\n\n"
    count = 0
    
    for link in links:
        if verificar_conteudo_furia(driver, link):
            resultado = extrair_conteudo_noticia(driver, link)
            if resultado:
                titulo, data, conteudo = resultado
                markdown += f"## {titulo}\n"
                markdown += f"*Publicado em: {data}*\n\n"
                markdown += f"{conteudo}\n\n"
                markdown += f"[Fonte]({link})\n\n"
                markdown += "---\n\n"
                count += 1
        time.sleep(1.5)
    
    print(f"Total de notícias sobre FURIA que foram encontradas: {count}")
    return markdown

if __name__ == "__main__":
    driver = iniciar_driver()
    todos_links = set()

    try:
        for offset in range(0, 601, 30):
            url = f"https://www.dust2.com.br/arquivo?offset={offset}"
            print(f"\nBuscando em: {url}")
            
            links_pagina = buscar_noticias_furia(driver, url)
            novos_links = [link for link in links_pagina if link not in todos_links]
            
            for link in novos_links:
                if verificar_conteudo_furia(driver, link):
                    todos_links.add(link)
                    print(f"Link confirmado: {link}")
                else:
                    print(f"Link descartado: {link}")
            
            print(f"Total acumulado: {len(todos_links)} links válidos")
            time.sleep(2)
            
            if not links_pagina:
                print("Nenhum novo link encontrado.")
                break
    finally:
        driver.quit()

    if not todos_links:
        print("Nenhuma notícia sobre FURIA encontrada.")
    else:
        driver = iniciar_driver()
        try:
            lista_links = list(todos_links)
            lista_links.sort()
            
            md_text = montar_markdown(driver, lista_links)

            with open("furia_datalog.md", "w", encoding="utf-8") as f:
                f.write(md_text)

            print(f"Arquivo criado com {len(lista_links)} notícias recentes sobre FURIA!")
        finally:
            driver.quit()