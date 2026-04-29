<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Cadastros</p>
        <h2>Gestão de Setores</h2>
        <p class="page-copy">Organize os setores disponíveis para a empresa logada.</p>
      </div>
    </section>

    <section v-if="canCreate || canEdit" class="card form-card">
      <div class="card-header">
        <h3>{{ isEditing ? 'Editar setor' : 'Novo setor' }}</h3>
        <p>Preencha os dados abaixo para manter a estrutura sempre atualizada.</p>
      </div>

      <form @submit.prevent="saveSetor" class="crud-form">
        <div class="input-group">
          <label>Nome do Setor</label>
          <input v-model="form.nome_setor" type="text" required placeholder="Ex: Manutenção Elétrica" />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ isEditing ? 'Atualizar' : 'Cadastrar' }}</button>
          <button type="button" v-if="isEditing" @click="cancelEdit" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </section>

    <section v-if="canView" class="card table-card">
      <div class="card-header">
        <h3>Setores cadastrados</h3>
        <p>{{ setores.length }} registro(s) disponíveis.</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome do Setor</th>
              <th class="col-acoes">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!setores.length">
              <td colspan="3" class="empty-state">Nenhum setor encontrado para esta empresa.</td>
            </tr>
            <tr v-for="setor in setores" :key="setor.id">
              <td>{{ setor.id }}</td>
              <td>{{ setor.nome_setor }}</td>
              <td class="col-acoes">
                <div class="action-buttons">
                  <button v-if="canEdit" @click="editSetor(setor)" class="btn-icon" title="Editar">✏️</button>
                  <button v-if="canDelete" @click="deleteSetor(setor.id)" class="btn-icon" title="Excluir">🗑️</button>
                  <span v-if="!canEdit && !canDelete" class="empty-actions">—</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="!canView && !canCreate && !canEdit && !canDelete" class="card empty-card">
      <div class="card-header">
        <h3>Acesso indisponível</h3>
        <p>Este CRUD será exibido somente quando alguma permissão de setores estiver liberada.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { api } from '../../services/api'
import { getStoredPermissions, hasPermission } from '../../utils/permissions'

const setores = ref([])
const isEditing = ref(false)
const editingId = ref(null)

const empresaIdLocal = Number(localStorage.getItem('empresa_id'))
const isEmpresaValida = Number.isInteger(empresaIdLocal) && empresaIdLocal > 0
const permissions = computed(() => getStoredPermissions())
const canView = computed(() => hasPermission('setores.visualizar', permissions.value))
const canCreate = computed(() => hasPermission('setores.criar', permissions.value))
const canEdit = computed(() => hasPermission('setores.editar', permissions.value))
const canDelete = computed(() => hasPermission('setores.excluir', permissions.value))

const createEmptyForm = () => ({
  nome_setor: '',
  empresa: empresaIdLocal
})

const pertenceAEmpresaLogada = (setor) => Number(setor?.empresa) === empresaIdLocal

const form = ref(createEmptyForm())

const fetchData = async () => {
  if (!canView.value) {
    setores.value = []
    return
  }

  if (!isEmpresaValida) {
    setores.value = []
    alert('Empresa do usuário não identificada. Faça login novamente.')
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
  if (!canCreate.value && !isEditing.value) {
    alert('Você não possui permissão para criar setores.')
    return
  }

  if (!canEdit.value && isEditing.value) {
    alert('Você não possui permissão para editar setores.')
    return
  }

  if (!isEmpresaValida) {
    alert('Empresa do usuário não identificada. Faça login novamente.')
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
  if (!canEdit.value) {
    alert('Você não possui permissão para editar setores.')
    return
  }

  if (!pertenceAEmpresaLogada(setor)) {
    alert('Você só pode editar setores da sua empresa.')
    return
  }

  isEditing.value = true
  editingId.value = setor.id
  form.value = { ...setor, empresa: empresaIdLocal }
}

const deleteSetor = async (id) => {
  if (!canDelete.value) {
    alert('Você não possui permissão para excluir setores.')
    return
  }

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

.crud-form { display: flex; flex-direction: column; gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input {
  box-sizing: border-box; width: 100%;
  padding: 0.9rem 1rem; border: 1px solid #cbd5e1;
  border-radius: 12px; background: #f8fafc;
  color: #0f172a; font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
}
.input-group input:focus {
  outline: none; background: #ffffff;
  border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14);
}

.form-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }

.btn { border: none; border-radius: 12px; padding: 0.8rem 1.15rem; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s, background-color 0.2s; }
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: #2563eb; color: #ffffff; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24); }
.btn-secondary { background: #e2e8f0; color: #1e293b; }

.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.data-table { width: 100%; border-collapse: collapse; min-width: 320px; }
.data-table th, .data-table td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }
.data-table th { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; white-space: nowrap; }
.data-table td { color: #1e293b; }

.col-acoes { text-align: left !important; }
.action-buttons { display: inline-flex; gap: 0.5rem; align-items: center; }

.btn-icon {
  background: none; border: none; cursor: pointer;
  font-size: 1.1rem; padding: 0.3rem;
  filter: grayscale(1); opacity: 0.7;
  display: inline-flex; align-items: center; justify-content: center;
  transition: filter 0.2s, opacity 0.2s, transform 0.2s;
}
.btn-icon:hover { filter: none; opacity: 1; transform: scale(1.2); }

.empty-actions { color: #94a3b8; font-size: 0.85rem; }
.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }
.empty-card { padding: 1.5rem; }

@media (max-width: 768px) {
  .page-header, .form-card, .table-card { padding: 1.2rem; border-radius: 16px; }
  .card { border-radius: 16px; }
  .form-actions { flex-direction: column; }
  .form-actions .btn { width: 100%; }
  .table-wrap { border-radius: 12px; border: 1px solid #e2e8f0; }
  .data-table th, .data-table td { padding: 0.75rem 0.85rem; font-size: 0.875rem; }
}
</style>