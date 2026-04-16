import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import SolicitarAcesso from '../views/SolicitarAcesso.vue'
import DashboardLayout from '../views/DashboardLayout.vue'

import Setores from '../views/CRUDs/Setores.vue'
import Usuarios from '../views/CRUDs/Usuarios.vue'
import Manuais from '../views/CRUDs/Manuais.vue'
import Equipamentos from '../views/CRUDs/Equipamentos.vue'
import TecnicoChamadosAbertos from '../views/TecnicoChamadosAbertos.vue'
import TecnicoHistoricoManutencoes from '../views/TecnicoHistoricoManutencoes.vue'
import OperadorAbrirChamado from '../views/OperadorAbrirChamado.vue'
import OperadorSituacaoChamado from '../views/OperadorSituacaoChamado.vue'

const PERFIS = {
  gerente: { id: '1', label: 'Gerente' },
  tecnico: { id: '2', label: 'T\u00e9cnico de Manuten\u00e7\u00e3o' },
  operador: { id: '3', label: 'Operador de M\u00e1quinas' }
}

const normalizeText = (value) =>
  String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim()
    .toLowerCase()

const getPerfilKey = () => {
  const perfilId = localStorage.getItem('perfil_id')
  const tipoPerfil = localStorage.getItem('tipo_perfil') || ''
  const normalized = normalizeText(tipoPerfil)

  if (perfilId === PERFIS.gerente.id || normalized === 'gerente') return 'gerente'
  if (perfilId === PERFIS.tecnico.id || normalized === 'tecnico de manutencao') return 'tecnico'
  if (perfilId === PERFIS.operador.id || normalized === 'operador de maquinas') return 'operador'

  return ''
}

const getDashboardHomeByPerfil = () => {
  const perfilKey = getPerfilKey()

  if (perfilKey === 'gerente') return '/dashboard/setores'
  if (perfilKey === 'tecnico') return '/dashboard/chamados-abertos'
  if (perfilKey === 'operador') return '/dashboard/abrir-chamado'

  return '/'
}

const routes = [
  { path: '/', component: Login, meta: { guestOnly: true } },
  { path: '/solicitar-acesso', component: SolicitarAcesso, meta: { guestOnly: true } },
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: () => getDashboardHomeByPerfil() },
      { path: 'setores', component: Setores, meta: { title: 'Setores', allowedPerfis: ['gerente'] } },
      { path: 'usuarios', component: Usuarios, meta: { title: 'Usu\u00e1rios', allowedPerfis: ['gerente'] } },
      { path: 'manuais', component: Manuais, meta: { title: 'Manuais', allowedPerfis: ['gerente'] } },
      { path: 'equipamentos', component: Equipamentos, meta: { title: 'Equipamentos', allowedPerfis: ['gerente'] } },
      { path: 'chamados-abertos', component: TecnicoChamadosAbertos, meta: { title: 'Chamados Abertos', allowedPerfis: ['tecnico'] } },
      { path: 'historico-manutencoes', component: TecnicoHistoricoManutencoes, meta: { title: 'Hist\u00f3rico de Manuten\u00e7\u00f5es', allowedPerfis: ['tecnico'] } },
      { path: 'abrir-chamado', component: OperadorAbrirChamado, meta: { title: 'Abrir Chamado', allowedPerfis: ['operador'] } },
      { path: 'situacao-chamado', component: OperadorSituacaoChamado, meta: { title: 'Situa\u00e7\u00e3o do Chamado', allowedPerfis: ['operador'] } }
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
  const perfilKey = getPerfilKey()
  const isAuthenticated = Boolean(token || sessionActive)

  if (to.meta.requiresAuth && !isAuthenticated) {
    return '/'
  }

  if (to.meta.guestOnly && isAuthenticated) {
    return getDashboardHomeByPerfil()
  }

  const allowedPerfis = to.meta.allowedPerfis
  if (allowedPerfis?.length && !allowedPerfis.includes(perfilKey)) {
    return getDashboardHomeByPerfil()
  }

  return true
})

export default router
