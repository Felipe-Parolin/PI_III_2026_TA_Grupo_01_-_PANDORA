<template>
  <div class="crud-page">
    <section class="page-header animate-fade-in">
      <p class="eyebrow">Manutenção Corretiva</p>
      <h2>Abrir Novo Chamado</h2>
      <p class="page-copy">Relate falhas enviando áudio, texto e imagens para a equipe técnica.</p>
    </section>

    <section v-if="canUseOpenCall" class="card form-card animate-fade-in">
      <div class="card-header">
        <h3>Detalhes da Ocorrência</h3>
        <p>Preencha os dados da falha para abrir o chamado técnico.</p>
      </div>

      <form @submit.prevent="salvarChamado" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label>Equipamento com Falha</label>
            <div class="equipment-search">
              <div class="equipment-search-box">
                <input
                  v-model="equipamentoBusca"
                  type="search"
                  placeholder="Pesquise por nome, ID interno, ID do sistema ou QR..."
                  autocomplete="off"
                  :disabled="carregando || !canViewEquipment"
                  @focus="abrirBuscaEquipamento"
                  @input="handleEquipamentoBusca"
                  @keydown.enter.prevent="selecionarPrimeiroEquipamento"
                  @keydown.esc="equipamentoBuscaAberta = false"
                  @blur="fecharBuscaEquipamento"
                />
                <button
                  v-if="form.equipamento"
                  type="button"
                  class="equipment-clear"
                  title="Limpar equipamento selecionado"
                  :disabled="carregando"
                  @mousedown.prevent
                  @click="limparEquipamentoSelecionado"
                >
                  &times;
                </button>
              </div>

              <div
                v-if="equipamentoBuscaAberta && canViewEquipment && !carregando"
                class="equipment-results"
              >
                <button
                  v-for="e in equipamentosFiltrados"
                  :key="e.id"
                  type="button"
                  class="equipment-result"
                  @mousedown.prevent="selecionarEquipamento(e)"
                >
                  <span class="equipment-result-title">{{ e.nome_equipamento || 'Equipamento sem nome' }}</span>
                  <span class="equipment-result-meta">
                    ID interno: #{{ e.id_interno || e.id }} - Sistema: {{ e.id }}
                    <template v-if="e.qr_code_token"> - QR: {{ e.qr_code_token }}</template>
                  </span>
                </button>
                <p v-if="!equipamentosFiltrados.length" class="equipment-empty">
                  Nenhum equipamento encontrado para essa busca.
                </p>
              </div>

              <p v-if="equipamentoSelecionado" class="equipment-selected">
                Selecionado: <strong>#{{ equipamentoSelecionado.id_interno || equipamentoSelecionado.id }}</strong>
                {{ equipamentoSelecionado.nome_equipamento }}
              </p>
              <p v-else class="equipment-hint">
                Digite para pesquisar e selecione um equipamento da lista.
              </p>
            </div>
          </div>

          <div class="input-group">
            <label>Nível de Urgência</label>
            <select v-model="form.urgencia" required>
              <option value="Baixa">Baixa</option>
              <option value="Média">Média</option>
              <option value="Alta">Alta</option>
              <option value="Crítica">Crítica</option>
            </select>
          </div>
        </div>

        <div class="input-group">
          <label>Descrição do Problema</label>
          <div class="textarea-container">
            <textarea
              v-model="form.descricao_problema"
              placeholder="Descreva o defeito detalhadamente..."
              class="custom-textarea"
              required
              :disabled="carregando || isRecording || transcrevendo"
            ></textarea>
            <button
              type="button"
              @click="toggleRecording"
              :class="['inner-mic-btn', { 'recording-active': isRecording }]"
              :title="isRecording ? 'Parar gravação' : 'Gravar por voz'"
              :disabled="carregando || transcrevendo"
            >
              <span v-if="transcrevendo" class="icon-text">...</span>
              <span v-else-if="!isRecording" class="icon-text">MIC</span>
              <span v-else class="icon-text">REC</span>
            </button>
          </div>
          <p v-if="isRecording" class="mic-hint recording">Gravando... clique no botão para parar.</p>
          <p v-else-if="transcrevendo" class="mic-hint processing">Transcrevendo áudio...</p>
        </div>

        <!-- ── Fotos do Problema ── -->
        <div class="upload-section-container">
          <div class="upload-block">
            <div class="upload-block-header">
              <label class="small-label">Fotos do Problema <span class="optional-tag">opcional</span></label>
              <label for="fotoProblemaInput" class="btn-add-file">+ Adicionar foto</label>
              <input
                type="file"
                id="fotoProblemaInput"
                @change="handleFotos"
                accept="image/*"
                multiple
                class="hidden-input"
              />
            </div>

            <div v-if="fotosProblema.length" class="file-chip-list">
              <div
                v-for="(f, i) in fotosProblema"
                :key="i"
                class="file-chip foto-chip foto-chip-new"
              >
                <img :src="f.preview" class="chip-thumb" />
                <span class="chip-name">{{ f.nome }}</span>
                <button type="button" @click="removerFoto(i)" class="chip-remove">×</button>
              </div>
            </div>
            <p v-else class="upload-empty">Nenhuma foto adicionada. Aceita PNG e JPG.</p>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="carregando || isRecording || transcrevendo || !canUseOpenCall" class="btn btn-primary">
            <span v-if="!carregando">Abrir Chamado</span>
            <span v-else>Enviando...</span>
          </button>
        </div>
      </form>
    </section>

    <section v-else class="card empty-card animate-fade-in">
      <div class="card-header">
        <h3>Acesso limitado</h3>
        <p>Para abrir chamados, libere ordens_servico.criar e equipamentos.visualizar.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { getStoredPermissions, hasPermission } from '../utils/permissions'

