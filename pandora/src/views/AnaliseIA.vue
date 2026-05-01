<template>
  <div class="crud-page">
    <section class="page-header animate-fade-in">
      <p class="eyebrow">Diagnóstico Inteligente</p>
      <h2>Análise Preditiva via IA</h2>
      <p class="page-copy">Utilize inteligência artificial para gerar pareceres técnicos baseados nos sintomas, histórico de falhas e manuais dos equipamentos.</p>
    </section>

    <section class="card form-card animate-fade-in">
      <div class="card-header">
        <h3>Detalhes da Ocorrência</h3>
        <p>Filtre e vincule uma Ordem de Serviço para enriquecer o diagnóstico com o histórico do equipamento.</p>
      </div>

      <div class="crud-form">

        <!-- ── PAINEL DE FILTROS ─────────────────────────────────────── -->
        <div class="filters-panel">
          <div class="filter-group">
            <label class="filter-label">ID / Equipamento</label>
            <input v-model="filtros.busca" type="text" placeholder="Ex: 10 ou Motor..." class="filter-input" />
          </div>
          <div class="filter-group">
            <label class="filter-label">Token QR Code</label>
            <input v-model="filtros.token" type="text" placeholder="Token do patrimônio" class="filter-input" />
          </div>
          <div class="filter-group">
            <label class="filter-label">Criticidade</label>
            <select v-model="filtros.urgencia" class="filter-input">
              <option value="">Todas</option>
              <option value="Baixa">Baixa</option>
              <option value="Média">Média</option>
              <option value="Alta">Alta</option>
              <option value="Crítica">Crítica</option>
            </select>
          </div>
          <button @click="limparFiltros" class="btn-clear-filters">✕ Limpar</button>
        </div>

        <!-- ── SELECT DE OS (filtrado) ──────────────────────────────── -->
        <div class="input-group">
          <label>Vincular Ordem de Serviço <span class="optional-tag">Opcional</span></label>

          <select v-model="osSelecionada" @change="vincularDadosOS" class="os-select">
            <option :value="null">Selecione uma OS da sua empresa...</option>
            <option v-if="osFiltradas.length === 0" disabled>— Nenhuma OS encontrada com esses filtros —</option>
            <option v-for="os in osFiltradas" :key="os.id" :value="os.id">
              #{{ os.id }} — {{ os.equipamento_nome || 'Equipamento' }} · Cod: {{ os.equipamento_id_interno || 'S/N' }} · {{ os.urgencia || 'S/U' }}
            </option>
          </select>

          <!-- Banner de confirmação quando uma OS está vinculada -->
          <div v-if="osSelecionadaObj" class="os-selected-summary">
            <span class="summary-icon">🔗</span>
            <span>OS <strong>#{{ osSelecionadaObj.id }}</strong> vinculada —
              <em>{{ osSelecionadaObj.equipamento_nome }}</em>.
              O histórico completo deste equipamento será enviado à IA.
            </span>
            <button @click="desselecionarOS" class="btn-desvincular">✕</button>
          </div>
        </div>

        <!-- ── DESCRIÇÃO / SINTOMAS ─────────────────────────────────── -->
        <div class="input-group">
          <label>Descrição do Problema / Sintomas</label>
          <div class="textarea-container">
            <textarea
              v-model="descricao"
              placeholder="Descreva detalhadamente o problema ou use o microfone para gravar..."
              class="custom-textarea"
              :disabled="loading || isRecording || transcrevendo"
            ></textarea>
            <button
              @click="toggleRecording"
              type="button"
              :class="['inner-mic-btn', { 'recording-active': isRecording }]"
              :title="isRecording ? 'Parar gravação' : 'Usar microfone'"
              :disabled="transcrevendo || loading"
            >
              <span v-if="transcrevendo">⏳</span>
              <span v-else-if="!isRecording">🎤</span>
              <span v-else>🔴</span>
            </button>
          </div>
          <p v-if="isRecording" class="mic-hint recording">🎙️ Gravando... clique no botão para parar.</p>
          <p v-else-if="transcrevendo" class="mic-hint processing">⏳ Transcrevendo áudio...</p>
        </div>

        <div class="form-actions">
          <button @click="solicitarAnalise" :disabled="loading || !descricao.trim()" class="btn btn-primary">
            <div v-if="loading" class="btn-loader">
              <div class="spinner-small"></div>
              <span>Analisando...</span>
            </div>
            <span v-else>🚀 Iniciar Diagnóstico Inteligente</span>
          </button>
        </div>
      </div>
    </section>

    <!-- ── RESULTADO ────────────────────────────────────────────────── -->
    <section v-if="resultado || loading" class="card result-card animate-slide-up">
      <div :class="['status-bar', resultado?.urgencia?.toLowerCase() || 'processando']"></div>

      <div class="result-header">
        <h3>Parecer Técnico Gerado</h3>
        <span v-if="resultado" :class="['status-tag', resultado.urgencia?.toLowerCase()]">
          {{ resultado.urgencia }}
        </span>
      </div>

      <div class="result-body">
        <div v-if="loading" class="loading-container">
          <div class="spinner-blue"></div>
          <p>A IA está cruzando sintomas com o histórico do equipamento...</p>
        </div>

        <template v-else-if="resultado">

          <!-- Diagnóstico principal -->
          <div class="result-block">
            <div class="result-block-header diagnosis">
              <span class="block-icon">🔍</span>
              <span class="block-title">Diagnóstico Principal</span>
            </div>
            <p class="text-content">{{ resultado.diagnostico }}</p>
          </div>

          <div class="ui-divider"></div>

          <!-- Histórico relacionado -->
          <div v-if="resultado.historico_relacionado" class="result-block">
            <div class="result-block-header history">
              <span class="block-icon">📋</span>
              <span class="block-title">Ocorrências Anteriores Relacionadas</span>
            </div>
            <div class="history-box">
              <p class="text-content">{{ resultado.historico_relacionado }}</p>
            </div>
          </div>

          <div v-if="resultado.historico_relacionado" class="ui-divider"></div>

          <!-- Probabilidade de recorrência -->
          <div v-if="resultado.probabilidade_recorrencia" class="result-block">
            <div class="result-block-header recurrence">
              <span class="block-icon">🔁</span>
              <span class="block-title">Probabilidade de Recorrência</span>
            </div>
            <div :class="['recurrence-bar-wrapper', resultado.nivel_recorrencia?.toLowerCase()]">
              <div class="recurrence-label">{{ resultado.probabilidade_recorrencia }}</div>
            </div>
          </div>

          <div v-if="resultado.probabilidade_recorrencia" class="ui-divider"></div>

          <!-- Causa raiz -->
          <div v-if="resultado.causa_raiz" class="result-block">
            <div class="result-block-header root-cause">
              <span class="block-icon">⚠️</span>
              <span class="block-title">Possível Causa Raiz</span>
            </div>
            <p class="text-content">{{ resultado.causa_raiz }}</p>
          </div>

          <div v-if="resultado.causa_raiz" class="ui-divider"></div>

          <!-- Plano de ação -->
          <div class="result-block">
            <div class="result-block-header plan">
              <span class="block-icon">🛠️</span>
              <span class="block-title">Plano de Ação Detalhado</span>
            </div>
            <p class="text-content plan-text">{{ formatarPlano(resultado.solucao) }}</p>
          </div>

          <!-- Peças/recursos sugeridos -->
          <div v-if="resultado.pecas_sugeridas" class="result-block mt-4">
            <div class="result-block-header parts">
              <span class="block-icon">🔩</span>
              <span class="block-title">Peças / Recursos Sugeridos</span>
            </div>
            <p class="text-content">{{ resultado.pecas_sugeridas }}</p>
          </div>

          <!-- Recomendação preventiva -->
          <div v-if="resultado.recomendacao_preventiva" class="result-block mt-4">
            <div class="result-block-header preventive">
              <span class="block-icon">🛡️</span>
              <span class="block-title">Recomendação Preventiva</span>
            </div>
            <div class="preventive-box">
              <p class="text-content">{{ resultado.recomendacao_preventiva }}</p>
            </div>
          </div>

        </template>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue'
