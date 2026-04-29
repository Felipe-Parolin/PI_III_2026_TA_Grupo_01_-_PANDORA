<template>
  <div class="dashboard-content animate-fade-in">
    <header class="p-header-card mb-4">
      <div class="card-padding">
        <p class="p-eyebrow">PAINEL DE MANUTENÇÃO</p>
        <h2 class="p-title">Ordens de Serviço</h2>
        <p class="p-subtitle">Gerencie as intervenções e alimente a base de conhecimento da IA.</p>
      </div>
    </header>

    <!-- PAINEL DE FILTROS -->
    <section class="filters-panel mb-4">
      <div class="filter-group">
        <label class="p-field-label">ID / Equipamento</label>
        <input v-model="filtros.busca" type="text" placeholder="Ex: 10 ou Motor..." class="filter-input">
      </div>
      <div class="filter-group">
        <label class="p-field-label">Token QR Code</label>
        <input v-model="filtros.token" type="text" placeholder="Token do patrimônio" class="filter-input">
      </div>
      <div class="filter-group">
        <label class="p-field-label">Criticidade</label>
        <select v-model="filtros.urgencia" class="filter-input">
          <option value="">Todas</option>
          <option value="Baixa">Baixa</option>
          <option value="Média">Média</option>
          <option value="Alta">Alta</option>
          <option value="Crítica">Crítica</option>
        </select>
      </div>
      <button @click="limparFiltros" class="btn-clear-filters">✕ Limpar</button>
    </section>

    <div class="p-main-container">
      <div class="p-tabs-container mb-4">
        <button @click="tabAtiva = 'abertas'" :class="['p-tab-btn', { active: tabAtiva === 'abertas' }]">
          Abertas <span class="p-badge">{{ filtrarPorStatus('Aberto').length }}</span>
        </button>
        <button @click="tabAtiva = 'andamento'" :class="['p-tab-btn', { active: tabAtiva === 'andamento' }]">
          Em Andamento <span class="p-badge warning">{{ filtrarPorStatus('Em Andamento').length }}</span>
        </button>
        <button @click="tabAtiva = 'concluidas'" :class="['p-tab-btn', { active: tabAtiva === 'concluidas' }]">
          Concluídas <span class="p-badge success">{{ filtrarPorStatus('Concluído').length }}</span>
        </button>
      </div>

      <div class="p-os-grid">
        <div v-for="os in osFiltradas" :key="os.id" class="p-os-card animate-slide-up">
          <div :class="['priority-bar', os.urgencia?.toLowerCase()]"></div>

          <div class="os-card-header">
            <span class="os-number">#{{ os.id }}</span>
            <span :class="['status-tag', os.status?.replace(' ', '-').toLowerCase()]">{{ os.status }}</span>
          </div>

          <div class="os-card-body">
            <h3 class="equip-name">{{ os.equipamento_nome || 'Equipamento' }}</h3>
            <div class="equip-meta-row">
              <span class="equip-code">ID: {{ os.equipamento_id_interno ?? 'N/A' }}</span>
              <span class="equip-token">QR: {{ os.equipamento_qr_token || 'N/A' }}</span>
            </div>

            <div class="info-row mt-3">
              <span class="info-label">Relatado por:</span>
              <span class="info-value">{{ os.usuario_abertura_nome || 'Usuário' }}</span>
            </div>

            <p class="problem-preview">
              <strong>Problema:</strong> "{{ truncateText(os.descricao_problema, 80) }}"
            </p>
          </div>

          <div class="os-card-footer">
            <button v-if="os.status === 'Aberto'" @click="assumirOS(os.id)" class="btn-p-sm primary">Assumir OS</button>
            <button v-if="os.status === 'Em Andamento'" @click="abrirModalFinalizar(os)" class="btn-p-sm success">Finalizar</button>
            <button @click="verDetalhes(os)" class="btn-p-sm outline">Ver Detalhes</button>
          </div>
        </div>
      </div>

      <div v-if="osFiltradas.length === 0" class="empty-results">
        Nenhum chamado encontrado com esses filtros.
      </div>
    </div>

    <!-- ======================== MODAL DETALHES ======================== -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="modalDetalhes" class="modal-overlay" @click.self="modalDetalhes = false">
          <div class="modal-box">
            <div class="modal-header">
              <h3 class="modal-title">Detalhes da OS <span class="modal-id">#{{ osSelecionada?.id }}</span></h3>
              <button @click="modalDetalhes = false" class="modal-close">&times;</button>
            </div>

            <div class="modal-body scrollable-content">

              <!-- Chips de status e criticidade -->
              <div class="detail-chips">
                <span class="p-chip">{{ osSelecionada?.status }}</span>
                <span :class="['p-chip', 'urgencia-chip', osSelecionada?.urgencia?.toLowerCase()]">
                  {{ osSelecionada?.urgencia || 'Sem criticidade' }}
                </span>
              </div>

              <!-- Bloco de info do equipamento -->
              <div class="detail-section equip-info-block mt-3">
                <div class="equip-info-grid">
                  <div class="equip-info-item">
                    <span class="equip-info-label">Equipamento</span>
                    <span class="equip-info-value">{{ osSelecionada?.equipamento_nome }}</span>
                  </div>
                  <div class="equip-info-item">
                    <span class="equip-info-label">ID Interno</span>
                    <span class="equip-info-value mono">{{ osSelecionada?.equipamento_id_interno ?? 'N/A' }}</span>
                  </div>
                  <div class="equip-info-item">
                    <span class="equip-info-label">Token QR</span>
                    <span class="equip-info-value mono">{{ osSelecionada?.equipamento_qr_token || 'N/A' }}</span>
                  </div>
                  <div class="equip-info-item">
                    <span class="equip-info-label">Tipo</span>
                    <span class="equip-info-value">{{ osSelecionada?.equipamento_tipo || 'N/A' }}</span>
                  </div>
                </div>
              </div>

              <!-- Problema relatado -->
              <div class="detail-section mt-4">
                <p class="p-section-label">Relatado por: {{ osSelecionada?.usuario_abertura_nome }}</p>
                <div class="p-text-box">
                  <strong class="problem-prefix">Problema:</strong> "{{ osSelecionada?.descricao_problema }}"
                </div>
              </div>

              <!-- ===== SEÇÃO: FOTOS DO PROBLEMA ===== -->
              <div class="detail-section mt-4">
                <p class="p-section-label problem-label">📷 Fotos do Problema</p>
                <div class="attachments-container">
                  <template v-if="fotosDoProblema.length">
                    <template v-for="doc in fotosDoProblema" :key="doc.id">
                      <a :href="doc.caminho_arquivo" target="_blank" class="attachment-link">
                        <span class="file-icon">🖼️</span>
                        <div class="file-meta">
                          <span class="file-name">{{ nomeExibicao(doc.nome_arquivo) }}</span>
                          <span class="file-action">Visualizar imagem</span>
                        </div>
                      </a>
                      <div class="foto-preview-wrapper">
                        <img :src="doc.caminho_arquivo" :alt="doc.nome_arquivo" class="foto-preview" />
                      </div>
                    </template>
                  </template>
                  <div v-else class="p-text-box empty-box">
                    Nenhuma foto enviada pelo operador.
                  </div>
                </div>
              </div>

              <!-- ===== SEÇÃO: DOCUMENTAÇÃO TÉCNICA DO EQUIPAMENTO ===== -->
              <div class="detail-section mt-4">
                <p class="p-section-label">📎 Documentação Técnica do Equipamento</p>
                <div class="attachments-container">
                  <template v-if="docsDoEquipamento.length">
                    <template v-for="doc in docsDoEquipamento" :key="doc.id">

                      <!-- É uma imagem -->
                      <template v-if="docIsImagem(doc)">
                        <a :href="doc.caminho_arquivo" target="_blank" class="attachment-link">
                          <span class="file-icon">🖼️</span>
                          <div class="file-meta">
                            <span class="file-name">{{ doc.nome_arquivo }}</span>
                            <span class="file-action">Visualizar imagem</span>
                          </div>
                        </a>
                        <div class="foto-preview-wrapper">
                          <img :src="doc.caminho_arquivo" :alt="doc.nome_arquivo" class="foto-preview" />
                        </div>
                      </template>

                      <!-- É um PDF ou outro documento -->
                      <a v-else :href="doc.caminho_arquivo" target="_blank" class="attachment-link">
                        <span class="file-icon">📄</span>
                        <div class="file-meta">
                          <span class="file-name">{{ doc.nome_arquivo }}</span>
                          <span class="file-action">Abrir documento</span>
                        </div>
                      </a>

                    </template>
                  </template>
                  <div v-else class="p-text-box empty-box">
                    Nenhum anexo técnico disponível para este equipamento.
                  </div>
                </div>
              </div>

              <!-- Solução (se concluída) -->
              <div v-if="osSelecionada?.descricao_solucao" class="detail-section mt-4">
                <p class="p-section-label success-label">
                  ✅ Solução — Técnico: {{ osSelecionada?.usuario_tecnico_nome || 'Não informado' }}
                </p>
                <div class="p-text-box success-box">{{ osSelecionada?.descricao_solucao }}</div>
              </div>

              <div v-else-if="osSelecionada?.usuario_tecnico_nome" class="detail-section mt-4">
                <p class="p-section-label warning-label">
                  🔧 Técnico Responsável: {{ osSelecionada?.usuario_tecnico_nome }}
                </p>
              </div>

            </div>

            <div class="modal-footer">
              <button
                v-if="osSelecionada?.status === 'Em Andamento'"
                @click="() => { modalDetalhes = false; abrirModalFinalizar(osSelecionada) }"
                class="btn-p-confirm success"
              >
                Finalizar OS
              </button>
              <button @click="modalDetalhes = false" class="btn-p-confirm outline">Fechar</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ======================== MODAL FINALIZAR ======================== -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="modalFinalizar" class="modal-overlay" @click.self="modalFinalizar = false">
          <div class="modal-box">
            <div class="modal-header">
              <h3 class="modal-title">Finalizar OS <span class="modal-id">#{{ osSelecionada?.id }}</span></h3>
              <button @click="modalFinalizar = false" class="modal-close">&times;</button>
            </div>
            <div class="modal-body">
              <div class="p-info-alert">
                <strong>💡 Dica PANDORA:</strong> Sua descrição alimenta a inteligência do sistema.
              </div>
              <div class="field-group mt-3">
                <label class="p-field-label">Como foi resolvido?</label>
                <div class="textarea-mic-wrapper">
                  <textarea
                    v-model="finalizacao.descricao_solucao"
                    class="p-textarea"
                    rows="4"
                    placeholder="Descreva detalhadamente a solução aplicada..."
                    :disabled="isRecording || transcrevendo"
                  ></textarea>
                  <button
                    @click="toggleRecording"
                    type="button"
                    :class="['inner-mic-btn', { 'recording-active': isRecording }]"
                    :title="isRecording ? 'Parar gravação' : 'Gravar por voz'"
                    :disabled="transcrevendo"
                  >
                    <span v-if="transcrevendo">⏳</span>
                    <span v-else-if="!isRecording">🎤</span>
                    <span v-else>🔴</span>
                  </button>
                </div>
                <p v-if="isRecording" class="mic-hint recording">🎙️ Gravando... clique no botão para parar.</p>
                <p v-else-if="transcrevendo" class="mic-hint processing">⏳ Transcrevendo áudio...</p>
              </div>
            </div>
            <div class="modal-footer">
              <button @click="modalFinalizar = false" class="btn-p-cancel">Cancelar</button>
              <button @click="confirmarFinalizacao" :disabled="loading || isRecording || transcrevendo" class="btn-p-confirm">
                {{ loading ? 'Salvando...' : '💾 Concluir' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue'
import axios from 'axios'

const tabAtiva = ref('abertas')
const ordens = ref([])
const modalFinalizar = ref(false)
const modalDetalhes = ref(false)
const loading = ref(false)
const osSelecionada = ref(null)
const finalizacao = ref({ descricao_solucao: '' })

// ── Áudio / transcrição ──────────────────────────────────────────────────────
const isRecording = ref(false)
const transcrevendo = ref(false)
let mediaRecorder = null
let audioChunks = []

const filtros = reactive({ busca: '', token: '', urgencia: '' })

const API_BASE = 'http://localhost:8000/api/ordens-servico/'

const getHeaders = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
})

