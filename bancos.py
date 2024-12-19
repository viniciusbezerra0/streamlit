import streamlit as st
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

path = "C:/Users/vini/OneDrive - Heritage Capital Partners/Network/Analises/03_Bancos/Dash/bases/"

#streamlit run "C:/Users/vini/OneDrive - Heritage Capital Partners/Network/Analises/03_Bancos/Dash/bancos-vinicius.py"

image_path = "https://www.dropbox.com/scl/fi/3gra61tqh9pstrav9dyfs/logo.png?rlkey=3yayojmnxi56nm12mjzzv46lv&st=692dwho6&dl=1"

links0 = [['ativo.csv','https://drive.google.com/file/d/1pasfIKhQB9s7grPZLbRyynFRkN6AgQ76/view?usp=drive_link'],
       ['capital.csv','https://drive.google.com/file/d/13OJ7Q-GNhsjd41uUqki9mMhshva-FS4t/view?usp=drive_link'],
       ['carteira_geografica_resumo.csv', 'https://drive.google.com/file/d/13OJ7Q-GNhsjd41uUqki9mMhshva-FS4t/view?usp=drive_link'],
       ['carteira_pf_resumo.csv', 'https://drive.google.com/file/d/13d0HaciSmsnhavAfGqdFwJLInwnwbI-o/view?usp=drive_link'],
       ['carteira_pj_resumo.csv', 'https://drive.google.com/file/d/1OcAiiqBPkUcnwHXPbrHZlJcQc63vxIjN/view?usp=drive_link'],
       ['carteira_risco_resumo.csv', 'https://drive.google.com/file/d/1FdZtFvhIiFcNLThWdw9--gROxc2-eWAc/view?usp=drive_link'],
       ['carteirapfpj.csv', 'https://drive.google.com/file/d/1L0u8GhHdaKr7-l4bAV-g3nJ-g_AjKiQ-/view?usp=drive_link'],
       ['dre.csv', 'https://drive.google.com/file/d/1cjivizrLkw8v4AHPyHoMfFuG-WLI65nb/view?usp=drive_link'],
       ['eh_historico.csv', 'https://drive.google.com/file/d/1x4DxSNDDb-4NjckPGDZ4ZJ5IyEBxRHPt/view?usp=drive_link'],
       ['empresastrimestres.csv', 'https://drive.google.com/file/d/16E18UoQVFXx1jVwc1g9flosORJ4mSfAK/view?usp=drive_link'],
       ['passivo.csv', 'https://drive.google.com/file/d/1ffbdj-yuTrzG_AFBcGCF-VEFo_uWhDAI/view?usp=drive_link'],
       ['perc_pf.csv', 'https://drive.google.com/file/d/1Knu9ZlKMefRAxqRVLHPw8oJloNk3LAmS/view?usp=drive_link'],
       ['resumo_consolidado.csv', 'https://drive.google.com/file/d/1l_g9Y-8dMIqiVaUNUvbgcF2m-VsVHJcE/view?usp=drive_link']]

links = []
#for i in range(len(links0)):
    #links.append([links0[i][0], path + links0[i][0]])
for i in range(len(links0)):
    links.append([links0[i][0], f'https://drive.google.com/uc?id={re.search(r'd/([^/]+)', links0[i][1]).group(1)}'])


html = f"""
    <style>
        .centered-image {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }}
    </style>
    <div class="centered-image">
        <img src="{image_path}" width="100">
    </div>
    </br>
"""

st.sidebar.markdown(html, unsafe_allow_html=True)


cat=st.sidebar.selectbox("",["Escolha a categoria", "Principais indicadores","Carteira","Resumo", "Demonstrativos", "Passivo"])

if cat != "Escolha a categoria":
    emptri = pd.read_csv(next(link for nome, link in links if nome == 'empresastrimestres.csv'))
    empresas = list(emptri['0'].unique())
    trimestres = list(emptri['1'].unique())

