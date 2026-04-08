<template>
  <div class="role-page">
    <section class="hero-card">
      <p class="eyebrow">Operador de M&aacute;quinas</p>
      <h2>Abrir Chamado</h2>
      <p class="hero-copy">Registre rapidamente qualquer problema percebido durante a opera&ccedil;&atilde;o.</p>
    </section>

    <section class="form-card">
      <div class="section-header">
        <h3>Novo chamado</h3>
        <p>Base inicial para conectar depois ao endpoint de abertura de chamados.</p>
      </div>

      <form class="ticket-form" @submit.prevent>
        <div class="input-row">
          <div class="input-group">
            <label>Equipamento</label>
            <input type="text" placeholder="Ex: Injetora 07" />
          </div>
          <div class="input-group">
            <label>Prioridade</label>
            <select>
              <option>Baixa</option>
              <option>M&eacute;dia</option>
              <option>Alta</option>
            </select>
          </div>
        </div>
        <div class="input-group">
          <label>Descri&ccedil;&atilde;o do problema</label>
          <textarea rows="5" placeholder="Descreva o que aconteceu, sintomas e impacto percebido."></textarea>
        </div>
        <button type="submit" class="btn-primary">Registrar chamado</button>
      </form>
    </section>
  </div>
</template>

<style scoped>
.role-page { display: flex; flex-direction: column; gap: 1.5rem; }
.hero-card, .form-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 1.5rem; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06); }
.eyebrow { margin: 0 0 0.35rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563eb; }
.hero-card h2, .section-header h3 { margin: 0; color: #0f172a; }
.hero-copy, .section-header p { color: #475569; }
.ticket-form { display: flex; flex-direction: column; gap: 1rem; }
.input-row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 0.45rem; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #334155; }
.input-group input, .input-group select, .input-group textarea { width: 100%; box-sizing: border-box; padding: 0.9rem 1rem; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; color: #0f172a; }
.btn-primary { width: fit-content; border: none; border-radius: 12px; padding: 0.85rem 1.2rem; background: #2563eb; color: #ffffff; font-weight: 700; cursor: pointer; }
@media (max-width: 900px) { .input-row { grid-template-columns: 1fr; } .btn-primary { width: 100%; } }
</style>
