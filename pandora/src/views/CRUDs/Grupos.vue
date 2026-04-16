<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Acessos</p>
        <h2>Gestao de Grupos</h2>
        <p class="page-copy">Crie grupos da empresa logada e marque as permissoes que cada grupo pode ter.</p>
      </div>
    </section>

    <section v-if="canCreate || canEdit || canAssignPermissions" class="card form-card">
      <div class="card-header">
        <h3>{{ isEditing ? 'Editar grupo' : 'Novo grupo' }}</h3>
        <p>Defina o nome do grupo e selecione as permissoes liberadas para ele.</p>
      </div>

      <form @submit.prevent="saveGrupo" class="crud-form">
        <div class="input-group">
          <label>Nome do Grupo</label>
          <input
            v-model="form.nome_grupo"
            type="text"
            required
            placeholder="Ex: Gerente Pavan"
            :disabled="isEditing && !canEdit"
          />
        </div>

        <div class="permission-panel">
          <div class="permission-panel-header">
            <div>
              <h4>Permissoes do grupo</h4>
              <p>Marque tudo o que esse grupo pode visualizar ou executar.</p>
            </div>
            <div class="permission-toolbar">
              <button type="button" class="btn btn-row" @click="selectAllPermissions" :disabled="!canManagePermissions">
                Marcar tudo
              </button>
              <button type="button" class="btn btn-secondary" @click="clearPermissions" :disabled="!canManagePermissions">
                Limpar
              </button>
            </div>
          </div>

          <div class="permissions-layout">
            <aside class="permissions-sidebar">
              <button
                v-for="group in permissionGroups"
                :key="group.key"
                type="button"
                class="permission-tab"
                :class="{ active: activePermissionGroupKey === group.key }"
                @click="activePermissionGroupKey = group.key"
              >
                <strong>{{ group.label }}</strong>
                <span>{{ countSelectedByGroup(group.items) }} selecionada(s)</span>
              </button>
            </aside>

            <section v-if="activePermissionGroup" class="permission-card">
              <header class="permission-card-header">
                <div>
                  <h5>{{ activePermissionGroup.label }}</h5>
                  <p>Escolha as acoes permitidas para este modulo.</p>
                </div>
                <span>{{ countSelectedByGroup(activePermissionGroup.items) }} selecionada(s)</span>
              </header>

              <div class="permission-card-list">
                <label
                  v-for="permission in activePermissionGroup.items"
                  :key="permission.id"
                  class="permission-option"
                  :class="{ disabled: !canManagePermissions }"
                >
                  <input
                    v-model="form.permissoes"
                    type="checkbox"
                    :value="permission.id"
                    :disabled="!canManagePermissions"
                  />
                  <div>
                    <strong>{{ permission.actionLabel }}</strong>
                    <span>{{ permission.nome_permissao }}</span>
                  </div>
                </label>
              </div>
            </section>
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
        <h3>Grupos cadastrados</h3>
        <p>{{ grupos.length }} registro(s) vinculados a empresa logada.</p>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome do Grupo</th>
              <th>Permissoes</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!grupos.length">
              <td colspan="4" class="empty-state">Nenhum grupo encontrado para esta empresa.</td>
            </tr>
            <tr v-for="grupo in grupos" :key="grupo.id">
              <td>{{ grupo.id }}</td>
              <td>{{ grupo.nome_grupo }}</td>
              <td>{{ formatPermissionCount(grupo.permissoes) }}</td>
              <td>
                <div class="action-buttons">
                  <button v-if="canEdit || canAssignPermissions" @click="editGrupo(grupo)" class="btn btn-row">Editar</button>
                  <button v-if="canDelete" @click="deleteGrupo(grupo)" class="btn btn-danger">Excluir</button>
                  <span v-if="!canEdit && !canAssignPermissions && !canDelete" class="empty-actions">Sem acoes disponiveis</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="!canView && !canCreate && !canEdit && !canDelete && !canAssignPermissions" class="card empty-card">
      <div class="card-header">
        <h3>Acesso indisponivel</h3>
        <p>Este CRUD aparecera quando alguma permissao relacionada a grupos estiver liberada.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { api } from '../../services/api'
import { getStoredPermissions, hasPermission } from '../../utils/permissions'

const grupos = ref([])
const permissoes = ref([])
const isEditing = ref(false)
const editingId = ref(null)
const originalGrupoSnapshot = ref(null)
const activePermissionGroupKey = ref('')