// ── Helpers de classificação de documentos ───────────────────────────────────

const docIsImagem = (doc) => {
  const nome = (doc.nome_arquivo || '').toLowerCase()
  const caminho = (doc.caminho_arquivo || '').toLowerCase()
  return (
    nome.startsWith('foto') ||
    /\.(jpg|jpeg|png|gif|webp)$/.test(nome) ||
    /\.(jpg|jpeg|png|gif|webp)$/.test(caminho)
  )
}

const docIsProblema = (doc, osId) => {
  const nome = (doc.nome_arquivo || '').toLowerCase()
  return nome.startsWith(`problema os#${osId}`)
}

const nomeExibicao = (nomeArquivo) => {
  return (nomeArquivo || '').replace(/^Problema OS#\d+ - /i, '')
}

const fotosDoProblema = computed(() => {
  if (!osSelecionada.value?.equipamento_documentos) return []
  return osSelecionada.value.equipamento_documentos.filter(
    doc => docIsProblema(doc, osSelecionada.value.id)
  )
})

const docsDoEquipamento = computed(() => {
  if (!osSelecionada.value?.equipamento_documentos) return []
  return osSelecionada.value.equipamento_documentos.filter(
    doc => !docIsProblema(doc, osSelecionada.value.id)
  )
})

// ── Fetch ────────────────────────────────────────────────────────────────────

const fetchOS = async () => {
  try {
    const res = await axios.get(API_BASE, getHeaders())
    ordens.value = res.data
  } catch (e) {
    console.error('Erro ao buscar OS:', e)
  }
}

const limparFiltros = () => {
  filtros.busca = ''
  filtros.token = ''
  filtros.urgencia = ''
}

const osFiltradas = computed(() => {
  const statusMap = {
    abertas: 'Aberto',
    andamento: 'Em Andamento',
    concluidas: 'Concluído'
  }
  return ordens.value.filter(o => {
    const matchStatus = o.status === statusMap[tabAtiva.value]
    const termo = filtros.busca.toLowerCase()
    const matchBusca = !filtros.busca ||
      o.id.toString().includes(termo) ||
      o.equipamento_id_interno?.toString().includes(termo) ||
      o.equipamento_nome?.toLowerCase().includes(termo)
    const matchToken = !filtros.token ||
      o.equipamento_qr_token?.toLowerCase().includes(filtros.token.toLowerCase())
    const matchUrgencia = !filtros.urgencia || o.urgencia === filtros.urgencia
    return matchStatus && matchBusca && matchToken && matchUrgencia
  })
})

const filtrarPorStatus = (status) => ordens.value.filter(o => o.status === status)

const assumirOS = async (id) => {
  try {
    await axios.patch(`${API_BASE}${id}/`, { status: 'Em Andamento' }, getHeaders())
    fetchOS()
  } catch (e) {
    alert('Erro ao assumir OS')
  }
}

const verDetalhes = (os) => {
  osSelecionada.value = os
  modalDetalhes.value = true
}

const abrirModalFinalizar = (os) => {
  osSelecionada.value = os
  finalizacao.value = { descricao_solucao: '' }
  isRecording.value = false
  transcrevendo.value = false
  modalFinalizar.value = true
}

const confirmarFinalizacao = async () => {
  if (!finalizacao.value.descricao_solucao.trim()) return alert('Descreva a solução!')
  loading.value = true
  try {
    await axios.patch(`${API_BASE}${osSelecionada.value.id}/`, {
      status: 'Concluído',
      descricao_solucao: finalizacao.value.descricao_solucao,
      data_fechamento: new Date().toISOString()
    }, getHeaders())
    modalFinalizar.value = false
    fetchOS()
  } catch (e) {
    alert('Erro ao finalizar OS')
  } finally {
    loading.value = false
  }
}

// ── Gravação de áudio ────────────────────────────────────────────────────────

const toggleRecording = async () => {
  if (!isRecording.value) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(stream)
      audioChunks = []

      mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data)

      mediaRecorder.onstop = async () => {
        // Para todas as trilhas do microfone imediatamente
        stream.getTracks().forEach(t => t.stop())

        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
        const formData = new FormData()
        formData.append('audio', audioBlob, 'record.wav')

        transcrevendo.value = true
        try {
          const res = await axios.post(
            'http://localhost:8000/api/analises-llm/transcrever/',
            formData,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'multipart/form-data'
              }
            }
          )
          finalizacao.value.descricao_solucao = res.data.transcricao
        } catch (err) {
          alert('Erro ao transcrever o áudio.')
          console.error(err)
        } finally {
          transcrevendo.value = false
        }
      }

      mediaRecorder.start()
      isRecording.value = true
    } catch (err) {
      alert('Microfone não disponível ou permissão negada.')
      console.error(err)
    }
  } else {
    mediaRecorder.stop()
    isRecording.value = false
  }
}

