import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import SolicitarAcesso from '../views/SolicitarAcesso.vue'
import DashboardLayout from '../views/Dashboard.vue'

import Grupos from '../views/CRUDs/Grupos.vue'
import Setores from '../views/CRUDs/Setores.vue'
import Usuarios from '../views/CRUDs/Usuarios.vue'
import { getStoredPermissions, hasCrudPermission } from '../utils/permissions'

const getDashboardHome = () => {
  const permissions = getStoredPermissions()
  if (hasCrudPermission('grupos', permissions)) return '/dashboard/grupos'
  if (hasCrudPermission('usuarios', permissions)) return '/dashboard/usuarios'
  if (hasCrudPermission('setores', permissions)) return '/dashboard/setores'
  return '/dashboard'
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
      { path: 'usuarios', component: Usuarios, meta: { title: 'Usuarios', permissionPrefix: 'usuarios' } },
      { path: 'setores', component: Setores, meta: { title: 'Setores', permissionPrefix: 'setores' } }
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
    return '/'
  }

  if (to.meta.guestOnly && isAuthenticated) {
    return dashboardHome
  }

  if (to.path === '/dashboard' && dashboardHome !== '/dashboard') {
    return dashboardHome
  }

  if (to.meta.permissionPrefix && !hasCrudPermission(to.meta.permissionPrefix)) {
    return dashboardHome
  }

  return true
})

export default router
