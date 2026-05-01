<template>
  <div class="dashboard-container">
    <!-- Overlay mobile -->
    <div
      v-if="sidebarOpen"
      class="sidebar-overlay"
      @click="sidebarOpen = false"
    />

    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <h2 class="logo">Pandora</h2>
        <p class="subtitle">Manutenção Inteligente</p>
      </div>

      <nav v-if="navItems.length" class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          active-class="active"
          @click="sidebarOpen = false"
        >
          <span class="nav-icon">{{ item.icon }}</span>
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
        <h3>{{ pageTitle }}</h3>
        <div class="user-profile">
          <span
            class="avatar"
            :class="{ open: sidebarOpen }"
            @click="toggleSidebar"
            :title="sidebarOpen ? 'Fechar menu' : 'Abrir menu'"
          >{{ userInitial }}</span>
        </div>
      </header>
      <div class="content-area">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStoredPermissions, hasCrudPermission } from '../utils/permissions'

const route = useRoute()
const router = useRouter()

const nomeUsuario = ref('Usuário')
const tipoPerfil = ref('Perfil')
const sidebarOpen = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
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
    items.push({ to: '/dashboard/grupos', label: 'Grupos', icon: '📁' })
  if (hasCrudPermission('usuarios', permissions)) {
    items.push({ to: '/dashboard/usuarios', label: 'Usuários', icon: '👤' })
    items.push({ to: '/dashboard/equipamentos', label: 'Equipamentos', icon: '⚙️' })
  }
  if (hasCrudPermission('setores', permissions))
    items.push({ to: '/dashboard/setores', label: 'Setores', icon: '🏢' })
  items.push({ to: '/dashboard/abrir-os', label: 'Abrir Chamado', icon: '🛠️' })
  items.push({ to: '/dashboard/gestao-os', label: 'Gestão de OS', icon: '📋' })
  items.push({ to: '/dashboard/analise', label: 'Análise PANDORA', icon: '🤖' })
  return items
})

const pageTitle = computed(() => route.meta.title || 'Painel')
const userInitial = computed(() => nomeUsuario.value.charAt(0).toUpperCase())

const logout = () => {
  localStorage.clear()
  router.push('/')
}
</script>

<style scoped>
/* ── Base ─────────────────────────────────────────── */
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', system-ui, sans-serif;
}

/* ── Overlay (mobile) ─────────────────────────────── */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 99;
  backdrop-filter: blur(2px);
}

/* ── Sidebar ──────────────────────────────────────── */
.sidebar {
  width: 280px;
  flex-shrink: 0;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s cubic-bezier(.4, 0, .2, 1);
  z-index: 100;
}
.sidebar-header { padding: 2rem; z-index: 2; }
.logo { font-size: 2rem; font-weight: 800; letter-spacing: -0.05em; margin: 0; }
.subtitle { font-size: 0.85rem; color: #bfdbfe; margin-top: 0.25rem; }
.sidebar-nav { display: flex; flex-direction: column; padding: 0 1rem; gap: 0.5rem; flex: 1; z-index: 2; }
.nav-item {
  display: flex; align-items: center; gap: 10px;
  color: #e2e8f0; text-decoration: none;
  padding: 0.9rem 1rem; border-radius: 12px;
  font-weight: 600; transition: all 0.2s;
}
.nav-item:hover { background: rgba(255, 255, 255, 0.1); color: white; }
.nav-item.active { background: rgba(255, 255, 255, 0.2); color: white; font-weight: 700; }
.sidebar-footer { padding: 1.5rem 2rem 2rem; z-index: 2; display: flex; flex-direction: column; gap: 1rem; }
.profile-card {
  display: flex; flex-direction: column; gap: 0.2rem;
  padding: 0.9rem 1rem; border-radius: 14px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
}
.profile-name { font-weight: 700; font-size: 0.95rem; }
.profile-role { font-size: 0.75rem; color: #bfdbfe; }
.btn-logout {
  width: 100%; padding: 0.85rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white; border-radius: 12px; cursor: pointer; font-weight: 600;
}
.btn-logout:hover { background: rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.3); }
.decor { position: absolute; border-radius: 50%; background: white; opacity: 0.05; pointer-events: none; }
.decor-1 { width: 300px; height: 300px; top: -100px; right: -150px; }

/* ── Main ─────────────────────────────────────────── */
.main-content { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.topbar {
  background: white; padding: 1.5rem 2rem;
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid #e2e8f0;
}
.topbar h3 { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.avatar {
  background: #2563eb; color: white;
  width: 42px; height: 42px; min-width: 42px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%; font-weight: 700;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.2);
  transition: transform 0.15s, box-shadow 0.15s;
}
.content-area { padding: 2rem; flex: 1; overflow-y: auto; }

/* ── Mobile ≤ 768px ───────────────────────────────── */
@media (max-width: 768px) {
  .sidebar-overlay { display: block; }

  .sidebar {
    position: fixed;
    top: 0; left: 0; bottom: 0;
    transform: translateX(-100%);
  }
  .sidebar.open { transform: translateX(0); }

  .topbar { padding: 1rem 1.2rem; }
  .content-area { padding: 1.2rem; }

  /* Avatar vira botão de menu no mobile */
  .avatar {
    cursor: pointer;
  }
  .avatar:hover { transform: scale(1.08); box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35); }
  .avatar.open { background: #1e3a8a; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3); }
}
</style>