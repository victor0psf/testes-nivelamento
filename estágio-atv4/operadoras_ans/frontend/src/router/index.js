import SearchOperadoras from '@/components/SearchOperadoras.vue'; // Importe diretamente seu componente
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: SearchOperadoras  // Use seu componente diretamente
    }
    // Remova a rota '/about' se não for usar
  ]
})

export default router