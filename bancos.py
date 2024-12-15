import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

def baixar(arquivo, url):
    gdown.download(url, arquivo, quiet=False)
    return pd.read_csv(arquivo)

ativo = baixar("ativo.csv", "https://drive.google.com/file/d/12xnRhBcTi_0bryw1OcwSl9V19VWNlEQy/view?usp=drive_link")

st.table(ativo)
