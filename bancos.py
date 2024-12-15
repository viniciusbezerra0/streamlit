import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

def baixar(arquivo, id):
    url = f'https://drive.google.com/uc?id={id}'
    gdown.download(url, arquivo, quiet=False)
    return pd.read_csv(arquivo)

capital_resumo = baixar("capital.csv", "12xnRhBcTi_0bryw1OcwSl9V19VWNlEQy")
resumo_financeiro = baixar("resumo_consolidado.csv", "14jyMjIe3P9HUUypmmpWd806XexYCtj-c")
ativo = baixar("ativo.csv", "1R_y8vtNABZO35PeoyuvZouEZDYIuBJdm")
passivo = baixar("passivo.csv", "1dhHMgSIC_bvdblg2OzMmr1kHYA7fYSIX")
dre = baixar("dre.csv", "1eiRk3ZnPlSRMyp4ZoiFKg-M4d7MQmSBz")
eh_historico = baixar("eh_historico.csv", "1Ss1pmXRrvxT0FH775ok9dBYogF3QLDxm")
resumo_risco = baixar("carteira_risco_resumo.csv", "1P3uuEzSlofgdNH_TK04MxYZU2Q_Wq7QA")
resumo_geografico = baixar("carteira_geografica_resumo.csv", "1nDsVB6rbBPTMkDP6jzSI8UT6hInDFVp7")
carteira_pf = baixar("carteira_pf_resumo.csv", "1SYqSqDg_cYQMHSYzqP8p6PCM0-L9v5ha")
carteira_pj = baixar("carteira_pj_resumo.csv", "1125I0cQmhvCR7_oO60PQmpZicC5wY9ld")
perc_pf = baixar("perc_pf.csv", "1luCZeOTeLhoZ9N-mbNbNxW7pMN8h0IjR")
