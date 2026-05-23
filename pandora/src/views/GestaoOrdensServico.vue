<template>
  <div class="crud-page">
    <header class="page-header">
      <p class="eyebrow">PAINEL DE MANUTENÇÃO</p>
      <h2>Ordens de Serviço</h2>
      <p class="page-copy">Gerencie as intervenções e mantenha o histórico técnico atualizado.</p>
    </header>

    <!-- PAINEL DE FILTROS -->
    <section v-if="canViewOS" class="filters-panel">
      <div class="filter-group equipment-filter-group">
        <label class="p-field-label">Equipamento</label>
        <div class="equipment-search">
          <div class="equipment-search-box">
            <input
              v-model="filtros.equipamentoBusca"
              type="search"
              placeholder="Pesquise por nome, ID interno ou ID do sistema..."
              class="filter-input"
              autocomplete="off"
              @focus="abrirBuscaEquipamento"
              @input="handleEquipamentoBusca"
              @keydown.enter.prevent="selecionarPrimeiroEquipamento"
              @keydown.esc="equipamentoBuscaAberta = false"
              @blur="fecharBuscaEquipamento"
            >
            <button
              v-if="filtros.equipamentoId"
              type="button"
              class="equipment-clear"
              title="Limpar equipamento selecionado"
              @mousedown.prevent
              @click="limparEquipamentoSelecionado"
            >
              &times;
            </button>
          </div>

          <div v-if="equipamentoBuscaAberta" class="equipment-results">
            <button
              v-for="equipamento in equipamentosFiltrados"
              :key="equipamento.id"
              type="button"
              class="equipment-result"
              @mousedown.prevent="selecionarEquipamento(equipamento)"
            >
              <span class="equipment-result-title">{{ equipamento.nome || 'Equipamento sem nome' }}</span>
              <span class="equipment-result-meta">
                ID interno: #{{ equipamento.idInterno || equipamento.id }} - Setor: {{ equipamento.setorNome || 'N/A' }}
              </span>
            </button>
            <p v-if="!equipamentosFiltrados.length" class="equipment-empty">
              Nenhum equipamento encontrado.
            </p>
          </div>
        </div>
      </div>
      <div class="filter-group">
        <label class="p-field-label">Setor</label>
        <select v-model="filtros.setor" class="filter-input">
          <option value="">Todos</option>
          <option v-for="setor in setoresDisponiveis" :key="setor.id" :value="setor.id">
            {{ setor.nome }}
          </option>
        </select>
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
      <button @click="limparFiltros" class="btn-clear-filters">Limpar</button>
    </section>

    <div v-if="canViewOS" class="card main-card">
      <div class="p-tabs-container">
        <button @click="tabAtiva = 'abertas'" :class="['p-tab-btn', { active: tabAtiva === 'abertas' }]">
          Abertas <span class="p-badge">{{ filtrarPorStatus('Aberto').length }}</span>
        </button>
        <button @click="tabAtiva = 'andamento'" :class="['p-tab-btn', { active: tabAtiva === 'andamento' }]">
          Em Andamento <span class="p-badge warning">{{ filtrarPorStatus('Em Andamento').length }}</span>
        </button>
        <button @click="tabAtiva = 'concluidas'" :class="['p-tab-btn', { active: tabAtiva === 'concluidas' }]">
          Concluídas <span class="p-badge success">{{ filtrarPorStatus('Concluido').length }}</span>
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
              <span class="equip-token">Setor: {{ os.equipamento_setor_nome || 'N/A' }}</span>
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
            <button v-if="os.status === 'Aberto' && canAssumeOS" @click="assumirOS(os.id)" class="btn-p-sm primary">Assumir OS</button>
            <button v-if="os.status === 'Em Andamento' && canCloseOS" @click="abrirModalFinalizar(os)" class="btn-p-sm success">Finalizar</button>
            <button @click="verDetalhes(os)" class="btn-p-sm outline">Ver Detalhes</button>
          </div>
        </div>
      </div>

      <div v-if="osFiltradas.length === 0" class="empty-results">
        Nenhum chamado encontrado com esses filtros.
      </div>
    </div>

    <section v-else class="card main-card empty-access">
      <h3>Acesso limitado</h3>
      <p>Libere ordens_servico.visualizar para consultar a gestao de ordens de servico.</p>
    </section>

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
                    <span class="equip-info-label">Setor</span>
                    <span class="equip-info-value">{{ osSelecionada?.equipamento_setor_nome || 'N/A' }}</span>
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

              <div class="detail-section mt-4 ai-solution-panel">
                <div class="ai-solution-header">
                  <div>
                    <p class="p-section-label ai-label">Sugestao da IA</p>
                    <span class="ai-helper">Considera a descricao da OS e ordens anteriores do mesmo equipamento.</span>
                  </div>
                  <button
                    type="button"
                    class="btn-ai-suggest"
                    :disabled="analiseIA.loading || !osSelecionada"
                    @click="gerarSugestaoIA"
                  >
                    {{ analiseIA.loading ? 'Analisando...' : sugestaoIAAtual ? 'Gerar novamente' : 'Sugerir solucao' }}
                  </button>
                </div>

                <div v-if="analiseIA.loading && analiseIA.osId === osSelecionada?.id" class="ai-loading-box">
                  Consultando historico tecnico e montando uma possivel solucao...
                </div>

                <div v-else-if="analiseIA.erro && analiseIA.osId === osSelecionada?.id" class="ai-error-box">
                  {{ analiseIA.erro }}
                </div>

                <div v-else-if="sugestaoIAAtual" class="ai-result-box">
                  <div v-if="sugestaoIAAtual.diagnostico" class="ai-result-section">
                    <span class="ai-result-label">Diagnostico provavel</span>
                    <p>{{ sugestaoIAAtual.diagnostico }}</p>
                  </div>
                  <div v-if="sugestaoIAAtual.solucao" class="ai-result-section">
                    <span class="ai-result-label">Possivel solucao</span>
                    <p class="ai-solution-text">{{ sugestaoIAAtual.solucao }}</p>
                  </div>
                  <div v-if="sugestaoIAAtual.historico_relacionado" class="ai-result-section muted">
                    <span class="ai-result-label">Historico considerado</span>
                    <p>{{ sugestaoIAAtual.historico_relacionado }}</p>
                  </div>
                  <div v-if="sugestaoIAAtual.alertas" class="ai-result-section warning">
                    <span class="ai-result-label">Cuidados</span>
                    <p>{{ sugestaoIAAtual.alertas }}</p>
                  </div>
                  <div class="ai-result-footer">
                    <span>{{ sugestaoIAAtual.historico_considerado || 0 }} OS relacionada(s) analisada(s)</span>
                    <button
                      v-if="osSelecionada?.status === 'Em Andamento' && canCloseOS && sugestaoIAAtual.solucao"
                      type="button"
                      class="btn-use-ai"
                      @click="usarSugestaoNaFinalizacao"
                    >
                      Usar na finalizacao
                    </button>
                  </div>
                </div>
              </div>

              <!-- ===== SEÇÃO: FOTOS DO PROBLEMA ===== -->
              <div v-if="canViewDocuments" class="detail-section mt-4">
                <p class="p-section-label problem-label">Fotos do Problema</p>
                <div class="attachments-container">
                  <template v-if="fotosDoProblema.length">
                    <template v-for="doc in fotosDoProblema" :key="doc.id">
                      <component
                        :is="canDownloadDocuments ? 'a' : 'div'"
                        :href="canDownloadDocuments ? doc.caminho_arquivo : null"
                        :target="canDownloadDocuments ? '_blank' : null"
                        class="attachment-link"
                        :class="{ 'attachment-disabled': !canDownloadDocuments }"
                      >
                        <span class="file-icon">IMG</span>
                        <div class="file-meta">
                          <span class="file-name">{{ nomeExibicao(doc.nome_arquivo) }}</span>
                          <span class="file-action">{{ canDownloadDocuments ? 'Visualizar imagem' : 'Sem permissao para abrir' }}</span>
                        </div>
                      </component>
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
              <div v-if="canViewDocuments" class="detail-section mt-4">
                <p class="p-section-label">Documentação Técnica do Equipamento</p>
                <div class="attachments-container">
                  <template v-if="docsDoEquipamento.length">
                    <template v-for="doc in docsDoEquipamento" :key="doc.id">

                      <!-- É uma imagem -->
                      <template v-if="docIsImagem(doc)">
                        <component
                          :is="canDownloadDocuments ? 'a' : 'div'"
                          :href="canDownloadDocuments ? doc.caminho_arquivo : null"
                          :target="canDownloadDocuments ? '_blank' : null"
                          class="attachment-link"
                          :class="{ 'attachment-disabled': !canDownloadDocuments }"
                        >
                          <span class="file-icon">IMG</span>
                          <div class="file-meta">
                            <span class="file-name">{{ doc.nome_arquivo }}</span>
                            <span class="file-action">{{ canDownloadDocuments ? 'Visualizar imagem' : 'Sem permissao para abrir' }}</span>
                          </div>
                        </component>
                        <div class="foto-preview-wrapper">
                          <img :src="doc.caminho_arquivo" :alt="doc.nome_arquivo" class="foto-preview" />
                        </div>
                      </template>

                      <!-- É um PDF ou outro documento -->
                      <component
                        v-else
                        :is="canDownloadDocuments ? 'a' : 'div'"
                        :href="canDownloadDocuments ? doc.caminho_arquivo : null"
                        :target="canDownloadDocuments ? '_blank' : null"
                        class="attachment-link"
                        :class="{ 'attachment-disabled': !canDownloadDocuments }"
                      >
                        <span class="file-icon">DOC</span>
                        <div class="file-meta">
                          <span class="file-name">{{ doc.nome_arquivo }}</span>
                          <span class="file-action">{{ canDownloadDocuments ? 'Abrir documento' : 'Sem permissao para abrir' }}</span>
                        </div>
                      </component>

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
                  Solução - Técnico: {{ osSelecionada?.usuario_tecnico_nome || 'Não informado' }}
                </p>
                <div class="p-text-box success-box">{{ osSelecionada?.descricao_solucao }}</div>
              </div>

              <div v-else-if="osSelecionada?.usuario_tecnico_nome" class="detail-section mt-4">
                <p class="p-section-label warning-label">
                  Técnico Responsável: {{ osSelecionada?.usuario_tecnico_nome }}
                </p>
              </div>

            </div>

            <div class="modal-footer">
              <button
                v-if="osSelecionada?.status === 'Em Andamento' && canCloseOS"
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
                <strong>Observação:</strong> Sua descrição enriquece o histórico técnico do equipamento.
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
                    <span v-if="transcrevendo" class="icon-text">...</span>
                    <span v-else-if="!isRecording" class="icon-text">MIC</span>
                    <span v-else class="icon-text">REC</span>
                  </button>
                </div>
                <p v-if="isRecording" class="mic-hint recording">Gravando... clique no botão para parar.</p>
                <p v-else-if="transcrevendo" class="mic-hint processing">Transcrevendo áudio...</p>
              </div>
            </div>
            <div class="modal-footer">
              <button @click="modalFinalizar = false" class="btn-p-cancel">Cancelar</button>
              <button @click="confirmarFinalizacao" :disabled="loading || isRecording || transcrevendo || !canCloseOS" class="btn-p-confirm">
                {{ loading ? 'Salvando...' : 'Concluir' }}
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
import { getStoredPermissions, hasPermission } from '../utils/permissions'

