<template>
  <div class="crud-page">
    <section class="page-header animate-fade-in">
      <p class="eyebrow">Ativos Técnicos</p>
      <h2>Gestão de Equipamentos</h2>
      <p class="page-copy">Cadastre, organize e vincule documentação técnica às máquinas da unidade.</p>
    </section>

    <section class="card form-card animate-fade-in">
      <div class="card-header">
        <h3>{{ editandoId ? 'Editar Equipamento' : 'Novo Equipamento' }}</h3>
        <p>Preencha os dados do ativo e vincule a documentação técnica.</p>
      </div>

      <form @submit.prevent="salvarEquipamento" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label class="field-label">Nome do Equipamento</label>
            <input v-model="form.nome_equipamento" type="text" placeholder="Ex: Torno CNC 01" required />
          </div>
          <div class="input-group">
            <label class="field-label">Tipo / Categoria</label>
            <input v-model="form.tipo_equipamento" type="text" placeholder="Ex: Injetora, Prensa..." required />
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label class="field-label">ID Interno (Código)</label>
            <input
              v-model.number="form.id_interno"
              type="number"
              placeholder="Ex: 1005"
              required
              :class="{ 'input-error': erros.id_interno }"
              @blur="validarCampoUnico('id_interno')"
            />
            <span v-if="erros.id_interno" class="error-msg">{{ erros.id_interno }}</span>
          </div>
          <div class="input-group">
            <label class="field-label">Status Inicial</label>
            <select v-model="form.status" required>
              <option value="Ativo">Ativo</option>
              <option value="Manutenção">Em Manutenção</option>
              <option value="Inativo">Inativo / Reserva</option>
            </select>
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label class="field-label">Setor Responsável</label>
            <select v-model="form.setor" required>
              <option value="" disabled>Selecione um setor...</option>
              <option v-for="s in setores" :key="s.id" :value="s.id">{{ s.nome_setor }}</option>
            </select>
          </div>
          <div class="input-group">
            <label class="field-label">Token do QR Code</label>
            <input
              v-model="form.qr_code_token"
              type="text"
              placeholder="Ex: QR-CNC-01"
              required
              :class="{ 'input-error': erros.qr_code_token }"
              @blur="validarCampoUnico('qr_code_token')"
            />
            <span v-if="erros.qr_code_token" class="error-msg">{{ erros.qr_code_token }}</span>
          </div>
        </div>

        <!-- ── Documentação Técnica ── -->
        <div class="upload-section-container">
          <p class="field-label">Documentação Técnica</p>

          <div class="upload-blocks-row">
            <!-- Fotos -->
            <div class="upload-block">
              <div class="upload-block-header">
                <span class="upload-block-icon">📸</span>
                <div class="upload-block-info">
                  <p class="upload-block-title">Fotos do Equipamento</p>
                  <p class="upload-block-subtitle">opcional</p>
                </div>
                <label for="fotoInput" class="btn-add-file">+ Adicionar foto</label>
                <input type="file" id="fotoInput" @change="handleFotos" accept="image/*" multiple class="hidden-input" />
              </div>

              <div v-if="fotos.length" class="file-chip-list">
                <div v-for="f in fotosExistentes" :key="'existing-'+f.id" class="file-chip foto-chip">
                  <img :src="f.url" class="chip-thumb" />
                  <span class="chip-name">{{ f.nome }}</span>
                  <button type="button" @click="removerFotoExistente(f)" class="chip-remove" title="Remover">×</button>
                </div>
                <div v-for="(f, i) in fotosNovas" :key="'new-'+i" class="file-chip foto-chip foto-chip-new">
                  <img :src="f.preview" class="chip-thumb" />
                  <span class="chip-name">{{ f.nome }}</span>
                  <button type="button" @click="removerFotoNova(i)" class="chip-remove">×</button>
                </div>
              </div>
              <p v-else class="upload-empty">Nenhuma foto adicionada. Aceita PNG e JPG.</p>
            </div>

            <!-- PDFs -->
            <div class="upload-block">
              <div class="upload-block-header">
                <span class="upload-block-icon">📄</span>
                <div class="upload-block-info">
                  <p class="upload-block-title">Manuais Técnicos (PDF)</p>
                  <p class="upload-block-subtitle">opcional</p>
                </div>
                <label for="manualInput" class="btn-add-file">+ Adicionar PDF</label>
                <input type="file" id="manualInput" @change="handleManuais" accept=".pdf" multiple class="hidden-input" />
              </div>

              <div v-if="manuais.length" class="file-chip-list">
                <div v-for="m in manuaisExistentes" :key="'existing-pdf-'+m.id" class="file-chip pdf-chip">
                  <span class="chip-icon">📄</span>
                  <span class="chip-name">{{ m.nome }}</span>
                  <button type="button" @click="removerManualExistente(m)" class="chip-remove" title="Remover">×</button>
                </div>
                <div v-for="(m, i) in manuaisNovos" :key="'new-pdf-'+i" class="file-chip pdf-chip pdf-chip-new">
                  <span class="chip-icon">📄</span>
                  <span class="chip-name">{{ m.nome }}</span>
                  <button type="button" @click="removerManualNovo(i)" class="chip-remove">×</button>
                </div>
              </div>
              <p v-else class="upload-empty">Nenhum PDF adicionado.</p>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="carregando || temErros" class="btn btn-primary">
            {{ carregando ? 'Processando...' : (editandoId ? 'Atualizar Equipamento' : 'Salvar Equipamento') }}
          </button>
          <button v-if="editandoId" type="button" @click="resetForm" class="btn btn-secondary">
            Cancelar
          </button>
        </div>
      </form>
    </section>

    <section class="card table-card animate-fade-in">
      <div class="card-header">
        <h3>Equipamentos Cadastrados</h3>
        <p>{{ equipamentos.length }} ativo(s) registrado(s).</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Setor</th>
              <th>Status</th>
              <th class="col-acoes">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!equipamentos.length">
              <td colspan="5" class="empty-state">Nenhum equipamento cadastrado.</td>
            </tr>
            <tr v-for="equip in equipamentos" :key="equip.id">
              <td><strong>#{{ equip.id_interno }}</strong></td>
              <td>{{ equip.nome_equipamento }}</td>
              <td>{{ getNomeSetor(equip.setor) }}</td>
              <td>
                <span :class="['status-badge', equip.status?.toLowerCase()]">{{ equip.status }}</span>
              </td>
              <td class="col-acoes">
                <div class="action-buttons">
                  <button @click="prepararEdicao(equip)" class="btn-icon" title="Editar">✏️</button>
                  <button @click="deletarEquipamento(equip.id)" class="btn-icon" title="Excluir">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const carregando = ref(false)
