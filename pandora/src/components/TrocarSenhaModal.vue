<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <section class="modal-panel" role="dialog" aria-modal="true" aria-labelledby="trocar-senha-title">
      <header class="modal-header">
        <div>
          <p class="eyebrow">Conta</p>
          <h2 id="trocar-senha-title">Trocar senha</h2>
        </div>
        <button type="button" class="icon-button" title="Fechar" @click="emit('close')">
          <AppIcon name="x" :size="18" />
        </button>
      </header>

      <form class="password-form" @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="senha-atual">Senha atual</label>
          <input
            id="senha-atual"
            v-model="form.senha_atual"
            type="password"
            autocomplete="current-password"
            required
            :disabled="isLoading"
            :class="{ invalid: fieldErrors.senha_atual }"
          />
          <p v-if="fieldErrors.senha_atual" class="field-error">{{ fieldErrors.senha_atual }}</p>
        </div>

        <div class="input-group">
          <label for="nova-senha">Nova senha</label>
          <input
            id="nova-senha"
            v-model="form.nova_senha"
            type="password"
            autocomplete="new-password"
            minlength="8"
            required
            :disabled="isLoading"
            :class="{ invalid: fieldErrors.nova_senha }"
          />
          <p v-if="fieldErrors.nova_senha" class="field-error">{{ fieldErrors.nova_senha }}</p>
        </div>

        <div class="input-group">
          <label for="confirmar-senha">Confirmar nova senha</label>
          <input
            id="confirmar-senha"
            v-model="form.confirmar_senha"
            type="password"
            autocomplete="new-password"
            minlength="8"
            required
            :disabled="isLoading"
            :class="{ invalid: fieldErrors.confirmar_senha }"
          />
          <p v-if="fieldErrors.confirmar_senha" class="field-error">{{ fieldErrors.confirmar_senha }}</p>
        </div>

        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" :disabled="isLoading" @click="emit('close')">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Alterando...' : 'Alterar senha' }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import AppIcon from './AppIcon.vue'
import { api } from '../services/api'

const emit = defineEmits(['close'])

const form = reactive({
  senha_atual: '',
  nova_senha: '',
  confirmar_senha: ''
})

const isLoading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const fieldErrors = ref({})

const firstMessage = (value) => {
  if (Array.isArray(value)) return value[0] || ''
  if (typeof value === 'string') return value
  return ''
}

const clearMessages = () => {
  successMessage.value = ''
  errorMessage.value = ''
  fieldErrors.value = {}
}

const resetForm = () => {
  form.senha_atual = ''
  form.nova_senha = ''
  form.confirmar_senha = ''
}

const applyFieldErrors = (data = {}) => {
  fieldErrors.value = {
    senha_atual: firstMessage(data.senha_atual),
    nova_senha: firstMessage(data.nova_senha),
    confirmar_senha: firstMessage(data.confirmar_senha)
  }
}

const handleSubmit = async () => {
  clearMessages()

  if (form.nova_senha !== form.confirmar_senha) {
    fieldErrors.value = { confirmar_senha: 'As senhas não conferem.' }
    return
  }

  isLoading.value = true

  try {
    const response = await api.changePassword({ ...form })
    successMessage.value = response?.detail || 'Senha alterada com sucesso.'
    resetForm()
  } catch (error) {
    applyFieldErrors(error?.data || {})
    errorMessage.value = firstMessage(error?.data?.non_field_errors) || error?.message || 'Não foi possível alterar a senha.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: grid;
  place-items: center;
  min-height: 100dvh;
  padding: 1.25rem;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(3px);
}

.modal-panel {
  box-sizing: border-box;
  width: min(440px, calc(100vw - 2.5rem));
  max-height: calc(100dvh - 2.5rem);
  overflow-y: auto;
  padding: 1.4rem;
  background: #ffffff;
  border: 1px solid #d8e2ec;
  border-radius: 10px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.24);
}

.modal-panel * {
  box-sizing: border-box;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.35rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.eyebrow {
  margin: 0 0 0.25rem;
  color: #2563eb;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.modal-header h2 {
  margin: 0;
  color: #0f172a;
  font-size: 1.2rem;
  line-height: 1.25;
}

.icon-button {
  width: 34px;
  height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  border: 1px solid #d8e2ec;
  border-radius: 8px;
  background: #ffffff;
  color: #475569;
  cursor: pointer;
  font-weight: 800;
}

.icon-button:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 1.05rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.input-group label {
  color: #334155;
  font-size: 0.85rem;
  font-weight: 700;
}

.input-group input {
  width: 100%;
  min-height: 44px;
  padding: 0.78rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
  color: #0f172a;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
}

.input-group input:focus {
  outline: none;
  background: #ffffff;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
}

.input-group input.invalid {
  border-color: #dc2626;
  background: #fff7f7;
}

.field-error,
.error-message {
  margin: 0;
  color: #b91c1c;
  font-size: 0.82rem;
  font-weight: 700;
}

.success-message {
  margin: 0;
  padding: 0.78rem 0.9rem;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  background: #f0fdf4;
  color: #166534;
  font-size: 0.86rem;
  font-weight: 700;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.25rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.btn {
  min-height: 40px;
  border-radius: 8px;
  padding: 0.65rem 0.95rem;
  font-size: 0.9rem;
  font-weight: 800;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s;
}

.btn-primary {
  border: 1px solid #2563eb;
  background: #2563eb;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #1d4ed8;
  border-color: #1d4ed8;
}

.btn-secondary {
  border: 1px solid #d8e2ec;
  background: #ffffff;
  color: #475569;
}

.btn-secondary:hover:not(:disabled) {
  background: #f8fafc;
  color: #0f172a;
}

.btn:disabled,
.input-group input:disabled {
  opacity: 0.68;
  cursor: not-allowed;
}

@media (max-width: 560px) {
  .modal-overlay {
    padding: 0.9rem;
  }

  .modal-panel {
    width: min(100%, calc(100vw - 1.8rem));
    max-height: calc(100dvh - 1.8rem);
    padding: 1rem;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn {
    width: 100%;
  }
}
</style>
