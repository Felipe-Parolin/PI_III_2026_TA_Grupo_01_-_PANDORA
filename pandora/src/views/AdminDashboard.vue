<template>
  <div class="admin-page">

    <!-- ── Header ─────────────────────────────────── -->
    <header class="admin-header">
      <div class="header-brand">
        <div class="brand-mark">P</div>
        <div>
          <p class="header-eyebrow">Pandora — Painel do Proprietário</p>
          <h1 class="header-title">Gerenciamento de Empresas</h1>
        </div>
      </div>
      <div class="header-actions">
        
        <button class="btn-logout" @click="sair">Sair</button>
      </div>
    </header>

    <!-- ── Loading ────────────────────────────────── -->
    <div v-if="carregando" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando dados do sistema...</p>
    </div>

    <template v-else>

      <!-- ── Tabela de empresas ──────────────────── -->
      <section class="table-section">
        <div class="section-header">
          <div class="kpi-inline">
            <div class="kpi-icon blue">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            </div>
            <div>
              <span class="kpi-value">{{ empresas.length }}</span>
              <span class="kpi-label">Empresas cadastradas</span>
            </div>
          </div>
          <button class="btn-nav primary" @click="mostrarForm = !mostrarForm">
            {{ mostrarForm ? '✕ Cancelar' : '+ Nova empresa' }}
          </button>
        </div>

        <!-- ── Formulário inline ───────────────── -->
        <div v-if="mostrarForm" class="form-inline">
          <div class="form-inline-titulo">
            <span class="form-secao-label">Empresa</span>
          </div>
          <div class="form-grid">
            <div class="input-group">
              <label>Nome Fantasia</label>
              <input v-model="form.nome_fantasia" type="text" placeholder="Ex: Pavan Tintas" :disabled="cadastrando" />
            </div>
            <div class="input-group">
              <label>CNPJ</label>
              <input :value="form.cnpj" @input="onCnpj" type="text" placeholder="00.000.000/0001-00" maxlength="18" :disabled="cadastrando" />
            </div>
          </div>

          <div class="form-inline-titulo" style="margin-top: 0.75rem">
            <span class="form-secao-label">Usuário Administrador</span>
          </div>
          <div class="form-grid">
            <div class="input-group">
              <label>Nome</label>
              <input v-model="form.nome_usuario" type="text" placeholder="Ex: João Silva" :disabled="cadastrando" />
            </div>
            <div class="input-group">
              <label>E-mail</label>
              <input v-model="form.email" type="email" placeholder="joao@empresa.com" :disabled="cadastrando" />
            </div>
            <div class="input-group">
              <label>Senha inicial</label>
              <input v-model="form.senha" type="password" placeholder="••••••••" :disabled="cadastrando" />
            </div>
          </div>

          <p v-if="erroForm" class="error-message">{{ erroForm }}</p>
          <p v-if="sucessoForm" class="success-message">{{ sucessoForm }}</p>

          <div class="form-inline-actions">
            <button class="btn-cadastrar" :disabled="cadastrando" @click="cadastrar">
              {{ cadastrando ? 'Cadastrando...' : 'Cadastrar cliente' }}
            </button>
          </div>
        </div>

        <!-- ── Tabela ──────────────────────────── -->
        <div class="table-wrap" :class="{ 'table-mt': mostrarForm }">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Empresa</th>
                <th>CNPJ</th>
                <th>Usuários</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!empresas.length">
                <td colspan="4" class="empty-state">Nenhuma empresa cadastrada ainda.</td>
              </tr>
              <tr v-for="empresa in empresas" :key="empresa.id" class="table-row">
                <td class="td-id">#{{ empresa.id }}</td>
                <td>
                  <div class="empresa-cell">
                    <strong class="empresa-nome">{{ empresa.nome_empresa || empresa.nome_fantasia }}</strong>
                  </div>
                </td>
                <td class="td-mono">{{ empresa.cnpj || '—' }}</td>
                <td>
                  <span class="count-badge">{{ contarPorEmpresa(usuarios, empresa.id) }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </template>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { api } from '../services/api'

const router = useRouter()

const carregando  = ref(true)
const cadastrando = ref(false)
const mostrarForm = ref(false)
const empresas    = ref([])
const usuarios    = ref([])
const erroForm    = ref('')
const sucessoForm = ref('')

const form = reactive({
  nome_fantasia: '',
  cnpj: '',
  nome_usuario: '',
  email: '',
  senha: '',
})

const API_BASE = 'http://127.0.0.1:8000/api'
const getHeaders = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
})

