
LOAD DATA INFILE 'C:/Users/victo/Desktop/teste-nivelamento/estágio-atv3/data/operadoras_utf8'
INTO TABLE operadoras
CHARACTER SET latin1
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, 
 logradouro, numero, complemento, bairro, cidade, uf, cep, 
 ddd, telefone, fax, email, representante, cargo_representante, 
 @data_registro_ans)
SET data_registro_ans = STR_TO_DATE(@data_registro_ans, '%Y-%m-%d');

-- Importação das demonstrações contábeis (executar para cada arquivo)
LOAD DATA INFILE 'C:/Users/victo/Desktop/teste-nivelamento/estágio-atv3/data/demonstrações'
INTO TABLE demonstracoes_contabeis
CHARACTER SET latin1
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, @competencia, conta_contabil, descricao, valor, tipo)
SET competencia = STR_TO_DATE(CONCAT('01/', @competencia), '%d/%m/%Y');