if cat=="Principais indicadores":

    capital_resumo = []
    resumo_financeiro = []

    col1, col2 = st.columns(2)
    with col1:
        filtro=st.multiselect("Selecione as empresas", empresas)
        if len(filtro) > 0:
            
            if len(capital_resumo) < 1:
                capital_resumo = pd.read_csv(next(link for nome, link in links if nome == 'capital.csv'))
                resumo_financeiro = pd.read_csv(next(link for nome, link in links if nome == 'resumo_consolidado.csv'))
                resumo_financeiro_invertido = resumo_financeiro.iloc[::-1]
            capital_resumo_filtrado = capital_resumo[capital_resumo["Empresa"].isin(filtro)]
            capital_resumo_filtrado = capital_resumo_filtrado[capital_resumo_filtrado["Nome"]=="CET1"]
            fig = px.line(
            capital_resumo_filtrado,
            x='AnoMes',  # Eixo X
            y='Saldo',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='CET1',  # Título do gráfico
            labels={'AnoMes': 'Ano e Mês', 'Saldo': '%'}
            )
            fig.update_yaxes(tickformat=".1%", title="Porcentagem")
            st.plotly_chart(fig)
            capital_resumo_filtrado= capital_resumo[capital_resumo["Empresa"].isin(filtro)]
            capital_resumo_filtrado= capital_resumo_filtrado[capital_resumo_filtrado["Nome"]=="basileia"]
            fig = px.line(
            capital_resumo_filtrado,
            x='AnoMes',  # Eixo X
            y='Saldo',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='Basileia',  # Título do gráfico
            labels={'AnoMes': 'Ano e Mês', 'Saldo': '%'}
            )
            fig.update_yaxes(tickformat=".1%")
            st.plotly_chart(fig)
        
            resumo_financeiro_filtrado=resumo_financeiro_invertido[resumo_financeiro_invertido["Empresa"].isin(filtro)]
            resumo_financeiro_filtrado= resumo_financeiro_filtrado[resumo_financeiro_filtrado["NomeColuna"]=="ROAE"]

            fig = px.bar(
            resumo_financeiro_filtrado,
            x='AnoMes',  # Eixo X
            y='Saldo',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='ROAE',  # Título do gráfico
            labels={'AnoMes': 'Ano e Mês', 'Saldo': 'ROAE'}, barmode='group')
            fig.update_yaxes(tickformat=".1%", title="Porcentagem")
            st.plotly_chart(fig)
            resumo_financeiro_filtrado= resumo_financeiro_invertido[resumo_financeiro_invertido["Empresa"].isin(filtro)]
            resumo_financeiro_filtrado= resumo_financeiro_filtrado[resumo_financeiro_filtrado["NomeColuna"]=="Lucro liquido trimestral"]

            fig = px.bar(
            resumo_financeiro_filtrado,
            x='AnoMes',  # Eixo X
            y='Saldo',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='Lucro Líquido',  # Título do gráfico
            labels={'AnoMes': 'Tri', 'Saldo': 'Lucro Líquido'}, barmode='group')
            st.plotly_chart(fig)

            carteiracla = resumo_financeiro[resumo_financeiro["Empresa"].isin(filtro)]
            carteiracla = carteiracla[carteiracla['NomeColuna'] == 'Carteira de Credito Classificada'].reset_index(drop=True)
            fig = px.line(
            carteiracla,
            x='AnoMes',  # Eixo X
            y='Saldo',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='Carteira Classificada',  # Título do gráfico
            labels={'AnoMes': 'Tri', 'Saldo': 'Carteira Classificada'})
            fig.update_layout(xaxis_title="Ano e Mês", yaxis_title="Saldo")
            st.plotly_chart(fig)


    with col2:
        filtro_unico=st.selectbox("", ["Selecione a empresa"] + empresas)
        if filtro_unico != "Selecione a empresa":
            if len(capital_resumo) < 1:
                capital_resumo = pd.read_csv(next(link for nome, link in links if nome == 'capital.csv'))
                resumo_financeiro = pd.read_csv(next(link for nome, link in links if nome == 'resumo_consolidado.csv'))
            capital_resumo_filtrado= capital_resumo[capital_resumo["Empresa"]==filtro_unico]
            fig = px.bar(
            capital_resumo_filtrado[capital_resumo_filtrado["Nome"].isin(['CET1', 'AT1', 'tier_2'])],
            x="AnoMes",         # Eixo horizontal
            y="Saldo",          # Eixo vertical
            color="Nome",       # Categorias empilhadas
            title="Decomposição Capital",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo", "grupo": "Grupo"})

            # Configurando o layout do gráfico
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_yaxes(tickformat=".1%")
            st.plotly_chart(fig)

            rwa = resumo_financeiro[resumo_financeiro["Empresa"]==filtro_unico].reset_index(drop=True)
            indice = [1] * len(trimestres)
            for i in range(len(rwa)):
                if rwa['NomeColuna'][i] == 'Patrimonio de Referencia para Comparacao com o RWA':
                    indice[trimestres.index(rwa['AnoMes'][i])] *= rwa['Saldo'][i]
                elif rwa['NomeColuna'][i] == 'Indice de Basileia':
                    indice[trimestres.index(rwa['AnoMes'][i])] /= rwa['Saldo'][i]
                    
            for i in range(len(indice)):
                if indice[i] > 1:
                    x = rwa.iloc[0].copy()
                    x['NomeColuna'] = 'Ativos Ponderados pelo Risco (RWA)'
                    x['AnoMes'] = trimestres[i]
                    x['Saldo'] = indice[i]
                    rwa.loc[len(rwa)] = x

            cols = ['Patrimonio de Referencia para Comparacao com o RWA', 'Ativos Ponderados pelo Risco (RWA)']
            rwa_2 = rwa[rwa["NomeColuna"].isin(cols)]
            fig = px.line(
            rwa_2,
            x='AnoMes',  # Eixo X
            y='Saldo',  # Eixo Y
            color='NomeColuna',  # Colorir as linhas por empresa
            title='Basileia',  # Título do gráfico
            labels={'AnoMes': 'Ano e Mês', 'Saldo': 'Saldo'}
            )
            

            basi = rwa[rwa["NomeColuna"] == 'Indice de Basileia']
            fig.add_trace(
                go.Scatter(
                    x=basi['AnoMes'],  # Eixo X
                    y=basi['Saldo'],  # Eixo Y secundário
                    mode='lines',
                    name='Indice de Basileia',  # Nome da linha
                    yaxis='y2'  # Definir este trace para usar o eixo Y secundário
                )
            )

            # Configurar o eixo Y secundário
            fig.update_layout(
                yaxis2=dict(
                    title='Indice de Basileia',  # Título do eixo Y secundário
                    overlaying='y',  # Este eixo sobrepõe o eixo Y principal
                    side='right',  # Colocar o eixo à direita
                    tickformat=".2f"  # Formato de exibição para o eixo Y secundário
                )
            )

            # Exibir o gráfico
            st.plotly_chart(fig)



if cat=="Carteira":
    st.markdown("### Análise da carteira")

    codfin = pd.read_excel(path + "codigos_financeiros.xlsx")
    empresas = list(codfin["Empresa"].unique())

    col1, col2 = st.columns(2)
    with col1:
        filtro=st.multiselect("Selecione as empresas", empresas)
    with col2:
        filtro_unico=st.selectbox("", ["Selecione a empresa"] + empresas)
        data=st.selectbox("Selecione a data", trimestres[::-1])

    if len(filtro) > 0 or filtro_unico != "Selecione a empresa":

        #st.columns(1,2)
        anos = range(2009,2025)  # Adapte para o intervalo de anos que você deseja
        ordem_trimestres = [f'{i}T{str(ano)[-2:]}' for ano in anos for i in range(1, 5)]

        # Garantir que 'AnoMes' seja tratada como uma categoria ordenada
        eh_historico=pd.read_csv(next(link for nome, link in links if nome == 'eh_historico.csv'))
        eh_historico["AnoMes"]=eh_historico["AnoMes"].astype(str)
        eh_historico['AnoMes'] = pd.Categorical(eh_historico['AnoMes'], categories=ordem_trimestres, ordered=True)
        eh_historico['ordem'] = eh_historico['AnoMes'].apply(lambda x: int(x[2:]) * 10 + int(x[0]))
        eh_historico=eh_historico.sort_values(by='ordem')
        empresas=eh_historico["Empresa"].unique()

        ordem_trimestres = [f'{i}T{str(year)[-2:]}' for year in range(2009, 2025) for i in range(1, 5)]

        # Definir 'AnoMes' como uma variável categórica com a ordem correta
        eh_historico['AnoMes'] = pd.Categorical(eh_historico['AnoMes'], categories=ordem_trimestres, ordered=True)
        resumo_risco=pd.read_csv(next(link for nome, link in links if nome == 'carteira_risco_resumo.csv'))
        
        resumo_geografico=pd.read_csv(next(link for nome, link in links if nome == "carteira_geografica_resumo.csv"))

        
        carteira_pf=pd.read_csv(next(link for nome, link in links if nome == 'carteira_pf_resumo.csv'))
        carteira_pf['ordem'] = carteira_pf['AnoMes'].apply(lambda x: int(x[2:]) * 10 + int(x[0]))
        carteira_pf=carteira_pf.sort_values(by='ordem')
        carteira_pf=carteira_pf.drop_duplicates(subset=['Grupo', 'Empresa', 'AnoMes'])

        carteira_pj=pd.read_csv(next(link for nome, link in links if nome == 'carteira_pj_resumo.csv'))
        carteira_pj['ordem'] = carteira_pj['AnoMes'].apply(lambda x: int(x[2:]) * 10 + int(x[0]))
        carteira_pj=carteira_pj.sort_values(by='ordem')
        carteira_pj=carteira_pj.drop_duplicates(subset=['Grupo', 'Empresa', 'AnoMes'])

        perc_pf=pd.read_csv(next(link for nome, link in links if nome == 'perc_pf.csv'))
        
        carteirapfpj = pd.read_csv(next(link for nome, link in links if nome == 'carteirapfpj.csv'))


        col1, col2 = st.columns(2)
        with col1:
            selecao_eh=eh_historico[eh_historico["Empresa"].isin(filtro)]
            fig = px.line(
            selecao_eh,
            x='AnoMes',  # Eixo X
            y='Saldo_Percentual',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='% EH',  # Título do gráfico
            labels={'AnoMes': 'Ano e Mês', 'Saldo_Percentual': 'Saldo Percentual'}
        )
            fig.update_yaxes(tickformat=".1%", title="Porcentagem")
            
            st.plotly_chart(fig)
            
        with col2:
            resumo_risco_filtrado=resumo_risco[resumo_risco["Empresa"]==filtro_unico]
            resumo_risco_filtrado = resumo_risco_filtrado.drop_duplicates(subset=['NomeColuna', 'Empresa', 'AnoMes'])
            resumo_risco_filtrado=resumo_risco_filtrado[resumo_risco_filtrado["AnoMes"]==data]
            fig = px.pie(resumo_risco_filtrado, values="Saldo_Percentual", names="NomeColuna", title="Distribuição do risco")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': resumo_risco_filtrado['AnoMes'].tolist()})
            st.plotly_chart(fig)
            # Exibindo o gráfico no Streamlit

        #%%#
        col1, col2 = st.columns(2)
        with col1:
            selecao_perc=perc_pf[perc_pf["Empresa"].isin(filtro)]
            fig = px.line(
            selecao_perc,
            x='AnoMes',  # Eixo X
            y='percentual_pf',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='% Carteira PF',  # Título do gráfico
            labels={'AnoMes': 'Ano e Mês', 'Saldo_Percentual': '% PF'}
        )
            fig.update_yaxes(tickformat=".1%", title="Porcentagem")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': selecao_perc['AnoMes'].tolist()})
            st.plotly_chart(fig)


        with col2:
            resumo_geografico_filtrado=resumo_geografico[resumo_geografico["Empresa"]==filtro_unico]
            resumo_geografico_filtrado=resumo_geografico_filtrado[resumo_geografico_filtrado["AnoMes"]==data]
            fig = px.pie(resumo_geografico_filtrado, values="Saldo_Percentual", names="NomeColuna", title="Distribuição Geográfica")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': resumo_geografico_filtrado['AnoMes'].tolist()})
            st.plotly_chart(fig)


            carteira_pf_filtrada=carteira_pf[carteira_pf["Empresa"]==filtro_unico]
            fig = px.bar(
            carteira_pf_filtrada,
            x="AnoMes",         # Eixo horizontal
            y="Saldo",          # Eixo vertical
            color="Grupo",       # Categorias empilhadas
            title="Saldo carteira PF por tipo",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': carteira_pf_filtrada['AnoMes'].tolist()})
            st.plotly_chart(fig)



            pf = carteira_pf_filtrada.reset_index(drop=True)
            listtri = list(pf['AnoMes'].unique())
            soma = [0] * len(listtri)
            for i in range(len(pf)):
                if abs(pf['Saldo'].iloc[i]) > 0:
                    soma[listtri.index(pf['AnoMes'].iloc[i])] += pf['Saldo'].iloc[i]
            for i in range(len(pf)):
                pf.loc[i, 'Saldo'] /= soma[listtri.index(pf.loc[i, 'AnoMes'])]

            fig = px.bar(
            pf,
            x="AnoMes",         # Eixo horizontal
            y="Saldo",          # Eixo vertical
            color="Grupo",       # Categorias empilhadas
            title="Distribução carteira PF por tipo",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': pf['AnoMes'].tolist()})
            st.plotly_chart(fig)


            carteira_pj_filtrada=carteira_pj[carteira_pj["Empresa"]==filtro_unico]
            fig = px.bar(
            carteira_pj_filtrada,
            x="AnoMes",         # Eixo horizontal
            y="Saldo",          # Eixo vertical
            color="Grupo",       # Categorias empilhadas
            title="Saldo carteira Pj por tipo",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': carteira_pj_filtrada['AnoMes'].tolist()})
            st.plotly_chart(fig)


            pj = carteira_pj_filtrada.reset_index(drop=True)
            listtri = list(pj['AnoMes'].unique())
            soma = [0] * len(listtri)
            for i in range(len(pj)):
                if abs(pj['Saldo'].iloc[i]) > 0:
                    soma[listtri.index(pj['AnoMes'].iloc[i])] += pj['Saldo'].iloc[i]
            for i in range(len(pj)):
                pj.loc[i, 'Saldo'] /= soma[listtri.index(pj.loc[i, 'AnoMes'])]

            fig = px.bar(
            pj,
            x="AnoMes",         # Eixo horizontal
            y="Saldo",          # Eixo vertical
            color="Grupo",       # Categorias empilhadas
            title="Distribuição carteira Pj por tipo",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': pj['AnoMes'].tolist()})
            st.plotly_chart(fig)


            carteirapfpj = carteirapfpj[carteirapfpj["Empresa"]==filtro_unico]
            fig = px.bar(
            carteirapfpj,
            x="AnoMes",         # Eixo horizontal
            y="Saldo",          # Eixo vertical
            color="NomeColuna",       # Categorias empilhadas
            title="Saldo carteira PF e PJ por duração",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Duração"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': carteirapfpj['AnoMes'].tolist()})
            st.plotly_chart(fig)



            pfpj = carteirapfpj.reset_index(drop=True)
            listtri = list(pfpj['AnoMes'].unique())
            soma = [0] * len(listtri)
            for i in range(len(pfpj)):
                if abs(pfpj['Saldo'].iloc[i]) > 0:
                    soma[listtri.index(pfpj['AnoMes'].iloc[i])] += pfpj['Saldo'].iloc[i]
            for i in range(len(pfpj)):
                pfpj.loc[i, 'Saldo'] /= soma[listtri.index(pfpj.loc[i, 'AnoMes'])]

            fig = px.bar(
            pfpj,
            x="AnoMes",         # Eixo horizontal
            y="Saldo",          # Eixo vertical
            color="NomeColuna",       # Categorias empilhadas
            title="Distribução carteira PF e PJ por duração",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Duração"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': pfpj['AnoMes'].tolist()})
            st.plotly_chart(fig)


if cat=="Resumo":
    st.markdown("### Resumo")
    col1, col2 = st.columns(2)
    with col1:
        empresas0 = st.multiselect("Selecione as empresas", empresas)
    with col2:
        # O slider seleciona um intervalo entre os trimestres disponíveis
        selected_range = st.select_slider(
                "Selecione os trimestres",
                options=trimestres,  # Passa a lista de trimestres como opções
                value=(trimestres[-4], trimestres[-1]),
        )
    
        # Obtendo os trimestres selecionados
        start_idx = trimestres.index(selected_range[0])
        end_idx = trimestres.index(selected_range[1])

        # Fatiando a lista tri com os índices encontrados
        tris = trimestres[start_idx:end_idx + 1]

    if len(empresas0) > 0 and len(tris) > 2:

        capital_resumo=pd.read_csv(next(link for nome, link in links if nome == 'capital.csv'))
        resumo_financeiro=pd.read_csv(next(link for nome, link in links if nome == 'resumo_consolidado.csv'))
        
        lista = ['Captacoes','Carteira de Credito Classificada','Indice de Basileia','Patrimonio Liquido','Lucro liquido trimestral','ROAE']
        rf = resumo_financeiro[resumo_financeiro['NomeColuna'].isin(lista)]
        
        cr = capital_resumo[capital_resumo['NomeColuna'].str.contains('apital Principa', na=False)]
        df = pd.concat([rf, cr], ignore_index=True)

        def trimestre_to_num(trimestre):
            trimestre_num = int(trimestre[0])  # 1, 2, 3, 4
            ano = int('20' + trimestre[2:])   # 23, 22, etc. para formar 2023, 2022
            return ano * 100 + trimestre_num
        df['Ordenacao'] = df['AnoMes'].apply(trimestre_to_num)
        df = df.sort_values(by='Ordenacao')
        df = df.drop(columns=['Ordenacao'])

        dfs = []
        falt = pd.DataFrame([[0] * (3 * len(empresas0) + 3)] * (len(lista)+1))
        for empresa in empresas0:
            ult = [0] * (len(lista) + 1)
            ltm = [0] * (len(lista) + 1)
            med = [0] * (len(lista) + 1)

        #Lucro Líquido 
            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[4]]
            ult[0] = list(df0['Saldo'])[-1]
            ltm[0] = 4*df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[0] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[0, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[1, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[0, (len(empresas0)+1)*2 - 1] = 1
                falt.loc[1, (len(empresas0)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[0, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[1, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[0, (len(empresas0)+1)*3 - 1] = 1
                falt.loc[1, (len(empresas0)+1)*3 - 1] = 1
                
                
            #Patrimônio Líquido
            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[3]]
            ult[2] = list(df0['Saldo'])[-1]
            ltm[2] = df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[2] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[2, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[1, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[2, (len(empresas0)+1)*2 - 1] = 1
                falt.loc[1, (len(empresas0)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[2, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[1, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[2, (len(empresas0)+1)*3 - 1] = 1
                falt.loc[1, (len(empresas0)+1)*3 - 1] = 1
            
            
            #ROAE
            ult[1] = 4*ult[0]/ult[2]
            ltm[1] = ltm[0]/ltm[2]
            med[1] = 4*med[0]/med[2]

            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[1]]
            ult[3] = list(df0['Saldo'])[-1]
            ltm[3] = df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[3] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[3, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[3, (len(empresas0)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[3, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[3, (len(empresas0)+1)*3 - 1] = 1
                

            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[0]]
            ult[4] = list(df0['Saldo'])[-1]
            ltm[4] = 4*df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[4] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[4, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[4, (len(empresas0)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[4, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[4, (len(empresas0)+1)*3 - 1] = 1
            
            
            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[2]]
            ult[5] = list(df0['Saldo'])[-1]
            ltm[5] = df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[5] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[5, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[5, (len(empresas0)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[5, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[5, (len(empresas0)+1)*3 - 1] = 1
            

            #CET1
            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == cr['NomeColuna'].unique()[1]]
            ult[6] = list(df0['Saldo'])[-1]
            ltm[6] = df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[6] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()
            
            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[6, len(empresas0) + empresas0.index(empresa) + 1] = 1
                falt.loc[6, (len(empresas0)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[6, (len(empresas0) + 1)*2 + empresas0.index(empresa)] = 1
                falt.loc[6, (len(empresas0)+1)*3 - 1] = 1
            

            df0 = pd.DataFrame([ult,ltm,med]).T  # Usando .T para transpor (mudar linhas por colunas)
            df0.columns = [trimestres[-1], 'LTM','Média ' + tris[0] + ' - ' + tris[-1]]
            df0.index = ['Lucro Líquido', 'ROAE', 'Patrimônio Líquido', 'Carteira', 'Captações', 'Basileia','CET1']
            dfs.append(df0)

        pd.DataFrame(falt)

        dfs0 = []
        for i in range(len(dfs[0].keys())):
            df0 = [df.iloc[:, i] for df in dfs]
            df0 = pd.DataFrame(df0).T
            df0['Média'] = df0.mean(axis=1)
            df0.columns = empresas0 + ['Média']
            dfs0.append(df0)
        dfs = pd.concat(dfs0, axis=1, keys=dfs[0].keys())

        dfs.fillna('-')

        def format_number(num):

            if type(num) == str:
                return (num)
            elif abs(num) >= 1_000_000_000_000:
                return f"{num / 1_000_000_000_000:.3f} tri"
                
            elif abs(num) >= 1_000_000_000:
                return f"{num / 1_000_000_000:.3f} bi"
            # Verificar se o número é maior que 1 milhão
            elif abs(num) >= 1_000_000:
                return f"{num / 1_000_000:.3f} mi"
            # Verificar se o número é maior que 1 mil
            elif abs(num) >= 1_000:
                return f"{num / 1_000:.3f} k"
            # Caso o número seja menor que mil
            elif abs(num) <= 3:
                return str(round(num*100,3)) + " %"
            else:
                return f"{num:.3f}"

        dfs = dfs.map(format_number)


        pintar = []
        for i in range(len(falt)):
            for j in range(len(falt.keys())):
                if falt.iloc[i,j] == 1:
                    pintar.append(dfs.iloc[i, j])

        def colorir(val):
            if val in pintar:
                color = 'color: orange'
            else:
                color = ''
            return color
            
        dfs = dfs.style.map(colorir)

        s = 0
        for i in range(len(falt)):
            s += sum(falt.iloc[i,:])

        st.table(dfs)
        if s > 0:
            st.write('*Os dados laranjas são imprecisos')



if cat=="Demonstrativos":
    st.markdown("### Demonstrativos")
    col1, col2 = st.columns(2)
    with col1:
        empresa = st.selectbox("", ["Selecione a empresa"] + empresas)
    with col2:
        # O slider seleciona um intervalo entre os trimestres disponíveis
        selected_range = st.select_slider(
                "Selecione os trimestres",
                options=trimestres,  # Passa a lista de trimestres como opções
                value=(trimestres[-4], trimestres[-1]),
        )
    
        # Obtendo os trimestres selecionados
        start_idx = trimestres.index(selected_range[0])
        end_idx = trimestres.index(selected_range[1])

        # Fatiando a lista tri com os índices encontrados
        tris = trimestres[start_idx:end_idx + 1]

    def csv(df):
        return df.to_csv(index=False).encode('utf-8')
    

    if empresa != "Selecione a empresa" and len(tris) > 2:
        
        
        col3, col4 = st.columns(2)
        with col3:
            demonstrativo = st.selectbox("", ['Escolha o demonstrativo', 'Balanço patrimonial', 'DRE'])

            # Obtendo os trimestres selecionados
            start_idx = trimestres.index(selected_range[0])
            end_idx = trimestres.index(selected_range[1])

            # Fatiando a lista tri com os índices encontrados
            tris = trimestres[start_idx:end_idx + 1]

        def format_number(num):

            if type(num) == str:
                return (num)
            elif abs(num) >= 1_000_000_000_000:
                return f"{num / 1_000_000_000_000:.3f} tri"
                
            elif abs(num) >= 1_000_000_000:
                return f"{num / 1_000_000_000:.3f} bi"
            # Verificar se o número é maior que 1 milhão
            elif abs(num) >= 1_000_000:
                return f"{num / 1_000_000:.3f} mi"
            # Verificar se o número é maior que 1 mil
            elif abs(num) >= 1_000:
                return f"{num / 1_000:.3f} k"
            else:
                return f"{num:.3f}"

        bpdown = []
        resdown = []

        if demonstrativo == 'Balanço patrimonial':

            ativo = pd.read_csv(next(link for nome, link in links if nome == 'ativo.csv'))
            passivo = pd.read_csv(next(link for nome, link in links if nome == 'passivo.csv'))
            bp = pd.concat([ativo,passivo])

            def trimestre_to_num(trimestre):
                trimestre_num = int(trimestre[0])  # 1, 2, 3, 4
                ano = int('20' + trimestre[2:])   # 23, 22, etc. para formar 2023, 2022
                return ano * 100 + trimestre_num
            bp['Ordenacao'] = bp['AnoMes'].apply(trimestre_to_num)
            bp = bp.sort_values(by='Ordenacao')
            bp = bp.drop(columns=['Ordenacao'])

            ordem = []
            cols = []
            atv = ativo[ativo['Empresa'] == empresa]
            for i in ativo['NomeColuna'].unique():
                ordem.append( i[i.index("(")+1:i.index(")")] )
                cols.append( i )
            ind = sorted(range(len(ordem)), key=lambda i: ordem[i])
            ind = [cols[i] for i in ind]
            
            atri = []
            for i in tris:
                x = atv[atv['AnoMes'] == i]
                x = x[['NomeColuna','Saldo']]
                x.columns = ['',i]
                x.set_index('', inplace=True)
                atri.append(x)
            atv  = pd.concat(atri, axis=1)
            ind0 = [x for x in ind if x in list(atv.index)]
            atv = atv.loc[ind0]
    
            
            ordem = []
            cols = []
            psv = passivo[passivo['Empresa'] == empresa]
            for i in psv['NomeColuna'].unique():
                ordem.append( i[i.index("(")+1:i.index(")")] )
                cols.append( i )
            ind = sorted(range(len(ordem)), key=lambda i: ordem[i])
            ind = [cols[i] for i in ind]
            
            ptri = []
            for i in tris:
                x = psv[psv['AnoMes'] == i]
                x = x[['NomeColuna','Saldo']]
                x.columns = ['',i]
                x.set_index('', inplace=True)
                ptri.append(x)
            psv  = pd.concat(ptri, axis=1)
            ind0 = [x for x in ind if x in list(psv.index)]
            psv = psv.loc[ind0]
    
    
            bp = pd.concat([atv,psv])
            index = []
            for i in bp.index:
                index.append(i[:i.index("(")-2])
            bp.index = index
            
            bp = bp.groupby(bp.index, sort=False).sum()
            bp = bp[~(bp.eq(0).all(axis=1))]

            bpdown = csv(bp.copy())

            bp.fillna('-')
            bp = bp.map(format_number)

            st.table(bp)

            with col4:
                st.download_button(
                    label="Baixar demonstrativo",
                    data=bpdown,
                    file_name="bp " + empresa + " " + tris[0] + "-" + tris[-1] + ".csv",
                    mime="text/csv"
                )

        elif demonstrativo == "DRE":

            dre = pd.read_csv(next(link for nome, link in links if nome == 'dre.csv'))

            res = dre[dre['Empresa'] == empresa].reset_index()
            def trimestre_to_num(trimestre):
                trimestre_num = int(trimestre[0])  # 1, 2, 3, 4
                ano = int('20' + trimestre[2:])   # 23, 22, etc. para formar 2023, 2022
                return ano * 100 + trimestre_num
            res['Ordenacao'] = res['AnoMes'].apply(trimestre_to_num)
            res = res.sort_values(by='Ordenacao')
            res = res.drop(columns=['Ordenacao'])

            ordem = []
            cols = []
            res = dre[dre['Empresa'] == empresa].reset_index()

            for i in range(len(res)):
                if int(res['AnoMes'][i][0])%2 == 0:
                    restri = res[res['AnoMes'] == str(int(res['AnoMes'][i][0]) - 1) + res['AnoMes'][i][1:]]
                    res.loc[i,'Saldo'] = res['Saldo'].iloc[i]- restri[restri['NomeColuna'] == res['NomeColuna'][i]]['Saldo'].iloc[0]
            
            for i in dre['NomeColuna'].unique():
                ordem.append( i[i.index("(")+1:i.index(")")] )
                cols.append( i )
            ind = sorted(range(len(ordem)), key=lambda i: ordem[i])
            ind = [cols[i] for i in ind]
            
            rtri = []
            for i in tris:
                x = res[res['AnoMes'] == i]
                x = x[['NomeColuna','Saldo']]
                x.columns = ['',i]
                x.set_index('', inplace=True)
                rtri.append(x)
            res  = pd.concat(rtri, axis=1)
            ind0 = [x for x in ind if x in list(res.index)]
            res = res.loc[ind0]

            index = []
            for i in res.index:
                index.append(i[:i.index("(")-2])
            res.index = index
            
            res = res.groupby(res.index, sort=False).sum()
            res = res[~(res.eq(0).all(axis=1))]

            resdown = csv(res.copy())

            res.fillna('-')
            res = res.map(format_number)

            st.table(res)

            with col4:
                st.download_button(
                    label="Baixar demonstrativo",
                    data=resdown,
                    file_name="dre " + empresa + " " + tris[0] + "-" + tris[-1] + ".csv",
                    mime="text/csv"
                )


if cat=="Passivo":
    st.markdown("### Passivo")

    col1, col2 = st.columns(2)
    with col1:
        empresas0=st.multiselect("Selecione as empresas", empresas)
    with col2:
        empresa=st.selectbox("", ["Selecione a empresa"] + empresas)
        data=st.selectbox("Selecione a data", trimestres[::-1])

    if len(empresas) > 0 or empresa != "Selecione a empresa":

        passivo = pd.read_csv(next(link for nome, link in links if nome == 'passivo.csv'))

        for i in passivo['NomeColuna'].unique():
            if 'aptac' in i:
                col = i
                break

        passivocap = passivo[passivo["Empresa"].isin(empresas0)]
        passivocap = passivocap[passivocap['NomeColuna'] == col]

        col1, col2 = st.columns(2)
        with col1:

            fig = px.line(
            passivocap,
            x='AnoMes',  # Eixo X
            y='Saldo',  # Eixo Y
            color='Empresa',  # Colorir as linhas por empresa
            title='Captações totais',  # Título do gráfico
            labels={'AnoMes': 'Ano e Mês', 'Saldo': '%'})

            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': passivocap['AnoMes'].tolist()})
            st.plotly_chart(fig)



        for i in passivo['NomeColuna'].unique():
            if 'eposito Total' in i:
                col01 = i
                break
        for i in passivo['NomeColuna'].unique():
            if 'peracoes Compromissada' in i:
                col02 = i
                break
        for i in passivo['NomeColuna'].unique():
            if i[1:7] == 'ecurso':
                col03 = i
                break
        for i in passivo['NomeColuna'].unique():
            if 'oes por Emprestimos e Repasse' in i:
                col04 = i
                break
        cols = [col01,col02,col03,col04]

        passivoemp = passivo[passivo['Empresa'] == empresa] 

        with col2:

            passivoabcd = passivoemp[passivoemp["NomeColuna"].isin(cols)].reset_index(drop=True)

            fig = px.bar(
            passivoabcd,
            x="AnoMes", 
            y="Saldo",     
            color="NomeColuna",  
            title="Tipos de captações",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "NomeColuna": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': passivoabcd['AnoMes'].tolist()})
            st.plotly_chart(fig)


            
            listtri = list(passivoabcd['AnoMes'].unique())
            soma = [0] * len(listtri)
            for i in range(len(passivoabcd)):
                if abs(passivoabcd['Saldo'].iloc[i]) > 0:
                    soma[listtri.index(passivoabcd['AnoMes'].iloc[i])] += passivoabcd['Saldo'].iloc[i]
            for i in range(len(passivoabcd)):
                passivoabcd.loc[i, 'Saldo'] /= soma[listtri.index(passivoabcd.loc[i, 'AnoMes'])]
            
            fig = px.bar(
            passivoabcd,
            x="AnoMes", 
            y="Saldo",     
            color="NomeColuna",  
            title="Distribuição das captações",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "NomeColuna": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': passivoabcd['AnoMes'].tolist()})
            st.plotly_chart(fig)



            cols = ['Depositos a Vista  (a1)', 'Depositos de Poupanca  (a2)', 'Depositos Interfinanceiros  (a3)', 'Depositos a Prazo  (a4)', 'Outros Depositos  (a5)', 'Depositos Outros  (a6)', 'Obrigacoes por Operacoes Compromissadas  (b)', 'Letras de Credito Imobiliario  (c1)', 'Letras de Credito do Agronegocio  (c2)', 'Letras Financeiras  (c3)', 'Obrigacoes por Titulos e Valores Mobiliarios no Exterior  (c4)', 'Outros Recursos de Aceites e Emissao de Titulos  (c5)', 'Obrigacoes por Emprestimos e Repasses  (d)']
            passivoacd = passivoemp[passivoemp["NomeColuna"].isin(cols)].reset_index(drop=True)

            fig = px.bar(
            passivoacd,
            x="AnoMes", 
            y="Saldo",     
            color="NomeColuna",  
            title="Tipos de passivos",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "NomeColuna": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': passivoacd['AnoMes'].tolist()})
            st.plotly_chart(fig)


            listtri = list(passivoacd['AnoMes'].unique())
            soma = [0] * len(listtri)
            for i in range(len(passivoacd)):
                if abs(passivoacd['Saldo'].iloc[i]) > 0:
                    soma[listtri.index(passivoacd['AnoMes'].iloc[i])] += passivoacd['Saldo'].iloc[i]
            for i in range(len(passivoacd)):
                passivoacd.loc[i, 'Saldo'] /= soma[listtri.index(passivoacd.loc[i, 'AnoMes'])]
            
            fig = px.bar(
            passivoacd,
            x="AnoMes", 
            y="Saldo",     
            color="NomeColuna",  
            title="Distribuição dos passivos",
            labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "NomeColuna": "Grupo"})
            fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': passivoacd['AnoMes'].tolist()})
            st.plotly_chart(fig)