const fetchAll = async () => {
  carregando.value = true
  try {
    const [resEmpresas, resUsuarios] = await Promise.all([
      axios.get(`${API_BASE}/empresas/`, getHeaders()),
      axios.get(`${API_BASE}/usuarios/`, getHeaders()),
    ])
    empresas.value = resEmpresas.data || []
    usuarios.value = resUsuarios.data || []
  } catch (e) {
    console.error('Erro ao carregar dashboard admin:', e)
  } finally {
    carregando.value = false
  }
}

const onCnpj = (e) => {
  const nums = e.target.value.replace(/\D/g, '').slice(0, 14)
  form.cnpj = nums
    .replace(/^(\d{2})(\d)/, '$1.$2')
    .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
    .replace(/\.(\d{3})(\d)/, '.$1/$2')
    .replace(/(\d{4})(\d)/, '$1-$2')
}

const cadastrar = async () => {
  erroForm.value = ''
  sucessoForm.value = ''
  if (!form.nome_fantasia || !form.cnpj || !form.nome_usuario || !form.email || !form.senha) {
    erroForm.value = 'Preencha todos os campos.'
    return
  }
  cadastrando.value = true
  try {
    const resposta = await api.create('owner/onboarding', form)
    sucessoForm.value = `Cliente "${resposta.empresa}" cadastrado com sucesso!`
    Object.keys(form).forEach(k => (form[k] = ''))
    await fetchAll()
    setTimeout(() => {
      mostrarForm.value = false
      sucessoForm.value = ''
    }, 2500)
  } catch (e) {
    erroForm.value = e.response?.data?.detail || 'Erro ao cadastrar cliente.'
  } finally {
    cadastrando.value = false
  }
}

const contarPorEmpresa = (lista, empresaId) =>
  lista.filter(item => {
    const eid = item.empresa?.id ?? item.empresa
    return String(eid) === String(empresaId)
  }).length

const sair = () => {
  localStorage.clear()
  router.push('/')
}

onMounted(fetchAll)
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', system-ui, sans-serif;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  box-sizing: border-box;
}

/* ── Header ─────────────────────────────────────── */
.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1rem 1.5rem;
  box-shadow: 0 2px 8px rgba(15,23,42,0.04);
  flex-wrap: wrap;
}

.header-brand { display: flex; align-items: center; gap: 0.85rem; }

.brand-mark {
  width: 40px; height: 40px;
  border-radius: 11px;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 1.1rem; flex-shrink: 0;
}

.header-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #2563eb; margin: 0; }
.header-title   { font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0; }
.header-actions { display: flex; align-items: center; gap: 0.65rem; flex-wrap: wrap; }