const editandoId = ref(null)
const setores = ref([])
const equipamentos = ref([])

const fotosExistentes = ref([])  // [{ id, nome, url }]
const fotosNovas      = ref([])  // [{ file, nome, preview }]

const manuaisExistentes = ref([]) // [{ id, nome, url }]
const manuaisNovos      = ref([]) // [{ file, nome }]

const fotos   = computed(() => [...fotosExistentes.value, ...fotosNovas.value])
const manuais = computed(() => [...manuaisExistentes.value, ...manuaisNovos.value])

const erros = ref({ id_interno: '', qr_code_token: '' })
const temErros = computed(() => !!(erros.value.id_interno || erros.value.qr_code_token))

const form = ref({
  nome_equipamento: '',
  tipo_equipamento: '',
  status: 'Ativo',
  id_interno: null,
  qr_code_token: '',
  setor: ''
})

const API_BASE = 'http://localhost:8000/api'

const getHeaders = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
})

// ── Helpers ──────────────────────────────────────────────────────────────────

// Detecta imagem apenas pela extensão do caminho_arquivo.
// Não usa nome_arquivo para evitar falsos positivos com prefixos textuais.
const docIsImagem = (d) => {
  const caminho = (d.caminho_arquivo || '').toLowerCase()
  return /\.(jpg|jpeg|png|gif|webp)(\?.*)?$/.test(caminho)
}

// FIX: Documentos de foto de problema (gerados pelas OS) são salvos com
// nome_arquivo começando em "Problema OS#..." e NÃO devem aparecer no
// cadastro do equipamento. Filtramos qualquer documento com esse prefixo.
const docEhDoEquipamento = (d) => {
  const nome = (d.nome_arquivo || '').toLowerCase()
  return !nome.startsWith('problema')
}

// ── Handlers de arquivo ──────────────────────────────────────────────────────

const handleFotos = (e) => {
  Array.from(e.target.files).forEach(file => {
    fotosNovas.value.push({ file, nome: file.name, preview: URL.createObjectURL(file) })
  })
  e.target.value = ''
}

const handleManuais = (e) => {
  Array.from(e.target.files).forEach(file => {
    manuaisNovos.value.push({ file, nome: file.name })
  })
  e.target.value = ''
}

const removerFotoNova = (index) => {
  URL.revokeObjectURL(fotosNovas.value[index].preview)
  fotosNovas.value.splice(index, 1)
}