const empresaIdLocal = Number(localStorage.getItem('empresa_id'))
const isEmpresaValida = Number.isInteger(empresaIdLocal) && empresaIdLocal > 0
const permissions = computed(() => getStoredPermissions())
const canView = computed(() => hasPermission('grupos.visualizar', permissions.value))
const canCreate = computed(() => hasPermission('grupos.criar', permissions.value))
const canEdit = computed(() => hasPermission('grupos.editar', permissions.value))
const canDelete = computed(() => hasPermission('grupos.excluir', permissions.value))
const canAssignPermissions = computed(() => hasPermission('grupos.atribuir_permissoes', permissions.value))
const canManagePermissions = computed(() => canCreate.value || canAssignPermissions.value || canEdit.value)

const createEmptyForm = () => ({
  nome_grupo: '',
  empresa: empresaIdLocal,
  permissoes: []
})

const form = ref(createEmptyForm())

const formatModuleLabel = (moduleKey) =>
  moduleKey
    .split('_')
    .map((chunk) => chunk.charAt(0).toUpperCase() + chunk.slice(1))
    .join(' ')

const formatActionLabel = (actionKey) =>
  actionKey
    .split('_')
    .map((chunk) => chunk.charAt(0).toUpperCase() + chunk.slice(1))
    .join(' ')

const normalizePermission = (item) => {
  const [moduleKey = 'geral', actionKey = 'acesso'] = String(item?.nome_permissao || '').split('.')
  return {
    ...item,
    moduleKey,
    actionKey,
    actionLabel: formatActionLabel(actionKey)
  }
}

const permissionGroups = computed(() => {
  const groupsMap = new Map()

  permissoes.value.forEach((permission) => {
    const normalized = normalizePermission(permission)
    const existing = groupsMap.get(normalized.moduleKey) || {
      key: normalized.moduleKey,
      label: formatModuleLabel(normalized.moduleKey),
      items: []
    }

    existing.items.push(normalized)
    groupsMap.set(normalized.moduleKey, existing)
  })

  return Array.from(groupsMap.values()).sort((a, b) => a.label.localeCompare(b.label, 'pt-BR'))
})

const activePermissionGroup = computed(
  () => permissionGroups.value.find((group) => group.key === activePermissionGroupKey.value) || permissionGroups.value[0]
)

const countSelectedByGroup = (items) =>
  items.filter((item) => form.value.permissoes.includes(item.id)).length

const formatPermissionCount = (items) => `${Array.isArray(items) ? items.length : 0} permissao(oes)`

const pertenceAEmpresaLogada = (grupo) => Number(grupo?.empresa) === empresaIdLocal

