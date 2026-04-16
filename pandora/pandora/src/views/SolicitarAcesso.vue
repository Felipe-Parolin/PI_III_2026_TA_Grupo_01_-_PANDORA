<template>
  <div class="page-container">
    <div class="auth-card">
      <aside class="brand-panel">
        <div class="brand-content">
          <h1 class="brand-logo-text">Pandora</h1>
          <p class="brand-tagline">
            Dê o próximo passo para a Indústria 4.0. Cadastre-se e otimize o tempo de máquina parada.
          </p>
        </div>
        
        <div class="decor decor-1"></div>
        <div class="decor decor-2"></div>
      </aside>

      <main class="form-panel">
        <div class="form-header">
          <h2>Solicitar Acesso</h2>
          <p>Preencha os dados da indústria para avaliação.</p>
        </div>

        <form @submit.prevent="handleRequest" class="auth-form">
          <div class="input-row">
            <div class="input-group">
              <label for="empresa">Empresa</label>
              <input id="empresa" v-model="form.empresa" type="text" placeholder="Razão Social" required />
            </div>

            <div class="input-group">
              <label for="cnpj">CNPJ</label>
              <input id="cnpj" v-model="form.cnpj" type="text" placeholder="00.000.000/0000-00" required />
            </div>
          </div>

          <div class="input-group">
            <label for="nome">Responsável</label>
            <input id="nome" v-model="form.nome" type="text" placeholder="Seu nome completo" required />
          </div>

          <div class="input-group">
            <label for="email">E-mail</label>
            <input id="email" v-model="form.email" type="email" placeholder="contato@empresa.com.br" required />
          </div>

          <div class="input-group">
            <label for="telefone">Telefone / WhatsApp</label>
            <input id="telefone" v-model="form.telefone" type="text" placeholder="(00) 00000-0000" required />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">Enviar solicitação</button>
            <button 
              type="button" 
              class="btn-secondary" 
              @click="$router.push('/')"
            >
              Voltar ao login
            </button>
          </div>
        </form>
      </main>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  empresa: '',
  cnpj: '',
  nome: '',
  email: '',
  telefone: ''
})

const handleRequest = () => {
  console.log('Solicitação enviada', form)
  alert('Solicitação enviada com sucesso! Aguarde nosso contato.')
}
</script>

<style scoped>
/* O CSS é idêntico ao Login.vue para manter a mesma caixa! */
.page-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #f1f5f9;
  font-family: 'Inter', system-ui, sans-serif;
}

.auth-card {
  display: flex;
  width: 100%;
  max-width: 900px; /* Largura ideal para formulários divididos */
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.brand-panel {
  flex: 1;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  color: white;
  padding: 3rem 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.brand-content {
  position: relative;
  z-index: 2;
}

.brand-logo-text {
  font-size: 3.5rem;
  font-weight: 800;
  letter-spacing: -0.05em;
  margin-bottom: 1rem;
  text-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.brand-tagline {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #bfdbfe;
  max-width: 280px;
  margin: 0 auto;
}

.decor {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  z-index: 1;
}

.decor-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
}

.decor-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  right: -50px;
}

.form-panel {
  flex: 1.2; /* Dá um pouco mais de espaço para o form do que para o lado azul */
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-header {
  margin-bottom: 1.5rem;
}

.form-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: #64748b;
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Um pouco mais apertado aqui para caber todos os inputs */
}

/* Nova classe para alinhar inputs lado a lado na tela de registro */
.input-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.input-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.input-group input {
  padding: 0.8rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.2s;
  background-color: #f8fafc;
}

.input-group input:focus {
  outline: none;
  background-color: #ffffff;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.form-actions {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.btn-primary {
  padding: 0.9rem;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

.btn-secondary {
  padding: 0.9rem;
  background: transparent;
  border: 2px solid #e2e8f0;
  color: #475569;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
  color: #1e293b;
}

@media (max-width: 768px) {
  .auth-card {
    flex-direction: column;
  }
  .brand-panel {
    padding: 3rem 2rem;
  }
  .form-panel {
    padding: 2.5rem;
  }
  .input-row {
    grid-template-columns: 1fr;
  }
}
</style>