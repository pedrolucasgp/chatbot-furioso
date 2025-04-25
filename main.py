import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.chat import ChatPromptTemplate
from PyPDF2 import PdfReader

load_dotenv()

avatar = "https://i.imgur.com/QnTYTCw.png"
user = "https://upload.wikimedia.org/wikipedia/pt/f/f9/Furia_Esports_logo.png"
pdf = PdfReader("Furia_DataBase.pdf")

llm = ChatGoogleGenerativeAI(
    temperature=0.8,
    model="gemini-2.0-flash",
    max_tokens=1000,
    api_key=os.getenv("SECRET_KEY")
)

def read_pdf():
    text = ""

    for page in pdf.pages:
        text += page.extract_text()
    return text

def chatbot_interaction(question):
    context = read_pdf()

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""Seu nome é RushAI e você é um especialista em e-sports, mais especificamente sobre a organização chamada Furia.
         Você deve responder as perguntas focando no time de CS2 da Furia, masculino e feminino.
         Você deve responder as perguntas de forma clara e objetiva.
         Você deve usar como fonte principal esse PDF: {context}.
         Você deve usar informações que não estão no PDF, de sites como HLTV, Liquipedia, Dust2, e redes sociais da Furia.
         Você deve sempre responder em português, mesmo se a pergunta for em inglês.
         Você deve analisar a pergunta e resposta anterior para responder de forma mais precisa a pergunta atual.
         Você deve sempre deve ser politico e amigável, mesmo se a pergunta for ofensiva ou provocativa.
         Você NUNCA deve inventar informações, em hipótese alguma, mesmo se não souber a resposta.
         Você não deve cometer erros de português, mesmo se a pergunta tiver erros de português.
         Você não deve deixar respostas em aberto, ou incompletas, mesmo se a pergunta for aberta ou incompleta.
         """),
        ("user", question),
    ])
    prompt = prompt.format_messages(question=question)
    response = llm.invoke(prompt)

    return response.content

st.set_page_config(
    page_title="RushAI",
    page_icon=avatar
    )

st.markdown(
    f"""
    <div style="text-align: center;">
        <div style=" display: flex; justify-content: center; align-items: center; margin: 20px; gap: 20px;">
            <img src={avatar} width="150">
            <h1>RushAI</h1>
        </div>
        <h5>Olá jogador! Sou o RushAI, a IA mais furiosa e especialista sobre nossa Furia!</h5><br><br>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Como o RushAI pode te ajudar hoje?"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"], avatar=avatar if message["role"] == "assistant" else user).write(message["content"])

if prompt := st.chat_input("Digite sua pergunta aqui..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=user).write(prompt)

    with st.spinner('RushAI está pensando...'):
        response = chatbot_interaction(prompt)
        st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant", avatar=avatar).write(response)
