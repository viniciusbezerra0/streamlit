import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

def baixar(arquivo, id):
    url = f'https://drive.google.com/uc?id={id}'
    gdown.download(url, arquivo, quiet=False)
    return pd.read_csv(arquivo)

ativo = baixar("perc_pf.csv", "1QKPGQiP6QIPQDMQg9Ygdlfg4l3snkZYI")

st.table(ativo)
