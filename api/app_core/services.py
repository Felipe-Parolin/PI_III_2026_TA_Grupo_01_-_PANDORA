from groq import APIConnectionError, APIStatusError, APITimeoutError, Groq
from django.conf import settings
import json
import os


class GroqServiceError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


def format_groq_error(error):
    response = getattr(error, 'response', None)
    if response is None:
        return str(error)

    try:
        data = response.json()
    except Exception:
        return getattr(response, 'text', None) or str(error)

    detail = data.get('error', data)
    if isinstance(detail, dict):
        return detail.get('message') or detail.get('error') or json.dumps(detail, ensure_ascii=False)
    return str(detail)


def get_groq_client():
    api_key = getattr(settings, 'GROQ_API_KEY', None) or os.getenv('GROQ_API_KEY') or os.getenv('API_KEY')
    if not api_key:
        raise GroqServiceError('GROQ_API_KEY não configurada no ambiente.', status_code=503)
    return Groq(api_key=api_key)

def transcrever_audio(caminho_audio):
    client = get_groq_client()
    try:
        with open(caminho_audio, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(caminho_audio), file.read()),
                model="whisper-large-v3",
                language="pt",
                temperature=0.0
            )
            return transcription.text
    except APIStatusError as e:
        raise GroqServiceError(format_groq_error(e), status_code=e.status_code) from e
    except (APIConnectionError, APITimeoutError) as e:
        raise GroqServiceError('Falha de conexão com o serviço de transcrição.', status_code=502) from e
    except Exception as e:
        raise GroqServiceError(str(e), status_code=502) from e

def _extrair_json_resposta(conteudo):
    try:
        return json.loads(conteudo)
    except json.JSONDecodeError:
        inicio = conteudo.find('{')
        fim = conteudo.rfind('}')
        if inicio != -1 and fim != -1 and fim > inicio:
            return json.loads(conteudo[inicio:fim + 1])
        raise


def _formatar_historico_para_prompt(historico_equipamento):
    if not historico_equipamento:
        return 'Nenhuma OS anterior relacionada foi encontrada.'

    linhas = []
    for os_item in historico_equipamento[:8]:
        linhas.append(
            "\n".join([
                f"- OS #{os_item.get('id', 'N/A')}",
                f"  Status: {os_item.get('status') or 'N/A'}",
                f"  Urgencia: {os_item.get('urgencia') or 'N/A'}",
                f"  Problema: {os_item.get('problema') or 'N/A'}",
                f"  Solucao aplicada: {os_item.get('solucao') or 'Sem solucao registrada'}",
            ])
        )
    return "\n".join(linhas)


def analisar_com_groq(texto_problema, historico_equipamento=None, contexto_os=None):
    """Gera análise técnica formatada em tópicos."""
    try:
        client = get_groq_client()
        historico_texto = _formatar_historico_para_prompt(historico_equipamento or [])
        contexto_texto = contexto_os or 'Sem contexto estruturado adicional.'
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
                {
                    "role": "user",
                    "content": (
                        f"Contexto da OS:\n{contexto_texto}\n\n"
                        f"Historico relacionado do equipamento:\n{historico_texto}\n\n"
                        f"Problema atual:\n{texto_problema}"
                    )
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2, 
            response_format={"type": "json_object"}
        )
        return _extrair_json_resposta(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"diagnostico": "Erro", "solucao": str(e), "urgencia": "baixa"}


def sugerir_solucao_os_com_groq(os_data, historico_equipamento=None):
    try:
        client = get_groq_client()
        historico_texto = _formatar_historico_para_prompt(historico_equipamento or [])
        contexto_os = "\n".join([
            f"OS atual: #{os_data.get('id')}",
            f"Equipamento: {os_data.get('equipamento_nome') or 'N/A'}",
            f"ID interno: {os_data.get('equipamento_id_interno') or 'N/A'}",
            f"Tipo do equipamento: {os_data.get('equipamento_tipo') or 'N/A'}",
            f"Setor: {os_data.get('equipamento_setor_nome') or 'N/A'}",
            f"Status da OS: {os_data.get('status') or 'N/A'}",
            f"Urgencia informada: {os_data.get('urgencia') or 'N/A'}",
            f"Descricao do problema: {os_data.get('descricao_problema') or 'N/A'}",
        ])

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """Voce e um especialista senior em manutencao industrial.
                    Gere uma sugestao tecnica pratica para a OS atual usando a descricao,
                    dados do equipamento e historico de OS do mesmo equipamento.
                    Nao invente dados que nao foram fornecidos. Se faltar evidencia, deixe isso claro.
                    A solucao deve ser acionavel, em passos numerados, e adequada para um tecnico registrar ou adaptar.
                    Responda somente JSON valido no formato:
                    {
                      "diagnostico": "Hipotese tecnica principal em ate 3 frases.",
                      "solucao": "1. Passo inicial\\n2. Passo seguinte\\n3. Passo final",
                      "historico_relacionado": "Como o historico influenciou a sugestao.",
                      "alertas": "Cuidados de seguranca ou verificacoes antes da intervencao.",
                      "urgencia_sugerida": "Baixa, Media, Alta ou Critica"
                    }"""
                },
                {
                    "role": "user",
                    "content": (
                        f"Dados da OS atual:\n{contexto_os}\n\n"
                        f"Historico do mesmo equipamento:\n{historico_texto}\n\n"
                        "Gere uma possivel solucao tecnica para esta ordem de servico."
                    )
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return _extrair_json_resposta(chat_completion.choices[0].message.content)
    except APIStatusError as e:
        raise GroqServiceError(format_groq_error(e), status_code=e.status_code) from e
    except (APIConnectionError, APITimeoutError) as e:
        raise GroqServiceError('Falha de conexao com o servico de IA.', status_code=502) from e
    except Exception as e:
        raise GroqServiceError(str(e), status_code=502) from e
