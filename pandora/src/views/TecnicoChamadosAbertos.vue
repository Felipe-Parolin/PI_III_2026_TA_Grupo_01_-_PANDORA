<template>
  <div class="role-page">
    <section class="hero-card">
      <p class="eyebrow">Técnico de Manutenção</p>
      <h2>Chamados Abertos</h2>
      <p class="hero-copy">Veja rapidamente o que precisa de atendimento e priorize sua próxima intervenção.</p>
    </section>

    <section class="metrics-grid">
      <article class="metric-card">
        <span class="metric-label">Chamados urgentes</span>
        <strong>06</strong>
        <p>Equipamentos com impacto direto na operação.</p>
      </article>
      <article class="metric-card">
        <span class="metric-label">Em andamento</span>
        <strong>14</strong>
        <p>Atendimentos já assumidos pela equipe técnica.</p>
      </article>
      <article class="metric-card">
        <span class="metric-label">Aguardando peças</span>
        <strong>03</strong>
        <p>Solicitações dependentes de reposição ou compra.</p>
      </article>
    </section>

    <section class="list-card">
      <div class="section-header">
        <h3>Fila de atendimento</h3>
        <p>Utilize a inteligência artificial para obter diagnósticos prévios dos problemas relatados.</p>
      </div>

      <div class="ticket-list">
        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1024 • Prensa Hidráulica 02</strong>
            <p>Parada intermitente durante o ciclo de produção.</p>
            <button @click="solicitarAnaliseIA('Parada intermitente durante o ciclo de produção na Prensa Hidráulica 02')" class="btn-ia">
               💡 Analisar com IA
            </button>
          </div>
          <span class="status critical">Crítico</span>
        </article>

        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1021 • Esteira de Embalagem</strong>
            <p>Ruído incomum reportado pelo operador do turno B.</p>
            <button @click="solicitarAnaliseIA('Ruído incomum na Esteira de Embalagem reportado pelo operador')" class="btn-ia">
               💡 Analisar com IA
            </button>
          </div>
          <span class="status warning">Médio</span>
        </article>

        <article class="ticket-item">
          <div class="ticket-info">
            <strong>CH-1018 • Compressor Central</strong>
            <p>Verificação preventiva pendente após oscilação de pressão.</p>
            <button @click="solicitarAnaliseIA('Verificação preventiva no Compressor Central após oscilação de pressão')" class="btn-ia">
               💡 Analisar com IA
            </button>
          </div>
          <span class="status normal">Planejado</span>
        </article>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  methods: {
    async solicitarAnaliseIA(descricaoChamado) {
      try {
        // Ajustado para a URL do seu router: /analises-llm/analisar/
        const response = await fetch('http://localhost:8000/analises-llm/analisar/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ descricao: descricaoChamado })
        });
        
        const analise = await response.json();
        
        if (analise.error) {
          alert("Erro: " + analise.error);
        } else {
          // Exibe o diagnóstico vindo do Llama
          alert("🤖 DIAGNÓSTICO IA:\n" + analise.diagnostico + "\n\n🛠️ SUGGESTÃO DE SOLUÇÃO:\n" + analise.solucao);
        }
      } catch (error) {
        console.error("Erro ao conectar com a IA:", error);
        alert("Não foi possível conectar ao servidor de IA.");
      }
    }
  }
}
</script>

<style scoped>
/* SEUS ESTILOS ORIGINAIS MANTIDOS */
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

/* NOVO ESTILO PARA O BOTÃO DE IA */
.btn-ia {
  margin-top: 0.75rem;
  padding: 0.4rem 0.8rem;
  border: 1px solid #dbeafe;
  border-radius: 8px;
  background: #f0f9ff;
  color: #0369a1;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
}
.btn-ia:hover {
  background: #e0f2fe;
  transform: translateY(-1px);
}

.status { border-radius: 999px; padding: 0.35rem 0.8rem; font-size: 0.8rem; font-weight: 700; white-space: nowrap; }
.status.critical { background: #fee2e2; color: #b91c1c; }
.status.warning { background: #fef3c7; color: #b45309; }
.status.normal { background: #dbeafe; color: #1d4ed8; }

@media (max-width: 900px) { .metrics-grid { grid-template-columns: 1fr; } .ticket-item { flex-direction: column; align-items: flex-start; } }
</style>