const route = useRoute()
const carregando = ref(false)
const equipamentos = ref([])
const equipamentoBusca = ref('')
const equipamentoBuscaAberta = ref(false)
const isRecording = ref(false)
const transcrevendo = ref(false)
const fotosProblema = ref([]) // [{ file, nome, preview }]
let mediaRecorder = null
let audioChunks = []
const permissions = computed(() => getStoredPermissions())
const canCreateOS = computed(() => hasPermission('ordens_servico.criar', permissions.value))
const canViewEquipment = computed(() => hasPermission('equipamentos.visualizar', permissions.value))
const canUseOpenCall = computed(() => canCreateOS.value && canViewEquipment.value)

const form = ref({
  equipamento: '',
  urgencia: 'Média',
  descricao_problema: '',
  status: 'Aberto'
})

const normalizarBusca = (valor) => String(valor ?? '')
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .trim()

const getEquipamentoLabel = (equipamento) => {
  if (!equipamento) return ''
  return `#${equipamento.id_interno || equipamento.id} - ${equipamento.nome_equipamento || 'Equipamento sem nome'}`
}

const equipamentoSelecionado = computed(() =>
  equipamentos.value.find((item) => String(item.id) === String(form.value.equipamento)) || null
)

const equipamentosFiltrados = computed(() => {
  const termo = normalizarBusca(equipamentoBusca.value)
  const lista = !termo
    ? equipamentos.value
    : equipamentos.value.filter((equipamento) => {
      const camposBusca = [
        equipamento.id,
        equipamento.id_interno,
        equipamento.nome_equipamento,
        equipamento.tipo_equipamento,
        equipamento.qr_code_token,
        equipamento.status
      ]

      return camposBusca.some((campo) => normalizarBusca(campo).includes(termo))
    })

  return lista.slice(0, 10)
})

const abrirBuscaEquipamento = () => {
  if (carregando.value || !canViewEquipment.value) return
  equipamentoBuscaAberta.value = true
}

const fecharBuscaEquipamento = () => {
  window.setTimeout(() => {
    equipamentoBuscaAberta.value = false
  }, 120)
}

const handleEquipamentoBusca = () => {
  form.value.equipamento = ''
  equipamentoBuscaAberta.value = true
}

const selecionarEquipamento = (equipamento) => {
  form.value.equipamento = equipamento.id
  equipamentoBusca.value = getEquipamentoLabel(equipamento)
  equipamentoBuscaAberta.value = false
}

const selecionarPrimeiroEquipamento = () => {
  const [primeiroEquipamento] = equipamentosFiltrados.value
  if (primeiroEquipamento) selecionarEquipamento(primeiroEquipamento)
}

const limparEquipamentoSelecionado = ({ manterAberta = true } = {}) => {
  form.value.equipamento = ''
  equipamentoBusca.value = ''
  equipamentoBuscaAberta.value = manterAberta
}

