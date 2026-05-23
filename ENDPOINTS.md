<div align="center">
<br/>

### PANDORA
**Documentação de Endpoints da API REST**
Projeto Interdisciplinar III · Sistemas de Informação · 5A · 2026
<br/>
</div>

---

## Informações Gerais

| Propriedade | Valor |
|-------------|-------|
| URL Base | `http://127.0.0.1:8000` |
| Formato | `application/json` |
| Autenticação | `Authorization: Bearer <access_token>` |
| Upload de arquivos | `multipart/form-data` |
| Framework | Django REST Framework com DefaultRouter |

---

## Autenticação

> Os endpoints de autenticação não exigem token.

### `POST /authentication/token/`
Realiza login e retorna os tokens JWT.

**Request Body:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `email` | string | Sim | E-mail do usuário cadastrado |
| `password` | string | Sim | Senha do usuário |

**Response `200 OK`:**
```json
{
  "access": "<token_de_acesso>",
  "refresh": "<token_de_refresh>",
  "usuario": {
    "id": 1,
    "nome_usuario": "Felipe",
    "empresa_id": 1
  },
  "permissoes": ["ver_equipamentos", "editar_os"]
}
```

| Código | Descrição |
|--------|-----------|
| `200` | Autenticado com sucesso |
| `400` | E-mail ou senha não informados |
| `401` | Credenciais inválidas |

---

### `POST /authentication/token/refresh/`
Gera um novo `access` token a partir de um `refresh` token válido.

**Request Body:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `refresh` | string | Sim | Token de refresh obtido no login |

**Response `200 OK`:**
```json
{
  "access": "<novo_token_de_acesso>"
}
```

---

## Padrão de Rotas

O Django REST Framework com `DefaultRouter` gera automaticamente os seguintes padrões para cada recurso:

| Método | URL | Ação |
|--------|-----|------|
| `GET` | `/api/{recurso}/` | Lista todos os registros |
| `POST` | `/api/{recurso}/` | Cria um novo registro |
| `GET` | `/api/{recurso}/{id}/` | Retorna um registro pelo ID |
| `PUT` | `/api/{recurso}/{id}/` | Atualiza todos os campos do registro |
| `PATCH` | `/api/{recurso}/{id}/` | Atualiza campos específicos |
| `DELETE` | `/api/{recurso}/{id}/` | Remove o registro pelo ID |

---

## Recursos