const fetchData = async () => {
  if (!isEmpresaValida) {
    grupos.value = []
    permissoes.value = []
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  try {
    const requests = [api.getAll('permissoes')]
    if (canView.value) {
      requests.unshift(api.getAll('grupos'))
    }

    const responses = await Promise.all(requests)
    const gruposResponse = canView.value ? responses[0] : []
    const permissoesResponse = canView.value ? responses[1] : responses[0]

    grupos.value = Array.isArray(gruposResponse) ? gruposResponse.filter(pertenceAEmpresaLogada) : []
    permissoes.value = Array.isArray(permissoesResponse) ? permissoesResponse : []
  } catch (error) {
    console.error(error)
    alert(error?.message || 'Erro ao carregar os dados de grupos.')
  }
}

const saveGrupo = async () => {
  if (!isEmpresaValida) {
    alert('Empresa do usuario nao identificada. Faca login novamente.')
    return
  }

  if (!canCreate.value && !isEditing.value) {
    alert('Voce nao possui permissao para criar grupos.')
    return
  }

  if (!canEdit.value && isEditing.value && form.value.nome_grupo !== currentGrupoName.value) {
    alert('Voce nao possui permissao para editar o nome do grupo.')
    return
  }

  const permissionsChanged =
    JSON.stringify([...(form.value.permissoes || [])].sort((a, b) => a - b)) !==
    JSON.stringify([...(originalGrupoSnapshot.value?.permissoes || [])].sort((a, b) => a - b))

  if (!canAssignPermissions.value && isEditing.value && permissionsChanged) {
    alert('Voce nao possui permissao para atribuir permissoes a grupos.')
    return
  }

  try {
    const payload = {
      nome_grupo: form.value.nome_grupo,
      empresa: empresaIdLocal,
      permissoes: form.value.permissoes
    }

    if (isEditing.value) {
      await api.update('grupos', editingId.value, payload)
    } else {
      await api.create('grupos', payload)
    }

    cancelEdit()
    await fetchData()
  } catch (error) {
    console.error(error)
    alert(error?.message || 'Erro ao salvar grupo.')
  }
}

const currentGrupoName = computed(() => {
  return originalGrupoSnapshot.value?.nome_grupo || ''
})

const editGrupo = (grupo) => {
  if (!canEdit.value && !canAssignPermissions.value) {
    alert('Voce nao possui permissao para editar grupos.')
    return
  }

  if (!pertenceAEmpresaLogada(grupo)) {
    alert('Voce so pode editar grupos da sua empresa.')
    return
  }

  isEditing.value = true
  editingId.value = grupo.id
  originalGrupoSnapshot.value = {
    nome_grupo: grupo.nome_grupo,
    permissoes: Array.isArray(grupo.permissoes) ? [...grupo.permissoes] : []
  }
  form.value = {
    nome_grupo: grupo.nome_grupo,
    empresa: empresaIdLocal,
    permissoes: Array.isArray(grupo.permissoes) ? [...grupo.permissoes] : []
  }
}

const deleteGrupo = async (grupo) => {
  if (!canDelete.value) {
    alert('Voce nao possui permissao para excluir grupos.')
    return
  }

  if (!pertenceAEmpresaLogada(grupo)) {
    alert('Voce so pode excluir grupos da sua empresa.')
    return
  }

  if (confirm(`Excluir o grupo "${grupo.nome_grupo}"?`)) {
    await api.delete('grupos', grupo.id)
    await fetchData()
  }
}

const cancelEdit = () => {
  isEditing.value = false
  editingId.value = null
  originalGrupoSnapshot.value = null
  form.value = createEmptyForm()
}

const selectAllPermissions = () => {
  if (!canManagePermissions.value) return
  form.value.permissoes = permissoes.value.map((item) => item.id)
}

const clearPermissions = () => {
  if (!canManagePermissions.value) return
  form.value.permissoes = []
}

onMounted(fetchData)

watch(
  permissionGroups,
  (groups) => {
    if (!groups.length) {
      activePermissionGroupKey.value = ''
      return
    }

    const hasActiveGroup = groups.some((group) => group.key === activePermissionGroupKey.value)
    if (!hasActiveGroup) {
      activePermissionGroupKey.value = groups[0].key
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.crud-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; border-radius: 20px; padding: 1.5rem 1.75rem; }
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.page-header h2, .card-header h3, .permission-panel-header h4, .permission-card-header h5 { margin: 0; color: #0f172a; }
.page-copy, .card-header p, .permission-panel-header p { margin: 0.4rem 0 0; color: #475569; }
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.form-card, .table-card, .empty-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.crud-form { display: flex; flex-direction: column; gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input { box-sizing: border-box; width: 100%; padding: 0.9rem 1rem; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; color: #0f172a; transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s; }
.input-group input:focus { outline: none; background: #ffffff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14); }
.permission-panel { border: 1px solid #dbeafe; border-radius: 18px; padding: 1rem; background: #f8fbff; }
.permission-panel-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 1rem; }
.permission-toolbar { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.permissions-layout { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 1rem; }
.permissions-sidebar { display: flex; flex-direction: column; gap: 0.75rem; }
.permission-tab { width: 100%; text-align: left; border: 1px solid #dbeafe; background: #ffffff; border-radius: 16px; padding: 0.95rem 1rem; cursor: pointer; transition: border-color 0.2s, transform 0.15s, box-shadow 0.2s; }
.permission-tab:hover { transform: translateY(-1px); border-color: #93c5fd; }
.permission-tab.active { border-color: #2563eb; background: #eff6ff; box-shadow: 0 12px 24px rgba(37, 99, 235, 0.12); }
.permission-tab strong { display: block; color: #0f172a; }
.permission-tab span { display: block; margin-top: 0.2rem; font-size: 0.85rem; color: #64748b; }
.permission-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1rem; }
.permission-card-header { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: 0.9rem; }
.permission-card-header p { margin: 0.35rem 0 0; color: #64748b; }
.permission-card-header span { font-size: 0.85rem; color: #64748b; }
.permission-card-list { display: flex; flex-direction: column; }
.permission-option { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 0; border-top: 1px solid #eef2f7; color: #1e293b; }
.permission-option:first-of-type { border-top: none; padding-top: 0; }
.permission-option input { margin-top: 0.15rem; }
.permission-option strong { display: block; }
.permission-option span { display: block; margin-top: 0.15rem; font-size: 0.85rem; color: #64748b; }
.permission-option.disabled { opacity: 0.65; }
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
.empty-actions { color: #64748b; font-size: 0.9rem; }
.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }
@media (max-width: 900px) { .permissions-layout { grid-template-columns: 1fr; } .permissions-sidebar { flex-direction: row; overflow-x: auto; padding-bottom: 0.25rem; } .permission-tab { min-width: 220px; } }
@media (max-width: 768px) { .page-header, .form-card, .table-card, .empty-card { padding: 1.2rem; } .permission-panel-header, .action-buttons, .form-actions { flex-direction: column; } .btn { width: 100%; } }
</style>
