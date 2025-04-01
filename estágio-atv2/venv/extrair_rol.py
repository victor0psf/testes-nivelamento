import os
import requests
import pdfplumber
import pandas as pd
import zipfile

# URL do PDF do Anexo I da ANS
url_pdf = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
caminho_pdf = "Anexo_I_Rol_2021.pdf"

# Baixar o PDF da URL
print("Baixando o PDF do Anexo I...")
resposta = requests.get(url_pdf)

if resposta.status_code == 200:
    with open(caminho_pdf, "wb") as arquivo_pdf:
        arquivo_pdf.write(resposta.content)
    print("PDF baixado com sucesso!")
else:
    print("Erro ao baixar o PDF.")
    exit()

# Lista para armazenar os dados extraídos do PDF
dados_tabela = []

print("Extraindo dados da tabela do PDF...")
with pdfplumber.open(caminho_pdf) as pdf:
    for pagina in pdf.pages:
        tabelas = pagina.extract_table()  # Extrai tabelas da página
        if tabelas:  # Certifique-se de que há uma tabela na página
            for linha in tabelas:
                if linha:  # Evita adicionar linhas vazias
                    dados_tabela.append(linha)  # Adiciona cada linha na lista

# Criar um DataFrame (tabela estruturada) com os dados extraídos
tabela_df = pd.DataFrame(dados_tabela).dropna(how='all')

tabela_df.columns = [
    "PROCEDIMENTO", "RN", "VIGÊNCIA", "OD", "AMB", "HCO", "HSO", 
    "REF", "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPÍTULO"
    ]
# Dicionário para substituir as abreviações OD e AMB
substituicoes = {
    "OD": "Procedimento odontológico",
    "AMB": "Procedimento ambulatorial"
}

# Aplicar as substituições na tabela
tabela_df.replace(substituicoes, inplace=True)

# Salvar a tabela em um arquivo CSV
nome_arquivo_csv = "Rol_de_Procedimentos.csv"
tabela_df.to_csv(nome_arquivo_csv, index=False, encoding="utf-8-sig")

# Compactar o CSV em um arquivo ZIP
nome_arquivo_zip = "Teste_Paulo_Victor.zip"
with zipfile.ZipFile(nome_arquivo_zip, "w") as arquivo_zip:
    arquivo_zip.write(nome_arquivo_csv, os.path.basename(nome_arquivo_csv))

print(f"Processo concluído! Arquivo compactado: {nome_arquivo_zip}")
 