import axios from 'axios'

const descricao = ref('')
const loading = ref(false)
const resultado = ref(null)
const ordensServico = ref([])
const osSelecionada = ref(null)
const isRecording = ref(false)
const transcrevendo = ref(false)

const filtros = reactive({ busca: '', token: '', urgencia: '' })

let mediaRecorder = null
let audioChunks = []

const getHeaders = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
})

// ── Fetch OS ─────────────────────────────────────────────────────────────────

const fetchOS = async () => {
  const empresaId = localStorage.getItem('empresa_id')
  try {
    const res = await axios.get(
      `http://localhost:8000/api/ordens-servico/?empresa=${empresaId}`,
      getHeaders()
    )
    ordensServico.value = res.data.filter(os => os.status !== 'Concluído')
  } catch (e) {
    console.error('Erro ao carregar OS', e)
  }
}

// ── Filtros ──────────────────────────────────────────────────────────────────

const osFiltradas = computed(() => {
  return ordensServico.value.filter(os => {
    const termo = filtros.busca.toLowerCase()
    const matchBusca = !filtros.busca ||
      os.id.toString().includes(termo) ||
      os.equipamento_id_interno?.toString().toLowerCase().includes(termo) ||
      os.equipamento_nome?.toLowerCase().includes(termo)
    const matchToken = !filtros.token ||
      os.equipamento_qr_token?.toLowerCase().includes(filtros.token.toLowerCase())
    const matchUrgencia = !filtros.urgencia || os.urgencia === filtros.urgencia
    return matchBusca && matchToken && matchUrgencia
  })
})

