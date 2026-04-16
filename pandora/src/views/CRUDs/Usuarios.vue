<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Acessos</p>
        <h2>Gestao de Usuarios</h2>
        <p class="page-copy">Cadastre usuarios da empresa logada, vincule setor e escolha os grupos de acesso.</p>
      </div>
    </section>

    <section v-if="canCreate || canEdit || canToggleActive || canAssignGroups" class="card form-card">
      <div class="card-header">
        <h3>{{ isEditing ? 'Editar usuario' : 'Novo usuario' }}</h3>
        <p>Preencha os dados principais e marque os grupos que esse usuario pode usar.</p>
      </div>

      <form @submit.prevent="saveUsuario" class="crud-form">
        <div class="input-row">
          <div class="input-group">
            <label>Nome do Usuario</label>
            <input
              v-model="form.nome_usuario"
              type="text"
              required
              placeholder="Ex: Felipe"
              :disabled="isEditing && !canEdit"
            />
          </div>

          <div class="input-group">
            <label>E-mail</label>
            <input
              v-model="form.email"
              type="email"
              required
              placeholder="usuario@empresa.com.br"
              :disabled="isEditing && !canEdit"
            />
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label>{{ isEditing ? 'Nova senha' : 'Senha' }}</label>
            <input
              v-model="form.password"
              type="password"
              :required="!isEditing"
              placeholder="••••••••"
              :disabled="isEditing && !canEdit"
            />
          </div>

          <div class="input-group">
            <label>Setor</label>
            <select v-model="form.setor" :disabled="isEditing && !canEdit">
              <option :value="null">Nenhum</option>
              <option v-for="setor in setores" :key="setor.id" :value="setor.id">
                {{ setor.nome_setor }}
              </option>
            </select>
          </div>
        </div>

        <div class="status-card">
          <div>
            <strong>Status do usuario</strong>
            <p>Ative ou desative o acesso deste usuario ao sistema.</p>
          </div>
          <label class="toggle-line" :class="{ disabled: !canManageStatus }">
            <input v-model="form.ativo" type="checkbox" :disabled="!canManageStatus" />
            <span>{{ form.ativo ? 'Ativo' : 'Inativo' }}</span>
          </label>
        </div>

        <div class="groups-panel">
          <div class="groups-panel-header">
            <div>
              <h4>Grupos de acesso</h4>
              <p>Selecione os grupos da empresa que este usuario pode utilizar.</p>
            </div>
            <div class="groups-toolbar">
              <button type="button" class="btn btn-row" @click="selectAllGroups" :disabled="!canManageGroups">
                Marcar tudo
              </button>
              <button type="button" class="btn btn-secondary" @click="clearGroups" :disabled="!canManageGroups">
                Limpar
              </button>
            </div>
          </div>

          <div class="groups-grid">
            <label
              v-for="grupo in gruposDisponiveis"
              :key="grupo.id"
              class="group-option"
              :class="{ disabled: !canManageGroups }"
            >
              <input
                v-model="form.grupos"
                type="checkbox"
                :value="grupo.id"
                :disabled="!canManageGroups"
              />
              <div>
                <strong>{{ grupo.nome_grupo }}</strong>
                <span>{{ formatPermissionCount(grupo.permissoes) }}</span>
              </div>
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ isEditing ? 'Atualizar' : 'Cadastrar' }}</button>
          <button type="button" v-if="isEditing" @click="cancelEdit" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </section>

    <section v-if="canView" class="card table-card">
      <div class="card-header">
        <h3>Usuarios cadastrados</h3>
        <p>{{ usuarios.length }} registro(s) vinculados a empresa logada.</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>E-mail</th>
              <th>Setor</th>
              <th>Grupos</th>
              <th>Status</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!usuarios.length">
              <td colspan="7" class="empty-state">Nenhum usuario encontrado para esta empresa.</td>
            </tr>
            <tr v-for="usuario in usuarios" :key="usuario.id">
              <td>{{ usuario.id }}</td>
              <td>{{ usuario.nome_usuario }}</td>
              <td>{{ usuario.email }}</td>
              <td>{{ getSetorLabel(usuario.setor) }}</td>
              <td>{{ formatGroupCount(usuario.grupos) }}</td>
              <td>
                <span class="status-pill" :class="usuario.ativo ? 'status-active' : 'status-inactive'">
                  {{ usuario.ativo ? 'Ativo' : 'Inativo' }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button v-if="canEdit || canAssignGroups || canToggleActive" @click="editUsuario(usuario)" class="btn btn-row">Editar</button>
                  <button v-if="canDelete" @click="deleteUsuario(usuario)" class="btn btn-danger">Excluir</button>
                  <span v-if="!canEdit && !canAssignGroups && !canToggleActive && !canDelete" class="empty-actions">Sem acoes disponiveis</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="!canView && !canCreate && !canEdit && !canDelete && !canToggleActive && !canAssignGroups" class="card empty-card">
      <div class="card-header">
        <h3>Acesso indisponivel</h3>
        <p>Este CRUD aparecera quando alguma permissao relacionada a usuarios estiver liberada.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '../../services/api'
import { getStoredPermissions, hasPermission } from '../../utils/permissions'

const usuarios = ref([])
const setores = ref([])
const gruposDisponiveis = ref([])
const isEditing = ref(false)
const editingId = ref(null)
const originalUsuarioSnapshot = ref(null)

const empresaIdLocal = Number(localStorage.getItem('empresa_id'))
const isEmpresaValida = Number.isInteger(empresaIdLocal) && empresaIdLocal > 0
const permissions = computed(() => getStoredPermissions())
const canView = computed(() => hasPermission('usuarios.visualizar', permissions.value))
const canCreate = computed(() => hasPermission('usuarios.criar', permissions.value))
const canEdit = computed(() => hasPermission('usuarios.editar', permissions.value))
const canDelete = computed(() => hasPermission('usuarios.excluir', permissions.value))
const canToggleActive = computed(() => hasPermission('usuarios.ativar_desativar', permissions.value))
const canAssignGroups = computed(() => hasPermission('usuarios.atribuir_grupos', permissions.value))
const canManageGroups = computed(() => canCreate.value || canAssignGroups.value || canEdit.value)
const canManageStatus = computed(() => canCreate.value || canToggleActive.value || canEdit.value)

const createEmptyForm = () => ({
  nome_usuario: '',
  email: '',
  password: '',
  ativo: true,
  empresa: empresaIdLocal,
  setor: null,
  grupos: []
})

const form = ref(createEmptyForm())

const getEmpresaId = (item) => Number(item?.empresa?.id ?? item?.empresa)
const pertenceAEmpresaLogada = (item) => getEmpresaId(item) === empresaIdLocal
const getNormalizedGroupIds = (groups) =>
  (Array.isArray(groups) ? groups : [])
    .map((group) => Number(group?.id ?? group))
    .filter((id) => Number.isInteger(id) && id > 0)

const fetchData = async () => {
  if (!isEmpresaValida) {
    usuarios.value = []
    setores.value = []
    gruposDisponiveis.value = []
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  try {
    const requests = [api.getAll('setores'), api.getAll('grupos')]
    if (canView.value) {
      requests.unshift(api.getAll('usuarios'))
    }

    const responses = await Promise.all(requests)
    const usuariosResponse = canView.value ? responses[0] : []
    const setoresResponse = canView.value ? responses[1] : responses[0]
    const gruposResponse = canView.value ? responses[2] : responses[1]

    usuarios.value = Array.isArray(usuariosResponse) ? usuariosResponse.filter(pertenceAEmpresaLogada) : []
    setores.value = Array.isArray(setoresResponse) ? setoresResponse.filter(pertenceAEmpresaLogada) : []
    gruposDisponiveis.value = Array.isArray(gruposResponse) ? gruposResponse.filter(pertenceAEmpresaLogada) : []
  } catch (error) {
    console.error(error)
    alert(error?.message || 'Erro ao carregar os dados de usuarios.')
  }
}

const getSetorLabel = (setorId) => {
  const normalizedId = Number(setorId?.id ?? setorId)
  return setores.value.find((setor) => setor.id === normalizedId)?.nome_setor || 'Nao informado'
}

const formatGroupCount = (groups) => `${getNormalizedGroupIds(groups).length} grupo(s)`
const formatPermissionCount = (permissionsList) => `${Array.isArray(permissionsList) ? permissionsList.length : 0} permissao(oes)`

const saveUsuario = async () => {
  if (!isEmpresaValida) {
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  if (!canCreate.value && !isEditing.value) {
    alert('Voce nao possui permissao para criar usuarios.')
    return
  }

  if (!canEdit.value && isEditing.value) {
    const nomeMudou = form.value.nome_usuario !== (originalUsuarioSnapshot.value?.nome_usuario || '')
    const emailMudou = form.value.email !== (originalUsuarioSnapshot.value?.email || '')
    const setorMudou = Number(form.value.setor ?? 0) !== Number(originalUsuarioSnapshot.value?.setor ?? 0)
    const passwordInformada = Boolean(form.value.password)

    if (nomeMudou || emailMudou || setorMudou || passwordInformada) {
      alert('Voce nao possui permissao para editar os dados principais do usuario.')
      return
    }
  }

  const statusMudou = Boolean(form.value.ativo) !== Boolean(originalUsuarioSnapshot.value?.ativo)
  if (!canToggleActive.value && isEditing.value && statusMudou) {
    alert('Voce nao possui permissao para ativar ou desativar usuarios.')
    return
  }

  const gruposMudaram =
    JSON.stringify([...getNormalizedGroupIds(form.value.grupos)].sort((a, b) => a - b)) !==
    JSON.stringify([...(originalUsuarioSnapshot.value?.grupos || [])].sort((a, b) => a - b))

  if (!canAssignGroups.value && isEditing.value && gruposMudaram) {
    alert('Voce nao possui permissao para atribuir grupos a usuarios.')
    return
  }

  try {
    const payload = {
      nome_usuario: form.value.nome_usuario,
      email: form.value.email,
      ativo: form.value.ativo,
      empresa: empresaIdLocal,
      setor: form.value.setor || null,
      grupos: getNormalizedGroupIds(form.value.grupos)
    }

    if (form.value.password) {
      payload.password = form.value.password
    }

    if (isEditing.value) {
      await api.update('usuarios', editingId.value, payload)
    } else {
      await api.create('usuarios', payload)
    }

    cancelEdit()
    await fetchData()
  } catch (error) {
    console.error(error)
    alert(error?.message || 'Erro ao salvar usuario.')
  }
}

const editUsuario = (usuario) => {
  if (!canEdit.value && !canAssignGroups.value && !canToggleActive.value) {
    alert('Voce nao possui permissao para editar usuarios.')
    return
  }

  if (!pertenceAEmpresaLogada(usuario)) {
    alert('Voce so pode editar usuarios da sua empresa.')
    return
  }

  const normalizedGroups = getNormalizedGroupIds(usuario.grupos)

  isEditing.value = true
  editingId.value = usuario.id
  originalUsuarioSnapshot.value = {
    nome_usuario: usuario.nome_usuario,
    email: usuario.email,
    ativo: Boolean(usuario.ativo),
    setor: Number(usuario.setor ?? 0),
    grupos: [...normalizedGroups]
  }

  form.value = {
    nome_usuario: usuario.nome_usuario,
    email: usuario.email,
    password: '',
    ativo: Boolean(usuario.ativo),
    empresa: empresaIdLocal,
    setor: usuario.setor ?? null,
    grupos: [...normalizedGroups]
  }
}

const deleteUsuario = async (usuario) => {
  if (!canDelete.value) {
    alert('Voce nao possui permissao para excluir usuarios.')
    return
  }

  if (!pertenceAEmpresaLogada(usuario)) {
    alert('Voce so pode excluir usuarios da sua empresa.')
    return
  }

  if (confirm(`Excluir o usuario "${usuario.nome_usuario}"?`)) {
    await api.delete('usuarios', usuario.id)
    await fetchData()
  }
}

const cancelEdit = () => {
  isEditing.value = false
  editingId.value = null
  originalUsuarioSnapshot.value = null
  form.value = createEmptyForm()
}

const selectAllGroups = () => {
  if (!canManageGroups.value) return
  form.value.grupos = gruposDisponiveis.value.map((grupo) => grupo.id)
}

const clearGroups = () => {
  if (!canManageGroups.value) return
  form.value.grupos = []
}

onMounted(fetchData)
</script>

<style scoped>
.crud-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; border-radius: 20px; padding: 1.5rem 1.75rem; }
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.page-header h2, .card-header h3, .groups-panel-header h4 { margin: 0; color: #0f172a; }
.page-copy, .card-header p, .groups-panel-header p { margin: 0.4rem 0 0; color: #475569; }
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.form-card, .table-card, .empty-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.crud-form { display: flex; flex-direction: column; gap: 1rem; }
.input-row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input, .input-group select { box-sizing: border-box; width: 100%; padding: 0.9rem 1rem; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; color: #0f172a; transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s; }
.input-group input:focus, .input-group select:focus { outline: none; background: #ffffff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14); }
.status-card { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1rem 1.1rem; border: 1px solid #dbeafe; border-radius: 16px; background: #f8fbff; }
.status-card strong { color: #0f172a; }
.status-card p { margin: 0.35rem 0 0; color: #64748b; }
.toggle-line { display: inline-flex; align-items: center; gap: 0.65rem; color: #1e293b; }
.toggle-line.disabled { opacity: 0.65; }
.groups-panel { border: 1px solid #dbeafe; border-radius: 18px; padding: 1rem; background: #f8fbff; }
.groups-panel-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 1rem; }
.groups-toolbar { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.groups-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.group-option { display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; border: 1px solid #e2e8f0; border-radius: 16px; background: #ffffff; color: #1e293b; }
.group-option strong { display: block; }
.group-option span { display: block; margin-top: 0.2rem; font-size: 0.85rem; color: #64748b; }
.group-option.disabled { opacity: 0.65; }
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
.status-pill { display: inline-flex; align-items: center; border-radius: 999px; padding: 0.35rem 0.75rem; font-size: 0.85rem; font-weight: 700; }
.status-active { background: #dcfce7; color: #166534; }
.status-inactive { background: #e2e8f0; color: #475569; }
.action-buttons { display: flex; gap: 0.6rem; flex-wrap: wrap; }
.empty-actions { color: #64748b; font-size: 0.9rem; }
.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }
@media (max-width: 900px) { .groups-grid { grid-template-columns: 1fr; } }
@media (max-width: 768px) { .page-header, .form-card, .table-card, .empty-card { padding: 1.2rem; } .input-row { grid-template-columns: 1fr; } .status-card, .groups-panel-header, .action-buttons, .form-actions { flex-direction: column; } .btn { width: 100%; } }
</style>
