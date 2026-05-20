<template>
  <div class="crud-page">
    <section class="page-header animate-fade-in">
      <p class="eyebrow">Ativos Técnicos</p>
      <h2>Gestão de Equipamentos</h2>
      <p class="page-copy">Cadastre, organize e vincule documentação técnica às máquinas da unidade.</p>
    </section>

    <section v-if="canOpenEquipmentForm" class="card form-card animate-fade-in">
      <div class="card-header">
        <h3>{{ editandoId ? 'Editar Equipamento' : 'Novo Equipamento' }}</h3>
        <p>Preencha os dados do ativo e vincule a documentação técnica.</p>
      </div>

      <form @submit.prevent="salvarEquipamento" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label class="field-label">Nome do Equipamento</label>
            <input v-model="form.nome_equipamento" type="text" placeholder="Ex: Torno CNC 01" required :disabled="!canEditEquipmentFields || carregando" />
          </div>
          <div class="input-group">
            <label class="field-label">Tipo / Categoria</label>
            <input v-model="form.tipo_equipamento" type="text" placeholder="Ex: Injetora, Prensa..." required :disabled="!canEditEquipmentFields || carregando" />
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
              :disabled="!canEditEquipmentFields || carregando"
              :class="{ 'input-error': erros.id_interno }"
              @blur="validarCampoUnico('id_interno')"
            />
            <span v-if="erros.id_interno" class="error-msg">{{ erros.id_interno }}</span>
          </div>
          <div class="input-group">
            <label class="field-label">Status Inicial</label>
            <select v-model="form.status" required :disabled="!canEditEquipmentFields || carregando">
              <option value="Ativo">Ativo</option>
              <option value="Manutenção">Em Manutenção</option>
              <option value="Inativo">Inativo / Reserva</option>
            </select>
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label class="field-label">Setor Responsável</label>
            <select v-model="form.setor" required :disabled="!canEditEquipmentFields || carregando">
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
              :disabled="!canEditEquipmentFields || carregando"
              :class="{ 'input-error': erros.qr_code_token }"
              @blur="validarCampoUnico('qr_code_token')"
            />
            <span v-if="erros.qr_code_token" class="error-msg">{{ erros.qr_code_token }}</span>
          </div>
        </div>

        <!-- ── Documentação Técnica ── -->
        <div v-if="canViewOrManageDocuments" class="upload-section-container">
          <p class="field-label">Documentação Técnica</p>

          <div class="upload-blocks-row">
            <!-- Fotos -->
            <div class="upload-block">
              <div class="upload-block-header">
                <span class="upload-block-icon">IMG</span>
                <div class="upload-block-info">
                  <p class="upload-block-title">Fotos do Equipamento</p>
                  <p class="upload-block-subtitle">opcional</p>
                </div>
                <label v-if="canCreateDocuments" for="fotoInput" class="btn-add-file">+ Adicionar foto</label>
                <input v-if="canCreateDocuments" type="file" id="fotoInput" @change="handleFotos" accept="image/*" multiple class="hidden-input" />
              </div>

              <div v-if="fotos.length" class="file-chip-list">
                <div v-for="f in fotosExistentes" :key="'existing-'+f.id" class="file-chip foto-chip">
                  <img :src="f.url" class="chip-thumb" />
                  <span class="chip-name">{{ f.nome }}</span>
                  <button v-if="canDeleteDocuments" type="button" @click="removerFotoExistente(f)" class="chip-remove" title="Remover">×</button>
                </div>
                <div v-for="(f, i) in fotosNovas" :key="'new-'+i" class="file-chip foto-chip foto-chip-new">
                  <img :src="f.preview" class="chip-thumb" />
                  <span class="chip-name">{{ f.nome }}</span>
                  <button v-if="canCreateDocuments" type="button" @click="removerFotoNova(i)" class="chip-remove">×</button>
                </div>
              </div>
              <p v-else class="upload-empty">Nenhuma foto adicionada. Aceita PNG e JPG.</p>
            </div>

            <!-- PDFs -->
            <div class="upload-block">
              <div class="upload-block-header">
                <span class="upload-block-icon">PDF</span>
                <div class="upload-block-info">
                  <p class="upload-block-title">Documentos Técnicos (PDF)</p>
                  <p class="upload-block-subtitle">opcional</p>
                </div>
                <label v-if="canCreateDocuments" for="manualInput" class="btn-add-file">+ Adicionar PDF</label>
                <input v-if="canCreateDocuments" type="file" id="manualInput" @change="handleManuais" accept=".pdf" multiple class="hidden-input" />
              </div>

              <div v-if="canCreateDocuments && canViewCategories" class="document-options">
                <label class="category-control">
                  <span>Categoria padrão dos novos PDFs</span>
                  <select v-model="categoriaManualSelecionada" :disabled="!categoriasDocumento.length">
                    <option value="">Sem categoria</option>
                    <option
                      v-for="categoria in categoriasDocumento"
                      :key="categoria.id"
                      :value="categoria.id"
                    >
                      {{ categoria.nome_categoria }}
                    </option>
                  </select>
                </label>
              </div>

              <div v-if="manuais.length" class="file-chip-list document-list">
                <div v-for="m in manuaisExistentes" :key="'existing-pdf-'+m.id" class="file-chip pdf-chip document-chip">
                  <span class="chip-icon">PDF</span>
                  <div class="chip-main">
                    <span class="chip-name">{{ m.nome }}</span>
                    <span class="chip-category">{{ getCategoriaNome(m.categoria) }}</span>
                  </div>
                  <select
                    v-if="canEditDocuments && canViewCategories"
                    v-model="m.categoria"
                    class="chip-category-select"
                    title="Categoria do documento"
                    @change="atualizarCategoriaDocumento(m)"
                  >
                    <option value="">Sem categoria</option>
                    <option
                      v-for="categoria in categoriasDocumento"
                      :key="categoria.id"
                      :value="categoria.id"
                    >
                      {{ categoria.nome_categoria }}
                    </option>
                  </select>
                  <button v-if="canDeleteDocuments" type="button" @click="removerManualExistente(m)" class="chip-remove" title="Remover">×</button>
                </div>
                <div v-for="(m, i) in manuaisNovos" :key="'new-pdf-'+i" class="file-chip pdf-chip pdf-chip-new document-chip">
                  <span class="chip-icon">PDF</span>
                  <div class="chip-main">
                    <span class="chip-name">{{ m.nome }}</span>
                    <span class="chip-category">{{ getCategoriaNome(m.categoria) }}</span>
                  </div>
                  <select v-if="canCreateDocuments && canViewCategories" v-model="m.categoria" class="chip-category-select" title="Categoria do documento">
                    <option value="">Sem categoria</option>
                    <option
                      v-for="categoria in categoriasDocumento"
                      :key="categoria.id"
                      :value="categoria.id"
                    >
                      {{ categoria.nome_categoria }}
                    </option>
                  </select>
                  <button v-if="canCreateDocuments" type="button" @click="removerManualNovo(i)" class="chip-remove">×</button>
                </div>
              </div>
              <p v-else class="upload-empty">Nenhum PDF adicionado.</p>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button v-if="canSubmitEquipment" type="submit" :disabled="carregando || temErros" class="btn btn-primary">
            {{ carregando ? 'Processando...' : (editandoId ? 'Atualizar Equipamento' : 'Salvar Equipamento') }}
          </button>
          <button v-if="editandoId" type="button" @click="resetForm" class="btn btn-secondary">
            Cancelar
          </button>
        </div>
      </form>
    </section>

    <section v-if="canViewEquipment" class="card table-card animate-fade-in">
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
                  <button v-if="canOpenExistingEquipment" @click="prepararEdicao(equip)" class="btn-icon" title="Editar">{{ canEditEquipment ? 'Editar' : 'Documentos' }}</button>
                  <button v-if="canGenerateLabel" @click="abrirEtiqueta(equip)" class="btn-icon" title="Gerar etiqueta">Etiqueta</button>
                  <button v-if="canDeleteEquipment" @click="deletarEquipamento(equip.id)" class="btn-icon danger" title="Excluir">Excluir</button>
                  <span v-if="!canOpenExistingEquipment && !canGenerateLabel && !canDeleteEquipment" class="empty-actions">--</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="!canViewEquipment && !canOpenEquipmentForm" class="card empty-card animate-fade-in">
      <div class="card-header">
        <h3>Acesso limitado</h3>
        <p>Solicite permissao para visualizar equipamentos ou criar novos ativos.</p>
      </div>
    </section>

    <Teleport to="body">
      <Transition name="modal">
        <div v-if="modalEtiqueta" class="modal-overlay" @click.self="fecharEtiqueta">
          <div class="label-modal">
            <div class="modal-header">
              <div>
                <p class="modal-eyebrow">Etiqueta de identificação</p>
                <h3>Etiqueta do equipamento</h3>
              </div>
              <button type="button" class="modal-close" @click="fecharEtiqueta">&times;</button>
            </div>

            <div class="modal-body">
              <div v-if="etiquetaPreviewUrl" class="label-preview-wrap">
                <img :src="etiquetaPreviewUrl" class="label-preview" alt="Prévia da etiqueta do equipamento" />
              </div>
              <div v-else class="label-loading">Gerando etiqueta...</div>

              <div v-if="etiquetaUrl" class="label-url-box">
                <span>URL do QR Code</span>
                <a :href="etiquetaUrl" target="_blank" rel="noopener">{{ etiquetaUrl }}</a>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="copiarUrlEtiqueta">Copiar URL</button>
              <button type="button" class="btn btn-secondary" @click="imprimirEtiqueta">Imprimir</button>
              <button type="button" class="btn btn-primary" @click="baixarEtiqueta">Baixar PNG</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import QRCode from 'qrcode'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { getStoredPermissions, hasPermission } from '../utils/permissions'