const tabAtiva = ref('abertas')
const ordens = ref([])
const modalFinalizar = ref(false)
const modalDetalhes = ref(false)
const loading = ref(false)
const osSelecionada = ref(null)
const finalizacao = ref({ descricao_solucao: '' })
const analiseIA = ref({
  loading: false,
  erro: '',
  resultado: null,
  osId: null
})
const permissions = computed(() => getStoredPermissions())
const canViewOS = computed(() => hasPermission('ordens_servico.visualizar', permissions.value))
const canChangeOSStatus = computed(() => hasPermission('ordens_servico.alterar_status', permissions.value))
const canAssignTechnician = computed(() => hasPermission('ordens_servico.atribuir_tecnico', permissions.value))
const canAssumeOS = computed(() => canChangeOSStatus.value && canAssignTechnician.value)
const canCloseOS = computed(() => hasPermission('ordens_servico.fechar', permissions.value))
const canViewDocuments = computed(() => hasPermission('documentos_equipamento.visualizar', permissions.value))
const canDownloadDocuments = computed(() => hasPermission('documentos_equipamento.baixar', permissions.value))

// ── Áudio / transcrição ──────────────────────────────────────────────────────
const isRecording = ref(false)
const transcrevendo = ref(false)
let mediaRecorder = null
let audioChunks = []

