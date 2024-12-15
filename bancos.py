import streamlit as st
import pandas as pd
import plotly.express as px

file_id = '1s8LmHMExpr1DgCm88FBZGc1Vxg9TxIjl'
url = f'https://drive.google.com/uc?id={file_id}'
output = 'capital.csv'  # Nome do arquivo que você quer salvar

# Baixar o arquivo CSV do Google Drive
gdown.download(url, output, quiet=False)

# Carregar o CSV em um DataFrame
capital_resumo = pd.read_csv(output)

# Mostrar o DataFrame no Streamlit
import streamlit as st
st.write(capital_resumo)
