<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="logo">Pandora</h2>
        <p class="subtitle">{{ sidebarSubtitle }}</p>
      </div>

      <nav v-if="navItems.length" class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          active-class="active"
        >
          {{ item.label }}
        </router-link>
      </nav>

      <div v-else class="sidebar-empty">
        Nenhum modulo liberado ainda.
      </div>

      <div class="sidebar-footer">
        <div class="profile-card">
          <span class="profile-name">{{ nomeUsuario }}</span>
          <span class="profile-role">{{ tipoPerfil }}</span>
        </div>
        <button @click="logout" class="btn-logout">Sair do Sistema</button>
      </div>

      <div class="decor decor-1"></div>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <div>
          <h3>{{ pageTitle }}</h3>
          <p class="topbar-subtitle">{{ topbarSubtitle }}</p>
        </div>
        <div class="user-profile">
          <span class="avatar">{{ userInitial }}</span>
        </div>
      </header>

      <div class="content-area">
        <div v-if="!navItems.length" class="empty-dashboard">
          <h4>Nenhum CRUD disponivel</h4>
          <p>Quando novas permissoes e modulos forem liberados, eles aparecerao aqui.</p>
        </div>
        <router-view v-else></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStoredPermissions, hasCrudPermission } from '../utils/permissions'

const router = useRouter()
const route = useRoute()

const nomeUsuario = computed(() => localStorage.getItem('nome_usuario') || 'Usuario Pandora')
const tipoPerfil = computed(() => localStorage.getItem('tipo_perfil') || 'Acesso por permissoes')
const userInitial = computed(() => nomeUsuario.value.charAt(0).toUpperCase())

const permissions = computed(() => getStoredPermissions())
const hasModulePermission = (prefix) => hasCrudPermission(prefix, permissions.value)

const modules = [
  {
    key: 'grupos',
    label: 'Grupos',
    to: '/dashboard/grupos',
    subtitle: 'Crie grupos e combine as permissoes liberadas para cada equipe.'
  },
  {
    key: 'usuarios',
    label: 'Usuarios',
    to: '/dashboard/usuarios',
    subtitle: 'Cadastre usuarios, vincule setores e controle os grupos de acesso.'
  },
  {
    key: 'setores',
    label: 'Setores',
    to: '/dashboard/setores',
    subtitle: 'Gerencie os setores da empresa conforme as permissoes liberadas.'
  }
]

const navItems = computed(() => modules.filter((module) => hasModulePermission(module.key)))
const currentModule = computed(() => navItems.value.find((item) => item.to === route.path))
const sidebarSubtitle = computed(() => 'Modulos por permissao')
const topbarSubtitle = computed(() => currentModule.value?.subtitle || 'Os CRUDs disponiveis aparecem conforme as permissoes do usuario.')
const pageTitle = computed(() => route.meta.title || 'Dashboard')

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('empresa_id')
  localStorage.removeItem('nome_usuario')
  localStorage.removeItem('tipo_perfil')
  localStorage.removeItem('perfil_id')
  localStorage.removeItem('permissoes')
  localStorage.removeItem('usuario')
  localStorage.removeItem('session_active')

  router.push('/')
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', system-ui, sans-serif;
}

.sidebar {
  width: 280px;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.sidebar-header {
  padding: 2rem;
  z-index: 2;
}

.logo {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.05em;
  margin: 0;
}

.subtitle {
  font-size: 0.85rem;
  color: #bfdbfe;
  margin-top: 0.25rem;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 0 1rem;
  gap: 0.5rem;
  flex: 1;
  z-index: 2;
}

.sidebar-empty {
  flex: 1;
  padding: 0 2rem;
  color: #dbeafe;
  font-size: 0.95rem;
  z-index: 2;
}

.nav-item {
  color: #e2e8f0;
  text-decoration: none;
  padding: 0.9rem 1rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.2s;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 700;
}

.sidebar-footer {
  padding: 1.5rem 2rem 2rem;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-card {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding: 0.9rem 1rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.profile-name {
  font-weight: 700;
}

.profile-role {
  font-size: 0.85rem;
  color: #dbeafe;
}

.btn-logout {
  width: 100%;
  padding: 0.85rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 12px;
  cursor: pointer;
  transition: 0.2s;
  font-weight: 600;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.2);
}

.decor {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  z-index: 1;
}

.decor-1 {
  width: 220px;
  height: 220px;
  bottom: -50px;
  left: -50px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.topbar {
  background: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
}

.topbar h3 {
  margin: 0;
  color: #1e293b;
}

.topbar-subtitle {
  margin: 0.35rem 0 0;
  color: #64748b;
  font-size: 0.95rem;
}

.avatar {
  background: #2563eb;
  color: white;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: 700;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.2);
}

.content-area {
  padding: 2rem;
  flex: 1;
  overflow-y: auto;
}

.empty-dashboard {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
}

.empty-dashboard h4 {
  margin: 0;
  color: #0f172a;
}

.empty-dashboard p {
  margin: 0.5rem 0 0;
  color: #475569;
}

@media (max-width: 900px) {
  .dashboard-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }
}
</style>
