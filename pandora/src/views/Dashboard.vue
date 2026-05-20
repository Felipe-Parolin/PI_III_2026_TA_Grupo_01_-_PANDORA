<template>
  <div class="dashboard-container">
    <div
      v-if="sidebarOpen"
      class="sidebar-overlay"
      @click="sidebarOpen = false"
    />

    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <section class="sidebar-header">
        <div class="brand-mark">P</div>
        <div>
          <h1 class="logo">Pandora</h1>
          <p class="subtitle">Gestão de Manutenção</p>
        </div>
      </section>

      <nav v-if="navItems.length" class="sidebar-nav" aria-label="Menu principal">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          active-class="active"
          @click="sidebarOpen = false"
        >
          <span class="nav-icon">
            <AppIcon :name="item.icon" :size="18" />
          </span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <div class="topbar-left">
          <button
            type="button"
            class="menu-button"
            :title="sidebarOpen ? 'Fechar menu' : 'Abrir menu'"
            @click="toggleSidebar"
          >
            <AppIcon name="menu" :size="20" />
          </button>

          <div class="topbar-copy">
            <span class="section-label">Painel</span>
            <h2>{{ pageTitle }}</h2>
          </div>
        </div>

        <section class="topbar-profile" aria-label="Perfil do usuário">
          <div class="profile-summary">
            <span class="avatar">{{ userInitial }}</span>
            <div class="profile-copy">
              <span class="profile-name">{{ nomeUsuario }}</span>
              <span class="profile-role">{{ tipoPerfil }}</span>
            </div>
          </div>

          <div class="profile-actions">
            <button
              type="button"
              class="profile-action"
              title="Trocar senha"
              @click="openPasswordModal"
            >
              <AppIcon name="key" :size="18" />
              <span>Trocar senha</span>
            </button>
            <button
              type="button"
              class="profile-action danger"
              title="Sair"
              @click="logout"
            >
              <AppIcon name="log-out" :size="18" />
              <span>Sair</span>
            </button>
          </div>
        </section>
      </header>

      <section class="content-area">
        <router-view></router-view>
      </section>
    </main>

    <TrocarSenhaModal v-if="showChangePassword" @close="showChangePassword = false" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppIcon from '../components/AppIcon.vue'
import TrocarSenhaModal from '../components/TrocarSenhaModal.vue'
import { getStoredPermissions, hasCrudPermission, hasPermission } from '../utils/permissions'

const route = useRoute()
const router = useRouter()

const nomeUsuario = ref('Usuário')
const tipoPerfil = ref('Colaborador')
const sidebarOpen = ref(false)
const showChangePassword = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const openPasswordModal = () => {
  sidebarOpen.value = false
  showChangePassword.value = true
}

onMounted(() => {
  const nomeSalvo = localStorage.getItem('nome_usuario')
  const perfilSalvo = localStorage.getItem('tipo_perfil')
  if (nomeSalvo) nomeUsuario.value = nomeSalvo
  if (perfilSalvo) tipoPerfil.value = perfilSalvo
})

const navItems = computed(() => {
  const permissions = getStoredPermissions()
  const items = []

  if (hasCrudPermission('grupos', permissions))
    items.push({ to: '/dashboard/grupos', label: 'Grupos', icon: 'layers' })
  if (hasCrudPermission('usuarios', permissions))
    items.push({ to: '/dashboard/usuarios', label: 'Usuários', icon: 'users' })
  if (hasCrudPermission('equipamentos', permissions))
    items.push({ to: '/dashboard/equipamentos', label: 'Equipamentos', icon: 'wrench' })
  if (hasCrudPermission('setores', permissions))
    items.push({ to: '/dashboard/setores', label: 'Setores', icon: 'building' })
  if (hasPermission('ordens_servico.criar', permissions))
    items.push({ to: '/dashboard/abrir-os', label: 'Abrir Chamado', icon: 'clipboard' })
  if (hasPermission('ordens_servico.visualizar', permissions))
    items.push({ to: '/dashboard/gestao-os', label: 'Ordens de Serviço', icon: 'clipboard' })
  if (hasPermission('ordens_servico.visualizar', permissions))
    items.push({ to: '/dashboard/historico-os', label: 'Histórico de OS', icon: 'clipboard' })

  items.push({ to: '/dashboard/analise', label: 'Análise Técnica', icon: 'sparkles' })
  return items
})

