import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import SolicitarAcesso from '../views/SolicitarAcesso.vue'
import DashboardLayout from '../views/Dashboard.vue'

import Grupos from '../views/CRUDs/Grupos.vue'
import Setores from '../views/CRUDs/Setores.vue'
import Usuarios from '../views/CRUDs/Usuarios.vue'
import AnaliseIA from '../views/AnaliseIA.vue'
import OperadorAbrirChamado from '../views/OperadorAbrirChamado.vue'
import Equipamentos from '../views/Equipamentos.vue'
import GestaoOrdensServico from '../views/GestaoOrdensServico.vue' // Importação correta
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
  { path: '/solicitar-acesso', component: SolicitarAcesso, meta: { guestOnly: true } },
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { path: 'grupos', component: Grupos, meta: { title: 'Grupos', permissionPrefix: 'grupos' } },
      { path: 'usuarios', component: Usuarios, meta: { title: 'Usuários', permissionPrefix: 'usuarios' } },
      { path: 'setores', component: Setores, meta: { title: 'Setores', permissionPrefix: 'setores' } },
      { path: 'analise', component: AnaliseIA, meta: { title: 'Análise Técnica' } },
      { path: 'abrir-os', component: OperadorAbrirChamado, meta: { title: 'Abrir Chamado', permissionName: 'ordens_servico.criar' } },
      { path: 'equipamentos', component: Equipamentos, meta: { title: 'Equipamentos', permissionPrefix: 'equipamentos' } },
      
      // AJUSTE AQUI: Removi a barra inicial do path para ser relativo ao /dashboard
      { path: 'gestao-os', name: 'GestaoOS', component: GestaoOrdensServico, meta: { title: 'Ordens de Serviço', permissionName: 'ordens_servico.visualizar' } }
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
  const dashboardHome = getDashboardHome()

  if (to.meta.requiresAuth && !isAuthenticated) {
    return { path: '/', query: { redirect: to.fullPath } }
  }
  if (to.meta.guestOnly && isAuthenticated) {
    return typeof to.query.redirect === 'string' ? to.query.redirect : dashboardHome
  }
  if (to.path === '/dashboard' && dashboardHome !== '/dashboard') return dashboardHome
  
  const permissions = getStoredPermissions()
  if (to.meta.permissionPrefix && !hasCrudPermission(to.meta.permissionPrefix, permissions)) return dashboardHome
  if (to.meta.permissionName && !hasPermission(to.meta.permissionName, permissions)) return dashboardHome

  return true
})

export default router
