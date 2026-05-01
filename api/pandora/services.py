from groq import Groq
import json
import os

API_KEY = os.getenv("API_KEY")


def transcrever_audio(caminho_audio):
    client = Groq(api_key=API_KEY)
    try:
        with open(caminho_audio, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(caminho_audio, file.read()),
                model="whisper-large-v3",
                language="pt",
                temperature=0.0
            )
            return transcription.text
    except Exception as e:
        print(f"Erro: {e}")
        return None

def analisar_com_groq(texto_problema):
    """Gera análise técnica formatada em tópicos."""
    client = Groq(api_key=API_KEY)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """Você é um Engenheiro de Manutenção Master. 
                    Ao descrever a solução, use obrigatoriamente tópicos numerados e quebras de linha (\n) entre cada passo.
                    Responda estritamente neste formato JSON:
                    {
                        "diagnostico": "Explicação técnica curta.",
                        "solucao": "1. Primeiro passo\n2. Segundo passo\n3. Terceiro passo",
                        "urgencia": "alta, media ou baixa"
                    }"""
                },
                {"role": "user", "content": f"Analise: {texto_problema}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2, 
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"diagnostico": "Erro", "solucao": str(e), "urgencia": "baixa"}