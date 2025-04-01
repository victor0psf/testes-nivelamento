import os
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
from zipfile import ZipFile


url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
requerimento = requests.get(url)
soup = BeautifulSoup(requerimento.text, 'html.parser')


pdf_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if 'Anexo I' in href and href.endswith('.pdf'):
        pdf_links.append(href)
    elif 'Anexo II' in href and href.endswith('.pdf'):
        pdf_links.append(href)

os.makedirs('anexos', exist_ok=True)
for pdf_url in pdf_links:
    pdf_name = pdf_url.split('/')[-1]
    pdf_path = os.path.join('anexos', pdf_name)
    with open(pdf_path, 'wb') as f:
        f.write(requests.get(pdf_url).content)
    print(f"Baixando: {pdf_name}")


zip_path = 'anexos_ans.zip'
with ZipFile(zip_path, 'w') as zipf:
    for file in os.listdir('anexos'):
        zipf.write(os.path.join('anexos', file), file)
print(f"Arquivos compactados em: {zip_path}")