<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Cadastros</p>
        <h2>Gestao de Equipamentos</h2>
        <p class="page-copy">Mantenha os ativos organizados por setor com um painel visualmente consistente.</p>
      </div>
    </section>

    <section class="card form-card">
      <div class="card-header">
        <h3>{{ isEditing ? 'Editar equipamento' : 'Novo equipamento' }}</h3>
        <p>Cadastre os dados tecnicos e vincule cada item ao setor correto.</p>
      </div>

      <form @submit.prevent="saveEquipamento" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label>Nome do Equipamento</label>
            <input v-model="form.nome_equipamento" type="text" required />
          </div>
          <div class="input-group">
            <label>Tipo</label>
            <input v-model="form.tipo_equipamento" type="text" required />
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label>Criticidade (1 a 5)</label>
            <input v-model.number="form.criticidade" type="number" required />
          </div>
          <div class="input-group">
            <label>Setor</label>
            <select v-model="form.setor" required>
              <option value="" disabled>Selecione um setor...</option>
              <option v-for="setor in setores" :key="setor.id" :value="setor.id">
                {{ setor.nome_setor }}
              </option>
            </select>
          </div>
        </div>

        <div class="input-row">
          <div class="toggle-card">
            <span class="toggle-label">Status do equipamento</span>
            <label class="toggle-line">
              <input v-model="form.status_ativo" type="checkbox" />
              <span>{{ form.status_ativo ? 'Ativo' : 'Inativo' }}</span>
            </label>
          </div>
          <div class="input-group">
            <label>ID Interno</label>
            <input v-model.number="form.id_interno" type="number" />
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ isEditing ? 'Atualizar' : 'Cadastrar' }}</button>
          <button type="button" v-if="isEditing" @click="cancelEdit" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </section>

    <section class="card table-card">
      <div class="card-header">
        <h3>Equipamentos cadastrados</h3>
        <p>{{ equipamentos.length }} registro(s) vinculados aos setores da empresa.</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Setor</th>
              <th>Status</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!equipamentos.length">
              <td colspan="5" class="empty-state">Nenhum equipamento encontrado para esta empresa.</td>
            </tr>
            <tr v-for="eq in equipamentos" :key="eq.id">
              <td>{{ eq.id }}</td>
              <td>{{ eq.nome_equipamento }}</td>
              <td>{{ getSetorName(eq.setor) }}</td>
              <td>
                <span class="status-pill" :class="eq.status_ativo ? 'status-active' : 'status-inactive'">
                  {{ eq.status_ativo ? 'Ativo' : 'Inativo' }}
                </span>
              </td>
              <td><div class="action-buttons">
                <button @click="editEquipamento(eq)" class="btn btn-row">Editar</button>
                <button @click="deleteEquipamento(eq.id)" class="btn btn-danger">Excluir</button>
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

const equipamentos = ref([])
const setores = ref([])
const isEditing = ref(false)
const editingId = ref(null)
const empresaIdLocal = Number(localStorage.getItem('empresa_id'))
const isEmpresaValida = Number.isInteger(empresaIdLocal) && empresaIdLocal > 0

const getEmpresaId = (item) => Number(item?.empresa?.id ?? item?.empresa)

const createEmptyForm = () => ({
  nome_equipamento: '',
  tipo_equipamento: '',
  criticidade: 1,
  status_ativo: true,
  id_interno: null,
  setor: ''
})

const form = ref(createEmptyForm())

const fetchData = async () => {
  if (!isEmpresaValida) {
    equipamentos.value = []
    setores.value = []
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  const [equipamentosResponse, setoresResponse] = await Promise.all([
    api.getAll('equipamentos'),
    api.getAll('setores')
  ])

  setores.value = setoresResponse.filter((setor) => getEmpresaId(setor) === empresaIdLocal)
  const setorIds = new Set(setores.value.map((setor) => Number(setor.id)))
  equipamentos.value = equipamentosResponse.filter((equipamento) => setorIds.has(Number(equipamento.setor)))
}

const getSetorName = (id) => {
  const setor = setores.value.find((s) => Number(s.id) === Number(id))
  return setor ? setor.nome_setor : 'Desconhecido'
}

const saveEquipamento = async () => {
  if (!isEmpresaValida) {
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  try {
    if (isEditing.value) {
      await api.update('equipamentos', editingId.value, form.value)
    } else {
      await api.create('equipamentos', form.value)
    }
    cancelEdit()
    await fetchData()
  } catch (error) {
    alert('Erro ao salvar equipamento.')
  }
}

const editEquipamento = (eq) => {
  const setorIds = new Set(setores.value.map((setor) => Number(setor.id)))
  if (!setorIds.has(Number(eq.setor))) {
    alert('Voce so pode editar equipamentos da sua empresa.')
    return
  }

  isEditing.value = true
  editingId.value = eq.id
  form.value = { ...eq }
}

const deleteEquipamento = async (id) => {
  if (confirm('Excluir equipamento?')) {
    await api.delete('equipamentos', id)
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
.input-group, .toggle-card { display: flex; flex-direction: column; gap: 0.45rem; }
.toggle-card { justify-content: center; padding: 1rem; border: 1px solid #dbeafe; border-radius: 16px; background: #f8fbff; }
.toggle-label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.toggle-line { display: inline-flex; align-items: center; gap: 0.65rem; color: #1e293b; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input, .input-group select { box-sizing: border-box; width: 100%; padding: 0.9rem 1rem; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; color: #0f172a; transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s; }
.input-group input:focus, .input-group select:focus { outline: none; background: #ffffff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14); }
.form-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.btn { border: none; border-radius: 12px; padding: 0.8rem 1.15rem; font-weight: 600; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s, background-color 0.2s; }
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: #2563eb; color: #ffffff; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24); }
.btn-secondary, .btn-row { background: #e2e8f0; color: #1e293b; }
.btn-danger { background: #fee2e2; color: #b91c1c; }
.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
.data-table th { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; }
.status-pill { display: inline-flex; align-items: center; border-radius: 999px; padding: 0.35rem 0.75rem; font-size: 0.85rem; font-weight: 700; }
.status-active { background: #dcfce7; color: #166534; }
.status-inactive { background: #e2e8f0; color: #475569; }
.action-buttons { display: flex; gap: 0.6rem; flex-wrap: wrap; }
.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }
@media (max-width: 768px) { .page-header, .form-card, .table-card { padding: 1.2rem; } .input-row { grid-template-columns: 1fr; } .action-buttons, .form-actions { flex-direction: column; } .btn { width: 100%; } }
</style>