const equipamentoBuscaAberta = ref(false)
const filtros = reactive({
  equipamentoBusca: '',
  equipamentoId: '',
  setor: '',
  urgencia: ''
})

const API_BASE = 'http://127.0.0.1:8000/api/ordens-servico/'

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

const sugestaoIAAtual = computed(() => {
  if (!osSelecionada.value || analiseIA.value.osId !== osSelecionada.value.id) return null
  return analiseIA.value.resultado
})

const normalizarBusca = (valor) => String(valor ?? '')
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .trim()

const getEquipamentoLabel = (equipamento) => {
  if (!equipamento) return ''
  return `#${equipamento.idInterno || equipamento.id} - ${equipamento.nome || 'Equipamento sem nome'}`
}

const equipamentosDisponiveis = computed(() => {
  const porId = new Map()
  ordens.value.forEach((os) => {
    const id = os.equipamento
    if (!id || porId.has(String(id))) return

    porId.set(String(id), {
      id,
      nome: os.equipamento_nome,
      idInterno: os.equipamento_id_interno,
      tipo: os.equipamento_tipo,
      setorId: os.equipamento_setor_id,
      setorNome: os.equipamento_setor_nome
    })
  })

  return Array.from(porId.values()).sort((a, b) =>
    String(a.nome || '').localeCompare(String(b.nome || ''), 'pt-BR')
  )
})

