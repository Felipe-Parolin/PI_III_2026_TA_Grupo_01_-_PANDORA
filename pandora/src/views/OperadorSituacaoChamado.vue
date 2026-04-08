<template>
  <div class="role-page">
    <section class="hero-card">
      <p class="eyebrow">Operador de M&aacute;quinas</p>
      <h2>Situa&ccedil;&atilde;o do Chamado</h2>
      <p class="hero-copy">Acompanhe o andamento das solicita&ccedil;&otilde;es abertas sem sair do painel operacional.</p>
    </section>

    <section class="list-card">
      <div class="section-header">
        <h3>Chamados recentes</h3>
        <p>Estrutura inicial para exibir a situa&ccedil;&atilde;o dos chamados do operador logado.</p>
      </div>

      <div class="ticket-list">
        <article class="ticket-item">
          <div>
            <strong>CH-1032 • Misturador Principal</strong>
            <p>Ru&iacute;do mec&acirc;nico acima do normal.</p>
          </div>
          <span class="status waiting">Em an&aacute;lise</span>
        </article>
        <article class="ticket-item">
          <div>
            <strong>CH-1027 • Linha de Envase</strong>
            <p>Falha no sensor de presen&ccedil;a.</p>
          </div>
          <span class="status progress">Em atendimento</span>
        </article>
        <article class="ticket-item">
          <div>
            <strong>CH-1015 • Dosador Autom&aacute;tico</strong>
            <p>Oscila&ccedil;&atilde;o resolvida pela manuten&ccedil;&atilde;o.</p>
          </div>
          <span class="status done">Conclu&iacute;do</span>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.role-page { display: flex; flex-direction: column; gap: 1.5rem; }
.hero-card, .list-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 1.5rem; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.hero-card h2, .section-header h3 { margin: 0; color: #0f172a; }
.hero-copy, .section-header p, .ticket-item p { color: #475569; }
.ticket-list { display: flex; flex-direction: column; gap: 0.85rem; }
.ticket-item { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1rem 0; border-bottom: 1px solid #e2e8f0; }
.ticket-item:last-child { border-bottom: none; }
.ticket-item strong { color: #0f172a; }
.ticket-item p { margin: 0.3rem 0 0; }
.status { border-radius: 999px; padding: 0.35rem 0.8rem; font-size: 0.8rem; font-weight: 700; white-space: nowrap; }
.status.waiting { background: #e0f2fe; color: #0369a1; }
.status.progress { background: #fef3c7; color: #b45309; }
.status.done { background: #dcfce7; color: #166534; }
@media (max-width: 900px) { .ticket-item { flex-direction: column; align-items: flex-start; } }
</style>
