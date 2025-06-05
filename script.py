import pandas as pd
import matplotlib.pyplot as plt
import requests

# --- Importação da API ---
url = "https://script.google.com/macros/s/AKfycbz6lbNDRjwV_W_Ft_t-pISctlSUNUfUNYQDUYdcivVlch0WTi-dgRSuChtAL_pJwbw/exec"
params = {
    "rota": "comentarios",
    "start_date": "01/03/2024",
    "end_date": "31/03/2025"
}

response = requests.get(url, params=params)
dados = response.json()
df = pd.DataFrame(dados)

# Conversões de data e cálculo do tempo de resolução
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
df['data_resolucao'] = pd.to_datetime(df['data_resolucao'], dayfirst=True, errors='coerce')
df['tempo_resolucao'] = (df['data_resolucao'] - df['data']).dt.days
df['resolvido'] = df['data_resolucao'].notna().replace({True: 'Sim', False: 'Não'})

# Categorização dos comentários
def categorizar_comentario(texto):
    texto = str(texto).lower()
    if 'não recomendo' in texto or 'ruim' in texto:
        return 'Negativo'
    elif 'bom' in texto or 'gostei' in texto:
        return 'Positivo'
    else:
        return 'Neutro'

df['categoria'] = df['comentario'].apply(categorizar_comentario)

# --- Visualizações com matplotlib ---
df['categoria'].value_counts().plot(kind='bar', title='Distribuição das Categorias de Feedback')
plt.xlabel('Categoria')
plt.ylabel('Quantidade')
plt.show()

df.groupby('analista')['tempo_resolucao'].mean().round(1).plot(kind='bar', title='Tempo Médio de Resolução por Analista')
plt.xlabel('Analista')
plt.ylabel('Dias')
plt.show()

# --- Exportação para Google Sheets ---
from gspread_dataframe import set_with_dataframe
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticação
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais-google.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Feedbacks_Clientes")

# Abas do Google Sheets
aba_feedbacks = sheet.worksheet("Feedbacks")

# --- PREPARAÇÃO DOS DADOS DA ABA "FEEDBACKS" ---
df_export = df.copy()

df_export = df_export.rename(columns={
    'data': 'Data do Comentário',
    'apartamento': 'Apartamento',
    'comentario': 'Comentário',
    'obs': 'Observações',
    'analista': 'Analista Responsável',
    'data_resolucao': 'Data da Resolução',
    'tempo_resolucao': 'Tempo para Resolver (Dias)',
    'resolvido': 'Já Resolvido?',
    'categoria': 'Categoria do Comentário'
})

# Ordenação das colunas
colunas_ordenadas = [
    'Data do Comentário',
    'Comentário',
    'Apartamento',
    'Observações',
    'Analista Responsável',
    'Já Resolvido?',
    'Data da Resolução',
    'Tempo para Resolver (Dias)',
    'Categoria do Comentário'
]
df_export = df_export[colunas_ordenadas]

# Ajustes de dados e formatações
for col in df_export.columns:
    if df_export[col].dtype == 'object':
        df_export[col] = df_export[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

df_export.replace(r'^\s*$', pd.NA, regex=True, inplace=True)

df_export['Data do Comentário'] = pd.to_datetime(df_export['Data do Comentário'], errors='coerce').dt.strftime('%d/%m/%Y')
df_export['Data da Resolução'] = pd.to_datetime(df_export['Data da Resolução'], errors='coerce').dt.strftime('%d/%m/%Y')

df_export['Data do Comentário'] = df_export['Data do Comentário'].replace('NaT', pd.NA).fillna('Não informado')
df_export['Data da Resolução'] = df_export['Data da Resolução'].replace('NaT', pd.NA).fillna('Não informado')

df_export['Tempo para Resolver (Dias)'] = df_export['Tempo para Resolver (Dias)'].replace(['nan', 'NaN'], pd.NA)
df_export['Tempo para Resolver (Dias)'] = df_export['Tempo para Resolver (Dias)'].fillna("Ainda não resolvido")

def manter_numero_ou_texto(x):
    if pd.isna(x) or x == "Ainda não resolvido":
        return x
    else:
        return int(x)

df_export['Tempo para Resolver (Dias)'] = df_export['Tempo para Resolver (Dias)'].apply(manter_numero_ou_texto)

for col in df_export.select_dtypes(include='object').columns:
    df_export[col] = df_export[col].fillna("Sem Informação")

df_export.dropna(how='all', inplace=True)

# --- EXPORTAÇÃO ABA "Feedbacks" ---
aba_feedbacks.clear()
set_with_dataframe(aba_feedbacks, df_export)

# --- EXPORTAÇÃO ABA "Resumo por Analista" ---
resumo_analistas = df.groupby('analista')['tempo_resolucao'].mean().round(0).astype(int).reset_index()
resumo_analistas = resumo_analistas.rename(columns={
    'analista': 'Analista',
    'tempo_resolucao': 'Tempo Médio de Resposta (Dias)'
})

try:
    aba_resumo = sheet.worksheet("Resumo por Analista")
except gspread.exceptions.WorksheetNotFound:
    aba_resumo = sheet.add_worksheet(title="Resumo por Analista", rows=100, cols=20)

aba_resumo.clear()
set_with_dataframe(aba_resumo, resumo_analistas)