const removerManualNovo = (index) => {
  manuaisNovos.value.splice(index, 1)
}

const removerFotoExistente = async (foto) => {
  if (!foto.id) {
    fotosExistentes.value = fotosExistentes.value.filter(f => f !== foto)
    return
  }
  if (!confirm(`Remover a foto "${foto.nome}"?`)) return
  try {
    await axios.delete(`${API_BASE}/documentos-equipamento/${foto.id}/`, getHeaders())
    fotosExistentes.value = fotosExistentes.value.filter(f => f.id !== foto.id)
  } catch (e) {
    alert('Erro ao remover foto: ' + JSON.stringify(e.response?.data))
  }
}

const removerManualExistente = async (manual) => {
  if (!confirm(`Remover o manual "${manual.nome}"?`)) return
  try {
    await axios.delete(`${API_BASE}/documentos-equipamento/${manual.id}/`, getHeaders())
    manuaisExistentes.value = manuaisExistentes.value.filter(m => m.id !== manual.id)
  } catch (e) {
    alert('Erro ao remover manual: ' + JSON.stringify(e.response?.data))
  }
}

// ── Validação de unicidade ───────────────────────────────────────────────────

const validarCampoUnico = (campo) => {
  const valor = form.value[campo]
  if (valor === null || valor === undefined || valor === '') {
    erros.value[campo] = ''
    return
  }
  const duplicado = equipamentos.value.some(equip => {
    if (editandoId.value && String(equip.id) === String(editandoId.value)) return false
    return String(equip[campo]) === String(valor)
  })
  if (duplicado) {
    const labels = { id_interno: 'ID Interno', qr_code_token: 'Token do QR Code' }
    erros.value[campo] = `${labels[campo]} já está em uso por outro equipamento.`
  } else {
    erros.value[campo] = ''
  }
}

// ── CRUD ─────────────────────────────────────────────────────────────────────

const fetchSetores = async () => {
  const empresaId = localStorage.getItem('empresa_id')
  try {
    const res = await axios.get(`${API_BASE}/setores/?empresa=${empresaId}`, getHeaders())
    setores.value = res.data
  } catch (e) { console.error(e) }
}

const fetchEquipamentos = async () => {
  try {
    const res = await axios.get(`${API_BASE}/equipamentos/`, getHeaders())
    equipamentos.value = res.data
  } catch (e) { console.error(e) }
}

const fetchDocumentosExistentes = async (equipamentoId) => {
  try {
    const res = await axios.get(
      `${API_BASE}/documentos-equipamento/?equipamento=${equipamentoId}`,
      getHeaders()
    )

    // Camada 1: só documentos deste equipamento (proteção contra backend sem filtro)
    // Camada 2: exclui fotos de problema geradas pelas OS (nome começa com "Problema")
    const docs = res.data
      .filter(d => String(d.equipamento) === String(equipamentoId))
      .filter(d => docEhDoEquipamento(d))

    fotosExistentes.value = docs
      .filter(d => docIsImagem(d))
      .map(d => ({
        id: d.id,
        nome: d.nome_arquivo || d.caminho_arquivo?.split('/').pop() || 'Foto',
        url: d.caminho_arquivo
      }))

    manuaisExistentes.value = docs
      .filter(d => !docIsImagem(d))
      .map(d => ({
        id: d.id,
        nome: d.nome_arquivo || d.caminho_arquivo?.split('/').pop() || 'Manual',
        url: d.caminho_arquivo
      }))

  } catch (e) {
    console.error('Erro ao buscar documentos existentes:', e)
  }
}

