<div align="center">
<br/>

### PANDORA
**Plataforma Inteligente de Prevenção e Detecção de Falhas em Maquinários via LLM**
Projeto Interdisciplinar III · Sistemas de Informação · 5A · 2026
<br/>
</div>

---

## Sobre o projeto
O PANDORA é uma plataforma web para gestão e prevenção inteligente de falhas em equipamentos corporativos. Através de um motor de IA (LLM), o sistema analisa tickets de manutenção, detecta padrões e sugere diagnósticos — transformando a manutenção reativa em preditiva.

---

## O que você vai precisar instalar
Antes de tudo, instale as ferramentas abaixo caso ainda não as tenha:

- **Python 3.11+** → https://www.python.org/downloads/
- **Node.js** → https://nodejs.org/ *(escolha a versão LTS)*

---

## Como rodar o projeto

### 1. Baixar o projeto
1. Acesse: https://github.com/Felipe-Parolin/PI_III_2026_TA_Grupo_01_-_PANDORA
2. Clique no botão verde **`< > Code`** → **`Download ZIP`**
3. Extraia o ZIP em qualquer pasta do seu computador

---

### 2. Criar o arquivo `.env`

Antes de rodar qualquer comando, crie o arquivo `.env` dentro da pasta `api/pandora`.

#### 2.1 Gerar sua chave da Groq
O projeto utiliza a API da Groq para as funcionalidades de IA. Você precisa gerar sua própria chave gratuita:

1. Acesse https://console.groq.com/home e crie uma conta (ou faça login)
2. No menu lateral, clique em **API Keys**
3. Clique em **Create API Key**, dê um nome e copie a chave gerada

> ⚠️ A chave só é exibida uma vez — guarde-a antes de fechar a janela.

#### 2.2 Conteúdo do `.env`
Com a chave em mãos, crie o arquivo `.env` com o seguinte conteúdo, substituindo o valor de `GROQ_API_KEY`:

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
GROQ_API_KEY=sua_chave_aqui
```

---

### 3. Rodar o Backend (pasta `api`)
Abra o terminal, entre na pasta `api` e siga os passos:

**Windows:**
```bash
cd api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

**macOS / Linux:**
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

> O backend estará rodando em `http://127.0.0.1:8000`

---

### 4. Rodar o Frontend (pasta `pandora`)
Abra **outro terminal** (sem fechar o anterior) e entre na pasta `pandora`, que fica na raiz do projeto.

```bash
cd pandora
npm install
npm run dev
```

> O frontend estará disponível em `http://localhost:5173`

Abra esse endereço no seu navegador para usar o sistema.

---

## Acessos para teste

| E-mail | Senha |
|--------|-------|
| felipeparolin10@gmail.com | felipe10 |
| gabrieldacunha51@gmail.com | gabriel |

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