.btn-nav {
  padding: 0.55rem 1.1rem;
  border-radius: 10px; font-size: 0.875rem; font-weight: 600;
  cursor: pointer; border: 1.5px solid #e2e8f0;
  background: #fff; color: #475569;
  transition: all 0.18s; font-family: inherit;
}
.btn-nav:hover { background: #f8fafc; border-color: #cbd5e1; color: #1e293b; }
.btn-nav.primary { background: #2563eb; border-color: #2563eb; color: #fff; }
.btn-nav.primary:hover { background: #1d4ed8; border-color: #1d4ed8; }

.btn-logout {
  padding: 0.55rem 1.1rem; border-radius: 10px;
  font-size: 0.875rem; font-weight: 600; cursor: pointer;
  border: 1.5px solid #fee2e2; background: #fff5f5; color: #b91c1c;
  transition: all 0.18s; font-family: inherit;
}
.btn-logout:hover { background: #fee2e2; }

/* ── Loading ─────────────────────────────────────── */
.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 2rem; color: #64748b; }
.spinner { width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Table section ───────────────────────────────── */
.table-section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(15,23,42,0.04);
}

.section-header {
  display: flex; align-items: center;
  justify-content: space-between; gap: 1rem;
  margin-bottom: 0; flex-wrap: wrap;
}

.kpi-inline { display: flex; align-items: center; gap: 0.85rem; }
.kpi-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.kpi-icon.blue { background: #eff6ff; color: #2563eb; }
.kpi-inline > div:last-child { display: flex; flex-direction: column; gap: 0.1rem; }
.kpi-value { font-size: 1.9rem; font-weight: 800; color: #0f172a; line-height: 1; }
.kpi-label { font-size: 0.82rem; font-weight: 600; color: #64748b; }

/* ── Formulário inline ───────────────────────────── */
.form-inline {
  margin-top: 1.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-inline-titulo { display: flex; align-items: center; }

.form-secao-label {
  font-size: 0.7rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #2563eb;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.input-group { display: flex; flex-direction: column; gap: 0.35rem; }
.input-group label { font-size: 0.8rem; font-weight: 600; color: #475569; }
.input-group input {
  padding: 0.7rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.9rem;
  background: #fff;
  transition: all 0.2s;
  font-family: inherit;
}
.input-group input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.12);
}
.input-group input:disabled { opacity: 0.6; cursor: not-allowed; }

.error-message   { margin: 0; color: #b91c1c; font-size: 0.85rem; font-weight: 600; }
.success-message { margin: 0; color: #15803d; font-size: 0.85rem; font-weight: 600; background: #f0fdf4; border: 1px solid #bbf7d0; padding: 0.55rem 0.8rem; border-radius: 8px; }

.form-inline-actions { display: flex; justify-content: flex-end; }

.btn-cadastrar {
  padding: 0.65rem 1.5rem;
  background: #2563eb; color: #fff;
  border: none; border-radius: 9px;
  font-size: 0.9rem; font-weight: 700;
  cursor: pointer; transition: background 0.18s;
  font-family: inherit;
}
.btn-cadastrar:hover:not(:disabled) { background: #1d4ed8; }
.btn-cadastrar:disabled { opacity: 0.65; cursor: not-allowed; }

/* ── Tabela ──────────────────────────────────────── */
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.table-mt   { margin-top: 1.25rem; }

.data-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.data-table th {
  padding: 0.75rem 1rem; text-align: left;
  font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em;
  text-transform: uppercase; color: #64748b;
  border-bottom: 1px solid #f1f5f9; white-space: nowrap;
}
.data-table td { padding: 1rem; border-bottom: 1px solid #f8fafc; color: #1e293b; vertical-align: middle; }
.table-row:last-child td { border-bottom: none; }
.table-row:hover td { background: #fafbff; }

.td-id   { color: #94a3b8; font-weight: 700; font-size: 0.8rem; white-space: nowrap; }
.td-mono { font-family: monospace; font-size: 0.82rem; color: #475569; white-space: nowrap; }

.empresa-cell    { display: flex; flex-direction: column; gap: 2px; }
.empresa-nome    { font-weight: 700; color: #0f172a; }
.empresa-fantasia { font-size: 0.75rem; color: #64748b; }

.count-badge {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 28px; padding: 0.2rem 0.55rem; border-radius: 20px;
  font-size: 0.78rem; font-weight: 700; background: #f1f5f9; color: #475569;
}

.empty-state { text-align: center; color: #94a3b8; padding: 2.5rem; font-style: italic; }

/* ── Responsivo ──────────────────────────────────── */
@media (max-width: 640px) {
  .admin-page     { padding: 1rem; gap: 1rem; }
  .admin-header   { flex-direction: column; align-items: flex-start; }
  .header-actions { width: 100%; }
  .section-header { flex-direction: column; align-items: flex-start; }
  .section-header .btn-nav { width: 100%; text-align: center; }
  .form-grid      { grid-template-columns: 1fr; }
  .form-inline-actions { justify-content: stretch; }
  .btn-cadastrar  { width: 100%; }
  .data-table th:nth-child(3), .data-table td:nth-child(3) { display: none; }
}
</style>