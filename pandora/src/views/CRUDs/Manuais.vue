<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Cadastros</p>
        <h2>Gestao de Manuais</h2>
        <p class="page-copy">Centralize os documentos tecnicos vinculados aos equipamentos da empresa.</p>
      </div>
    </section>

    <section class="card form-card">
      <div class="card-header">
        <h3>{{ isEditing ? 'Editar manual' : 'Novo manual' }}</h3>
        <p>Cadastre links de referencia e mantenha o acervo acessivel pela operacao.</p>
      </div>

      <form @submit.prevent="saveManual" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label>Tipo de Arquivo</label>
            <input v-model="form.tipo_arquivo" type="text" required placeholder="Ex: PDF, DOCX" />
          </div>
          <div class="input-group">
            <label>Equipamento Vinculado</label>
            <select v-model="form.equipamento" required>
              <option value="" disabled>Selecione um equipamento...</option>
              <option v-for="eq in equipamentos" :key="eq.id" :value="eq.id">
                {{ eq.nome_equipamento }}
              </option>
            </select>
          </div>
        </div>

        <div class="input-group">
          <label>URL do Caminho</label>
          <input v-model="form.caminho_url" type="url" required placeholder="https://..." />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ isEditing ? 'Atualizar' : 'Cadastrar' }}</button>
          <button type="button" v-if="isEditing" @click="cancelEdit" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </section>

    <section class="card table-card">
      <div class="card-header">
        <h3>Manuais cadastrados</h3>
        <p>{{ manuais.length }} registro(s) vinculados aos equipamentos visiveis.</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Tipo</th>
              <th>Link</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!manuais.length">
              <td colspan="4" class="empty-state">Nenhum manual encontrado para esta empresa.</td>
            </tr>
            <tr v-for="man in manuais" :key="man.id">
              <td>{{ man.id }}</td>
              <td>{{ man.tipo_arquivo }}</td>
              <td>
                <a :href="man.caminho_url" target="_blank" rel="noopener" class="manual-link">Acessar arquivo</a>
              </td>
              <td><div class="action-buttons">
                <button @click="editManual(man)" class="btn btn-row">Editar</button>
                <button @click="deleteManual(man.id)" class="btn btn-danger">Excluir</button>
              </div></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../../services/api'

const manuais = ref([])
const equipamentos = ref([])
const isEditing = ref(false)
const editingId = ref(null)
const empresaIdLocal = Number(localStorage.getItem('empresa_id'))
const isEmpresaValida = Number.isInteger(empresaIdLocal) && empresaIdLocal > 0

const getEmpresaId = (item) => Number(item?.empresa?.id ?? item?.empresa)

const createEmptyForm = () => ({
  tipo_arquivo: '',
  caminho_url: '',
  equipamento: ''
})

const form = ref(createEmptyForm())

const fetchData = async () => {
  if (!isEmpresaValida) {
    manuais.value = []
    equipamentos.value = []
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  const [manuaisResponse, equipamentosResponse, setoresResponse] = await Promise.all([
    api.getAll('manuais'),
    api.getAll('equipamentos'),
    api.getAll('setores')
  ])

  const setoresDaEmpresa = setoresResponse.filter((setor) => getEmpresaId(setor) === empresaIdLocal)
  const setorIds = new Set(setoresDaEmpresa.map((setor) => Number(setor.id)))

  equipamentos.value = equipamentosResponse.filter((equipamento) => setorIds.has(Number(equipamento.setor)))

  const equipamentoIds = new Set(equipamentos.value.map((equipamento) => Number(equipamento.id)))
  manuais.value = manuaisResponse.filter((manual) => equipamentoIds.has(Number(manual.equipamento)))
}

const saveManual = async () => {
  if (!isEmpresaValida) {
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  if (isEditing.value) await api.update('manuais', editingId.value, form.value)
  else await api.create('manuais', form.value)
  cancelEdit()
  await fetchData()
}

const editManual = (man) => {
  const equipamentoIds = new Set(equipamentos.value.map((equipamento) => Number(equipamento.id)))
  if (!equipamentoIds.has(Number(man.equipamento))) {
    alert('Voce so pode editar manuais da sua empresa.')
    return
  }

  isEditing.value = true
  editingId.value = man.id
  form.value = { ...man }
}

const deleteManual = async (id) => {
  if (confirm('Excluir manual?')) {
    await api.delete('manuais', id)
    await fetchData()
  }
}

const cancelEdit = () => {
  isEditing.value = false
  editingId.value = null
  form.value = createEmptyForm()
}

onMounted(fetchData)
</script>

<style scoped>
.crud-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; border-radius: 20px; padding: 1.5rem 1.75rem; }
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.page-header h2, .card-header h3 { margin: 0; color: #0f172a; }
.page-copy, .card-header p { margin: 0.4rem 0 0; color: #475569; }
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.form-card, .table-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.crud-form { display: flex; flex-direction: column; gap: 1rem; }
.input-row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input, .input-group select { box-sizing: border-box; width: 100%; padding: 0.9rem 1rem; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; color: #0f172a; transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s; }
.input-group input:focus, .input-group select:focus { outline: none; background: #ffffff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14); }
.form-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.btn { border: none; border-radius: 12px; padding: 0.8rem 1.15rem; font-weight: 600; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s, background-color 0.2s; }
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: #2563eb; color: #ffffff; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24); }
.btn-secondary, .btn-row { background: #e2e8f0; color: #1e293b; }
.btn-danger { background: #fee2e2; color: #b91c1c; }
.manual-link { color: #2563eb; font-weight: 600; text-decoration: none; }
.manual-link:hover { text-decoration: underline; }
.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
.data-table th { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; }
.action-buttons { display: flex; gap: 0.6rem; flex-wrap: wrap; }
.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }
@media (max-width: 768px) { .page-header, .form-card, .table-card { padding: 1.2rem; } .input-row { grid-template-columns: 1fr; } .action-buttons, .form-actions { flex-direction: column; } .btn { width: 100%; } }
</style>


