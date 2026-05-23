import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import SolicitarAcesso from '../views/SolicitarAcesso.vue'
import DashboardLayout from '../views/Dashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

import Grupos from '../views/CRUDs/Grupos.vue'
import Setores from '../views/CRUDs/Setores.vue'
import Usuarios from '../views/CRUDs/Usuarios.vue'
import AnaliseIA from '../views/AnaliseIA.vue'
import OperadorAbrirChamado from '../views/OperadorAbrirChamado.vue'
import Equipamentos from '../views/Equipamentos.vue'
import GestaoOrdensServico from '../views/GestaoOrdensServico.vue'
import TecnicoHistoricoManutencoes from '../views/TecnicoHistoricoManutencoes.vue'
import { getStoredPermissions, hasCrudPermission, hasPermission } from '../utils/permissions'

const getDashboardHome = () => {
  const permissions = getStoredPermissions()
  if (hasCrudPermission('grupos', permissions)) return '/dashboard/grupos'
  if (hasCrudPermission('usuarios', permissions)) return '/dashboard/usuarios'
  if (hasCrudPermission('equipamentos', permissions)) return '/dashboard/equipamentos'
  if (hasCrudPermission('setores', permissions)) return '/dashboard/setores'
  if (hasPermission('ordens_servico.criar', permissions)) return '/dashboard/abrir-os'
  if (hasPermission('ordens_servico.visualizar', permissions)) return '/dashboard/gestao-os'
  return '/dashboard/analise'
}

const routes = [
  { path: '/', component: Login, meta: { guestOnly: true } },

  // ── Rotas do superusuário (admin do sistema) ──────────────────
  {
    path: '/admin',
    redirect: '/admin/dashboard',
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
  },

  // ── Rotas públicas ────────────────────────────────────────────
  { path: '/solicitar-acesso', component: SolicitarAcesso, meta: { guestOnly: true } },

  // ── Dashboard dos usuários das empresas ───────────────────────
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { path: 'grupos',       component: Grupos,                      meta: { title: 'Grupos',           permissionPrefix: 'grupos' } },
      { path: 'usuarios',     component: Usuarios,                    meta: { title: 'Usuários',         permissionPrefix: 'usuarios' } },
      { path: 'setores',      component: Setores,                     meta: { title: 'Setores',          permissionPrefix: 'setores' } },
      { path: 'analise',      component: AnaliseIA,                   meta: { title: 'Análise Técnica' } },
      { path: 'abrir-os',     component: OperadorAbrirChamado,        meta: { title: 'Abrir Chamado',    permissionName: 'ordens_servico.criar' } },
      { path: 'equipamentos', component: Equipamentos,                meta: { title: 'Equipamentos',     permissionPrefix: 'equipamentos' } },
      { path: 'historico-os', component: TecnicoHistoricoManutencoes, meta: { title: 'Historico de OS',  permissionName: 'ordens_servico.visualizar' } },
      { path: 'gestao-os',    name: 'GestaoOS', component: GestaoOrdensServico, meta: { title: 'Ordens de Serviço', permissionName: 'ordens_servico.visualizar' } },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  const sessionActive = localStorage.getItem('session_active') === 'true'
  const isAuthenticated = Boolean(token || sessionActive)
  const isSuperuser = localStorage.getItem('is_superuser') === 'true'
  const dashboardHome = getDashboardHome()

  // Redireciona para login se precisar de auth e não estiver autenticado
  if (to.meta.requiresAuth && !isAuthenticated) {
    return { path: '/', query: { redirect: to.fullPath } }
  }

  // Usuário já logado tentando acessar página de guest (ex: tela de login)
  if (to.meta.guestOnly && isAuthenticated) {
    if (isSuperuser) return '/admin/dashboard'
    return typeof to.query.redirect === 'string' ? to.query.redirect : dashboardHome
  }

  // /dashboard sem sub-rota redireciona para a home correta
  if (to.path === '/dashboard' && dashboardHome !== '/dashboard') return dashboardHome

  // Guarda de permissões para rotas do dashboard
  const permissions = getStoredPermissions()
  if (to.meta.permissionPrefix && !hasCrudPermission(to.meta.permissionPrefix, permissions)) return dashboardHome
  if (to.meta.permissionName  && !hasPermission(to.meta.permissionName, permissions))       return dashboardHome

  return true
})

export default router