const setoresDisponiveis = computed(() => {
  const porId = new Map()
  ordens.value.forEach((os) => {
    if (!os.equipamento_setor_id || porId.has(String(os.equipamento_setor_id))) return
    porId.set(String(os.equipamento_setor_id), {
      id: os.equipamento_setor_id,
      nome: os.equipamento_setor_nome || 'Setor sem nome'
    })
  })

  return Array.from(porId.values()).sort((a, b) =>
    String(a.nome || '').localeCompare(String(b.nome || ''), 'pt-BR')
  )
})

const equipamentosFiltrados = computed(() => {
  const termo = normalizarBusca(filtros.equipamentoBusca)
  const lista = !termo
    ? equipamentosDisponiveis.value
    : equipamentosDisponiveis.value.filter((equipamento) => {
      const camposBusca = [
        equipamento.id,
        equipamento.idInterno,
        equipamento.nome,
        equipamento.tipo,
        equipamento.setorNome
      ]

      return camposBusca.some((campo) => normalizarBusca(campo).includes(termo))
    })

  return lista.slice(0, 10)
})

const abrirBuscaEquipamento = () => {
  equipamentoBuscaAberta.value = true
}

const fecharBuscaEquipamento = () => {
  window.setTimeout(() => {
    equipamentoBuscaAberta.value = false
  }, 120)
}

const handleEquipamentoBusca = () => {
  filtros.equipamentoId = ''
  equipamentoBuscaAberta.value = true
}

const selecionarEquipamento = (equipamento) => {
  filtros.equipamentoId = equipamento.id
  filtros.equipamentoBusca = getEquipamentoLabel(equipamento)
  equipamentoBuscaAberta.value = false
}

const selecionarPrimeiroEquipamento = () => {
  const [primeiroEquipamento] = equipamentosFiltrados.value
  if (primeiroEquipamento) selecionarEquipamento(primeiroEquipamento)
}

const limparEquipamentoSelecionado = () => {
  filtros.equipamentoBusca = ''
  filtros.equipamentoId = ''
  equipamentoBuscaAberta.value = true
}

// ── Fetch ────────────────────────────────────────────────────────────────────

const fetchOS = async () => {
  if (!canViewOS.value) {
    ordens.value = []
    return
  }
  try {
    const res = await axios.get(API_BASE, getHeaders())
    ordens.value = res.data
  } catch (e) {
    console.error('Erro ao buscar OS:', e)
  }
}

const limparFiltros = () => {
  filtros.equipamentoBusca = ''
  filtros.equipamentoId = ''
  filtros.setor = ''
  filtros.urgencia = ''
  equipamentoBuscaAberta.value = false
}

const osFiltradas = computed(() => {
  if (!canViewOS.value) return []
  const statusMap = {
    abertas: 'Aberto',
    andamento: 'Em Andamento',
    concluidas: 'Concluido'
  }
  return ordens.value.filter(o => {
    const matchStatus = o.status === statusMap[tabAtiva.value]
    const termo = normalizarBusca(filtros.equipamentoBusca)
    const matchEquipamentoSelecionado = !filtros.equipamentoId ||
      String(o.equipamento) === String(filtros.equipamentoId)
    const matchEquipamentoDigitado = Boolean(filtros.equipamentoId) || !termo || [
      o.equipamento,
      o.equipamento_id_interno,
      o.equipamento_nome,
      o.equipamento_tipo,
      o.equipamento_setor_nome
    ].some((campo) => normalizarBusca(campo).includes(termo))
    const matchSetor = !filtros.setor ||
      String(o.equipamento_setor_id) === String(filtros.setor)
    const matchUrgencia = !filtros.urgencia || o.urgencia === filtros.urgencia
    return matchStatus && matchEquipamentoSelecionado && matchEquipamentoDigitado && matchSetor && matchUrgencia
  })
})

