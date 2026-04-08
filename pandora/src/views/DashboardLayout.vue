<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="logo">Pandora</h2>
        <p class="subtitle">{{ sidebarSubtitle }}</p>
      </div>

      <nav class="sidebar-nav">
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
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const tipoPerfil = computed(() => localStorage.getItem('tipo_perfil') || 'Usu\u00e1rio')
const perfilId = computed(() => localStorage.getItem('perfil_id') || '')
const normalizeText = (value) => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim().toLowerCase()
const perfilKey = computed(() => {
  const normalized = normalizeText(tipoPerfil.value)
  if (perfilId.value === '1' || normalized === 'gerente') return 'gerente'
  if (perfilId.value === '2' || normalized === 'tecnico de manutencao') return 'tecnico'
  if (perfilId.value === '3' || normalized === 'operador de maquinas') return 'operador'
  return ''
})
const nomeUsuario = computed(() => localStorage.getItem('nome_usuario') || 'Usu\u00e1rio Pandora')
const userInitial = computed(() => nomeUsuario.value.charAt(0).toUpperCase())

const navByPerfil = {
  gerente: [
    { label: 'Setores', to: '/dashboard/setores' },
    { label: 'Usu\u00e1rios', to: '/dashboard/usuarios' },
    { label: 'Manuais', to: '/dashboard/manuais' },
    { label: 'Equipamentos', to: '/dashboard/equipamentos' }
  ],
  tecnico: [
    { label: 'Chamados Abertos', to: '/dashboard/chamados-abertos' },
    { label: 'Hist\u00f3rico de Manuten\u00e7\u00f5es', to: '/dashboard/historico-manutencoes' }
  ],
  operador: [
    { label: 'Abrir Chamado', to: '/dashboard/abrir-chamado' },
    { label: 'Situa\u00e7\u00e3o do Chamado', to: '/dashboard/situacao-chamado' }
  ]
}

const subtitleByPerfil = {
  gerente: 'Painel de Gest\u00e3o',
  tecnico: 'Painel T\u00e9cnico',
  operador: 'Painel Operacional'
}

const topbarByPerfil = {
  gerente: 'Gerencie cadastros, ativos e acessos da opera\u00e7\u00e3o.',
  tecnico: 'Acompanhe chamados e o hist\u00f3rico das interven\u00e7\u00f5es.',
  operador: 'Abra chamados e acompanhe o andamento das solicita\u00e7\u00f5es.'
}

const navItems = computed(() => navByPerfil[perfilKey.value] || [])
const sidebarSubtitle = computed(() => subtitleByPerfil[perfilKey.value] || 'Painel do Sistema')
const topbarSubtitle = computed(() => topbarByPerfil[perfilKey.value] || 'Acompanhe as informa\u00e7\u00f5es da sua \u00e1rea.')
const pageTitle = computed(() => route.meta.title || 'Vis\u00e3o Geral')

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('empresa_id')
  localStorage.removeItem('nome_usuario')
  localStorage.removeItem('tipo_perfil')
  localStorage.removeItem('perfil_id')
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

@media (max-width: 900px) {
  .dashboard-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }
}
</style>