// ── Utils ────────────────────────────────────────────────────────────────────

const truncateText = (text, limit) =>
  text?.length > limit ? text.substring(0, limit) + '...' : text

onMounted(fetchOS)
</script>

<style scoped>
.dashboard-content { padding: 0; max-width: 100%; font-family: 'Inter', system-ui, sans-serif; }
.p-main-container { background: #fff; padding: 2rem; border-radius: 16px; border: 1px solid #e2e8f0; margin-top: 1.5rem; }
.p-header-card { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; border-radius: 16px; padding: 1rem; }
.card-padding { padding: 1rem 1.5rem; }
.p-eyebrow { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #2563eb; margin: 0 0 0.4rem; }
.p-title { font-size: 1.6rem; font-weight: 800; margin: 0 0 0.3rem; color: #1e293b; }
.p-subtitle { font-size: 0.85rem; color: #64748b; margin: 0; }

/* FILTROS */
.filters-panel { background: white; padding: 1.5rem; border-radius: 16px; border: 1px solid #e2e8f0; display: flex; gap: 1rem; align-items: flex-end; flex-wrap: wrap; }
.filter-group { flex: 1; min-width: 150px; display: flex; flex-direction: column; gap: 4px; }
.filter-input { padding: 0.6rem 0.75rem; border-radius: 8px; border: 1px solid #cbd5e1; background: #f8fafc; font-size: 0.85rem; transition: border-color 0.2s; }
.filter-input:focus { outline: none; border-color: #2563eb; background: #fff; }
.btn-clear-filters { background: #f1f5f9; color: #64748b; border: none; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.85rem; white-space: nowrap; }
.btn-clear-filters:hover { background: #e2e8f0; }

/* TABS */
.p-tabs-container { display: flex; gap: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 0; }
.p-tab-btn { padding: 0.8rem 1.2rem; border: none; background: none; cursor: pointer; font-weight: 700; color: #94a3b8; border-bottom: 3px solid transparent; transition: 0.2s; font-size: 0.9rem; }
.p-tab-btn.active { color: #2563eb; border-bottom-color: #2563eb; }
.p-badge { background: #f1f5f9; color: #64748b; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; margin-left: 6px; font-weight: 800; }
.p-badge.warning { background: #fef3c7; color: #b45309; }
.p-badge.success { background: #dcfce7; color: #166534; }

/* CARDS */
.p-os-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 1.5rem; }
.p-os-card { background: #fff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; display: flex; flex-direction: column; transition: box-shadow 0.2s; }
.p-os-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.priority-bar { height: 3px; width: 100%; }
.priority-bar.alta, .priority-bar.crítica { background: #ef4444; }
.priority-bar.média { background: #f59e0b; }
.priority-bar.baixa { background: #10b981; }
.os-card-header { padding: 0.8rem 1.2rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; }
.os-number { font-weight: 800; color: #64748b; font-size: 0.85rem; }
.status-tag { font-size: 0.65rem; font-weight: 800; padding: 3px 9px; border-radius: 20px; text-transform: uppercase; }
.status-tag.aberto { background: #eff6ff; color: #1d4ed8; }
.status-tag.em-andamento { background: #fffbeb; color: #b45309; }
.status-tag.concluído { background: #dcfce7; color: #166534; }
.os-card-body { padding: 1.2rem; flex-grow: 1; }
.equip-name { font-size: 1.05rem; font-weight: 700; color: #1e293b; margin: 0 0 2px; }
.equip-meta-row { display: flex; gap: 12px; }
.equip-code, .equip-token { font-size: 0.72rem; color: #94a3b8; font-family: monospace; }
.info-row { display: flex; gap: 6px; align-items: center; }
.info-label { font-size: 0.78rem; color: #94a3b8; }
.info-value { font-size: 0.78rem; font-weight: 600; color: #475569; }
.problem-preview { font-size: 0.85rem; color: #475569; background: #f8fafc; padding: 10px; border-radius: 8px; margin-top: 0.75rem; border-left: 3px solid #e2e8f0; }
.os-card-footer { padding: 0.8rem 1.2rem; background: #fafafa; border-top: 1px solid #f1f5f9; display: flex; gap: 8px; }
.btn-p-sm { flex: 1; padding: 9px; border-radius: 8px; font-weight: 700; font-size: 0.8rem; cursor: pointer; border: none; transition: opacity 0.2s; }
.btn-p-sm:hover { opacity: 0.85; }
.btn-p-sm.primary { background: #2563eb; color: white; }
.btn-p-sm.success { background: #10b981; color: white; }
.btn-p-sm.outline { background: white; border: 1px solid #e2e8f0; color: #64748b; }

/* CHIPS */
.detail-chips { display: flex; gap: 8px; flex-wrap: wrap; }
.p-chip { font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; background: #f1f5f9; color: #475569; }
.urgencia-chip.alta, .urgencia-chip.crítica { background: #fee2e2; color: #b91c1c; }
.urgencia-chip.média { background: #fef3c7; color: #b45309; }
.urgencia-chip.baixa { background: #dcfce7; color: #166534; }

/* EQUIPAMENTO INFO */
.equip-info-block { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; }
.equip-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.equip-info-item { display: flex; flex-direction: column; gap: 2px; }
.equip-info-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.05em; }
.equip-info-value { font-size: 0.88rem; font-weight: 600; color: #1e293b; }
.equip-info-value.mono { font-family: monospace; font-size: 0.82rem; color: #2563eb; }

/* ANEXOS */
.attachments-container { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.attachment-link { display: flex; align-items: center; gap: 12px; padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; text-decoration: none; transition: 0.2s; }
.attachment-link:hover { border-color: #2563eb; background: #eff6ff; }
.file-icon { font-size: 1.4rem; line-height: 1; }
.file-meta { display: flex; flex-direction: column; gap: 2px; }
.file-name { font-size: 0.88rem; font-weight: 700; color: #1e293b; }
.file-action { font-size: 0.72rem; color: #2563eb; font-weight: 700; }
.foto-preview-wrapper { border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; max-height: 200px; }
.foto-preview { width: 100%; height: 200px; object-fit: cover; display: block; }
.empty-box { font-style: italic; color: #94a3b8; font-size: 0.82rem; }

/* SEÇÕES */
.detail-section { display: flex; flex-direction: column; gap: 6px; }
.p-section-label { font-size: 0.8rem; font-weight: 700; color: #64748b; margin: 0; }
.problem-label { color: #b45309; }
.success-label { color: #166534; }
.warning-label { color: #b45309; }
.p-text-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-size: 0.9rem; color: #334155; line-height: 1.5; }
.success-box { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }
.scrollable-content { max-height: 65vh; overflow-y: auto; padding-right: 4px; }

/* MODAL */
.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); z-index: 9999; display: flex; align-items: center; justify-content: center; padding: 20px; backdrop-filter: blur(3px); }
.modal-box { background: #fff; width: 100%; max-width: 520px; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15); font-family: 'Inter', system-ui, sans-serif; }
.modal-header { padding: 1.2rem 1.5rem; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; background: #f8fafc; }
.modal-title { font-size: 1.1rem; font-weight: 800; color: #1e293b; margin: 0; }
.modal-id { color: #2563eb; }
.modal-close { background: none; border: none; font-size: 1.4rem; cursor: pointer; color: #94a3b8; line-height: 1; padding: 0; }
.modal-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 0; }
.modal-footer { padding: 1rem 1.5rem; border-top: 1px solid #f1f5f9; display: flex; gap: 8px; justify-content: flex-end; background: #f8fafc; }
.btn-p-confirm { padding: 0.65rem 1.5rem; border-radius: 8px; font-weight: 700; font-size: 0.9rem; cursor: pointer; border: none; background: #2563eb; color: white; transition: opacity 0.2s; }
.btn-p-confirm:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-p-confirm:hover:not(:disabled) { opacity: 0.9; }
.btn-p-confirm.success { background: #10b981; }
.btn-p-confirm.outline { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.btn-p-cancel { padding: 0.65rem 1.2rem; border-radius: 8px; font-weight: 600; font-size: 0.9rem; cursor: pointer; border: 1px solid #e2e8f0; background: white; color: #64748b; }
.p-field-label { font-size: 0.85rem; font-weight: 700; color: #475569; display: block; margin-bottom: 0.3rem; }

/* TEXTAREA + MIC */
.textarea-mic-wrapper { position: relative; width: 100%; }
.p-textarea { width: 100%; padding: 0.75rem; padding-right: 3.2rem; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.9rem; resize: vertical; font-family: inherit; background: #f8fafc; box-sizing: border-box; }
.p-textarea:focus { outline: none; border-color: #2563eb; background: #fff; }
.p-textarea:disabled { opacity: 0.6; cursor: not-allowed; }

.inner-mic-btn {
  position: absolute; right: 10px; bottom: 10px;
  width: 36px; height: 36px; border-radius: 50%;
  border: 1px solid #e2e8f0; background: white; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem; transition: background 0.2s, border-color 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.inner-mic-btn:hover:not(:disabled) { background: #f1f5f9; }
.inner-mic-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.recording-active {
  background: #fee2e2 !important;
  border-color: #ef4444 !important;
  animation: pulse-mic 1.5s infinite;
}
@keyframes pulse-mic {
  0%   { box-shadow: 0 0 0 0    rgba(239, 68, 68, 0.4); }
  70%  { box-shadow: 0 0 0 8px  rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0    rgba(239, 68, 68, 0); }
}

.mic-hint { font-size: 0.78rem; font-weight: 600; margin: 5px 0 0; }
.mic-hint.recording { color: #ef4444; }
.mic-hint.processing { color: #2563eb; }

.p-info-alert { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px; font-size: 0.85rem; color: #1d4ed8; }
.field-group { display: flex; flex-direction: column; gap: 4px; }

.empty-results { text-align: center; padding: 3rem; color: #94a3b8; font-style: italic; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }
.mb-4 { margin-bottom: 1rem; }

.animate-fade-in { animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>