const router = useRouter()
const carregando = ref(false)
const editandoId = ref(null)
const setores = ref([])
const equipamentos = ref([])
const categoriasDocumento = ref([])
const categoriaManualSelecionada = ref('')
const empresaIdLocal = localStorage.getItem('empresa_id') || ''
const modalEtiqueta = ref(false)
const equipamentoEtiqueta = ref(null)
const etiquetaPreviewUrl = ref('')
const etiquetaUrl = ref('')

const fotosExistentes = ref([])  // [{ id, nome, url, categoria }]
const fotosNovas      = ref([])  // [{ file, nome, preview, categoria }]

const manuaisExistentes = ref([]) // [{ id, nome, url, categoria }]
const manuaisNovos      = ref([]) // [{ file, nome, categoria }]

const fotos   = computed(() => [...fotosExistentes.value, ...fotosNovas.value])
const manuais = computed(() => [...manuaisExistentes.value, ...manuaisNovos.value])

const erros = ref({ id_interno: '', qr_code_token: '' })
const temErros = computed(() => !!(erros.value.id_interno || erros.value.qr_code_token))
const permissions = computed(() => getStoredPermissions())
const canViewEquipment = computed(() => hasPermission('equipamentos.visualizar', permissions.value))
const canCreateEquipment = computed(() => hasPermission('equipamentos.criar', permissions.value))
const canEditEquipment = computed(() => hasPermission('equipamentos.editar', permissions.value))
const canDeleteEquipment = computed(() => hasPermission('equipamentos.excluir', permissions.value))
const canViewCategories = computed(() => hasPermission('categorias_documento.visualizar', permissions.value))
const canViewDocuments = computed(() => hasPermission('documentos_equipamento.visualizar', permissions.value))
const canCreateDocuments = computed(() => hasPermission('documentos_equipamento.criar', permissions.value))
const canEditDocuments = computed(() => hasPermission('documentos_equipamento.editar', permissions.value))
const canDeleteDocuments = computed(() => hasPermission('documentos_equipamento.excluir', permissions.value))
const canViewOrManageDocuments = computed(() =>
  canViewDocuments.value ||
  canCreateDocuments.value ||
  canEditDocuments.value ||
  canDeleteDocuments.value
)
const canOpenExistingEquipment = computed(() =>
  canEditEquipment.value || canViewOrManageDocuments.value
)
const canOpenEquipmentForm = computed(() =>
  (!editandoId.value && canCreateEquipment.value) ||
  (Boolean(editandoId.value) && canOpenExistingEquipment.value)
)
const canEditEquipmentFields = computed(() =>
  !editandoId.value ? canCreateEquipment.value : canEditEquipment.value
)
const hasNewDocuments = computed(() => fotosNovas.value.length > 0 || manuaisNovos.value.length > 0)
const canSubmitEquipment = computed(() =>
  !editandoId.value
    ? canCreateEquipment.value
    : canEditEquipment.value || (canCreateDocuments.value && hasNewDocuments.value)
)
const canGenerateLabel = computed(() => canViewEquipment.value)

