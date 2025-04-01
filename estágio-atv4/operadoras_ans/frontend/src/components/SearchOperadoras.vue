<template>
    <div class="search-container">
      <h1>Busca de Operadoras de Saúde Ativas na ANS</h1>
      
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="onSearchInput" 
          placeholder="Digite nome, CNPJ ou registro..."
          @keyup.enter="performSearch"
        />
        <button @click="performSearch">
          <span v-if="!loading">Buscar</span>
          <span v-else class="loader-small"></span>
        </button>
      </div>
      
      <div v-if="loading" class="loading">
        <span class="loader"></span> Buscando operadoras...
      </div>
      
      <div v-if="error" class="error">
        <strong>Erro:</strong> {{ error }}
      </div>
      
      <div v-if="results.length > 0" class="results-container">
        <div class="result-info">
          <div class="result-count">
            {{ meta.total }} resultado(s) encontrado(s)
          </div>
          <div class="result-query">
            Busca por: "{{ searchQuery }}"
          </div>
        </div>
        
        <div class="table-wrapper">
          <table class="results-table">
            <thead>
              <tr>
                <th @click="sortResults('REGISTRO ANS')">
                  Registro ANS
                  <span v-if="sortColumn === 'REGISTRO ANS'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortResults('NOME FANTASIA')">
                  Nome Fantasia
                  <span v-if="sortColumn === 'NOME FANTASIA'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortResults('RAZÃO SOCIAL')">
                  Razão Social
                  <span v-if="sortColumn === 'RAZÃO SOCIAL'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortResults('CNPJ')">
                  CNPJ
                  <span v-if="sortColumn === 'CNPJ'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortResults('MODALIDADE')">
                  Modalidade
                  <span v-if="sortColumn === 'MODALIDADE'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="operadora in paginatedResults" :key="operadora['REGISTRO ANS'] + operadora['CNPJ']">
                <td>{{ operadora['REGISTRO ANS'] }}</td>
                <td>{{ operadora['NOME FANTASIA'] || '-' }}</td>
                <td>{{ operadora['RAZÃO SOCIAL'] || '-' }}</td>
                <td>{{ formatCNPJ(operadora['CNPJ']) }}</td>
                <td>{{ operadora['MODALIDADE'] || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <div v-if="totalPages > 1" class="pagination">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1"
            class="page-btn"
          >
            &lt; Anterior
          </button>
          
          <span class="page-info">
            Página {{ currentPage }} de {{ totalPages }}
          </span>
          
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages"
            class="page-btn"
          >
            Próxima &gt;
          </button>
        </div>
      </div>
      
      <div v-else-if="searchPerformed && !loading" class="no-results">
        Nenhuma operadora encontrada para "{{ searchQuery }}"
        <div v-if="meta.total > 0" class="suggestion">
          Sugestão: tente termos mais gerais como "saúde" ou "medicina"
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SearchOperadoras',
    data() {
      return {
        searchQuery: '',
        results: [],
        meta: {
          total: 0,
          query: ''
        },
        loading: false,
        error: null,
        searchPerformed: false,
        currentPage: 1,
        itemsPerPage: 10,
        sortColumn: '',
        sortDirection: 'asc',
        searchTimeout: null
      }
    },
    computed: {
      totalPages() {
        return Math.ceil(this.results.length / this.itemsPerPage);
      },
      paginatedResults() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        
        // Ordenação
        let sorted = [...this.results];
        if (this.sortColumn) {
          sorted.sort((a, b) => {
            let valA = a[this.sortColumn] || '';
            let valB = b[this.sortColumn] || '';
            
            if (this.sortDirection === 'asc') {
              return valA.localeCompare(valB);
            } else {
              return valB.localeCompare(valA);
            }
          });
        }
        
        return sorted.slice(start, end);
      }
    },
    methods: {
      async performSearch() {
        if (this.searchQuery.trim().length < 2) {
          this.results = [];
          this.searchPerformed = false;
          this.error = 'Digite pelo menos 2 caracteres para buscar';
          return;
        }
        
        this.loading = true;
        this.error = null;
        this.searchPerformed = true;
        this.currentPage = 1;
        
        try {
          const response = await axios.get('http://localhost:5000/api/search', {
            params: { q: this.searchQuery }
          });
          
          this.results = response.data.data || [];
          this.meta = response.data.meta || { total: 0 };
          
          if (this.meta.total > 0 && this.results.length === 0) {
            this.error = 'Muitos resultados. Tente uma busca mais específica.';
          }
          
        } catch (err) {
          console.error('Erro na busca:', {
            error: err,
            response: err.response?.data
          });
          
          this.error = err.response?.data?.error || 
                      'Erro ao conectar com o servidor. Tente novamente.';
          this.results = [];
          this.meta = { total: 0 };
        } finally {
          this.loading = false;
        }
      },
      
      onSearchInput() {
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
          if (this.searchQuery.trim().length >= 2) {
            this.performSearch();
          }
        }, 600);
      },
      
      sortResults(column) {
        if (this.sortColumn === column) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortColumn = column;
          this.sortDirection = 'asc';
        }
      },
      
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      },
      
      prevPage() {
        if (this.currentPage > 1) {
          this.currentPage--;
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      },
      
      formatCNPJ(cnpj) {
        if (!cnpj || cnpj.trim() === '') return '-';
        
        // Remove tudo que não é dígito
        const digits = cnpj.replace(/\D/g, '');
        
        // Verifica se tem 14 dígitos
        if (digits.length !== 14) return cnpj;
        
        // Formatação do CNPJ
        return digits.replace(
          /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
          '$1.$2.$3/$4-$5'
        );
      }
    }
  }
  </script>
  
  <style scoped>
  .search-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  h1 {
    color: #0e5399;
    text-align: center;
    margin-bottom: 30px;
    font-weight: 600;
  }
  
  .search-box {
    display: flex;
    margin-bottom: 25px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border-radius: 6px;
    overflow: hidden;
  }
  
  .search-box input {
    flex: 1;
    padding: 14px 20px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-right: none;
    outline: none;
    transition: border-color 0.3s;
  }
  
  .search-box input:focus {
    border-color: #42b983;
  }
  
  .search-box button {
    padding: 0 25px;
    background-color: #42b983;
    color: white;
    border: none;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 100px;
  }
  
  .search-box button:hover {
    background-color: #369f6b;
  }
  
  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30px;
    font-size: 18px;
    color: #555;
  }
  
  .loader, .loader-small {
    display: inline-block;
    border: 3px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top-color: #42b983;
    animation: spin 1s ease-in-out infinite;
    margin-right: 10px;
  }
  
  .loader {
    width: 20px;
    height: 20px;
  }
  
  .loader-small {
    width: 16px;
    height: 16px;
    border-width: 2px;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .error {
    background-color: #ffeeee;
    color: #d32f2f;
    padding: 15px;
    border-radius: 4px;
    margin: 20px 0;
    border-left: 4px solid #d32f2f;
  }
  
  .results-container {
    margin-top: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    overflow: hidden;
  }
  
  .result-info {
    padding: 15px 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .result-count {
    font-weight: 600;
    color: #2c3e50;
  }
  
  .result-query {
    color: #666;
    font-size: 14px;
  }
  
  .table-wrapper {
    overflow-x: auto;
  }
  
  .results-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 800px;
  }
  
  .results-table th {
    background-color: #42b983;
    color: white;
    padding: 14px 16px;
    text-align: left;
    font-weight: 500;
    position: sticky;
    top: 0;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .results-table th:hover {
    background-color: #3aa876;
  }
  
  .results-table th span {
    margin-left: 5px;
  }
  
  .results-table td {
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
    color: #333;
  }
  
  .results-table tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .results-table tr:hover {
    background-color: #f1f8e9;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background: #f8f9fa;
    border-top: 1px solid #eee;
  }
  
  .page-btn {
    padding: 8px 16px;
    margin: 0 10px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .page-btn:hover:not(:disabled) {
    background-color: #369f6b;
  }
  
  .page-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
    opacity: 0.7;
  }
  
  .page-info {
    margin: 0 15px;
    color: #555;
    font-size: 14px;
  }
  
  .no-results {
    text-align: center;
    padding: 40px 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    color: #555;
    font-size: 18px;
  }
  
  .suggestion {
    margin-top: 15px;
    font-size: 14px;
    color: #888;
  }
  
  @media (max-width: 768px) {
    .search-box {
      flex-direction: column;
    }
    
    .search-box input {
      border-right: 1px solid #ddd;
      border-bottom: none;
    }
    
    .search-box button {
      padding: 12px;
    }
    
    .result-info {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
  }
  </style>