<template>
  <div class="crud-page">
    <section class="page-header">
      <div>
        <p class="eyebrow">Historico de OS</p>
        <h2>Historico de Ordens de Servico</h2>
        <p class="page-copy">Consulte somente ordens de servico concluidas e veja as movimentacoes completas ao abrir uma OS.</p>
      </div>
    </section>

    <section class="card filter-card">
      <div class="card-header">
        <h3>Filtros</h3>
        <p>Refine as ordens concluidas por numero da OS, comentario do tecnico ou data de fechamento.</p>
      </div>
      <div class="input-row">
        <div class="input-group">
          <label>ID da Ordem de Servico</label>
          <input v-model="filtros.os_id" type="number" placeholder="Ex: 23" />
        </div>
        <div class="input-group">
          <label>Comentario do Tecnico</label>
          <input v-model="filtros.comentario" type="text" placeholder="Ex: troca de sensor" />
        </div>
        <div class="input-group">
          <label>Data Inicial</label>
          <input v-model="filtros.data_inicio" type="date" />
        </div>
        <div class="input-group">
          <label>Data Final</label>
          <input v-model="filtros.data_fim" type="date" />
        </div>
      </div>
      <div class="form-actions" style="margin-top: 1rem;">
        <button @click="aplicarFiltros" class="btn btn-primary">Filtrar</button>
        <button @click="limparFiltros" class="btn btn-secondary">Limpar</button>
      </div>
    </section>

    <section class="card table-card">
      <div class="card-header">
        <h3>Ordens Concluidas</h3>
        <p>{{ historicoAplicado.length }} ordem(ns) concluida(s) encontrada(s).</p>
      </div>

      <div v-if="carregando" class="empty-state">Carregando...</div>

      <div v-else class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID OS</th>
              <th>Comentario do Tecnico</th>
              <th>Usuario Abertura</th>
              <th>Tecnico Fechamento</th>
              <th>Data Fechamento</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!historicoFiltrado.length">
              <td colspan="5" class="empty-state">Nenhuma ordem concluida encontrada.</td>
            </tr>
            <tr
              v-for="item in historicoFiltrado"
              :key="item.os_id ?? item.os"
              @click="abrirModal(item)"
            >
              <td><span class="os-badge">#{{ item.os_id ?? item.os }}</span></td>
              <td>{{ truncate(getComentarioTecnico(item), 90) }}</td>
              <td>{{ getUsuarioAbertura(item) }}</td>
              <td>{{ getTecnicoFechamento(item) }}</td>
              <td>{{ formatarData(item.os_data_fechamento || item.data_modificacao) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination" v-if="totalPaginas > 1">
        <button class="btn btn-secondary pag-btn" :disabled="paginaAtual === 1" @click="paginaAtual--">Anterior</button>
        <span class="pag-info">Pagina {{ paginaAtual }} de {{ totalPaginas }}</span>
        <button class="btn btn-secondary pag-btn" :disabled="paginaAtual === totalPaginas" @click="paginaAtual++">Proxima</button>
      </div>
    </section>

    <div class="modal-overlay" v-if="itemSelecionado" @click.self="fecharModal">
      <div class="modal-box">
        <div class="modal-header">
          <h3>Historico da OS #{{ itemSelecionado.os_id ?? itemSelecionado.os }}</h3>
          <button class="btn-close" @click="fecharModal">x</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">ID OS</span>
            <span class="detail-value os-badge">#{{ itemSelecionado.os_id ?? itemSelecionado.os }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Comentario do Tecnico</span>
            <span class="detail-value">{{ getComentarioTecnico(itemSelecionado) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Usuario Abertura</span>
            <span class="detail-value">{{ getUsuarioAbertura(itemSelecionado) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Tecnico Fechamento</span>
            <span class="detail-value">{{ getTecnicoFechamento(itemSelecionado) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Data Fechamento</span>
            <span class="detail-value">{{ formatarData(itemSelecionado.os_data_fechamento || itemSelecionado.data_modificacao) }}</span>
          </div>
          <div class="movements-block">
            <h4>Movimentacoes da OS</h4>
            <div class="table-wrap mini-table-wrap">
              <table class="data-table movements-table">
                <thead>
                  <tr>
                    <th>Data</th>
                    <th>Usuario</th>
                    <th>Movimentacao</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="movimento in getMovimentacoesOs(itemSelecionado)" :key="movimento.id">
                    <td>{{ formatarData(movimento.data_modificacao) }}</td>
                    <td>{{ movimento.usuario_nome || 'Nao informado' }}</td>
                    <td>{{ getDescricaoMovimentacao(movimento) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'

const historico = ref([])
const historicoCompleto = ref([])
const historicoAplicado = ref([])
const itemSelecionado = ref(null)
const carregando = ref(true)

const filtros = ref({ os_id: '', comentario: '', data_inicio: '', data_fim: '' })
const ITENS_POR_PAGINA = 15
const paginaAtual = ref(1)

const totalPaginas = computed(() =>
  Math.max(1, Math.ceil(historicoAplicado.value.length / ITENS_POR_PAGINA))
)

const historicoFiltrado = computed(() => {
  const inicio = (paginaAtual.value - 1) * ITENS_POR_PAGINA
  return historicoAplicado.value.slice(inicio, inicio + ITENS_POR_PAGINA)
})

const getOsId = (item) => item?.os_id ?? item?.os

const getComentarioTecnico = (item) => {
  if (item?.os_comentario_tecnico) return item.os_comentario_tecnico

  if (item?.campo_alterado === 'descricao_solucao' && item?.valor_novo) {
    return item.valor_novo
  }

  return 'Sem comentario final do tecnico'
}

const isConcluida = (item) => {
  const status = String(item?.os_status || item?.valor_novo || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()

  return status === 'concluido' || status === 'concluida'
}

const consolidarPorOrdemServico = (registros) => {
  const porOs = new Map()

  registros.forEach((registro) => {
    const osId = getOsId(registro)
    if (!osId) return

    const atual = porOs.get(osId)
    const dataRegistro = new Date(registro.data_modificacao || 0)
    const dataAtual = atual ? new Date(atual.data_modificacao || 0) : null

    if (!atual || dataRegistro > dataAtual) {
      porOs.set(osId, { ...registro })
      return
    }

    if (!atual.os_comentario_tecnico && registro.campo_alterado === 'descricao_solucao') {
      porOs.set(osId, {
        ...atual,
        os_comentario_tecnico: registro.valor_novo
      })
    }
  })

  return Array.from(porOs.values()).filter(isConcluida).sort(
    (a, b) => new Date(b.data_modificacao || 0) - new Date(a.data_modificacao || 0)
  )
}

const aplicarFiltros = () => {
  paginaAtual.value = 1
  let resultado = [...historico.value]

  if (filtros.value.os_id) {
    resultado = resultado.filter((h) => String(getOsId(h)) === String(filtros.value.os_id))
  }

  if (filtros.value.comentario) {
    const busca = filtros.value.comentario.toLowerCase()
    resultado = resultado.filter((h) => getComentarioTecnico(h).toLowerCase().includes(busca))
  }

  if (filtros.value.data_inicio) {
    resultado = resultado.filter((h) => new Date(h.os_data_fechamento || h.data_modificacao) >= new Date(filtros.value.data_inicio))
  }

  if (filtros.value.data_fim) {
    const df = new Date(filtros.value.data_fim)
    df.setHours(23, 59, 59, 999)
    resultado = resultado.filter((h) => new Date(h.os_data_fechamento || h.data_modificacao) <= df)
  }

  historicoAplicado.value = resultado
}

const limparFiltros = () => {
  filtros.value = { os_id: '', comentario: '', data_inicio: '', data_fim: '' }
  historicoAplicado.value = [...historico.value]
  paginaAtual.value = 1
}

const abrirModal = (item) => { itemSelecionado.value = item }
const fecharModal = () => { itemSelecionado.value = null }

const formatarData = (iso) => {
  if (!iso) return '-'
  return new Date(iso).toLocaleString('pt-BR', {
    timeZone: 'America/Sao_Paulo',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const nomesCampos = {
  status: 'Status',
  urgencia: 'Urgencia',
  descricao_problema: 'Descricao do problema',
  descricao_solucao: 'Comentario do tecnico',
  usuario_tecnico_id: 'Tecnico responsavel',
  data_fechamento: 'Data de fechamento'
}

const formatarValorHistorico = (valor) => {
  if (valor === null || valor === undefined || valor === '') return 'nao informado'
  return String(valor)
}

const getDescricaoMovimentacao = (item) => {
  const campo = item?.campo_alterado || 'registro'
  const nomeCampo = nomesCampos[campo] || campo.replaceAll('_', ' ')
  const anterior = formatarValorHistorico(item?.valor_anterior)
  const novo = formatarValorHistorico(item?.valor_novo)

  if (campo === 'status' && !item?.valor_anterior && item?.valor_novo === 'Aberto') {
    return 'OS aberta'
  }

  if (campo === 'descricao_solucao') {
    return 'Comentario do tecnico registrado'
  }

  if (campo === 'data_fechamento') {
    return `Data de fechamento definida como ${formatarData(item?.valor_novo)}`
  }

  if (campo === 'usuario_tecnico_id') {
    const tecnico = item?.usuario_tecnico_nome || item?.usuario_nome || 'Tecnico'
    return `${tecnico} assumiu o chamado`
  }

  if (!item?.valor_anterior && item?.valor_novo) {
    return `${nomeCampo} definido como ${novo}`
  }

  if (item?.valor_anterior && !item?.valor_novo) {
    return `${nomeCampo} removido`
  }

  return `${nomeCampo} alterado de ${anterior} para ${novo}`
}

const getMovimentacoesOs = (item) => {
  const osId = getOsId(item)
  return historicoCompleto.value
    .filter((movimento) => String(getOsId(movimento)) === String(osId))
    .sort((a, b) => new Date(a.data_modificacao || 0) - new Date(b.data_modificacao || 0))
}

const getUsuarioAbertura = (item) =>
  item?.usuario_abertura_nome || item?.usuario_abertura || 'Nao informado'

const getTecnicoFechamento = (item) =>
  item?.usuario_tecnico_nome || item?.usuario_tecnico || 'Nao fechado'

const truncate = (val, max = 40) => {
  if (!val) return '-'
  return val.length > max ? val.slice(0, max) + '...' : val
}

onMounted(async () => {
  try {
    const data = await api.getAll('historicos-os')
    historicoCompleto.value = data
    const chamados = consolidarPorOrdemServico(data)
    historico.value = chamados
    historicoAplicado.value = [...chamados]
  } catch (e) {
    console.error('Erro ao carregar historico:', e)
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.crud-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; border-radius: 20px; padding: 1.5rem 1.75rem; }
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.page-header h2, .card-header h3 { margin: 0; color: #0f172a; }
.page-copy, .card-header p { margin: 0.4rem 0 0; color: #475569; }
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.filter-card, .table-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.input-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input { box-sizing: border-box; width: 100%; padding: 0.9rem 1rem; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; color: #0f172a; transition: border-color 0.2s, box-shadow 0.2s; }
.input-group input:focus { outline: none; background: #ffffff; border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14); }
.form-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.btn { border: none; border-radius: 12px; padding: 0.8rem 1.15rem; font-weight: 600; cursor: pointer; transition: transform 0.15s, box-shadow 0.2s; }
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: #2563eb; color: #ffffff; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24); }
.btn-secondary { background: #e2e8f0; color: #1e293b; }
.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
.data-table th { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; }
.data-table tr:hover td { background: #f8fafc; cursor: pointer; }
.empty-state { text-align: center; color: #64748b; padding: 1.5rem 1rem; }
.os-badge { display: inline-flex; align-items: center; padding: 0.3rem 0.7rem; border-radius: 999px; background: #dbeafe; color: #1d4ed8; font-weight: 700; font-size: 0.82rem; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; }
.pag-btn { padding: 0.6rem 1rem; }
.pag-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
.pag-info { font-size: 0.88rem; color: #64748b; font-weight: 600; }
.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.45); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal-box { background: #ffffff; border-radius: 20px; padding: 2rem; width: 100%; max-width: 920px; max-height: 88vh; overflow-y: auto; box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18); }
.modal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
.modal-header h3 { margin: 0; color: #0f172a; }
.btn-close { background: #f1f5f9; border: none; border-radius: 10px; padding: 0.5rem 0.8rem; font-size: 1rem; cursor: pointer; color: #475569; }
.btn-close:hover { background: #e2e8f0; }
.modal-body { display: flex; flex-direction: column; gap: 0.85rem; }
.detail-row { display: flex; align-items: flex-start; gap: 1rem; padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9; }
.detail-row:last-child { border-bottom: none; }
.detail-label { min-width: 130px; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #64748b; padding-top: 0.1rem; }
.detail-value { color: #0f172a; font-size: 0.92rem; word-break: break-word; }
.movements-block { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; }
.movements-block h4 { margin: 0 0 0.75rem; color: #0f172a; }
.mini-table-wrap { border: 1px solid #e2e8f0; border-radius: 12px; }
.movements-table th, .movements-table td { padding: 0.8rem; vertical-align: top; }
@media (max-width: 768px) {
  .filter-card, .table-card { padding: 1.2rem; }
  .input-row { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column; }
  .btn { width: 100%; }
  .modal-box { margin: 1rem; padding: 1.5rem; }
}
</style>