// ── Áudio / transcrição ──────────────────────────────────────────────────────
const getAudioMimeType = () => {
  if (!window.MediaRecorder) return ''
  if (MediaRecorder.isTypeSupported('audio/webm')) return 'audio/webm'
  if (MediaRecorder.isTypeSupported('audio/ogg')) return 'audio/ogg'
  return ''
}

const getAudioExtension = (mimeType) => {
  if (mimeType.includes('webm')) return 'webm'
  if (mimeType.includes('ogg')) return 'ogg'
  if (mimeType.includes('mp4')) return 'mp4'
  return 'wav'
}

const aplicarTranscricao = (transcricao) => {
  const texto = String(transcricao || '').trim()
  if (!texto) return

  const descricaoAtual = form.value.descricao_problema.trim()
  form.value.descricao_problema = descricaoAtual
    ? `${descricaoAtual}\n${texto}`
    : texto
}

const enviarAudioParaTranscricao = async (audioBlob, filename) => {
  const formData = new FormData()
  formData.append('audio', audioBlob, filename)

  const res = await axios.post(
    'http://127.0.0.1:8000/api/analises-llm/transcrever/',
    formData,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  )

  aplicarTranscricao(res.data.transcricao)
}

const toggleRecording = async () => {
  if (!window.MediaRecorder || !navigator.mediaDevices?.getUserMedia) {
    alert('Gravação de áudio não disponível neste navegador.')
    return
  }

  if (!isRecording.value) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mimeType = getAudioMimeType()
      mediaRecorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream)
      audioChunks = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data?.size) audioChunks.push(event.data)
      }

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach(track => track.stop())

        const blobType = mediaRecorder.mimeType || mimeType || 'audio/webm'
        const audioBlob = new Blob(audioChunks, { type: blobType })
        const extension = getAudioExtension(blobType)

        transcrevendo.value = true
        try {
          await enviarAudioParaTranscricao(audioBlob, `chamado.${extension}`)
        } catch (err) {
          console.error('Erro ao transcrever áudio:', err.response?.data || err)
          const detalhe = err.response?.data?.error || 'Erro ao transcrever o áudio.'
          alert(`Erro ao transcrever o áudio: ${detalhe}`)
        } finally {
          transcrevendo.value = false
          audioChunks = []
        }
      }

      mediaRecorder.start()
      isRecording.value = true
    } catch (err) {
      console.error('Erro ao acessar microfone:', err)
      alert('Microfone não disponível ou permissão negada.')
    }
  } else {
    if (mediaRecorder?.state === 'recording') {
      mediaRecorder.stop()
    }
    isRecording.value = false
  }
}

// ── Handlers de foto ──────────────────────────────────────────────────────────
const handleFotos = (e) => {
  Array.from(e.target.files).forEach(file => {
    fotosProblema.value.push({
      file,
      nome: file.name,
      preview: URL.createObjectURL(file)
    })
  })
  e.target.value = ''
}

const removerFoto = (index) => {
  URL.revokeObjectURL(fotosProblema.value[index].preview)
  fotosProblema.value.splice(index, 1)
}

// ── Auth headers ──────────────────────────────────────────────────────────────
const getHeaders = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
})

// ── Fetch ─────────────────────────────────────────────────────────────────────
const fetchEquipamentos = async () => {
  if (!canViewEquipment.value) {
    equipamentos.value = []
    return
  }
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/equipamentos/', getHeaders())
    equipamentos.value = res.data
    preselecionarEquipamentoPorQuery()
  } catch (e) {
    console.error('Erro ao buscar equipamentos:', e.response?.status)
  }
}

const preselecionarEquipamentoPorQuery = () => {
  const equipamentoId = route.query.equipamento
  const idInterno = route.query.id_interno
  const token = route.query.token

  const equipamento = equipamentos.value.find((item) => (
    (equipamentoId && String(item.id) === String(equipamentoId)) ||
    (idInterno && String(item.id_interno) === String(idInterno)) ||
    (token && String(item.qr_code_token) === String(token))
  ))

  if (equipamento) {
    selecionarEquipamento(equipamento)
  }
}

