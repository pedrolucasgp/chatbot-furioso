# 🖥️🤖 RushAI
Uma IA Generativa especialista no time da Furia de CS para te ajudar a obter informações de forma rápida.

## O que ela faz?
Com o RushAI você pode fazer qualquer pergunta relacionada ao time de Counter Strike da Furia.



<div align="center">
   <img align="center" height="450" width="550" src="https://i.imgur.com/nmARMeT.png">
</div>

## IA Utlizada:
Gemini

## Bibliotecas Utilizadas:

* Selenium - Biblioteca popular de código aberto utilizada principalmente para automatizar testes em aplicativos web. Ele oferece uma API que permite controlar um navegador web de forma programática, realizando ações como clicar em botões, preencher formulários, navegar em páginas e verificar o conteúdo exibido. Essencialmente, o Selenium simula as interações humanas com o navegador, o que o torna extremamente útil para testes automatizados e também para tarefas de scraping (coleta de dados) na web.

* Langchain_google_genai - Fornece acesso a embeddings gerados por IA (Inteligência Artificial) da Google para aplicações de processamento de linguagem natural (NLP).

* Streamlit - Biblioteca de código aberto em Python projetada para facilitar a criação de aplicativos web interativos para ciência de dados e aprendizado de máquina.

## Instruções para Rodar:
Primeiramente, é necessário clonar o repositório:

```bash
git clone https://github.com/pedrolucasgp/chatbot-furioso.git
```

* Este projeto utiliza o Virtual Environment (venv) para gerenciar um ambiente virtual para a instalação das dependências.

* Para criar o venv e instalar as dependências, abra o Prompt de Comando (cmd) dentro do projeto e utilize a sequência de comandos a seguir:

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

* E por fim, utilize o seguinte comando para rodar o projeto:

```bash
streamlit run main.py
```

## Pronto!
 
* O projeto abrirá automaticamente em seu navegador, mas caso não abra, será fornecido o link de acesso no console.
