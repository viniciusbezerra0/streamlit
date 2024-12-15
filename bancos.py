import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

def baixar(arquivo, id):
    url = f'https://drive.google.com/uc?id={id}'
    gdown.download(url, arquivo, quiet=False)
    return pd.read_csv(arquivo)

ativo = baixar("ativo.csv", "1R_y8vtNABZO35PeoyuvZouEZDYIuBJdm")
passivo = baixar("passivo.csv", "1dhHMgSIC_bvdblg2OzMmr1kHYA7fYSIX")
dre = baixar("dre.csv", "1eiRk3ZnPlSRMyp4ZoiFKg-M4d7MQmSBz")

st.table(ativo[:10])
