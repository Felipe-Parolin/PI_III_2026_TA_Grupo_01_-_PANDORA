<template>
  <div class="crud-page">
    <section class="page-header">
      <p class="eyebrow">Operador de Máquinas</p>
      <h2>Situação do Chamado</h2>
      <p class="page-copy">Acompanhe o andamento das solicitações abertas sem sair do painel operacional.</p>
    </section>

    <section class="card table-card">
      <div class="card-header">
        <h3>Chamados recentes</h3>
        <p>Situação dos chamados do operador logado.</p>
      </div>

      <div class="ticket-list">
        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1032 · Misturador Principal</strong>
            <p>Ruído mecânico acima do normal.</p>
          </div>
          <span class="status-badge analise">Em análise</span>
        </article>
        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1027 · Linha de Envase</strong>
            <p>Falha no sensor de presença.</p>
          </div>
          <span class="status-badge andamento">Em atendimento</span>
        </article>
        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1015 · Dosador Automático</strong>
            <p>Oscilação resolvida pela manutenção.</p>
          </div>
          <span class="status-badge concluido">Concluído</span>
        </article>
      </div>
    </section>
  </div>
</template>

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

.ticket-list { display: flex; flex-direction: column; }
.ticket-item {
  display: flex; justify-content: space-between; align-items: center;
  gap: 1rem; padding: 1rem 0; border-bottom: 1px solid #e2e8f0;
}
.ticket-item:last-child { border-bottom: none; padding-bottom: 0; }
.ticket-info { display: flex; flex-direction: column; gap: 0.3rem; }
.ticket-info strong { color: #0f172a; font-size: 0.95rem; }
.ticket-info p { margin: 0; color: #475569; font-size: 0.875rem; }

.status-badge {
  flex-shrink: 0;
  border-radius: 999px; padding: 0.35rem 0.8rem;
  font-size: 0.78rem; font-weight: 700; white-space: nowrap;
}
.status-badge.analise  { background: #e0f2fe; color: #0369a1; }
.status-badge.andamento { background: #fef3c7; color: #b45309; }
.status-badge.concluido { background: #dcfce7; color: #166534; }

@media (max-width: 768px) {
  .page-header, .table-card { padding: 1.2rem; border-radius: 16px; }
  .card { border-radius: 16px; }
  .ticket-item { flex-direction: column; align-items: flex-start; }
}
</style>