const pageTitle = computed(() => route.meta.title || 'Painel')
const userInitial = computed(() => nomeUsuario.value.trim().charAt(0).toUpperCase() || 'U')

const logout = () => {
  localStorage.clear()
  router.push('/')
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
  color: #0f172a;
  font-family: 'Inter', system-ui, sans-serif;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 90;
  background: rgba(15, 23, 42, 0.46);
  backdrop-filter: blur(2px);
}

.sidebar {
  width: 280px;
  flex: 0 0 280px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 1.25rem 1rem;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  color: #ffffff;
  box-shadow: 12px 0 32px rgba(30, 58, 138, 0.16);
  transition: transform 0.28s ease;
  z-index: 100;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.5rem 0.65rem 1.25rem;
}

.brand-mark {
  width: 42px;
  height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.24);
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 900;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.14);
}

.logo {
  margin: 0;
  color: #ffffff;
  font-size: 1.75rem;
  line-height: 1;
  font-weight: 900;
  letter-spacing: 0;
}

.subtitle {
  margin: 0.28rem 0 0;
  color: #bfdbfe;
  font-size: 0.82rem;
  font-weight: 700;
}

.sidebar-nav {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 0.45rem;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-height: 46px;
  padding: 0.72rem 0.78rem;
  border: 1px solid transparent;
  border-radius: 8px;
  color: #e2e8f0;
  text-decoration: none;
  font-size: 0.94rem;
  font-weight: 800;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.14);
  color: #ffffff;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.22);
  color: #ffffff;
}

.nav-icon {
  width: 34px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.13);
  border: 1px solid rgba(255, 255, 255, 0.16);
  color: #dbeafe;
}

.nav-item.active .nav-icon {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.nav-label {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.main-content {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  min-height: 78px;
  padding: 1rem 1.75rem;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  min-width: 0;
}

.topbar-copy {
  min-width: 0;
}

.section-label {
  display: block;
  margin-bottom: 0.12rem;
  color: #2563eb;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.topbar h2 {
  margin: 0;
  overflow: hidden;
  color: #0f172a;
  font-size: 1.2rem;
  line-height: 1.25;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.menu-button {
  display: none;
  width: 42px;
  height: 42px;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #ffffff;
  color: #1e293b;
  cursor: pointer;
}

.topbar-profile {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.85rem;
  min-width: 0;
}

.profile-summary {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  min-width: 0;
}

.avatar {
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  border-radius: 50%;
  background: #2563eb;
  color: #ffffff;
  font-weight: 900;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.2);
}

.profile-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.profile-name {
  max-width: 190px;
  overflow: hidden;
  color: #0f172a;
  font-size: 0.92rem;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-role {
  color: #64748b;
  font-size: 0.75rem;
  font-weight: 700;
}

.profile-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.profile-action {
  min-height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0.58rem 0.78rem;
  border: 1px solid #dbeafe;
  border-radius: 8px;
  background: #f8fbff;
  color: #1d4ed8;
  cursor: pointer;
  font-size: 0.86rem;
  font-weight: 800;
  white-space: nowrap;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s;
}

.profile-action:hover {
  background: #eff6ff;
  border-color: #bfdbfe;
  color: #1e40af;
}

.profile-action.danger {
  border-color: #fee2e2;
  background: #fff7f7;
  color: #b91c1c;
}

.profile-action.danger:hover {
  background: #fee2e2;
  border-color: #fecaca;
  color: #991b1b;
}

.content-area {
  flex: 1;
  min-width: 0;
  padding: 2rem;
  overflow-y: auto;
}

@media (max-width: 980px) {
  .sidebar-overlay {
    display: block;
  }

  .sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    transform: translateX(-100%);
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .menu-button {
    display: inline-flex;
  }
}

@media (max-width: 760px) {
  .topbar {
    align-items: flex-start;
    min-height: auto;
    padding: 1rem;
  }

  .topbar-profile {
    flex-direction: column;
    align-items: flex-end;
    gap: 0.55rem;
  }

  .profile-copy {
    display: none;
  }

  .profile-action span {
    display: none;
  }

  .profile-action {
    width: 38px;
    padding: 0;
  }

  .content-area {
    padding: 1.2rem;
  }
}

@media (max-width: 520px) {
  .topbar {
    gap: 0.65rem;
  }

  .topbar h2 {
    max-width: 150px;
  }
}
</style>
