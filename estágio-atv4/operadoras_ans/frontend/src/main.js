// src/main.js

import { createPinia } from 'pinia'; // Importa gerenciador de estado
import { createApp } from 'vue'; // Importa função para criar aplicação Vue
import './assets/main.css'; // Importa estilos globais

import App from './App.vue'; // Importa componente raiz
import router from './router'; // Importa configuração de rotas

// Cria e configura a aplicação Vue
const app = createApp(App)

// Adiciona plugins
app.use(createPinia())  // Habilita Pinia para gerenciamento de estado
app.use(router)         // Habilita o roteador

// Monta a aplicação no elemento #app do HTML
app.mount('#app')