- [Empresas](#empresas)
- [Setores](#setores)
- [Usuários](#usuários)
- [Permissões](#permissões)
- [Grupos](#grupos)
- [Equipamentos](#equipamentos)
- [Ordens de Serviço](#ordens-de-serviço)
- [Histórico de OS](#histórico-de-os)
- [Anexos de OS](#anexos-de-os)
- [Categorias de Documento](#categorias-de-documento)
- [Documentos de Equipamento](#documentos-de-equipamento)
- [Análises LLM](#análises-llm)

---

## Empresas

**Base URL:** `/api/empresas/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/empresas/` | Lista todas as empresas |
| `POST` | `/api/empresas/` | Cria uma nova empresa |
| `GET` | `/api/empresas/{id}/` | Retorna uma empresa específica |
| `PUT` | `/api/empresas/{id}/` | Atualiza completamente uma empresa |
| `PATCH` | `/api/empresas/{id}/` | Atualiza parcialmente uma empresa |
| `DELETE` | `/api/empresas/{id}/` | Remove uma empresa |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome_empresa` | string | Sim | Nome/razão social da empresa |
| `cnpj` | string | Não | CNPJ da empresa |
| `email_empresa` | string | Não | E-mail de contato |
| `telefone` | string | Não | Telefone de contato |
| `endereco` | string | Não | Endereço completo |

---

## Setores

**Base URL:** `/api/setores/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/setores/` | Lista todos os setores |
| `POST` | `/api/setores/` | Cria um novo setor |
| `GET` | `/api/setores/{id}/` | Retorna um setor específico |
| `PUT` | `/api/setores/{id}/` | Atualiza completamente um setor |
| `PATCH` | `/api/setores/{id}/` | Atualiza parcialmente um setor |
| `DELETE` | `/api/setores/{id}/` | Remove um setor |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome_setor` | string | Sim | Nome do setor (ex: Produção, Manutenção) |
| `empresa` | integer | Sim | ID da empresa à qual o setor pertence |

---

## Usuários

**Base URL:** `/api/usuarios/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/usuarios/` | Lista todos os usuários |
| `POST` | `/api/usuarios/` | Cria um novo usuário |
| `GET` | `/api/usuarios/{id}/` | Retorna um usuário específico |
| `PUT` | `/api/usuarios/{id}/` | Atualiza completamente um usuário |
| `PATCH` | `/api/usuarios/{id}/` | Atualiza parcialmente um usuário |
| `DELETE` | `/api/usuarios/{id}/` | Remove um usuário |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome_usuario` | string | Sim | Nome de exibição do usuário |
| `email` | string | Sim | E-mail de login (deve ser único) |
| `password` | string | Sim | Senha (armazenada com hash) |
| `empresa` | integer | Não | ID da empresa vinculada ao usuário |
| `grupos` | array | Não | Lista de IDs dos grupos de permissão |

---

## Permissões

**Base URL:** `/api/permissoes/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/permissoes/` | Lista todas as permissões |
| `POST` | `/api/permissoes/` | Cria uma nova permissão |
| `GET` | `/api/permissoes/{id}/` | Retorna uma permissão específica |
| `PUT` | `/api/permissoes/{id}/` | Atualiza completamente uma permissão |
| `PATCH` | `/api/permissoes/{id}/` | Atualiza parcialmente uma permissão |
| `DELETE` | `/api/permissoes/{id}/` | Remove uma permissão |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome_permissao` | string | Sim | Identificador da permissão (ex: `ver_equipamentos`) |
| `descricao` | string | Não | Descrição da permissão |

---

## Grupos

**Base URL:** `/api/grupos/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/grupos/` | Lista todos os grupos |
| `POST` | `/api/grupos/` | Cria um novo grupo |
| `GET` | `/api/grupos/{id}/` | Retorna um grupo específico |
| `PUT` | `/api/grupos/{id}/` | Atualiza completamente um grupo |
| `PATCH` | `/api/grupos/{id}/` | Atualiza parcialmente um grupo |
| `DELETE` | `/api/grupos/{id}/` | Remove um grupo |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome_grupo` | string | Sim | Nome do grupo (ex: Administrador, Técnico) |
| `permissoes` | array | Não | Lista de IDs das permissões vinculadas |

---

## Equipamentos

**Base URL:** `/api/equipamentos/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/equipamentos/` | Lista todos os equipamentos |
| `POST` | `/api/equipamentos/` | Cadastra um novo equipamento |
| `GET` | `/api/equipamentos/{id}/` | Retorna detalhes de um equipamento |
| `PUT` | `/api/equipamentos/{id}/` | Atualiza completamente um equipamento |
| `PATCH` | `/api/equipamentos/{id}/` | Atualiza parcialmente um equipamento |
| `DELETE` | `/api/equipamentos/{id}/` | Remove um equipamento |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome_equipamento` | string | Sim | Nome ou modelo do equipamento |
| `tipo_equipamento` | string | Sim | Tipo/categoria do equipamento |
| `status` | string | Sim | Status atual (ex: `Ativo`, `Inativo`) |
| `id_interno` | integer | Sim | Identificador interno do equipamento |
| `qr_code_token` | string | Sim | Token único para geração do QR Code |
| `setor` | integer | Sim | ID do setor onde está alocado |
| `empresa` | integer | Não | ID da empresa proprietária |
| `foto` | file | Não | Foto do equipamento (`multipart/form-data`) |
| `manual_tecnico` | file | Não | Manual técnico em arquivo (`multipart/form-data`) |

---

## Ordens de Serviço

**Base URL:** `/api/ordens-servico/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/ordens-servico/` | Lista todas as ordens de serviço |
| `POST` | `/api/ordens-servico/` | Cria uma nova OS |
| `GET` | `/api/ordens-servico/{id}/` | Retorna detalhes de uma OS |
| `PUT` | `/api/ordens-servico/{id}/` | Atualiza completamente uma OS |
| `PATCH` | `/api/ordens-servico/{id}/` | Atualiza parcialmente uma OS |
| `DELETE` | `/api/ordens-servico/{id}/` | Remove uma OS |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `descricao_problema` | string | Sim | Descrição detalhada do problema |
| `urgencia` | string | Sim | Nível de urgência (ex: `Baixa`, `Média`, `Alta`) |
| `status` | string | Sim | `Aberto` \| `Em Andamento` \| `Concluido` |
| `equipamento` | integer | Sim | ID do equipamento relacionado |
| `usuario_abertura` | integer | Sim | ID do usuário que abriu a OS |
| `foto_problema` | file | Não | Foto do problema (`multipart/form-data`) |
| `descricao_solucao` | string | Não | Descrição da solução aplicada |
| `usuario_tecnico` | integer | Não | ID do técnico responsável *(preenchido automaticamente)* |
| `data_abertura` | datetime | Não | Data/hora de criação *(gerada automaticamente)* |
| `data_fechamento` | datetime | Não | Data/hora de conclusão |
| `empresa` | integer | Não | ID da empresa *(preenchido automaticamente)* |

> **Regra de negócio:** ao alterar o `status` para `Em Andamento` ou `Concluido` via `PUT`/`PATCH`, o campo `usuario_tecnico` é preenchido automaticamente com o usuário autenticado na requisição.

**Campos extras somente leitura na resposta (via serializer):**
| Campo | Descrição |
|-------|-----------|
| `usuario_abertura_nome` | Nome do usuário que abriu a OS |
| `usuario_tecnico_nome` | Nome do técnico responsável |
| `equipamento_nome` | Nome do equipamento |
| `equipamento_id_interno` | ID interno do equipamento |
| `equipamento_qr_token` | Token QR Code do equipamento |
| `equipamento_tipo` | Tipo do equipamento |
| `equipamento_setor_id` | ID do setor do equipamento |
| `equipamento_setor_nome` | Nome do setor do equipamento |
| `equipamento_foto` | URL da foto do equipamento |
| `equipamento_documentos` | Lista de documentos vinculados ao equipamento |

---

## Histórico de OS

**Base URL:** `/api/historicos-os/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/historicos-os/` | Lista todos os registros de histórico |
| `POST` | `/api/historicos-os/` | Cria um novo registro |
| `GET` | `/api/historicos-os/{id}/` | Retorna um registro específico |
| `PUT` | `/api/historicos-os/{id}/` | Atualiza um registro |
| `PATCH` | `/api/historicos-os/{id}/` | Atualiza parcialmente um registro |
| `DELETE` | `/api/historicos-os/{id}/` | Remove um registro |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `os` | integer | Sim | ID da OS relacionada |
| `usuario_modificacao` | integer | Sim | ID do usuário que realizou a alteração |
| `campo_alterado` | string | Não | Nome do campo que foi modificado |
| `valor_anterior` | string | Não | Valor do campo antes da alteração |
| `valor_novo` | string | Não | Valor do campo após a alteração |
| `comentario` | string | Não | Comentário livre sobre a alteração |
| `data_modificacao` | datetime | Não | Data/hora do registro *(gerada automaticamente)* |

> **Nota:** os registros são ordenados por `-data_modificacao` (mais recentes primeiro). O histórico é gerado automaticamente pela API ao criar ou atualizar uma OS — criação manual via este endpoint é reservada a casos excepcionais.

---

## Anexos de OS

**Base URL:** `/api/anexos-os/`

> Requisições de criação devem usar `Content-Type: multipart/form-data`.

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/anexos-os/` | Lista todos os anexos |
| `POST` | `/api/anexos-os/` | Faz upload de um novo anexo |
| `GET` | `/api/anexos-os/{id}/` | Retorna um anexo específico |
| `PUT` | `/api/anexos-os/{id}/` | Atualiza um anexo |
| `PATCH` | `/api/anexos-os/{id}/` | Atualiza parcialmente um anexo |
| `DELETE` | `/api/anexos-os/{id}/` | Remove um anexo |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `ordem_servico` | integer | Sim | ID da OS à qual o arquivo será vinculado |
| `arquivo` | file | Sim | Arquivo a ser enviado |
| `descricao` | string | Não | Descrição ou nome do anexo |

---

## Categorias de Documento

**Base URL:** `/api/categorias-documento/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/categorias-documento/` | Lista todas as categorias |
| `POST` | `/api/categorias-documento/` | Cria uma nova categoria |
| `GET` | `/api/categorias-documento/{id}/` | Retorna uma categoria específica |
| `PUT` | `/api/categorias-documento/{id}/` | Atualiza completamente uma categoria |
| `PATCH` | `/api/categorias-documento/{id}/` | Atualiza parcialmente uma categoria |
| `DELETE` | `/api/categorias-documento/{id}/` | Remove uma categoria |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome_categoria` | string | Sim | Nome da categoria (ex: Manual, Certificado, NF) |
| `descricao` | string | Não | Descrição complementar |

---

## Documentos de Equipamento

**Base URL:** `/api/documentos-equipamento/`

> Requisições de criação devem usar `Content-Type: multipart/form-data`.

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/documentos-equipamento/` | Lista todos os documentos |
| `POST` | `/api/documentos-equipamento/` | Faz upload de um novo documento |
| `GET` | `/api/documentos-equipamento/{id}/` | Retorna um documento específico |
| `PUT` | `/api/documentos-equipamento/{id}/` | Atualiza um documento |
| `PATCH` | `/api/documentos-equipamento/{id}/` | Atualiza parcialmente um documento |
| `DELETE` | `/api/documentos-equipamento/{id}/` | Remove um documento |

**Campos:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `equipamento` | integer | Sim | ID do equipamento ao qual o documento pertence |
| `categoria` | integer | Não | ID da categoria do documento |
| `arquivo` | file | Sim | Arquivo a ser enviado |
| `nome_arquivo` | string | Não | Nome descritivo do arquivo |

---

## Análises LLM

**Base URL:** `/api/analises-llm/`

Além das rotas padrão, este recurso possui três endpoints customizados para integração com o modelo de linguagem via **Groq**.

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/analises-llm/` | Lista todas as análises realizadas |
| `POST` | `/api/analises-llm/` | Cria um registro de análise |
| `GET` | `/api/analises-llm/{id}/` | Retorna uma análise específica |
| `PUT` | `/api/analises-llm/{id}/` | Atualiza uma análise |
| `PATCH` | `/api/analises-llm/{id}/` | Atualiza parcialmente uma análise |
| `DELETE` | `/api/analises-llm/{id}/` | Remove uma análise |
| `POST` | `/api/analises-llm/analisar/` | Envia descrição de manutenção para análise pelo LLM |
| `POST` | `/api/analises-llm/sugerir-solucao-os/` | Sugere solução para uma OS com base no histórico do equipamento |
| `POST` | `/api/analises-llm/transcrever/` | Transcreve um arquivo de áudio para texto via LLM |

---

### `POST /api/analises-llm/analisar/`
Envia uma descrição de problema ou ticket de manutenção para análise pelo modelo LLM.

**Request Body:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `descricao` | string | Sim | Texto com a descrição do problema a ser analisado |
| `historico_equipamento` | array | Não | Lista de OSs anteriores do equipamento para enriquecer o contexto |
| `os_id` | integer | Não | ID da OS vinculada (incluso no contexto enviado ao LLM) |

**Response `200 OK`:**
```json
{
  "diagnostico": "Possível falha no rolamento do motor...",
  "sugestoes": ["Verificar lubrificação", "Substituir rolamento"],
  "classificacao": "Falha mecânica"
}
```

| Código | Descrição |
|--------|-----------|
| `200` | Análise realizada com sucesso |
| `400` | Campo `descricao` não informado |

---

### `POST /api/analises-llm/sugerir-solucao-os/`
Sugere uma solução para uma OS aberta com base nos dados da OS e no histórico de manutenções do equipamento. Retorna a sugestão do LLM junto com o número de OSs históricas consideradas.

**Request Body:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `os_id` | integer | Sim | ID da OS para a qual se deseja sugestão |

**Response `200 OK`:**
```json
{
  "diagnostico": "...",
  "sugestoes": ["..."],
  "classificacao": "...",
  "historico_considerado": 3
}
```

| Código | Descrição |
|--------|-----------|
| `200` | Sugestão gerada com sucesso |
| `400` | Campo `os_id` não informado |
| `403` | Usuário sem empresa vinculada |
| `404` | OS não encontrada ou fora da empresa do usuário |

---

### `POST /api/analises-llm/transcrever/`
Transcreve um arquivo de áudio para texto via LLM.

> Requisição deve usar `Content-Type: multipart/form-data`.

**Request Body:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `audio` | file | Sim | Arquivo de áudio (mp3, mp4, wav, webm, m4a) |

**Response `200 OK`:**
```json
{
  "transcricao": "O equipamento está fazendo um barulho estranho desde ontem..."
}
```

| Código | Descrição |
|--------|-----------|
| `200` | Transcrição realizada com sucesso |
| `400` | Arquivo de áudio não enviado |
| `502` | Não foi possível transcrever o áudio |

---

## Equipe

| RA | Nome |
|----|------|
| 116758 | Eduardo Souza Gomes |
| 116276 | Felipe Antonio Parolin |
| 116849 | Gabriel Eduardo da Cunha |
| 116743 | Gabriel Moi Stensen |
| 117224 | Matheus Henrique Araujo Silva |
| 116305 | Rafael Donizete Mantoan |

---

📋 **Kanban do projeto:** https://github.com/users/Felipe-Parolin/projects/2/views/1