// ── Salvar chamado + fotos ────────────────────────────────────────────────────
const salvarChamado = async () => {
  if (!canCreateOS.value) {
    alert('Voce nao possui permissao para abrir chamados.')
    return
  }
  if (!canViewEquipment.value) {
    alert('Voce precisa da permissao equipamentos.visualizar para selecionar o equipamento.')
    return
  }
  const usuarioId = localStorage.getItem('user_id') ? parseInt(localStorage.getItem('user_id')) : null
  if (!usuarioId) return alert('Sessão expirada. Faça login novamente.')
  if (!form.value.equipamento) return alert('Selecione um equipamento.')

  carregando.value = true

  try {
    // 1. Cria a OS
    const payload = {
      equipamento: form.value.equipamento,
      urgencia: form.value.urgencia,
      descricao_problema: form.value.descricao_problema,
      status: 'Aberto',
      usuario_abertura: usuarioId
    }
    const resOS = await axios.post('http://127.0.0.1:8000/api/ordens-servico/', payload, getHeaders())
    const osId = resOS.data.id

    // 2. Faz upload das fotos como DocumentoEquipamento com prefixo especial
    //    O prefixo "Problema OS#<id>" permite distingui-las na exibição da OS
    for (const foto of fotosProblema.value) {
      const docData = new FormData()
      docData.append('equipamento', form.value.equipamento)
      docData.append('caminho_arquivo', foto.file)
      docData.append('nome_arquivo', `Problema OS#${osId} - ${foto.nome}`)
      try {
        await axios.post('http://127.0.0.1:8000/api/documentos-equipamento/', docData, getHeaders())
      } catch (docErr) {
        console.error('Erro ao salvar foto do problema:', docErr.response?.data)
        alert(`Erro no upload de "${foto.nome}":\n` + JSON.stringify(docErr.response?.data))
      }
    }

    alert('Chamado aberto com sucesso!')

    // 3. Limpa o formulário
    form.value.descricao_problema = ''
    limparEquipamentoSelecionado({ manterAberta: false })
    fotosProblema.value.forEach(f => URL.revokeObjectURL(f.preview))
    fotosProblema.value = []

  } catch (e) {
    console.error('Erro ao abrir chamado:', e.response?.data)
    alert('Erro ao abrir chamado. Verifique os campos.')
  } finally {
    carregando.value = false
  }
}

