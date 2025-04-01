from flask import Flask, request, jsonify # type: ignore
import pandas as pd
from flask_cors import CORS # type: ignore
import os
import logging
from datetime import datetime
from unidecode import unidecode  # type: ignore # Para remover acentos nas buscas

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Configuração robusta de CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})

def load_operadoras_data():
    """Carrega os dados com tratamento específico para o formato ANS"""
    try:
        csv_path = 'data/operadoras_ativas.csv'
        
        # Verificação física do arquivo
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Arquivo não encontrado em: {os.path.abspath(csv_path)}")
        if os.path.getsize(csv_path) == 0:
            raise ValueError("O arquivo CSV está vazio")

        # Carrega com encoding correto para caracteres especiais
        df = pd.read_csv(
            csv_path,
            sep=';',
            encoding='latin1',
            on_bad_lines='warn',
            dtype='string'
        )
        
        # Normaliza nomes de colunas
        df.columns = df.columns.str.strip().str.upper()
        
        # Mapeamento de colunas para nomes padronizados
        column_mapping = {
            'REGISTRO_ANS': 'REGISTRO ANS',
            'RAZAO_SOCIAL': 'RAZÃO SOCIAL',
            'NOME_FANTASIA': 'NOME FANTASIA',
            'ENDERECO_ELETRONICO': 'EMAIL'
        }
        df = df.rename(columns=column_mapping)
        
        # Seleciona e ordena colunas relevantes
        cols_manter = [
            'REGISTRO ANS', 
            'CNPJ', 
            'RAZÃO SOCIAL', 
            'NOME FANTASIA', 
            'MODALIDADE',
            'CIDADE',
            'UF'
        ]
        df = df[[col for col in cols_manter if col in df.columns]]
        
        # Limpeza dos dados
        df = df.fillna('')
        
        logging.info("\n✅ Dados carregados com sucesso!")
        logging.info(f"Total de registros: {len(df)}")
        logging.info(f"Colunas disponíveis: {df.columns.tolist()}")
        logging.info(f"\nExemplo de registro:\n{df.iloc[0].to_dict()}\n")
        
        return df

    except Exception as e:
        logging.error("\n❌ ERRO AO CARREGAR DADOS:")
        logging.error(f"Tipo: {type(e).__name__}")
        logging.error(f"Detalhes: {str(e)}")
        logging.error(f"Caminho do arquivo: {os.path.abspath(csv_path)}")
        return pd.DataFrame()

# Carregamento inicial dos dados
df = load_operadoras_data()

@app.route('/api/healthcheck', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde do serviço"""
    response = {
        'status': 'healthy' if not df.empty else 'error',
        'record_count': len(df),
        'columns': list(df.columns) if not df.empty else [],
        'timestamp': datetime.now().isoformat(),
        'sample_record': df.iloc[0].to_dict() if not df.empty else None
    }
    return jsonify(response)

@app.route('/api/search', methods=['GET'])
def search_operadoras():
    """Endpoint de busca com tratamento robusto"""
    try:
        start_time = datetime.now()
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'data': [], 'meta': {'query': '', 'total': 0}})
            
        if df.empty:
            return jsonify({'error': 'Dados não disponíveis'}), 503
        
        # Normaliza a query (remove acentos e torna minúscula)
        query = unidecode(query).lower()
        
        # Campos para busca (priorizando Nome Fantasia)
        search_fields = [
            'NOME FANTASIA', 
            'RAZÃO SOCIAL', 
            'CNPJ', 
            'REGISTRO ANS',
            'CIDADE',
            'UF'
        ]
        available_fields = [f for f in search_fields if f in df.columns]
        
        # Busca case-insensitive e sem acentos
        mask = pd.Series(False, index=df.index)
        for field in available_fields:
            mask = mask | (
                df[field]
                .str.normalize('NFKD')
                .str.encode('ascii', errors='ignore')
                .str.decode('utf-8')
                .str.lower()
                .str.contains(query, na=False)
            )
        
        results = df[mask]
        
        # Formata a resposta
        response_data = {
            'data': results.to_dict(orient='records'),
            'meta': {
                'query': query,
                'total': len(results),
                'returned': min(len(results), 100),
                'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f"ERRO na busca: {type(e).__name__} - {str(e)}")
        return jsonify({'error': 'Erro ao processar busca'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)