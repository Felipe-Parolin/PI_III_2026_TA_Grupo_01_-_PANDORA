<template>
  <div class="crud-page">
    <section class="page-header animate-fade-in">
      <p class="eyebrow">Manutenção Corretiva</p>
      <h2>Abrir Novo Chamado</h2>
      <p class="page-copy">Relate falhas enviando áudio, texto e imagens para a equipe técnica.</p>
    </section>

    <section class="card form-card animate-fade-in">
      <div class="card-header">
        <h3>Detalhes da Ocorrência</h3>
        <p>Preencha os dados da falha para abrir o chamado técnico.</p>
      </div>

      <form @submit.prevent="salvarChamado" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label>Equipamento com Falha</label>
            <select v-model="form.equipamento" required>
              <option value="" disabled>Selecione o equipamento...</option>
              <option v-for="e in equipamentos" :key="e.id" :value="e.id">
                #{{ e.id_interno || e.id }} - {{ e.nome_equipamento }}
              </option>
            </select>
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
            ></textarea>
            <button
              type="button"
              @click="toggleRecording"
              :class="['inner-mic-btn', { 'recording-active': isRecording }]"
              title="Transcrever Áudio"
            >
              <span v-if="!isRecording">🎤</span>
              <span v-else>🛑</span>
            </button>
          </div>
        </div>

        <!-- ── Fotos do Problema ── -->
        <div class="upload-section-container">
          <div class="upload-block">
            <div class="upload-block-header">
              <label class="small-label">📸 Fotos do Problema <span class="optional-tag">opcional</span></label>
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
          <button type="submit" :disabled="carregando" class="btn btn-primary">
            <span v-if="!carregando">🚀 Abrir Chamado</span>
            <span v-else>Enviando...</span>
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const carregando = ref(false)
const equipamentos = ref([])
const isRecording = ref(false)
const fotosProblema = ref([]) // [{ file, nome, preview }]

const form = ref({
  equipamento: '',
  urgencia: 'Média',
  descricao_problema: '',
  status: 'Aberto'
})

// ── WebSpeech API ─────────────────────────────────────────────────────────────
let recognition = null
if (window.webkitSpeechRecognition || window.SpeechRecognition) {
  const SpeechConstructor = window.webkitSpeechRecognition || window.SpeechRecognition
  recognition = new SpeechConstructor()
  recognition.lang = 'pt-BR'
  recognition.continuous = true
  recognition.interimResults = true

  recognition.onresult = (event) => {
    let transcript = ''
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript
    }
    form.value.descricao_problema = transcript
  }
}

const toggleRecording = () => {
  if (!recognition) return alert('Navegador incompatível com áudio.')
  if (isRecording.value) {
    recognition.stop()
    isRecording.value = false
  } else {
    recognition.start()
    isRecording.value = true
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
  try {
    const res = await axios.get('http://localhost:8000/api/equipamentos/', getHeaders())
    equipamentos.value = res.data
  } catch (e) {
    console.error('Erro ao buscar equipamentos:', e.response?.status)
  }
}

// ── Salvar chamado + fotos ────────────────────────────────────────────────────
const salvarChamado = async () => {
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
    const resOS = await axios.post('http://localhost:8000/api/ordens-servico/', payload, getHeaders())
    const osId = resOS.data.id

    // 2. Faz upload das fotos como DocumentoEquipamento com prefixo especial
    //    O prefixo "Problema OS#<id>" permite distingui-las na exibição da OS
    for (const foto of fotosProblema.value) {
      const docData = new FormData()
      docData.append('equipamento', form.value.equipamento)
      docData.append('caminho_arquivo', foto.file)
      docData.append('nome_arquivo', `Problema OS#${osId} - ${foto.nome}`)
      try {
        await axios.post('http://localhost:8000/api/documentos-equipamento/', docData, getHeaders())
      } catch (docErr) {
        console.error('Erro ao salvar foto do problema:', docErr.response?.data)
        alert(`Erro no upload de "${foto.nome}":\n` + JSON.stringify(docErr.response?.data))
      }
    }

    alert('Chamado aberto com sucesso!')

    // 3. Limpa o formulário
    form.value.descricao_problema = ''
    form.value.equipamento = ''
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
.form-card { padding: 1.5rem; }
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
.recording-active { background: #fee2e2; border-color: #ef4444; }

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