onMounted(fetchEquipamentos)
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
.form-card, .empty-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.card-header h3 { margin: 0; color: #0f172a; }
.card-header p { margin: 0.4rem 0 0; color: #475569; }

/* ── Formulário ───────────────────────────────────── */
.crud-form { display: flex; flex-direction: column; gap: 1rem; }
.input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }

.input-group input,
.input-group select,
.input-group textarea {
  box-sizing: border-box; width: 100%;
  padding: 0.9rem 1rem; border: 1px solid #cbd5e1;
  border-radius: 12px; background: #f8fafc;
  color: #0f172a; font-size: 0.95rem; font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
}
.input-group input:focus,
.input-group select:focus,
.input-group textarea:focus {
  outline: none; background: #ffffff;
  border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14);
}
.input-group textarea:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.equipment-search {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.equipment-search-box {
  position: relative;
}
.equipment-search-box input {
  padding-right: 2.8rem;
}
.equipment-clear {
  position: absolute;
  top: 50%;
  right: 0.7rem;
  transform: translateY(-50%);
  width: 30px;
  height: 30px;
  border: 1px solid #cbd5e1;
  border-radius: 50%;
  background: #ffffff;
  color: #64748b;
  font-size: 1.1rem;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s, background-color 0.2s;
}
.equipment-clear:hover:not(:disabled) {
  color: #0f172a;
  border-color: #94a3b8;
  background: #f8fafc;
}
.equipment-clear:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.equipment-results {
  position: absolute;
  z-index: 20;
  top: calc(100% + 0.3rem);
  left: 0;
  right: 0;
  max-height: 280px;
  overflow-y: auto;
  padding: 0.35rem;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 18px 35px rgba(15, 23, 42, 0.14);
}
.equipment-result {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.2rem;
  padding: 0.75rem 0.85rem;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: #0f172a;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
}
.equipment-result:hover,
.equipment-result:focus {
  outline: none;
  background: #eff6ff;
}
.equipment-result-title {
  width: 100%;
  font-size: 0.92rem;
  font-weight: 700;
  overflow-wrap: anywhere;
}
.equipment-result-meta {
  width: 100%;
  color: #64748b;
  font-size: 0.78rem;
  line-height: 1.35;
  overflow-wrap: anywhere;
}
.equipment-empty,
.equipment-hint,
.equipment-selected {
  margin: 0;
  font-size: 0.78rem;
  line-height: 1.35;
}
.equipment-empty {
  padding: 0.75rem 0.85rem;
  color: #64748b;
}
.equipment-hint {
  color: #64748b;
}
.equipment-selected {
  color: #166534;
}
.equipment-selected strong {
  color: #14532d;
}

/* ── Textarea + mic ───────────────────────────────── */
.textarea-container { position: relative; width: 100%; }
.custom-textarea { min-height: 160px; resize: none; padding-right: 3.5rem; line-height: 1.5; }

.inner-mic-btn {
  position: absolute; right: 12px; bottom: 12px;
  width: 40px; height: 40px; border-radius: 50%;
  border: 1px solid #e2e8f0; background: white; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: background 0.2s, border-color 0.2s;
}
.inner-mic-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.recording-active { background: #fee2e2; border-color: #ef4444; }
.icon-text {
  font-size: 0.58rem;
  font-weight: 800;
  letter-spacing: 0.03em;
}
.mic-hint { font-size: 0.78rem; font-weight: 600; margin: 5px 0 0; }
.mic-hint.recording { color: #ef4444; }
.mic-hint.processing { color: #2563eb; }

/* ── Upload ───────────────────────────────────────── */
.upload-section-container {
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
}
.upload-block { display: flex; flex-direction: column; gap: 0.6rem; }
.upload-block-header { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
.hidden-input { opacity: 0; position: absolute; z-index: -1; width: 0.1px; }
.small-label { font-size: 0.85rem; color: #334155; font-weight: 600; }
.optional-tag {
  font-size: 0.7rem; font-weight: 500; color: #94a3b8;
  background: #f1f5f9; border-radius: 20px;
  padding: 1px 8px; margin-left: 4px;
}

.btn-add-file {
  display: inline-flex; align-items: center;
  padding: 0.3rem 0.75rem;
  font-size: 0.78rem; font-weight: 600; color: #2563eb;
  border: 1.5px solid #bfdbfe; border-radius: 20px;
  background: #eff6ff; cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.btn-add-file:hover { background: #dbeafe; border-color: #93c5fd; }

.upload-empty { font-size: 0.8rem; color: #94a3b8; margin: 0; }

.file-chip-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.file-chip {
  display: inline-flex; align-items: center; gap: 0.45rem;
  padding: 0.3rem 0.6rem 0.3rem 0.4rem;
  border-radius: 20px; font-size: 0.78rem; font-weight: 500;
  max-width: 220px;
}
.foto-chip { background: #eff6ff; border: 1px solid #bfdbfe; color: #1d4ed8; }
.foto-chip-new { border-style: dashed; }
.chip-thumb { width: 22px; height: 22px; border-radius: 4px; object-fit: cover; flex-shrink: 0; }
.chip-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
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
.btn { border: none; border-radius: 12px; padding: 0.8rem 1.5rem; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s, background-color 0.2s; }
.btn:hover:not(:disabled) { transform: translateY(-1px); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary { background: #2563eb; color: #ffffff; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24); }

/* ── Animação ─────────────────────────────────────── */
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out; }

/* ── Mobile ≤ 768px ───────────────────────────────── */
@media (max-width: 768px) {
  .page-header { padding: 1.1rem 1.2rem; border-radius: 16px; }
  .page-header h2 { font-size: 1.4rem; }
  .form-card { padding: 1.1rem 1.2rem; border-radius: 16px; }
  .card { border-radius: 16px; }
  .input-row { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column; }
  .form-actions .btn { width: 100%; }
}

/* ── Mobile pequeno ≤ 480px ───────────────────────── */
@media (max-width: 480px) {
  .page-header h2 { font-size: 1.2rem; }
  .card-header h3 { font-size: 1rem; }
  .input-group input,
  .input-group select,
  .input-group textarea { padding: 0.75rem 0.85rem; }
  .btn { padding: 0.7rem 1rem; }
}
</style>
