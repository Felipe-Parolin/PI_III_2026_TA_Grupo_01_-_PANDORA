const POSSIBLE_PERMISSION_KEYS = [
  'nome_permissao',
  'permission',
  'permissao',
  'codigo',
  'code',
  'name',
  'nome',
  'slug'
]

const POSSIBLE_COLLECTION_KEYS = [
  'permissoes',
  'permissions',
  'perfis_permissoes',
  'grupo_permissoes',
  'scopes',
  'scope'
]

const normalizePermissionValue = (value) => {
  if (typeof value !== 'string') return ''
  return value.trim()
}

export const extractPermissionNames = (input) => {
  const collected = new Set()

  const visit = (value) => {
    if (!value) return

    if (typeof value === 'string') {
      const normalized = normalizePermissionValue(value)
      if (normalized.includes('.')) {
        collected.add(normalized)
      }
      return
    }

    if (Array.isArray(value)) {
      value.forEach(visit)
      return
    }

    if (typeof value !== 'object') return

    POSSIBLE_PERMISSION_KEYS.forEach((key) => {
      const nested = value[key]
      if (typeof nested === 'string') {
        const normalized = normalizePermissionValue(nested)
        if (normalized.includes('.')) {
          collected.add(normalized)
        }
      } else {
        visit(nested)
      }
    })

    POSSIBLE_COLLECTION_KEYS.forEach((key) => {
      if (key in value) {
        visit(value[key])
      }
    })
  }

  visit(input)

  return Array.from(collected)
}

export const getStoredPermissions = () => {
  try {
    const parsed = JSON.parse(localStorage.getItem('permissoes') || '[]')
    return extractPermissionNames(parsed)
  } catch {
    return []
  }
}

export const hasCrudPermission = (prefix, permissions = getStoredPermissions()) =>
  permissions.some((permission) => permission.startsWith(`${prefix}.`))

export const hasPermission = (permissionName, permissions = getStoredPermissions()) =>
  permissions.includes(permissionName)
