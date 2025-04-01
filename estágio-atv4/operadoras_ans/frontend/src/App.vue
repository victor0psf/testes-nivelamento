<template>
  <div id="app">
    <SearchOperadoras />
  </div>
</template>

<script>
import SearchOperadoras from './components/SearchOperadoras.vue'

export default {
  name: 'App',
  components: {
    SearchOperadoras
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 20px;
}
</style>