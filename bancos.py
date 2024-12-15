import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

file_id = '1s8LmHMExpr1DgCm88FBZGc1Vxg9TxIjl'
url = f'https://drive.google.com/uc?id={file_id}'
output = 'capital.csv'  # Nome do arquivo que você quer salvar

gdown.download(url, output, quiet=False)

capital_resumo = pd.read_csv(output)

st.write(capital_resumo)
