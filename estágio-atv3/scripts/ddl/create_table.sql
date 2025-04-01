-- Tabela de operadoras ativas
CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(18) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE,
    INDEX idx_nome_fantasia (nome_fantasia),
    INDEX idx_cnpj (cnpj)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de demonstrações contábeis
CREATE TABLE demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20) NOT NULL,
    competencia DATE NOT NULL,
    conta_contabil VARCHAR(50) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(15, 2) NOT NULL,
    tipo VARCHAR(20) NOT NULL, -- 'receita' ou 'despesa'
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans),
    INDEX idx_competencia (competencia),
    INDEX idx_conta_contabil (conta_contabil),
    INDEX idx_registro_competencia (registro_ans, competencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;