const filtrarPorStatus = (status) => ordens.value.filter(o => o.status === status)

const assumirOS = async (id) => {
  if (!canAssumeOS.value) {
    alert('Voce precisa das permissoes para alterar status e atribuir tecnico.')
    return
  }
  try {
    await axios.patch(`${API_BASE}${id}/`, { status: 'Em Andamento' }, getHeaders())
    fetchOS()
  } catch (e) {
    alert('Erro ao assumir OS')
  }
}

const verDetalhes = (os) => {
  if (!canViewOS.value) {
    alert('Voce nao possui permissao para visualizar ordens de servico.')
    return
  }
  osSelecionada.value = os
  modalDetalhes.value = true
}

const gerarSugestaoIA = async () => {
  if (!osSelecionada.value) return

  const osId = osSelecionada.value.id
  analiseIA.value = {
    loading: true,
    erro: '',
    resultado: null,
    osId
  }

  try {
    const res = await axios.post(
      'http://127.0.0.1:8000/api/analises-llm/sugerir-solucao-os/',
      { os_id: osId },
      getHeaders()
    )

    analiseIA.value = {
      loading: false,
      erro: '',
      resultado: res.data,
      osId
    }
  } catch (e) {
    const detalhe = e.response?.data?.error || 'Nao foi possivel gerar a sugestao agora.'
    analiseIA.value = {
      loading: false,
      erro: detalhe,
      resultado: null,
      osId
    }
  }
}

const abrirModalFinalizar = (os, descricaoInicial = '') => {
  if (!canCloseOS.value) {
    alert('Voce nao possui permissao para finalizar ordens de servico.')
    return
  }
  osSelecionada.value = os
  finalizacao.value = { descricao_solucao: descricaoInicial }
  isRecording.value = false
  transcrevendo.value = false
  modalFinalizar.value = true
}

const usarSugestaoNaFinalizacao = () => {
  const sugestao = sugestaoIAAtual.value?.solucao
  if (!sugestao || !osSelecionada.value) return

  const os = osSelecionada.value
  modalDetalhes.value = false
  abrirModalFinalizar(os, sugestao)
}

