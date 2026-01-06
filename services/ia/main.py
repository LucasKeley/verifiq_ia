import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core. exceptions import NotFound

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-2.5-flash-lite"


mapa_de_patologia = '/home/lucas/Projetos/verifiq_ia/data/Mapa de Patologia.csv'

def carrega(nome_do_arquivo):
  try:
    with open(nome_do_arquivo, "r") as arquivo:
      dados = arquivo.read()
      return dados
  except IOError as e:
    print(f"Erro: {e}")

dados = carrega(mapa_de_patologia)

prompt_sistema = f"""Você é um engenheiro civil especializado em inspeções técnicas de edifícios. Seu único objetivo é
fornecer sugestões de soluções para patologias identificadas nessas inspeções. As respostas devem ser diretas e técnicas,
podendo ter um tamanho curto ou moderado, mas sempre focadas na resolução do problema. As sugestões serão colocadas em um
relatório técnico, porém não precisa de um modelo formal—apenas um parágrafo objetivo com a solução proposta.
Caso o usuário faça perguntas sobre outros temas, não responda e ignore a solicitação, limitando-se exclusivamente ao escopo das soluções
para patologias em patologias em edificações.  

 Use como contexto para responder as perguntas os dados {dados} """  

prompt_usuario = 'Responda com uma lista de 4 elementos. TETO: Infiltração, possível problema de calha sem impermeabilização ou danificada, Motor chopeira: Benfeitoria de troca de motor de chopeira, porém sem fixação;, Saída de gás: Saída do queimador obstruída/danificada, Sauna a vapor: Problemas na saída do vapor, escorrendo água;'

configuração_modelo = {
    "temperature" : 0.5,
    "top_p" : 0.95,
    "top_k" : 40,
    "max_output_tokens" : 1000,
    "response_mime_type" : "text/plain"
}

try:
  llm = genai.GenerativeModel(
      model_name=MODELO_ESCOLHIDO,
      system_instruction=prompt_sistema,
      generation_config=configuração_modelo
  )

  resposta = llm.generate_content(prompt_usuario)
  print("Resposta Gerada: {}".format(resposta.text))

except NotFound as e:
  print(f"Erro no nome do modode: {e}")
