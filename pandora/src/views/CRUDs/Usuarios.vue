<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Cadastros</p>
        <h2>Gestao de Usuarios</h2>
        <p class="page-copy">Controle acessos, perfis e vinculacao por setor com o mesmo visual do dashboard.</p>
      </div>
    </section>

    <section class="card form-card">
      <div class="card-header">
        <h3>{{ isEditing ? 'Editar usuario' : 'Novo usuario' }}</h3>
        <p>Os campos abaixo alimentam a conta vinculada a empresa logada.</p>
      </div>

      <form @submit.prevent="saveUsuario" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label>Nome do Usuario</label>
            <input v-model="form.nome_usuario" type="text" required />
          </div>
          <div class="input-group">
            <label>E-mail</label>
            <input v-model="form.email" type="email" required />
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label>Senha</label>
            <input v-model="form.senha_hash" type="password" required />
          </div>
          <div class="input-group">
            <label>Perfil</label>
            <select v-model="form.perfil" required>
              <option value="" disabled>Selecione o perfil...</option>
              <option v-for="p in perfis" :key="p.id" :value="p.id">{{ p.tipo_perfil }}</option>
            </select>
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label>Setor</label>
            <select v-model="form.setor">
              <option :value="null">Nenhum</option>
              <option v-for="s in setores" :key="s.id" :value="s.id">{{ s.nome_setor }}</option>
            </select>
          </div>
          <div class="toggle-card">
            <span class="toggle-label">Status do usuario</span>
            <label class="toggle-line">
              <input v-model="form.ativo" type="checkbox" />
              <span>{{ form.ativo ? 'Ativo' : 'Inativo' }}</span>
            </label>
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
        <h3>Usuarios cadastrados</h3>
        <p>{{ usuarios.length }} registro(s) ativos nesta listagem.</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>E-mail</th>
              <th>Ativo</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!usuarios.length">
              <td colspan="5" class="empty-state">Nenhum usuario encontrado para esta empresa.</td>
            </tr>
            <tr v-for="usr in usuarios" :key="usr.id">
              <td>{{ usr.id }}</td>
              <td>{{ usr.nome_usuario }}</td>
              <td>{{ usr.email }}</td>
              <td>
                <span class="status-pill" :class="usr.ativo ? 'status-active' : 'status-inactive'">
                  {{ usr.ativo ? 'Sim' : 'Nao' }}
                </span>
              </td>
              <td><div class="action-buttons">
                <button @click="editUsuario(usr)" class="btn btn-row">Editar</button>
                <button @click="deleteUsuario(usr.id)" class="btn btn-danger">Excluir</button>
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

const usuarios = ref([])
const perfis = ref([])
const setores = ref([])
const isEditing = ref(false)
const editingId = ref(null)

const empresaIdLocal = Number(localStorage.getItem('empresa_id'))
const isEmpresaValida = Number.isInteger(empresaIdLocal) && empresaIdLocal > 0

const getEmpresaId = (item) => Number(item?.empresa?.id ?? item?.empresa)

const createEmptyForm = () => ({
  nome_usuario: '',
  email: '',
  senha_hash: '',
  ativo: true,
  empresa: empresaIdLocal,
  perfil: '',
  setor: null
})

const form = ref(createEmptyForm())

const fetchData = async () => {
  if (!isEmpresaValida) {
    usuarios.value = []
    setores.value = []
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  try {
    const [usuariosResponse, perfisResponse, setoresResponse] = await Promise.all([
      api.getAll('usuarios'),
      api.getAll('perfis'),
      api.getAll('setores')
    ])

    usuarios.value = usuariosResponse.filter((usr) => getEmpresaId(usr) === empresaIdLocal)
    perfis.value = perfisResponse
    setores.value = setoresResponse.filter((setor) => getEmpresaId(setor) === empresaIdLocal)
  } catch (error) {
    console.error(error)
  }
}

const saveUsuario = async () => {
  if (!isEmpresaValida) {
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  try {
    const payload = {
      ...form.value,
      empresa: empresaIdLocal
    }

    if (isEditing.value) await api.update('usuarios', editingId.value, payload)
    else await api.create('usuarios', payload)

    cancelEdit()
    await fetchData()
  } catch (error) {
    alert('Erro ao salvar usuario.')
  }
}

const editUsuario = (usr) => {
  if (getEmpresaId(usr) !== empresaIdLocal) {
    alert('Voce so pode editar usuarios da sua empresa.')
    return
  }

  isEditing.value = true
  editingId.value = usr.id
  form.value = { ...usr, empresa: empresaIdLocal, senha_hash: '' }
}

const deleteUsuario = async (id) => {
  if (confirm('Excluir este usuario?')) {
    await api.delete('usuarios', id)
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


