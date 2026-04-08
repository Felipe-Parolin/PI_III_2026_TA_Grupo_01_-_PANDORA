<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Cadastros</p>
        <h2>Gestao de Setores</h2>
        <p class="page-copy">Organize os setores disponiveis para a empresa logada.</p>
      </div>
    </section>

    <section class="card form-card">
      <div class="card-header">
        <h3>{{ isEditing ? 'Editar setor' : 'Novo setor' }}</h3>
        <p>Preencha os dados abaixo para manter a estrutura sempre atualizada.</p>
      </div>

      <form @submit.prevent="saveSetor" class="crud-form">
        <div class="input-group">
          <label>Nome do Setor</label>
          <input v-model="form.nome_setor" type="text" required placeholder="Ex: Manutencao Eletrica" />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ isEditing ? 'Atualizar' : 'Cadastrar' }}</button>
          <button type="button" v-if="isEditing" @click="cancelEdit" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </section>

    <section class="card table-card">
      <div class="card-header">
        <h3>Setores cadastrados</h3>
        <p>{{ setores.length }} registro(s) disponiveis.</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome do Setor</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!setores.length">
              <td colspan="3" class="empty-state">Nenhum setor encontrado para esta empresa.</td>
            </tr>
            <tr v-for="setor in setores" :key="setor.id">
              <td>{{ setor.id }}</td>
              <td>{{ setor.nome_setor }}</td>
              <td><div class="action-buttons">
                <button @click="editSetor(setor)" class="btn btn-row">Editar</button>
                <button @click="deleteSetor(setor.id)" class="btn btn-danger">Excluir</button>
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

const setores = ref([])
const isEditing = ref(false)
const editingId = ref(null)

const empresaIdLocal = Number(localStorage.getItem('empresa_id'))
const isEmpresaValida = Number.isInteger(empresaIdLocal) && empresaIdLocal > 0

const createEmptyForm = () => ({
  nome_setor: '',
  empresa: empresaIdLocal
})

const pertenceAEmpresaLogada = (setor) => Number(setor?.empresa) === empresaIdLocal

const form = ref(createEmptyForm())

const fetchData = async () => {
  if (!isEmpresaValida) {
    setores.value = []
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  try {
    const setoresResponse = await api.getAll('setores')
    setores.value = setoresResponse.filter(pertenceAEmpresaLogada)
  } catch (error) {
    alert('Erro ao carregar os dados.')
  }
}

const saveSetor = async () => {
  if (!isEmpresaValida) {
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  try {
    const payload = {
      ...form.value,
      empresa: empresaIdLocal
    }

    if (isEditing.value) {
      await api.update('setores', editingId.value, payload)
    } else {
      await api.create('setores', payload)
    }

    cancelEdit()
    await fetchData()
  } catch (error) {
    alert('Erro ao salvar setor.')
  }
}

const editSetor = (setor) => {
  if (!pertenceAEmpresaLogada(setor)) {
    alert('Voce so pode editar setores da sua empresa.')
    return
  }

  isEditing.value = true
  editingId.value = setor.id
  form.value = { ...setor, empresa: empresaIdLocal }
}

const deleteSetor = async (id) => {
  if (confirm('Tem certeza que deseja excluir?')) {
    await api.delete('setores', id)
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
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input { box-sizing: border-box; width: 100%; padding: 0.9rem 1rem; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; color: #0f172a; transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s; }
.input-group input:focus { outline: none; background: #ffffff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14); }
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
.data-table td { color: #1e293b; }
.action-buttons { display: flex; gap: 0.6rem; flex-wrap: wrap; }
.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }
@media (max-width: 768px) { .page-header, .form-card, .table-card { padding: 1.2rem; } .action-buttons, .form-actions { flex-direction: column; } .btn { width: 100%; } }
</style>


