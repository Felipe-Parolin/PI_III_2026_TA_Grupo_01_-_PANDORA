<template>
  <div class="role-page">
    <section class="hero-card">
      <p class="eyebrow">T&eacute;cnico de Manuten&ccedil;&atilde;o</p>
      <h2>Hist&oacute;rico de Manuten&ccedil;&otilde;es</h2>
      <p class="hero-copy">Consulte o que j&aacute; foi executado e acompanhe a recorr&ecirc;ncia das interven&ccedil;&otilde;es.</p>
    </section>

    <section class="list-card">
      <div class="section-header">
        <h3>&Uacute;ltimas manuten&ccedil;&otilde;es conclu&iacute;das</h3>
        <p>Estrutura pronta para receber os dados reais da API de hist&oacute;rico.</p>
      </div>

      <div class="history-list">
        <article class="history-item">
          <strong>Torno CNC 05</strong>
          <span>Troca de sensor de fim de curso • 05/04/2026</span>
        </article>
        <article class="history-item">
          <strong>Empilhadeira El&eacute;trica</strong>
          <span>Revis&atilde;o preventiva trimestral • 03/04/2026</span>
        </article>
        <article class="history-item">
          <strong>Forno de Cura</strong>
          <span>Calibra&ccedil;&atilde;o de temperatura • 29/03/2026</span>
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
.hero-copy, .section-header p { color: #475569; }
.history-list { display: flex; flex-direction: column; gap: 0.9rem; }
.history-item { display: flex; flex-direction: column; gap: 0.25rem; padding: 1rem; border-radius: 16px; background: #f8fafc; border: 1px solid #e2e8f0; }
.history-item strong { color: #0f172a; }
.history-item span { color: #475569; }
</style>