const prepararEdicao = async (equip) => {
  editandoId.value = equip.id

  form.value = {
    nome_equipamento: equip.nome_equipamento,
    tipo_equipamento: equip.tipo_equipamento,
    status: equip.status,
    id_interno: equip.id_interno,
    qr_code_token: equip.qr_code_token,
    setor: equip.setor
  }

  fotosNovas.value = []
  manuaisNovos.value = []
  fotosExistentes.value = []
  manuaisExistentes.value = []

  await fetchDocumentosExistentes(equip.id)

  erros.value = { id_interno: '', qr_code_token: '' }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const salvarEquipamento = async () => {
  validarCampoUnico('id_interno')
  validarCampoUnico('qr_code_token')
  if (temErros.value) return

  carregando.value = true

  const formData = new FormData()
  Object.keys(form.value).forEach(key => formData.append(key, form.value[key]))

  try {
    let resEquip

    if (editandoId.value) {
      resEquip = await axios.patch(
        `${API_BASE}/equipamentos/${editandoId.value}/`,
        formData,
        getHeaders()
      )
      alert('Equipamento atualizado!')
    } else {
      resEquip = await axios.post(`${API_BASE}/equipamentos/`, formData, getHeaders())
      alert('Equipamento cadastrado com sucesso!')
    }

    const equipId = resEquip.data.id

    for (const foto of fotosNovas.value) {
      const docData = new FormData()
      docData.append('equipamento', equipId)
      docData.append('caminho_arquivo', foto.file)
      docData.append('nome_arquivo', `Foto - ${form.value.nome_equipamento} - ${foto.nome}`)
      try {
        await axios.post(`${API_BASE}/documentos-equipamento/`, docData, getHeaders())
      } catch (docErr) {
        console.error('Erro ao salvar foto:', docErr.response?.data)
        alert(`Erro no upload da foto "${foto.nome}":\n` + JSON.stringify(docErr.response?.data))
      }
    }

    for (const manual of manuaisNovos.value) {
      const docData = new FormData()
      docData.append('equipamento', equipId)
      docData.append('caminho_arquivo', manual.file)
      docData.append('nome_arquivo', `Manual - ${form.value.nome_equipamento} - ${manual.nome}`)
      try {
        await axios.post(`${API_BASE}/documentos-equipamento/`, docData, getHeaders())
      } catch (docErr) {
        console.error('Erro ao salvar manual:', docErr.response?.data)
        alert(`Erro no upload do manual "${manual.nome}":\n` + JSON.stringify(docErr.response?.data))
      }
    }

    resetForm()
    fetchEquipamentos()
  } catch (e) {
    console.error('Erro na operação:', e.response?.data)
    alert('Erro ao processar: ' + JSON.stringify(e.response?.data || 'Verifique os dados.'))
  } finally {
    carregando.value = false
  }
}

const resetForm = () => {
  editandoId.value = null
  form.value = { nome_equipamento: '', tipo_equipamento: '', status: 'Ativo', id_interno: null, qr_code_token: '', setor: '' }
  fotosNovas.value = []
  fotosExistentes.value = []
  manuaisNovos.value = []
  manuaisExistentes.value = []
  erros.value = { id_interno: '', qr_code_token: '' }
}

const deletarEquipamento = async (id) => {
  if (!confirm('Deseja realmente excluir este ativo?')) return
  try {
    await axios.delete(`${API_BASE}/equipamentos/${id}/`, getHeaders())
    fetchEquipamentos()
  } catch (e) { console.error(e) }
}

const getNomeSetor = (id) => {
  const setor = setores.value.find(s => s.id === id)
  return setor ? setor.nome_setor : '---'
}

onMounted(() => { fetchSetores(); fetchEquipamentos() })
</script>

<style scoped>
/* ── Base ─────────────────────────────────────────── */
.crud-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-header {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 1px solid #bfdbfe;
  border-radius: 20px;
  padding: 1.5rem 1.75rem;
}
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.page-header h2 { margin: 0; color: #0f172a; font-size: 1.5rem; font-weight: 700; }
.page-copy { margin: 0.4rem 0 0; color: #475569; font-size: 0.95rem; }

.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.form-card, .table-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.card-header h3 { margin: 0; color: #0f172a; }
.card-header p { margin: 0.4rem 0 0; color: #475569; }

/* ── Formulário ───────────────────────────────────── */
.crud-form { display: flex; flex-direction: column; gap: 1.2rem; }
.input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.field-label { font-size: 0.9rem; font-weight: 600; color: #334155; }

.input-group input,
.input-group select {
  box-sizing: border-box; width: 100%;
  padding: 0.9rem 1rem; border: 1px solid #cbd5e1;
  border-radius: 12px; background: #f8fafc;
  color: #0f172a; font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
}
.input-group input:focus,
.input-group select:focus {
  outline: none; background: #ffffff;
  border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14);
}
.input-group input.input-error { border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.12); }
.error-msg { font-size: 0.78rem; color: #dc2626; font-weight: 500; }

/* ── Upload section ───────────────────────────────── */
.upload-section-container {
  padding-top: 1.25rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Dois blocos lado a lado */
.upload-blocks-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.upload-block {
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 1rem 1.1rem;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.upload-block-header {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.upload-block-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.upload-block-info {
  flex: 1;
  min-width: 0;
}

.upload-block-title {
  margin: 0;
  font-size: 0.82rem;
  font-weight: 600;
  color: #334155;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.upload-block-subtitle {
  margin: 0;
  font-size: 0.72rem;
  color: #94a3b8;
}

.hidden-input { opacity: 0; position: absolute; z-index: -1; width: 0.1px; }

.btn-add-file {
  display: inline-flex;
  align-items: center;
  padding: 0.28rem 0.65rem;
  font-size: 0.73rem;
  font-weight: 600;
  color: #2563eb;
  border: 1.5px solid #bfdbfe;
  border-radius: 20px;
  background: #eff6ff;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  transition: background 0.2s, border-color 0.2s;
}
.btn-add-file:hover { background: #dbeafe; border-color: #93c5fd; }

.upload-empty {
  font-size: 0.78rem;
  color: #94a3b8;
  margin: 0;
}

/* ── Chips ────────────────────────────────────────── */
.file-chip-list { display: flex; flex-wrap: wrap; gap: 0.4rem; }

.file-chip {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.25rem 0.55rem 0.25rem 0.35rem;
  border-radius: 20px; font-size: 0.75rem; font-weight: 500;
  max-width: 100%;
}
.foto-chip { background: #eff6ff; border: 1px solid #bfdbfe; color: #1d4ed8; }
.foto-chip-new { border-style: dashed; }
.pdf-chip  { background: #fef3c7; border: 1px solid #fde68a; color: #92400e; }
.pdf-chip-new { border-style: dashed; }

.chip-thumb { width: 20px; height: 20px; border-radius: 4px; object-fit: cover; flex-shrink: 0; }
.chip-icon  { font-size: 0.9rem; flex-shrink: 0; }
.chip-name  { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 120px; }
.chip-remove {
  background: none; border: none; cursor: pointer;
  font-size: 1rem; line-height: 1; color: inherit;
  opacity: 0.5; padding: 0; flex-shrink: 0;
  transition: opacity 0.2s;
}
.chip-remove:hover { opacity: 1; }

/* ── Ações ────────────────────────────────────────── */
.form-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; padding-top: 1.25rem; border-top: 1px solid #f1f5f9; }

/* ── Botões ───────────────────────────────────────── */
.btn { border: none; border-radius: 12px; padding: 0.8rem 1.15rem; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s, background-color 0.2s; }
.btn:hover:not(:disabled) { transform: translateY(-1px); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary { background: #2563eb; color: #ffffff; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24); }
.btn-secondary { background: #e2e8f0; color: #1e293b; }

/* ── Tabela ───────────────────────────────────────── */
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.data-table { width: 100%; border-collapse: collapse; min-width: 480px; }
.data-table th, .data-table td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }
.data-table th { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; white-space: nowrap; }
.data-table td { color: #1e293b; }
.col-acoes { text-align: left !important; }
.action-buttons { display: inline-flex; gap: 0.5rem; align-items: center; }

.status-badge { padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; white-space: nowrap; }
.status-badge.ativo { background: #dcfce7; color: #15803d; }
.status-badge.manutenção { background: #fef9c3; color: #854d0e; }
.status-badge.inativo { background: #fee2e2; color: #b91c1c; }

.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }

/* ── Animação ─────────────────────────────────────── */
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out; }

/* ── Mobile ≤ 768px ───────────────────────────────── */
@media (max-width: 768px) {
  .page-header { padding: 1.1rem 1.2rem; border-radius: 16px; }
  .form-card, .table-card { padding: 1.1rem 1.2rem; border-radius: 16px; }
  .card { border-radius: 16px; }
  .input-row { grid-template-columns: 1fr; }
  .upload-blocks-row { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column; }
  .form-actions .btn { width: 100%; }
  .table-wrap { border-radius: 12px; border: 1px solid #e2e8f0; }
  .data-table th, .data-table td { padding: 0.75rem 0.85rem; font-size: 0.875rem; }
}

/* ── Mobile pequeno ≤ 480px ───────────────────────── */
@media (max-width: 480px) {
  .page-header h2 { font-size: 1.2rem; }
  .card-header h3 { font-size: 1rem; }
  .input-group input, .input-group select { padding: 0.75rem 0.85rem; }
  .btn { padding: 0.7rem 1rem; }
}

.btn-icon {
  background: none; border: none; cursor: pointer;
  font-size: 1.1rem; padding: 0.3rem;
  filter: grayscale(1); opacity: 0.7;
  display: inline-flex; align-items: center; justify-content: center;
  transition: filter 0.2s, opacity 0.2s, transform 0.2s;
}
.btn-icon:hover { filter: none; opacity: 1; transform: scale(1.2); }
</style>