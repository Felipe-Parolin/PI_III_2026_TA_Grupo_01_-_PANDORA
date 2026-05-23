<template>
  <div class="crud-page">
    <section class="page-header">
      <p class="eyebrow">Técnico de Manutenção</p>
      <h2>Chamados Abertos</h2>
      <p class="page-copy">Veja rapidamente o que precisa de atendimento e priorize sua próxima intervenção.</p>
    </section>

    <section class="card table-card">
      <div class="card-header">
        <h3>Métricas rápidas</h3>
        <p>Visão geral da fila de atendimento atual.</p>
      </div>
      <div class="metrics-row">
        <div class="metric-item">
          <span class="metric-value">06</span>
          <span class="metric-label">Chamados urgentes</span>
        </div>
        <div class="metric-item">
          <span class="metric-value">14</span>
          <span class="metric-label">Em andamento</span>
        </div>
        <div class="metric-item">
          <span class="metric-value">03</span>
          <span class="metric-label">Aguardando peças</span>
        </div>
      </div>
    </section>

    <section class="card table-card">
      <div class="card-header">
        <h3>Fila de atendimento</h3>
        <p>Gere uma análise técnica preliminar dos problemas relatados.</p>
      </div>

      <div class="ticket-list">
        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1024 · Prensa Hidráulica 02</strong>
            <p>Parada intermitente durante o ciclo de produção.</p>
            <button @click="solicitarAnaliseIA('Parada intermitente durante o ciclo de produção na Prensa Hidráulica 02')" class="btn-ia">
              Gerar análise técnica
            </button>
          </div>
          <span class="status-badge critico">Crítico</span>
        </article>

        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1021 · Esteira de Embalagem</strong>
            <p>Ruído incomum reportado pelo operador do turno B.</p>
            <button @click="solicitarAnaliseIA('Ruído incomum na Esteira de Embalagem reportado pelo operador')" class="btn-ia">
              Gerar análise técnica
            </button>
          </div>
          <span class="status-badge medio">Médio</span>
        </article>

        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1018 · Compressor Central</strong>
            <p>Verificação preventiva pendente após oscilação de pressão.</p>
            <button @click="solicitarAnaliseIA('Verificação preventiva no Compressor Central após oscilação de pressão')" class="btn-ia">
              Gerar análise técnica
            </button>
          </div>
          <span class="status-badge planejado">Planejado</span>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
const solicitarAnaliseIA = async (descricaoChamado) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/analises-llm/analisar/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ descricao: descricaoChamado })
    })
    const analise = await response.json()
    if (analise.error) {
      alert('Erro: ' + analise.error)
    } else {
      alert('DIAGNÓSTICO TÉCNICO:\n' + analise.diagnostico + '\n\nSUGESTÃO DE SOLUÇÃO:\n' + analise.solucao)
    }
  } catch (error) {
    console.error('Erro ao conectar com o serviço de análise:', error)
    alert('Não foi possível conectar ao serviço de análise.')
  }
}
</script>

<style scoped>
.crud-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-header {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 1px solid #bfdbfe;
  border-radius: 20px;
  padding: 1.5rem 1.75rem;
}
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.page-header h2 { margin: 0; color: #0f172a; font-size: 1.5rem; font-weight: 700; }
.page-copy { margin: 0.4rem 0 0; color: #475569; font-size: 0.95rem; }

.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.table-card { padding: 1.5rem; }
.card-header { margin-bottom: 1.25rem; }
.card-header h3 { margin: 0; color: #0f172a; }
.card-header p { margin: 0.4rem 0 0; color: #475569; }

.metrics-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.metric-item {
  display: flex; flex-direction: column; gap: 0.25rem;
  padding: 1rem 1.25rem;
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px;
}
.metric-value { font-size: 2rem; font-weight: 800; color: #0f172a; line-height: 1; }
.metric-label { font-size: 0.82rem; font-weight: 600; color: #64748b; }

.ticket-list { display: flex; flex-direction: column; }
.ticket-item {
  display: flex; justify-content: space-between; align-items: flex-start;
  gap: 1rem; padding: 1rem 0; border-bottom: 1px solid #e2e8f0;
}
.ticket-item:last-child { border-bottom: none; padding-bottom: 0; }
.ticket-info { display: flex; flex-direction: column; gap: 0.3rem; }
.ticket-info strong { color: #0f172a; font-size: 0.95rem; }
.ticket-info p { margin: 0; color: #475569; font-size: 0.875rem; }

.btn-ia {
  margin-top: 0.5rem;
  padding: 0.38rem 0.75rem;
  border: 1px solid #bfdbfe; border-radius: 8px;
  background: #eff6ff; color: #1d4ed8;
  font-size: 0.75rem; font-weight: 700;
  cursor: pointer; font-family: inherit;
  transition: background 0.2s, transform 0.15s;
  align-self: flex-start;
}
.btn-ia:hover { background: #dbeafe; transform: translateY(-1px); }

.status-badge {
  flex-shrink: 0;
  border-radius: 999px; padding: 0.35rem 0.8rem;
  font-size: 0.78rem; font-weight: 700; white-space: nowrap;
}
.status-badge.critico  { background: #fee2e2; color: #b91c1c; }
.status-badge.medio    { background: #fef3c7; color: #b45309; }
.status-badge.planejado { background: #dbeafe; color: #1d4ed8; }

@media (max-width: 768px) {
  .page-header, .table-card { padding: 1.2rem; border-radius: 16px; }
  .card { border-radius: 16px; }
  .metrics-row { grid-template-columns: 1fr; }
  .ticket-item { flex-direction: column; }
}
</style>