const createEmptyForm = () => ({
  nome_equipamento: '',
  tipo_equipamento: '',
  status: 'Ativo',
  id_interno: null,
  qr_code_token: '',
  setor: '',
  empresa: empresaIdLocal
})

const form = ref(createEmptyForm())

const API_BASE = 'http://127.0.0.1:8000/api'

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

const normalizarTexto = (texto) =>
  String(texto || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()

const getCategoriaPadrao = (termos) => {
  const categoria = categoriasDocumento.value.find((item) => {
    const nome = normalizarTexto(item.nome_categoria)
    return termos.some(termo => nome.includes(normalizarTexto(termo)))
  })
  return categoria?.id || ''
}

const getCategoriaManualPadrao = () =>
  getCategoriaPadrao(['manual tecnico']) ||
  getCategoriaPadrao(['manual do usuario']) ||
  categoriasDocumento.value[0]?.id ||
  ''

const getCategoriaImagemPadrao = () =>
  getCategoriaPadrao(['imagens da maquina']) ||
  getCategoriaPadrao(['imagem']) ||
  ''

const getCategoriaNome = (categoriaId) => {
  const categoria = categoriasDocumento.value.find(
    item => String(item.id) === String(categoriaId)
  )
  return categoria?.nome_categoria || 'Sem categoria'
}

// ── Handlers de arquivo ──────────────────────────────────────────────────────

const handleFotos = (e) => {
  if (!canCreateDocuments.value) {
    alert('Voce nao possui permissao para adicionar documentos do equipamento.')
    e.target.value = ''
    return
  }
  Array.from(e.target.files).forEach(file => {
    fotosNovas.value.push({
      file,
      nome: file.name,
      preview: URL.createObjectURL(file),
      categoria: getCategoriaImagemPadrao()
    })
  })
  e.target.value = ''
}

const handleManuais = (e) => {
  if (!canCreateDocuments.value) {
    alert('Voce nao possui permissao para adicionar documentos do equipamento.')
    e.target.value = ''
    return
  }
  Array.from(e.target.files).forEach(file => {
    manuaisNovos.value.push({
      file,
      nome: file.name,
      categoria: categoriaManualSelecionada.value || getCategoriaManualPadrao()
    })
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
  if (!canDeleteDocuments.value) {
    alert('Voce nao possui permissao para remover documentos do equipamento.')
    return
  }
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
  if (!canDeleteDocuments.value) {
    alert('Voce nao possui permissao para remover documentos do equipamento.')
    return
  }
  if (!confirm(`Remover o manual "${manual.nome}"?`)) return
  try {
    await axios.delete(`${API_BASE}/documentos-equipamento/${manual.id}/`, getHeaders())
    manuaisExistentes.value = manuaisExistentes.value.filter(m => m.id !== manual.id)
  } catch (e) {
    alert('Erro ao remover manual: ' + JSON.stringify(e.response?.data))
  }
}

const atualizarCategoriaDocumento = async (documento) => {
  if (!canEditDocuments.value) {
    alert('Voce nao possui permissao para editar documentos do equipamento.')
    return
  }
  if (!documento.id) return
  try {
    await axios.patch(
      `${API_BASE}/documentos-equipamento/${documento.id}/`,
      { categoria: documento.categoria || null },
      getHeaders()
    )
  } catch (e) {
    alert('Erro ao atualizar categoria do documento.')
    if (editandoId.value) await fetchDocumentosExistentes(editandoId.value)
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
  if (!canViewEquipment.value && !canCreateEquipment.value && !canEditEquipment.value) {
    setores.value = []
    return
  }
  const empresaId = localStorage.getItem('empresa_id')
  try {
    const res = await axios.get(`${API_BASE}/setores/?empresa=${empresaId}`, getHeaders())
    setores.value = res.data
  } catch (e) { console.error(e) }
}

const fetchEquipamentos = async () => {
  if (!canViewEquipment.value) {
    equipamentos.value = []
    return
  }
  try {
    const res = await axios.get(`${API_BASE}/equipamentos/`, getHeaders())
    equipamentos.value = res.data
  } catch (e) { console.error(e) }
}

const fetchCategoriasDocumento = async () => {
  if (!canViewCategories.value) {
    categoriasDocumento.value = []
    return
  }
  try {
    const res = await axios.get(`${API_BASE}/categorias-documento/`, getHeaders())
    categoriasDocumento.value = Array.isArray(res.data) ? res.data : []
    if (!categoriaManualSelecionada.value) {
      categoriaManualSelecionada.value = getCategoriaManualPadrao()
    }
  } catch (e) {
    console.error('Erro ao buscar categorias de documento:', e)
  }
}

const fetchDocumentosExistentes = async (equipamentoId) => {
  if (!canViewOrManageDocuments.value) {
    fotosExistentes.value = []
    manuaisExistentes.value = []
    return
  }
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
        url: d.caminho_arquivo,
        categoria: d.categoria || ''
      }))

    manuaisExistentes.value = docs
      .filter(d => !docIsImagem(d))
      .map(d => ({
        id: d.id,
        nome: d.nome_arquivo || d.caminho_arquivo?.split('/').pop() || 'Manual',
        url: d.caminho_arquivo,
        categoria: d.categoria || ''
      }))

  } catch (e) {
    console.error('Erro ao buscar documentos existentes:', e)
  }
}

