import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from llama_cpp import Llama

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
llm_local = Llama(
    model_path="models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf",
    n_ctx=2048,
    verbose=False
)

def gerar_query(prompt):
    system_prompt = """
    Você é um tradutor de perguntas para SQL na tabela 'Games'.
    Retorne APENAS o comando SQL puro. Não use explicações, não use markdown e não use crases (```).

    Colunas da tabela 'Games':
    - appid: ID do jogo
    - name: Nome do jogo
    - img_icon_url: URL da imagem
    - playtime_forever: Tempo total geral (minutos)
    - playtime_windows_forever: Tempo no Windows (minutos)
    - playtime_linux_forever: Tempo no Linux (minutos)
    - playtime_deck_forever: Tempo no Steam Deck (minutos)
    - playtime_disconnected: Tempo offline (minutos)
    - rtime_last_played: Última data jogada

    REGRAS:
    1. O SELECT deve conter SEMPRE as colunas: appid, img_icon_url, name.
    2. Além das três colunas acima, inclua também a coluna de tempo específica que o usuário pediu.

    EXEMPLOS:

    Pergunta: Quais os 5 jogos mais jogados no geral?
    SELECT appid, img_icon_url, name, playtime_forever FROM Games ORDER BY playtime_forever DESC LIMIT 5

    Pergunta: Quais jogos eu joguei no linux?
    SELECT appid, img_icon_url, name, playtime_linux_forever FROM Games WHERE playtime_linux_forever > 0
    """
    response = llm_local.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        temperature=0.1,
        stop=["```"]
        
    )
    
    return response["choices"][0]["message"]["content"].strip().removeprefix("```sql").removesuffix("```").strip()

def formatar_resposta(prompt, resultado):
    system_prompt = """
    Você é um assistente que formata resultados de consultas em banco de dados 
    em respostas amigáveis e legíveis em linguagem natural para o usuário.
    Atue exclusivamente como um fornecedor de dados. Apresente as informações solicitadas de forma objetiva e encerre o output. 
    Não use frases de transição como 'Espero que ajude', não faça perguntas e não sugira próximos passos.
    Os dados são de um único usuário. Não alucine. Não invente dados.
    Os valores de tempo estão em minutos. Converta para horas e minutos ao apresentar pro usuário.
    Para montar URLs de imagem, use SOMENTE a estrutura https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{img_icon_url}.jpg. 
    Nunca invente URLs ou use outros valores no lugar do appid E img_icon_url.
    Quando a resposta for uma lista de jogos, inclua o ícone de cada jogo usando markdown de imagem: ![nome do jogo](url completa). 
    Quando a resposta mencionar apenas um jogo ou for uma resposta direta sem lista, não inclua imagens.
    Sempre inclua o tempo de horas jogadas na resposta.
    .
    """
    conteudo = f"Pergunta do usuário: {prompt}\n\nResultado da consulta: {resultado}"
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents = conteudo,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )
    
    return response.text