const osSelecionadaObj = computed(() =>
  ordensServico.value.find(o => o.id === osSelecionada.value) || null
)

const limparFiltros = () => {
  filtros.busca = ''
  filtros.token = ''
  filtros.urgencia = ''
}

const vincularDadosOS = () => {
  const os = ordensServico.value.find(o => o.id === osSelecionada.value)
  if (os) descricao.value = os.descricao_problema || os.descricao || ''
}

const desselecionarOS = () => {
  osSelecionada.value = null
  descricao.value = ''
}

// ── Análise ──────────────────────────────────────────────────────────────────

const solicitarAnalise = async () => {
  if (!descricao.value.trim()) return
  loading.value = true
  resultado.value = null

  try {
    // Busca histórico de OS CONCLUÍDAS do mesmo equipamento para enriquecer o contexto
    let historicoEquipamento = []
    if (osSelecionadaObj.value?.equipamento_id_interno) {
      try {
        const resHistorico = await axios.get(
          `http://localhost:8000/api/ordens-servico/?equipamento_id=${osSelecionadaObj.value.equipamento_id_interno}&status=Concluído`,
          getHeaders()
        )
        historicoEquipamento = resHistorico.data || []
      } catch (_) { /* silencia erro de histórico */ }
    }

    const res = await axios.post(
      'http://localhost:8000/api/analises-llm/analisar/',
      {
        descricao: descricao.value,
        os_id: osSelecionada.value || null,
        historico_equipamento: historicoEquipamento.map(os => ({
          id: os.id,
          problema: os.descricao_problema,
          solucao: os.descricao_solucao,
          data_fechamento: os.data_fechamento,
          urgencia: os.urgencia
        }))
      },
      getHeaders()
    )
    resultado.value = res.data
  } catch (e) {
    console.error('Erro na análise', e)
  } finally {
    loading.value = false
  }
}

// ── Formatação ───────────────────────────────────────────────────────────────

const formatarPlano = (texto) => {
  if (!texto) return ''
  return texto.replace(/\s*([1-9][0-9]?\.)/g, '\n$1').trim()
}

// ── Áudio ────────────────────────────────────────────────────────────────────

const toggleRecording = async () => {
  if (!isRecording.value) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(stream)
      audioChunks = []
      mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data)
      mediaRecorder.onstop = async () => {
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
          descricao.value = res.data.transcricao
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
    }
  } else {
    mediaRecorder.stop()
    isRecording.value = false
  }
}

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