const prepararEdicao = async (equip) => {
  if (!canOpenExistingEquipment.value) {
    alert('Voce nao possui permissao para editar ou consultar documentos deste equipamento.')
    return
  }
  editandoId.value = equip.id

  form.value = {
    nome_equipamento: equip.nome_equipamento,
    tipo_equipamento: equip.tipo_equipamento,
    status: equip.status,
    id_interno: equip.id_interno,
    qr_code_token: equip.qr_code_token,
    setor: equip.setor,
    empresa: equip.empresa || empresaIdLocal
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
  if (!editandoId.value && !canCreateEquipment.value) {
    alert('Voce nao possui permissao para cadastrar equipamentos.')
    return
  }
  if (editandoId.value && !canEditEquipment.value && !(canCreateDocuments.value && hasNewDocuments.value)) {
    alert('Voce nao possui permissao para atualizar este equipamento.')
    return
  }
  if (!canCreateDocuments.value && hasNewDocuments.value) {
    alert('Voce nao possui permissao para adicionar documentos do equipamento.')
    return
  }

  validarCampoUnico('id_interno')
  validarCampoUnico('qr_code_token')
  if (temErros.value) return
  if (categoriasDocumento.value.length && manuaisNovos.value.some(manual => !manual.categoria)) {
    alert('Selecione a categoria dos PDFs adicionados.')
    return
  }

  carregando.value = true

  const formData = new FormData()
  Object.keys(form.value).forEach(key => {
    const value = form.value[key]
    if (value !== null && value !== undefined && value !== '') {
      formData.append(key, value)
    }
  })

  try {
    let resEquip
    let houveErroUpload = false
    const mensagemSucesso = editandoId.value
      ? 'Equipamento atualizado com sucesso!'
      : 'Equipamento cadastrado com sucesso!'

    let equipId = editandoId.value

    if (editandoId.value && canEditEquipment.value) {
      resEquip = await axios.patch(
        `${API_BASE}/equipamentos/${editandoId.value}/`,
        formData,
        getHeaders()
      )
      equipId = resEquip.data.id
    } else if (!editandoId.value) {
      resEquip = await axios.post(`${API_BASE}/equipamentos/`, formData, getHeaders())
      equipId = resEquip.data.id
    }

    for (const foto of fotosNovas.value) {
      const docData = new FormData()
      docData.append('equipamento', equipId)
      docData.append('caminho_arquivo', foto.file)
      docData.append('nome_arquivo', `Foto - ${form.value.nome_equipamento} - ${foto.nome}`)
      if (foto.categoria) docData.append('categoria', foto.categoria)
      try {
        await axios.post(`${API_BASE}/documentos-equipamento/`, docData, getHeaders())
      } catch (docErr) {
        houveErroUpload = true
        console.error('Erro ao salvar foto:', docErr.response?.data)
        alert(`Erro no upload da foto "${foto.nome}":\n` + JSON.stringify(docErr.response?.data))
      }
    }

    for (const manual of manuaisNovos.value) {
      const docData = new FormData()
      docData.append('equipamento', equipId)
      docData.append('caminho_arquivo', manual.file)
      docData.append('nome_arquivo', `Manual - ${form.value.nome_equipamento} - ${manual.nome}`)
      if (manual.categoria) docData.append('categoria', manual.categoria)
      try {
        await axios.post(`${API_BASE}/documentos-equipamento/`, docData, getHeaders())
      } catch (docErr) {
        houveErroUpload = true
        console.error('Erro ao salvar manual:', docErr.response?.data)
        alert(`Erro no upload do manual "${manual.nome}":\n` + JSON.stringify(docErr.response?.data))
      }
    }

    alert(houveErroUpload ? 'Equipamento salvo, mas um ou mais documentos não foram enviados.' : mensagemSucesso)
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
  form.value = createEmptyForm()
  fotosNovas.value = []
  fotosExistentes.value = []
  manuaisNovos.value = []
  manuaisExistentes.value = []
  categoriaManualSelecionada.value = getCategoriaManualPadrao()
  erros.value = { id_interno: '', qr_code_token: '' }
}

const deletarEquipamento = async (id) => {
  if (!canDeleteEquipment.value) {
    alert('Voce nao possui permissao para excluir equipamentos.')
    return
  }
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

const carregarImagem = (src) =>
  new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = reject
    img.src = src
  })

const criarUrlChamado = (equipamento) => {
  const href = router.resolve({
    path: '/dashboard/abrir-os',
    query: {
      equipamento: equipamento.id,
      id_interno: equipamento.id_interno,
      token: equipamento.qr_code_token
    }
  }).href
  const baseUrl = (import.meta.env.VITE_APP_PUBLIC_URL || window.location.origin).replace(/\/$/, '')
  return new URL(href, baseUrl).toString()
}

const desenharTextoQuebrado = (ctx, texto, x, y, larguraMaxima, alturaLinha, limiteLinhas = 2) => {
  const palavras = String(texto || '').split(' ')
  const linhas = []
  let linhaAtual = ''

  palavras.forEach((palavra) => {
    const tentativa = linhaAtual ? `${linhaAtual} ${palavra}` : palavra
    if (ctx.measureText(tentativa).width <= larguraMaxima) {
      linhaAtual = tentativa
      return
    }

    if (linhaAtual) linhas.push(linhaAtual)
    linhaAtual = palavra
  })

  if (linhaAtual) linhas.push(linhaAtual)

  linhas.slice(0, limiteLinhas).forEach((linha, index) => {
    const textoLinha = index === limiteLinhas - 1 && linhas.length > limiteLinhas
      ? `${linha.replace(/\.*$/, '')}...`
      : linha
    ctx.fillText(textoLinha, x, y + index * alturaLinha)
  })
}

const desenharCampoEtiqueta = (ctx, rotulo, valor, x, y, largura) => {
  ctx.fillStyle = '#64748b'
  ctx.font = '700 20px Arial'
  ctx.fillText(rotulo.toUpperCase(), x, y)

  ctx.fillStyle = '#0f172a'
  ctx.font = '700 30px Arial'
  desenharTextoQuebrado(ctx, valor || 'Não informado', x, y + 34, largura, 34, 2)
}

const gerarImagemEtiqueta = async (equipamento) => {
  const urlChamado = criarUrlChamado(equipamento)
  const qrDataUrl = await QRCode.toDataURL(urlChamado, {
    errorCorrectionLevel: 'M',
    margin: 1,
    width: 320,
    color: {
      dark: '#0f172a',
      light: '#ffffff'
    }
  })

  const qrImage = await carregarImagem(qrDataUrl)
  const canvas = document.createElement('canvas')
  canvas.width = 960
  canvas.height = 540

  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#ffffff'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  ctx.strokeStyle = '#0f172a'
  ctx.lineWidth = 8
  ctx.strokeRect(16, 16, canvas.width - 32, canvas.height - 32)

  ctx.fillStyle = '#0f172a'
  ctx.fillRect(16, 16, canvas.width - 32, 86)

  ctx.fillStyle = '#ffffff'
  ctx.font = '800 36px Arial'
  ctx.fillText('PANDORA', 48, 70)
  ctx.font = '700 20px Arial'
  ctx.fillText('ETIQUETA DE ATIVO', 740, 70)

  ctx.fillStyle = '#f8fafc'
  ctx.fillRect(626, 132, 276, 276)
  ctx.strokeStyle = '#e2e8f0'
  ctx.lineWidth = 3
  ctx.strokeRect(626, 132, 276, 276)
  ctx.drawImage(qrImage, 646, 152, 236, 236)

  ctx.fillStyle = '#1e293b'
  ctx.font = '700 20px Arial'
  ctx.fillText('Escaneie para abrir OS', 646, 444)

  ctx.fillStyle = '#475569'
  ctx.font = '600 15px Arial'
 

  desenharCampoEtiqueta(ctx, 'Equipamento', equipamento.nome_equipamento, 56, 158, 500)
  desenharCampoEtiqueta(ctx, 'Setor', getNomeSetor(equipamento.setor), 56, 258, 500)
  desenharCampoEtiqueta(ctx, 'ID interno', `#${equipamento.id_interno ?? equipamento.id}`, 56, 358, 230)
  desenharCampoEtiqueta(ctx, 'Status', equipamento.status, 326, 358, 230)

  ctx.fillStyle = '#64748b'
  ctx.font = '700 18px Arial'
  ctx.fillText('TOKEN QR', 56, 462)
  ctx.fillStyle = '#0f172a'
  ctx.font = '700 24px Arial'
  desenharTextoQuebrado(ctx, equipamento.qr_code_token || 'Não informado', 56, 494, 500, 26, 1)

  return {
    imageUrl: canvas.toDataURL('image/png'),
    targetUrl: urlChamado
  }
}

const abrirEtiqueta = async (equipamento) => {
  if (!canGenerateLabel.value) {
    alert('Voce nao possui permissao para visualizar equipamentos.')
    return
  }
  equipamentoEtiqueta.value = equipamento
  etiquetaPreviewUrl.value = ''
  etiquetaUrl.value = ''
  modalEtiqueta.value = true

  try {
    if (!setores.value.length) await fetchSetores()
    const etiqueta = await gerarImagemEtiqueta(equipamento)
    etiquetaPreviewUrl.value = etiqueta.imageUrl
    etiquetaUrl.value = etiqueta.targetUrl
  } catch (e) {
    console.error('Erro ao gerar etiqueta:', e)
    alert('Não foi possível gerar a etiqueta deste equipamento.')
    fecharEtiqueta()
  }
}

const fecharEtiqueta = () => {
  modalEtiqueta.value = false
  equipamentoEtiqueta.value = null
  etiquetaPreviewUrl.value = ''
  etiquetaUrl.value = ''
}

const baixarEtiqueta = () => {
  if (!etiquetaPreviewUrl.value || !equipamentoEtiqueta.value) return
  const link = document.createElement('a')
  const idInterno = equipamentoEtiqueta.value.id_interno || equipamentoEtiqueta.value.id
  link.href = etiquetaPreviewUrl.value
  link.download = `etiqueta-equipamento-${idInterno}.png`
  link.click()
}

const imprimirEtiqueta = () => {
  if (!etiquetaPreviewUrl.value) return
  const printWindow = window.open('', '_blank')
  if (!printWindow) {
    alert('Permita pop-ups para imprimir a etiqueta.')
    return
  }

  printWindow.document.write(`
    <html>
      <head>
        <title>Etiqueta do equipamento</title>
        <style>
          body { margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #fff; }
          img { width: 150mm; max-width: 95vw; height: auto; }
          @media print { body { min-height: auto; } img { width: 150mm; } }
        </style>
      </head>
      <body>
        <img src="${etiquetaPreviewUrl.value}" alt="Etiqueta do equipamento" />
        <script>
          window.onload = () => { window.print(); window.close(); }
        <\/script>
      </body>
    </html>
  `)
  printWindow.document.close()
}

const copiarUrlEtiqueta = async () => {
  if (!etiquetaUrl.value) return
  try {
    await navigator.clipboard.writeText(etiquetaUrl.value)
    alert('URL copiada para a área de transferência.')
  } catch (e) {
    alert('Não foi possível copiar automaticamente. Selecione a URL exibida na tela.')
  }
}

onMounted(() => { fetchSetores(); fetchEquipamentos(); fetchCategoriasDocumento() })
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
  width: 34px;
  height: 26px;
  border-radius: 7px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #e0f2fe;
  color: #0369a1;
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 0.04em;
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

.document-options {
  padding: 0.7rem 0.8rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #ffffff;
}

.category-control {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.category-control span {
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
}

.category-control select,
.chip-category-select {
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #ffffff;
  color: #0f172a;
  font-family: inherit;
  font-size: 0.76rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.category-control select {
  width: 100%;
  padding: 0.55rem 0.65rem;
}

.category-control select:focus,
.chip-category-select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

/* ── Chips ────────────────────────────────────────── */
.file-chip-list { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.document-list { flex-direction: column; flex-wrap: nowrap; }

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
.document-chip {
  width: 100%;
  border-radius: 12px;
  padding: 0.55rem 0.6rem;
  align-items: center;
  box-sizing: border-box;
}

.chip-thumb { width: 20px; height: 20px; border-radius: 4px; object-fit: cover; flex-shrink: 0; }
.chip-icon  { font-size: 0.65rem; font-weight: 800; letter-spacing: 0.04em; flex-shrink: 0; }
.chip-main { min-width: 0; flex: 1; display: flex; flex-direction: column; gap: 0.15rem; }
.chip-name  { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 120px; }
.document-chip .chip-name { max-width: 100%; }
.chip-category { font-size: 0.68rem; color: #64748b; font-weight: 600; }
.chip-category-select {
  width: min(190px, 42%);
  padding: 0.42rem 0.5rem;
  flex-shrink: 0;
}
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
.empty-card { padding: 1.5rem; }
.empty-actions { color: #94a3b8; font-size: 0.85rem; }
.input-group input:disabled,
.input-group select:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

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
  .document-chip { align-items: flex-start; flex-wrap: wrap; }
  .chip-category-select { width: 100%; }
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
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer;
  color: #475569; font-size: 0.75rem; font-weight: 700; padding: 0.38rem 0.65rem;
  display: inline-flex; align-items: center; justify-content: center;
  transition: border-color 0.2s, color 0.2s, background 0.2s, transform 0.2s;
}
.btn-icon:hover { border-color: #2563eb; color: #1d4ed8; background: #eff6ff; transform: translateY(-1px); }
.btn-icon.danger:hover { border-color: #fecaca; color: #b91c1c; background: #fef2f2; }

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(3px);
}

.label-modal {
  width: min(920px, 100%);
  max-height: 92vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.24);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-eyebrow {
  margin: 0 0 0.25rem;
  color: #2563eb;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.modal-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 1.1rem;
}

.modal-close {
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  font-size: 1.5rem;
  line-height: 1;
}

.modal-body {
  padding: 1.25rem;
  overflow-y: auto;
}

.label-preview-wrap {
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
}

.label-preview {
  width: 100%;
  display: block;
  border-radius: 8px;
  background: #ffffff;
}

.label-loading {
  padding: 3rem;
  text-align: center;
  color: #64748b;
  border: 1px dashed #cbd5e1;
  border-radius: 12px;
  background: #f8fafc;
}

.label-url-box {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-top: 1rem;
  padding: 0.85rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #ffffff;
}

.label-url-box span {
  color: #64748b;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.label-url-box a {
  color: #1d4ed8;
  font-size: 0.82rem;
  font-weight: 600;
  overflow-wrap: anywhere;
  text-decoration: none;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .modal-overlay { padding: 0.75rem; }
  .modal-footer { flex-direction: column; }
  .modal-footer .btn { width: 100%; }
}
</style>
