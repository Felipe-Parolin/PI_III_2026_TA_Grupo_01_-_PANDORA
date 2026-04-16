<div align="center">

<br/>

### **PANDORA · PI III · Grupo 01 · 2026**

### Plataforma Inteligente de Prevenção e Detecção de Falhas em Maquinários via LLM

</div>

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação passo a passo](#-instalação-passo-a-passo)
  - [1. Baixar o projeto](#1-baixar-o-projeto)
  - [2. Configurar o Backend (API Python)](#2-configurar-o-backend-api-python)
  - [3. Configurar o Frontend](#3-configurar-o-frontend)
  - [4. Executar o sistema](#4-executar-o-sistema)
- [Acessos de Teste](#-acessos-de-teste)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Equipe](#-equipe)

---

## 🤖 Sobre o Projeto

O **PANDORA** é uma plataforma web integrada a uma API em Python voltada para a **gestão inteligente de maquinários e equipamentos corporativos**. Por meio de Modelos de Linguagem de Grande Escala (LLMs), o sistema analisa semanticamente os tickets de manutenção em tempo real, detecta padrões de desgaste e diagnostica causas raiz — transformando o modelo de manutenção **reativa** em **preditiva**.

O projeto está alinhado à **ODS 9** da ONU (Indústria, Inovação e Infraestrutura) e foi desenvolvido como Projeto Interdisciplinar III — Sistemas de Informação · 5º A · 2026.

---

## ✨ Funcionalidades

| Módulo | Descrição |
|--------|-----------|
| 🔐 **Controle de Acesso (RBAC)** | Grupos customizáveis com permissões granulares por módulo |
| 📦 **Gestão de Equipamentos** | Cadastro, edição e categorização por setor e criticidade |
| 📋 **Ordens de Serviço** | Abertura manual ou via QR Code, com histórico completo |
| 🤖 **Motor LLM** | Diagnóstico preditivo com base no histórico e manuais técnicos |
| 🎙️ **Registro Multimodal** | Descrição de problemas por texto, áudio (com transcrição) ou foto |
| 📄 **Documentação Técnica** | Anexo de manuais PDF vinculados a equipamentos |
| 📊 **Dashboard Dinâmica** | Interface que se adapta em tempo real às permissões do usuário |

---

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de que você tem instalado em sua máquina:

| Ferramenta | Versão Mínima | Download |
|------------|--------------|----------|
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **pip** | (incluso no Python) | — |
| **Git** *(opcional)* | qualquer | [git-scm.com](https://git-scm.com/) |

> **Sistema Operacional:** Windows 10/11, macOS ou Linux  
> **Navegadores suportados:** Chrome, Edge ou Opera (versões recentes)

---

## 🚀 Instalação passo a passo

### 1. Baixar o projeto

1. Acesse o repositório: [github.com/Felipe-Parolin/PI_III_2026_TA_Grupo_01_-_PANDORA](https://github.com/Felipe-Parolin/PI_III_2026_TA_Grupo_01_-_PANDORA)
2. Clique no botão verde **`< > Code`**
3. Selecione **`Download ZIP`**
4. Extraia o arquivo ZIP em uma pasta de sua preferência

```
📁 PI_III_2026_TA_Grupo_01_-_PANDORA/
├── 📁 backend/
├── 📁 frontend/
└── ...
```

---

### 2. Configurar o Backend (API Python)

Abra o terminal (Prompt de Comando, PowerShell ou Terminal) e navegue até a pasta do backend:

```bash
cd PI_III_2026_TA_Grupo_01_-_PANDORA/backend
```

#### 2.1 — Criar o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

> ✅ Você saberá que funcionou quando `(venv)` aparecer no início da linha do terminal.

#### 2.2 — Instalar as dependências

```bash
pip install -r requirements.txt
```

#### 2.3 — Configurar as variáveis de ambiente

Crie um arquivo chamado **`.env`** dentro da pasta `backend/` com o seguinte conteúdo:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
```

> 💡 Para gerar uma `SECRET_KEY` segura, execute:  
> `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

#### 2.4 — Aplicar as migrações do banco de dados

```bash
python manage.py migrate
```

#### 2.5 — (Opcional) Criar um superusuário próprio

```bash
python manage.py createsuperuser
```

---

### 3. Configurar o Frontend

O frontend é composto por arquivos estáticos (HTML, CSS, JavaScript) — **não requer instalação adicional**.

Basta garantir que a pasta `frontend/` está presente no projeto extraído.

---

### 4. Executar o sistema

#### 4.1 — Iniciar o servidor backend

Com o ambiente virtual ativado e dentro da pasta `backend/`, execute:

```bash
python manage.py runserver
```

O servidor será iniciado em:

```
http://127.0.0.1:8000
```

#### 4.2 — Abrir o frontend

Navegue até a pasta `frontend/` e abra o arquivo `index.html` diretamente no navegador, **ou** acesse via:

```
http://127.0.0.1:8000
```

> ⚠️ **Importante:** mantenha o servidor backend rodando enquanto utiliza a aplicação.

---

## 🔑 Acessos de Teste

Para explorar o sistema sem precisar cadastrar novos usuários, utilize as credenciais preliminares abaixo:

### 👤 Usuário 1 — Felipe Parolin
| Campo | Valor |
|-------|-------|
| **E-mail** | `felipeparolin10@gmail.com` |
| **Senha** | `felipe` |

### 👤 Usuário 2 — Gabriel da Cunha
| Campo | Valor |
|-------|-------|
| **E-mail** | `gabrieldacunha51@gmail.com` |
| **Senha** | `gabriel` |

> 🔒 Cada usuário possui permissões distintas conforme o grupo ao qual pertence. Explore o sistema com ambos para observar as diferenças de interface e acesso.

---

## 📁 Estrutura do Projeto

```
PI_III_2026_TA_Grupo_01_-_PANDORA/
│
├── 📁 backend/                  # API REST em Python (Django)
│   ├── 📁 core/                 # Configurações principais do projeto
│   ├── 📁 usuarios/             # Módulo de usuários e grupos (RBAC)
│   ├── 📁 equipamentos/         # Módulo de gestão de ativos
│   ├── 📁 ordens_servico/       # Módulo de ordens de serviço
│   ├── 📁 llm/                  # Motor de análise via LLM
│   ├── 📄 manage.py
│   └── 📄 requirements.txt
│
├── 📁 frontend/                 # Interface web (HTML/CSS/JS)
│   ├── 📄 index.html            # Ponto de entrada / Login
│   ├── 📁 pages/                # Páginas da aplicação
│   ├── 📁 assets/               # Imagens, ícones e fontes
│   └── 📁 js/                   # Scripts e consumo da API
│
└── 📄 README.md
```

---

## 👥 Equipe

| RA | Nome |
|----|------|
| 116758 | Eduardo Souza Gomes |
| 116276 | Felipe Antonio Parolin |
| 116849 | Gabriel Eduardo da Cunha |
| 116743 | Gabriel Moi Stensen |
| 117224 | Matheus Henrique Araujo Silva |
| 116305 | Rafael Donizete Mantoan |

**Curso:** Sistemas de Informação  
**Disciplina:** Projeto Interdisciplinar III  
**Turma:** 5º A · 2026  

---

## 🔗 Links Úteis

| Recurso | Link |
|---------|------|
| 📦 Repositório | [GitHub](https://github.com/Felipe-Parolin/PI_III_2026_TA_Grupo_01_-_PANDORA) |
| 📋 Kanban / Cronograma | [GitHub Projects](https://github.com/users/Felipe-Parolin/projects/2/views/1) |
| 🌐 ODS 9 — ONU | [brasil.un.org](https://brasil.un.org/pt-br/sdgs/9) |

---

<div align="center">

<br/>

**PANDORA · PI III · Grupo 01 · 2026**

</div>