const confirmarFinalizacao = async () => {
  if (!canCloseOS.value) {
    alert('Voce nao possui permissao para finalizar ordens de servico.')
    return
  }
  if (!finalizacao.value.descricao_solucao.trim()) return alert('Descreva a solução!')
  loading.value = true
  try {
    await axios.patch(`${API_BASE}${osSelecionada.value.id}/`, {
      status: 'Concluido',
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
            'http://127.0.0.1:8000/api/analises-llm/transcrever/',
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
.main-card { padding: 2rem; border-radius: 20px; }

/* ── Filtros ──────────────────────────────────────── */
.filters-panel {
  background: #ffffff; padding: 1.5rem; border-radius: 20px;
  border: 1px solid #e2e8f0; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
  display: flex; gap: 1rem; align-items: flex-end; flex-wrap: wrap;
}
.filter-group { flex: 1; min-width: 150px; display: flex; flex-direction: column; gap: 4px; }
.p-field-label { font-size: 0.85rem; font-weight: 700; color: #475569; display: block; }
.filter-input {
  padding: 0.6rem 0.75rem; border-radius: 8px; border: 1px solid #cbd5e1;
  background: #f8fafc; font-size: 0.85rem; font-family: inherit; color: #0f172a;
  transition: border-color 0.2s; box-sizing: border-box; width: 100%;
}
.filter-input:focus { outline: none; border-color: #2563eb; background: #fff; }
.equipment-filter-group { flex: 1.6; min-width: 280px; }
.equipment-search { position: relative; }
.equipment-search-box { position: relative; }
.equipment-search-box .filter-input { box-sizing: border-box; width: 100%; padding-right: 2.5rem; }
.equipment-search-box input[type="search"]::-webkit-search-cancel-button,
.equipment-search-box input[type="search"]::-webkit-search-decoration { -webkit-appearance: none; appearance: none; }
.equipment-clear {
  position: absolute; top: 50%; right: 0.55rem; transform: translateY(-50%);
  width: 28px; height: 28px; border: 1px solid #cbd5e1; border-radius: 50%;
  background: #ffffff; color: #64748b; line-height: 1; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.equipment-clear:hover { color: #0f172a; border-color: #94a3b8; background: #f8fafc; }
.equipment-results {
  position: absolute; z-index: 30; top: calc(100% + 0.35rem); left: 0; right: 0;
  max-height: 280px; overflow-y: auto; padding: 0.35rem;
  border: 1px solid #cbd5e1; border-radius: 10px; background: #ffffff;
  box-shadow: 0 18px 35px rgba(15, 23, 42, 0.14);
}
.equipment-result {
  width: 100%; display: flex; flex-direction: column; align-items: flex-start;
  gap: 0.18rem; padding: 0.68rem 0.75rem; border: none; border-radius: 8px;
  background: transparent; color: #0f172a; font-family: inherit; text-align: left; cursor: pointer;
}
.equipment-result:hover, .equipment-result:focus { outline: none; background: #eff6ff; }
.equipment-result-title { width: 100%; font-size: 0.86rem; font-weight: 800; overflow-wrap: anywhere; }
.equipment-result-meta { width: 100%; color: #64748b; font-size: 0.75rem; line-height: 1.35; overflow-wrap: anywhere; }
.equipment-empty { margin: 0; padding: 0.7rem 0.75rem; color: #64748b; font-size: 0.8rem; }
.btn-clear-filters {
  background: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0;
  padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600;
  cursor: pointer; font-size: 0.85rem; white-space: nowrap; font-family: inherit;
}
.btn-clear-filters:hover { background: #e2e8f0; }

/* ── Tabs ─────────────────────────────────────────── */
.p-tabs-container { display: flex; gap: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 0; margin-bottom: 1.5rem; }
.p-tab-btn {
  padding: 0.8rem 1.2rem; border: none; background: none; cursor: pointer;
  font-weight: 700; color: #94a3b8; border-bottom: 3px solid transparent;
  transition: 0.2s; font-size: 0.9rem; font-family: inherit;
}
.p-tab-btn.active { color: #2563eb; border-bottom-color: #2563eb; }
.p-badge { background: #f1f5f9; color: #64748b; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; margin-left: 6px; font-weight: 800; }
.p-badge.warning { background: #fef3c7; color: #b45309; }
.p-badge.success { background: #dcfce7; color: #166534; }

/* ── Cards de OS ──────────────────────────────────── */
.p-os-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 1.5rem; }
.p-os-card {
  background: #fff; border-radius: 14px; border: 1px solid #e2e8f0;
  overflow: hidden; display: flex; flex-direction: column;
  transition: box-shadow 0.2s;
}
.p-os-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.priority-bar { height: 3px; width: 100%; }
.priority-bar.alta, .priority-bar.crítica { background: #ef4444; }
.priority-bar.média { background: #f59e0b; }
.priority-bar.baixa { background: #10b981; }
.os-card-header {
  padding: 0.8rem 1.2rem; display: flex;
  justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9;
}
.os-number { font-weight: 800; color: #64748b; font-size: 0.85rem; }
.status-tag { font-size: 0.65rem; font-weight: 800; padding: 3px 9px; border-radius: 20px; text-transform: uppercase; }
.status-tag.aberto { background: #eff6ff; color: #1d4ed8; }
.status-tag.em-andamento { background: #fffbeb; color: #b45309; }
.status-tag.concluído { background: #dcfce7; color: #166534; }
.os-card-body { padding: 1.2rem; flex-grow: 1; }
.equip-name { font-size: 1.05rem; font-weight: 700; color: #1e293b; margin: 0 0 2px; }
.equip-meta-row { display: flex; gap: 12px; }
.equip-code, .equip-token { font-size: 0.72rem; color: #94a3b8; }
.equip-code { font-family: monospace; }
.info-row { display: flex; gap: 6px; align-items: center; }
.info-label { font-size: 0.78rem; color: #94a3b8; }
.info-value { font-size: 0.78rem; font-weight: 600; color: #475569; }
.problem-preview { font-size: 0.85rem; color: #475569; background: #f8fafc; padding: 10px; border-radius: 8px; margin-top: 0.75rem; border-left: 3px solid #e2e8f0; }
.os-card-footer { padding: 0.8rem 1.2rem; background: #fafafa; border-top: 1px solid #f1f5f9; display: flex; gap: 8px; }
.btn-p-sm { flex: 1; padding: 9px; border-radius: 8px; font-weight: 700; font-size: 0.8rem; cursor: pointer; border: none; transition: opacity 0.2s; font-family: inherit; }
.btn-p-sm:hover { opacity: 0.85; }
.btn-p-sm.primary { background: #2563eb; color: white; }
.btn-p-sm.success { background: #10b981; color: white; }
.btn-p-sm.outline { background: white; border: 1px solid #e2e8f0; color: #64748b; }

/* ── Modal ────────────────────────────────────────── */
.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); z-index: 9999; display: flex; align-items: center; justify-content: center; padding: 20px; backdrop-filter: blur(3px); }
.modal-box { background: #fff; width: 100%; max-width: 520px; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15); font-family: Inter, system-ui, -apple-system, sans-serif; }
.modal-header { padding: 1.2rem 1.5rem; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; background: #f8fafc; }
.modal-title { font-size: 1.1rem; font-weight: 800; color: #1e293b; margin: 0; }
.modal-id { color: #2563eb; }
.modal-close { background: none; border: none; font-size: 1.4rem; cursor: pointer; color: #94a3b8; line-height: 1; padding: 0; }
.modal-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 0; font-family: Inter, system-ui, -apple-system, sans-serif; }
.modal-footer { padding: 1rem 1.5rem; border-top: 1px solid #f1f5f9; display: flex; gap: 8px; justify-content: flex-end; background: #f8fafc; }

.btn-p-confirm { padding: 0.65rem 1.5rem; border-radius: 8px; font-weight: 700; font-size: 0.9rem; cursor: pointer; border: none; background: #2563eb; color: white; transition: opacity 0.2s; font-family: inherit; }
.btn-p-confirm:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-p-confirm:hover:not(:disabled) { opacity: 0.9; }
.btn-p-confirm.success { background: #10b981; }
.btn-p-confirm.outline { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.btn-p-cancel { padding: 0.65rem 1.2rem; border-radius: 8px; font-weight: 600; font-size: 0.9rem; cursor: pointer; border: 1px solid #e2e8f0; background: white; color: #64748b; font-family: inherit; }

/* ── Detalhes ─────────────────────────────────────── */
.detail-chips { display: flex; gap: 8px; flex-wrap: wrap; }
.p-chip { font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; background: #f1f5f9; color: #475569; }
.urgencia-chip.alta, .urgencia-chip.crítica { background: #fee2e2; color: #b91c1c; }
.urgencia-chip.média { background: #fef3c7; color: #b45309; }
.urgencia-chip.baixa { background: #dcfce7; color: #166534; }

.equip-info-block { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; }
.equip-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.equip-info-item { display: flex; flex-direction: column; gap: 2px; }
.equip-info-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.05em; }
.equip-info-value { font-size: 0.88rem; font-weight: 600; color: #1e293b; }
.equip-info-value.mono { font-family: monospace; font-size: 0.82rem; color: #2563eb; }

.detail-section { display: flex; flex-direction: column; gap: 6px; }
.p-section-label { font-size: 0.8rem; font-weight: 700; color: #64748b; margin: 0; }
.problem-label { color: #b45309; }
.success-label { color: #166534; }
.warning-label { color: #b45309; }
.p-text-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-size: 0.9rem; color: #334155; line-height: 1.5; }
.success-box { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }
.empty-box { font-style: italic; color: #94a3b8; font-size: 0.82rem; }
.scrollable-content { max-height: 65vh; overflow-y: auto; padding-right: 4px; }

/* ── Anexos ───────────────────────────────────────── */
.attachments-container { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.attachment-link { display: flex; align-items: center; gap: 12px; padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; text-decoration: none; transition: 0.2s; }
.attachment-link:hover { border-color: #2563eb; background: #eff6ff; }
.attachment-disabled { cursor: not-allowed; opacity: 0.75; }
.attachment-disabled:hover { border-color: #e2e8f0; background: #f8fafc; }
.file-icon { width: 38px; height: 28px; border-radius: 7px; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; background: #e0f2fe; color: #0369a1; font-size: 0.68rem; font-weight: 800; letter-spacing: 0.04em; }
.file-meta { display: flex; flex-direction: column; gap: 2px; }
.file-name { font-size: 0.88rem; font-weight: 700; color: #1e293b; }
.file-action { font-size: 0.72rem; color: #2563eb; font-weight: 700; }
.foto-preview-wrapper { border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; max-height: 200px; }
.foto-preview { width: 100%; height: 200px; object-fit: cover; display: block; }

/* ── IA ───────────────────────────────────────────── */
.ai-solution-panel { border: 1px solid #bfdbfe; background: #f8fbff; border-radius: 10px; padding: 1rem; }
.ai-solution-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.ai-label { color: #1d4ed8; }
.ai-helper { display: block; margin-top: 2px; color: #64748b; font-size: 0.78rem; line-height: 1.35; }
.btn-ai-suggest, .btn-use-ai { border: none; border-radius: 8px; background: #2563eb; color: #ffffff; font-weight: 800; cursor: pointer; transition: opacity 0.2s, transform 0.2s; font-family: inherit; }
.btn-ai-suggest { flex-shrink: 0; padding: 0.55rem 0.9rem; font-size: 0.78rem; }
.btn-use-ai { padding: 0.48rem 0.75rem; font-size: 0.75rem; }
.btn-ai-suggest:hover:not(:disabled), .btn-use-ai:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
.btn-ai-suggest:disabled, .btn-use-ai:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }
.ai-loading-box, .ai-error-box, .ai-result-box { margin-top: 0.75rem; border-radius: 8px; padding: 0.85rem; font-size: 0.86rem; line-height: 1.5; }
.ai-loading-box { background: #eff6ff; border: 1px dashed #93c5fd; color: #1d4ed8; }
.ai-error-box { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; }
.ai-result-box { background: #ffffff; border: 1px solid #dbeafe; color: #334155; display: flex; flex-direction: column; gap: 0.75rem; }
.ai-result-section { display: flex; flex-direction: column; gap: 0.25rem; }
.ai-result-section p { margin: 0; white-space: pre-line; }
.ai-result-section.muted { color: #64748b; }
.ai-result-section.warning { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 0.65rem; color: #92400e; }
.ai-result-label { color: #1e293b; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; }
.ai-solution-text { color: #0f172a; }
.ai-result-footer { display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; padding-top: 0.65rem; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 0.75rem; font-weight: 700; }

/* ── Textarea + mic ───────────────────────────────── */
.textarea-mic-wrapper { position: relative; width: 100%; }
.p-textarea { width: 100%; padding: 0.75rem; padding-right: 3.2rem; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.9rem; resize: vertical; font-family: inherit; background: #f8fafc; box-sizing: border-box; }
.p-textarea:focus { outline: none; border-color: #2563eb; background: #fff; }
.p-textarea:disabled { opacity: 0.6; cursor: not-allowed; }
.inner-mic-btn { position: absolute; right: 10px; bottom: 10px; width: 36px; height: 36px; border-radius: 50%; border: 1px solid #e2e8f0; background: white; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1rem; transition: background 0.2s, border-color 0.2s; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.inner-mic-btn:hover:not(:disabled) { background: #f1f5f9; }
.inner-mic-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.icon-text { font-size: 0.62rem; font-weight: 800; letter-spacing: 0.04em; }
.recording-active { background: #fee2e2 !important; border-color: #ef4444 !important; animation: pulse-mic 1.5s infinite; }
@keyframes pulse-mic { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
.mic-hint { font-size: 0.78rem; font-weight: 600; margin: 5px 0 0; }
.mic-hint.recording { color: #ef4444; }
.mic-hint.processing { color: #2563eb; }
.p-info-alert { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px; font-size: 0.85rem; color: #1d4ed8; }
.field-group { display: flex; flex-direction: column; gap: 4px; }

/* ── Misc ─────────────────────────────────────────── */
.empty-results { text-align: center; padding: 3rem; color: #94a3b8; font-style: italic; }
.empty-access h3 { margin: 0 0 0.35rem; color: #1e293b; }
.empty-access p { margin: 0; color: #64748b; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }
.mb-4 { margin-bottom: 1rem; }

.animate-fade-in { animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes animate-slide-up { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.animate-slide-up { animation: animate-slide-up 0.3s ease; }

/* ── Responsivo ───────────────────────────────────── */
@media (max-width: 768px) {
  .page-header { padding: 1.1rem 1.2rem; border-radius: 16px; }
  .card { border-radius: 16px; }
  .main-card { padding: 1.2rem; border-radius: 16px; }
  .filters-panel { border-radius: 16px; }
  .p-os-grid { grid-template-columns: 1fr; }
  .modal-overlay { padding: 0.75rem; }
  .modal-footer { flex-direction: column; }
  .modal-footer .btn-p-confirm,
  .modal-footer .btn-p-cancel { width: 100%; }
  .equip-info-grid { grid-template-columns: 1fr; }
}
</style>