<template>
  <div class="page-container">
    <div class="auth-card">
      <aside class="brand-panel">
        <div class="brand-content">
          <h1 class="brand-logo-text">Pandora</h1>
          <p class="brand-tagline">
            O motor da sua indústria não pode parar. Gestão inteligente de chamados e manutenção de máquinas em um só lugar.
          </p>
        </div>
        
        <div class="decor decor-1"></div>
        <div class="decor decor-2"></div>
      </aside>

      <main class="form-panel">
        <div class="form-header">
          <h2>Acesse sua conta</h2>
          <p>Insira suas credenciais para entrar no sistema.</p>
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="input-group">
            <label for="email">E-mail corporativo</label>
            <input 
              id="email" 
              v-model="form.email" 
              type="email" 
              placeholder="exemplo@empresa.com.br" 
              required 
            />
          </div>

          <div class="input-group">
            <label for="password">Senha</label>
            <input 
              id="password" 
              v-model="form.password" 
              type="password" 
              placeholder="••••••••" 
              required 
            />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">Entrar no sistema</button>
            <button 
              type="button" 
              class="btn-secondary" 
              @click="$router.push('/solicitar-acesso')"
            >
              Nova empresa? Solicitar acesso
            </button>
          </div>
        </form>
      </main>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api' // Ajuste o caminho se a sua pasta for diferente

const router = useRouter()

const form = reactive({
  email: '',
  password: ''
})

const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    // 1. Faz a chamada para a API
    const data = await api.login(form.email, form.password)
    
    // 2. Salva o token de acesso (se sua API retornar um token). 
    // Ajuste 'data.token' para o nome exato do campo que o Django devolve (ex: data.access)
    if (data.token) {
      localStorage.setItem('access_token', data.token)
    }

    const nomeUsuario = data?.usuario?.nome_usuario
    const empresaId = data?.usuario?.empresa?.id
    const perfilId = data?.usuario?.perfil?.id
    const tipoPerfil = data?.usuario?.perfil?.tipo_perfil

    if (empresaId) {
      localStorage.setItem('empresa_id', String(empresaId))
    } else {
      localStorage.removeItem('empresa_id')
    }

    if (nomeUsuario) {
      localStorage.setItem('nome_usuario', nomeUsuario)
    } else {
      localStorage.removeItem('nome_usuario')
    }

    if (tipoPerfil) {
      localStorage.setItem('tipo_perfil', tipoPerfil)
    } else {
      localStorage.removeItem('tipo_perfil')
    }

    if (perfilId) {
      localStorage.setItem('perfil_id', String(perfilId))
    } else {
      localStorage.removeItem('perfil_id')
    }

    localStorage.setItem('session_active', 'true')

    // 3. Redireciona o usuário para a tela inicial do Dashboard
    // Pode direcionar direto para equipamentos, por exemplo:
    router.push('/dashboard')
    
  } catch (error) {
    console.error('Falha no login:', error.message)
    errorMessage.value = error.message
    alert(errorMessage.value) // Exibe o erro para o usuário
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Container de fundo */
.page-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #f1f5f9; /* Fundo cinza bem claro para destacar o cartão */
  font-family: 'Inter', system-ui, sans-serif;
}

/* O Cartão Centralizado */
.auth-card {
  display: flex;
  width: 100%;
  max-width: 900px;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

/* --- PAINEL ESQUERDO (AZUL) --- */
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

/* Decorações do fundo azul */
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

/* --- PAINEL DIREITO (BRANCO/FORMULÁRIO) --- */
.form-panel {
  flex: 1.2;
  padding: 3.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-header {
  margin-bottom: 2rem;
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
  gap: 1.25rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
}

.input-group input {
  padding: 0.85rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 1rem;
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
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-primary {
  padding: 1rem;
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
  padding: 1rem;
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

/* Responsividade */
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
}
</style>



