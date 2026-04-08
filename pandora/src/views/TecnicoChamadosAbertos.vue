<template>
  <div class="role-page">
    <section class="hero-card">
      <p class="eyebrow">T&eacute;cnico de Manuten&ccedil;&atilde;o</p>
      <h2>Chamados Abertos</h2>
      <p class="hero-copy">Veja rapidamente o que precisa de atendimento e priorize sua pr&oacute;xima interven&ccedil;&atilde;o.</p>
    </section>

    <section class="metrics-grid">
      <article class="metric-card">
        <span class="metric-label">Chamados urgentes</span>
        <strong>06</strong>
        <p>Equipamentos com impacto direto na opera&ccedil;&atilde;o.</p>
      </article>
      <article class="metric-card">
        <span class="metric-label">Em andamento</span>
        <strong>14</strong>
        <p>Atendimentos j&aacute; assumidos pela equipe t&eacute;cnica.</p>
      </article>
      <article class="metric-card">
        <span class="metric-label">Aguardando pe&ccedil;as</span>
        <strong>03</strong>
        <p>Solicita&ccedil;&otilde;es dependentes de reposi&ccedil;&atilde;o ou compra.</p>
      </article>
    </section>

    <section class="list-card">
      <div class="section-header">
        <h3>Fila de atendimento</h3>
        <p>Estrutura inicial do dashboard t&eacute;cnico. Aqui voc&ecirc; pode ligar a API dos chamados abertos.</p>
      </div>

      <div class="ticket-list">
        <article class="ticket-item">
          <div>
            <strong>CH-1024 • Prensa Hidr&aacute;ulica 02</strong>
            <p>Parada intermitente durante o ciclo de produ&ccedil;&atilde;o.</p>
          </div>
          <span class="status critical">Cr&iacute;tico</span>
        </article>
        <article class="ticket-item">
          <div>
            <strong>CH-1021 • Esteira de Embalagem</strong>
            <p>Ru&iacute;do incomum reportado pelo operador do turno B.</p>
          </div>
          <span class="status warning">M&eacute;dio</span>
        </article>
        <article class="ticket-item">
          <div>
            <strong>CH-1018 • Compressor Central</strong>
            <p>Verifica&ccedil;&atilde;o preventiva pendente ap&oacute;s oscila&ccedil;&atilde;o de press&atilde;o.</p>
          </div>
          <span class="status normal">Planejado</span>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.role-page { display: flex; flex-direction: column; gap: 1.5rem; }
.hero-card, .list-card, .metric-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.hero-card, .list-card { padding: 1.5rem; }
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.hero-card h2, .section-header h3 { margin: 0; color: #0f172a; }
.hero-copy, .section-header p, .metric-card p, .ticket-item p { color: #475569; }
.metrics-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
.metric-card { padding: 1.25rem; }
.metric-label { display: block; color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem; }
.metric-card strong { font-size: 2rem; color: #1e293b; }
.ticket-list { display: flex; flex-direction: column; gap: 0.85rem; }
.ticket-item { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1rem 0; border-bottom: 1px solid #e2e8f0; }
.ticket-item:last-child { border-bottom: none; }
.ticket-item strong { color: #0f172a; }
.ticket-item p { margin: 0.3rem 0 0; }
.status { border-radius: 999px; padding: 0.35rem 0.8rem; font-size: 0.8rem; font-weight: 700; white-space: nowrap; }
.status.critical { background: #fee2e2; color: #b91c1c; }
.status.warning { background: #fef3c7; color: #b45309; }
.status.normal { background: #dbeafe; color: #1d4ed8; }
@media (max-width: 900px) { .metrics-grid { grid-template-columns: 1fr; } .ticket-item { flex-direction: column; align-items: flex-start; } }
</style>
