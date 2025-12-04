import google.generativeai as genai
import yaml
import time
import json

try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    GOOGLE_API_KEY = config['GOOGLE_API_KEY']

    genai.configure(api_key=GOOGLE_API_KEY)

    print("Setup concluído! API Key carregada\n")

    start_time = time.time()
    print("--- Iniciando modelo ---\n")

    model_flash = genai.GenerativeModel('gemini-2.5-flash')

    quantidade = input("Digite a quantidade de dados que deseja criar: ")
    campos = input("Por fim, digite os campos obrigatórios: ")

    prompt_json = f"Gere {quantidade} dados para teste de sistema. Campos obrigatórios {campos}. Saída: Apenas um JSON Array puro. Sem blocos de código markdown(```json). Sem textos introdutórios."

    print("\nSolicitando dados JSON...\n")
    response = model_flash.generate_content(prompt_json)

    texto_limpo = response.text.replace("```json", "").replace("```", "").strip()

    end_time = time.time()

    print(f"Tempo para gerar: {end_time - start_time:.2f} segundos\n")
    print(texto_limpo)

    dados = json.loads(texto_limpo)

    print(f"\nTotal de dados gerados: {len(dados)}")

except FileNotFoundError:
    print("Erro: Crie o arquivo config.yaml")
except KeyError:
    print("Erro: Verifique se a chave no yaml chama-se 'GOOGLE_API_KEY'")