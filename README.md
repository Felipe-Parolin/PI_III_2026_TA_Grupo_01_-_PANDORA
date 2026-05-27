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
- **PostgreSQL 15+** → https://www.postgresql.org/download/ *(escolha seu sistema operacional)*

---

## Como rodar o projeto

### 1. Baixar o projeto
1. Acesse: https://github.com/Felipe-Parolin/PI_III_2026_TA_Grupo_01_-_PANDORA
2. Clique no botão verde **`< > Code`** → **`Download ZIP`**
3. Extraia o ZIP em qualquer pasta do seu computador

---

### 2. Criar o banco de dados no pgAdmin

1. Abra o **pgAdmin** (instalado junto com o PostgreSQL)
2. Na barra lateral esquerda, expanda **Servers** → clique no seu servidor (geralmente chamado `PostgreSQL 15` ou similar)
3. Digite a senha do PostgreSQL se solicitado
4. Clique com o botão direito em **Databases** → **Create** → **Database...**
5. No campo **Database**, digite: `pandora_db`
6. Clique em **Save**

O banco `pandora_db` aparecerá na lista e está pronto para uso.

---

### 3. Criar o arquivo `.env`

Antes de rodar qualquer comando, crie o arquivo `.env` dentro da pasta `api`.

#### 3.1 Gerar sua chave da Groq
O projeto utiliza a API da Groq para as funcionalidades de IA. Você precisa gerar sua própria chave gratuita:

1. Acesse https://console.groq.com/home e crie uma conta (ou faça login)
2. No menu lateral, clique em **API Keys**
3. Clique em **Create API Key**, dê um nome e copie a chave gerada

> ⚠️ A chave só é exibida uma vez — guarde-a antes de fechar a janela.

#### 3.2 Conteúdo do `.env`

Crie o arquivo `.env` dentro da pasta `api` com o seguinte conteúdo, substituindo o valor de `GROQ_API_KEY`:

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
GROQ_API_KEY=sua_chave_aqui
```

#### 3.3 Ajustar a senha do banco no `settings.py`

Abra o arquivo `api/app/settings.py` e localize o bloco `DATABASES`. Altere o campo `PASSWORD` para a senha do seu PostgreSQL local:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pandora_db',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha_aqui',  # ← altere aqui
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

> ⚠️ Não commite essa alteração — a senha é local e não deve ir para o repositório.

---

### 4. Rodar o Backend (pasta `api`)
Abra o terminal, entre na pasta `api` e siga os passos:

**Windows:**
```bash
cd api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata seed.json
python manage.py runserver
```

**macOS / Linux:**
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata seed.json
python manage.py runserver
```

> O backend estará rodando em `http://127.0.0.1:8000`

---

### 5. Rodar o Frontend (pasta `pandora`)
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

## Para membros da equipe: exportar os dados

> **Atenção:** este passo é apenas para quem **já tem os dados** e quer gerar o arquivo para o repositório.

Com o ambiente virtual ativado e dentro da pasta `api`, rode:

```bash
python manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes --indent 2 > fixtures/seed.json
```

Depois commite o arquivo `api/fixtures/seed.json` no repositório. Os outros membros vão importá-lo automaticamente no passo 4.

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