.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); overflow: hidden; }
.form-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.card-header h3 { margin: 0; color: #0f172a; }
.card-header p { margin: 0.4rem 0 0; color: #475569; font-size: 0.9rem; }

/* ── Filtros ──────────────────────────────────────── */
.filters-panel {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  flex-wrap: wrap;
}
.filter-group { flex: 1; min-width: 140px; display: flex; flex-direction: column; gap: 4px; }
.filter-label { font-size: 0.8rem; font-weight: 700; color: #475569; }
.filter-input {
  padding: 0.6rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #fff;
  font-size: 0.85rem;
  font-family: inherit;
  color: #0f172a;
  transition: border-color 0.2s;
  box-sizing: border-box;
  width: 100%;
}
.filter-input:focus { outline: none; border-color: #2563eb; }
.btn-clear-filters {
  background: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0;
  padding: 0.6rem 1.1rem; border-radius: 8px; font-weight: 600;
  cursor: pointer; font-size: 0.82rem; white-space: nowrap;
  transition: background 0.2s;
}
.btn-clear-filters:hover { background: #e2e8f0; }

/* ── Formulário ───────────────────────────────────── */
.crud-form { display: flex; flex-direction: column; gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group > label { font-size: 0.9rem; font-weight: 600; color: #334155; display: flex; align-items: center; gap: 8px; }
.optional-tag { font-size: 0.72rem; font-weight: 600; color: #94a3b8; background: #f1f5f9; padding: 2px 8px; border-radius: 20px; }
.empty-filter-msg { padding: 1rem; text-align: center; color: #94a3b8; font-style: italic; font-size: 0.85rem; }

/* ── Select de OS ─────────────────────────────────── */
.os-select {
  box-sizing: border-box; width: 100%;
  padding: 0.9rem 1rem; border: 1px solid #cbd5e1;
  border-radius: 12px; background: #f8fafc;
  color: #0f172a; font-size: 0.95rem; font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
  cursor: pointer;
}
.os-select:focus { outline: none; background: #fff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,0.12); }

.os-selected-summary {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.85rem;
  color: #1d4ed8;
}
.summary-icon { font-size: 1rem; }
.btn-desvincular { margin-left: auto; background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 0.9rem; padding: 0 4px; }
.btn-desvincular:hover { color: #ef4444; }

.empty-filter-msg { padding: 1rem; text-align: center; color: #94a3b8; font-style: italic; font-size: 0.85rem; }

/* ── Textarea + mic ───────────────────────────────── */
.textarea-container { position: relative; width: 100%; }
.custom-textarea {
  box-sizing: border-box; width: 100%;
  min-height: 150px; resize: none;
  padding: 0.9rem 3.5rem 0.9rem 1rem;
  border: 1px solid #cbd5e1; border-radius: 12px;
  background: #f8fafc; color: #0f172a;
  font-size: 0.95rem; font-family: inherit; line-height: 1.5;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.custom-textarea:focus { outline: none; background: #fff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,0.12); }
.custom-textarea:disabled { opacity: 0.6; cursor: not-allowed; }

.inner-mic-btn {
  position: absolute; right: 12px; bottom: 12px;
  width: 40px; height: 40px; border-radius: 50%;
  border: 1px solid #e2e8f0; background: white; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s, border-color 0.2s;
  font-size: 1rem;
}
.inner-mic-btn:hover:not(:disabled) { background: #f1f5f9; }
.inner-mic-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.recording-active { background: #fee2e2 !important; border-color: #ef4444 !important; animation: pulse 1.5s infinite; }
@keyframes pulse {
  0%   { transform: scale(1);   box-shadow: 0 0 0 0    rgba(239,68,68,0.4); }
  70%  { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(239,68,68,0);   }
  100% { transform: scale(1);   box-shadow: 0 0 0 0    rgba(239,68,68,0);   }
}
.mic-hint { font-size: 0.78rem; font-weight: 600; margin: 4px 0 0; }
.mic-hint.recording { color: #ef4444; }
.mic-hint.processing { color: #2563eb; }

/* ── Ações ────────────────────────────────────────── */
.form-actions { display: flex; justify-content: flex-end; gap: 0.75rem; flex-wrap: wrap; padding-top: 1.25rem; border-top: 1px solid #f1f5f9; }
.btn { border: none; border-radius: 12px; padding: 0.8rem 1.5rem; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s; }
.btn:hover:not(:disabled) { transform: translateY(-1px); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary { background: #2563eb; color: #fff; box-shadow: 0 10px 24px rgba(37,99,235,0.24); }
.btn-loader { display: flex; align-items: center; gap: 0.5rem; }

/* ── Resultado ────────────────────────────────────── */
.status-bar { height: 6px; width: 100%; background: #cbd5e1; }
.status-bar.alta     { background: #ef4444; }
.status-bar.crítica  { background: #7f1d1d; }
.status-bar.média    { background: #f59e0b; }
.status-bar.baixa    { background: #10b981; }
.status-bar.processando { background: linear-gradient(90deg, #bfdbfe, #2563eb, #bfdbfe); background-size: 200%; animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

.result-header { padding: 1rem 1.5rem; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; }
.result-header h3 { margin: 0; color: #0f172a; font-size: 1rem; }
.status-tag { padding: 0.3rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.status-tag.alta    { background: #fee2e2; color: #b91c1c; }
.status-tag.crítica { background: #7f1d1d; color: #fff; }
.status-tag.média   { background: #fef9c3; color: #854d0e; }
.status-tag.baixa   { background: #dcfce7; color: #15803d; }

.result-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 0; }
.loading-container { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 2rem; color: #64748b; }

/* Blocos de resultado */
.result-block { padding: 0.5rem 0; }
.result-block-header { display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem; }
.block-icon { font-size: 1rem; }
.block-title { font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }

/* Destaque por tipo de bloco */
.result-block-header.history .block-title  { color: #b45309; }
.result-block-header.recurrence .block-title { color: #7c3aed; }
.result-block-header.root-cause .block-title { color: #dc2626; }
.result-block-header.plan .block-title     { color: #0369a1; }
.result-block-header.parts .block-title    { color: #475569; }
.result-block-header.preventive .block-title { color: #166534; }

.text-content { color: #1e293b; line-height: 1.65; margin: 0; font-size: 0.93rem; }
.plan-text { white-space: pre-line; background: #f0f9ff; padding: 1rem; border-radius: 10px; border: 1px solid #bae6fd; }

.history-box { background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 1rem; }
.history-box .text-content { color: #78350f; }

.preventive-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 1rem; }
.preventive-box .text-content { color: #166534; }

.recurrence-bar-wrapper { padding: 0.6rem 1rem; border-radius: 10px; }
.recurrence-bar-wrapper.alto   { background: #fee2e2; }
.recurrence-bar-wrapper.médio  { background: #fef3c7; }
.recurrence-bar-wrapper.baixo  { background: #dcfce7; }
.recurrence-label { font-size: 0.9rem; font-weight: 600; color: #1e293b; line-height: 1.5; }

.ui-divider { height: 1px; background: #f1f5f9; margin: 1rem 0; }
.mt-4 { margin-top: 1rem; }

/* Spinners */
.spinner-blue { width: 36px; height: 36px; border-radius: 50%; border: 3px solid #dbeafe; border-top-color: #2563eb; animation: spin 0.8s linear infinite; }
.spinner-small { width: 16px; height: 16px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.4); border-top-color: white; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Animações ────────────────────────────────────── */
@keyframes fadeIn  { from { opacity: 0; transform: translateY(5px);  } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in  { animation: fadeIn  0.4s ease-out; }
.animate-slide-up { animation: slideUp 0.4s ease-out; }

/* ── Mobile ───────────────────────────────────────── */
@media (max-width: 768px) {
  .page-header, .form-card { padding: 1.1rem 1.2rem; border-radius: 16px; }
  .card { border-radius: 16px; }
  .filters-panel { gap: 0.75rem; }
  .form-actions { justify-content: stretch; flex-direction: column; }
  .form-actions .btn { width: 100%; }
  .result-header, .result-body { padding: 1rem 1.2rem; }
}
@media (max-width: 480px) {
  .page-header h2 { font-size: 1.2rem; }
  .card-header h3 { font-size: 1rem; }
  .filter-input { padding: 0.6rem 0.7rem; }
}
</style>