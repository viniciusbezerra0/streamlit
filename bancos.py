import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

capital_resumo = pd.read_csv("https://drive.google.com/uc?id=12xnRhBcTi_0bryw1OcwSl9V19VWNlEQy")
resumo_financeiro = pd.read_csv("https://drive.google.com/uc?id=14jyMjIe3P9HUUypmmpWd806XexYCtj-c")
ativo = pd.read_csv("https://drive.google.com/uc?id=1R_y8vtNABZO35PeoyuvZouEZDYIuBJdm")
passivo = pd.read_csv("https://drive.google.com/uc?id=1dhHMgSIC_bvdblg2OzMmr1kHYA7fYSIX")
dre = pd.read_csv("https://drive.google.com/uc?id=1eiRk3ZnPlSRMyp4ZoiFKg-M4d7MQmSBz")
eh_historico = pd.read_csv("https://drive.google.com/uc?id=1Ss1pmXRrvxT0FH775ok9dBYogF3QLDxm")
resumo_risco = pd.read_csv("https://drive.google.com/uc?id=1P3uuEzSlofgdNH_TK04MxYZU2Q_Wq7QA")
resumo_geografico = pd.read_csv("https://drive.google.com/uc?id=1nDsVB6rbBPTMkDP6jzSI8UT6hInDFVp7")
carteira_pf = pd.read_csv("https://drive.google.com/uc?id=1SYqSqDg_cYQMHSYzqP8p6PCM0-L9v5ha")
carteira_pj = pd.read_csv("https://drive.google.com/uc?id=1125I0cQmhvCR7_oO60PQmpZicC5wY9ld")
perc_pf = pd.read_csv("https://drive.google.com/uc?id=1luCZeOTeLhoZ9N-mbNbNxW7pMN8h0IjR")

st.table(capital_resumo[:10])
