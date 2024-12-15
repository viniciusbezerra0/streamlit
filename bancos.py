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

bp = pd.concat([ativo,passivo])

empresas=capital_resumo["Empresa"].unique()

anos = range(2009,2025)  # Adapte para o intervalo de anos que você deseja
ordem_trimestres = [f'{i}T{str(ano)[-2:]}' for ano in anos for i in range(1, 5)]

eh_historico["AnoMes"]=eh_historico["AnoMes"].astype(str)
eh_historico['AnoMes'] = pd.Categorical(eh_historico['AnoMes'], categories=ordem_trimestres, ordered=True)
eh_historico['ordem'] = eh_historico['AnoMes'].apply(lambda x: int(x[2:]) * 10 + int(x[0]))
eh_historico=eh_historico.sort_values(by='ordem')
empresas=eh_historico["Empresa"].unique()

ordem_trimestres = [f'{i}T{str(year)[-2:]}' for year in range(2009, 2025) for i in range(1, 5)]

# Definir 'AnoMes' como uma variável categórica com a ordem correta
eh_historico['AnoMes'] = pd.Categorical(eh_historico['AnoMes'], categories=ordem_trimestres, ordered=True)

carteira_pf['ordem'] = carteira_pf['AnoMes'].apply(lambda x: int(x[2:]) * 10 + int(x[0]))
carteira_pf=carteira_pf.sort_values(by='ordem')
carteira_pf=carteira_pf.drop_duplicates(subset=['Grupo', 'Empresa', 'AnoMes'])

carteira_pj['ordem'] = carteira_pj['AnoMes'].apply(lambda x: int(x[2:]) * 10 + int(x[0]))
carteira_pj=carteira_pj.sort_values(by='ordem')


cat=st.sidebar.selectbox("Escolha a categora",["Principais indicadores","Carteira","Resumo", "Demonstrativos"])

if cat=="Principais indicadores":
    col1, col2 = st.columns(2)
    with col1:
        filtro=st.multiselect("Selecione as empresas",empresas)
        capital_resumo_filtrado= capital_resumo[capital_resumo["Empresa"].isin(filtro)]
        capital_resumo_filtrado= capital_resumo_filtrado[capital_resumo_filtrado["Nome"]=="CET1"]
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
        resumo_financeiro_filtrado=resumo_financeiro_invertido[resumo_financeiro_invertido["Empresa"].isin(filtro)]
        resumo_financeiro_filtrado= resumo_financeiro_filtrado[resumo_financeiro_filtrado["NomeColuna"]=="Lucro liquido trimestral"]

        fig = px.bar(
        resumo_financeiro_filtrado,
        x='AnoMes',  # Eixo X
        y='Saldo',  # Eixo Y
        color='Empresa',  # Colorir as linhas por empresa
        title='Lucro Líquido',  # Título do gráfico
        labels={'AnoMes': 'Tri', 'Saldo': 'Lucro Líquido'}, barmode='group')


        st.plotly_chart(fig)
    with col2:
        filtro_unico=st.selectbox("Selecione as empresas",empresas)
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



#aba carteira
if cat=="Carteira":
    st.markdown("### Análise da carteira")
    
    col1, col2 = st.columns(2)
    with col1:
        filtro=st.multiselect("Selecione as empresas",empresas)
    with col2:
        filtro_unico=st.selectbox("Selecione as empresas",empresas)
    col1, col2 = st.columns(2)
    with col2:
        data=st.selectbox("Selecione a data",resumo_geografico["AnoMes"].unique())
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
        st.plotly_chart(fig)
    with col2:
        resumo_geografico_filtrado=resumo_geografico[resumo_geografico["Empresa"]==filtro_unico]
        resumo_geografico_filtrado=resumo_geografico_filtrado[resumo_geografico_filtrado["AnoMes"]==data]
        fig = px.pie(resumo_geografico_filtrado, values="Saldo_Percentual", names="NomeColuna", title="Distribuição Geográfica")
        st.plotly_chart(fig)
        carteira_pf_filtrada=carteira_pf[carteira_pf["Empresa"]==filtro_unico]
        fig = px.bar(
        carteira_pf_filtrada,
        x="AnoMes",         # Eixo horizontal
        y="Saldo",          # Eixo vertical
        color="Grupo",       # Categorias empilhadas
        title="Saldo carteira PF por tipo",
        labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Grupo"})

        # Configurando o layout do gráfico
        fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
        st.plotly_chart(fig)

        carteira_pj_filtrada=carteira_pj[carteira_pj["Empresa"]==filtro_unico]

        fig = px.bar(
        carteira_pj_filtrada,
        x="AnoMes",         # Eixo horizontal
        y="Saldo",          # Eixo vertical
        color="Grupo",       # Categorias empilhadas
        title="Saldo carteira Pj por tipo",
        labels={"AnoMes": "Ano e Mês", "Saldo": "Saldo (em R$)", "grupo": "Grupo"})

        # Configurando o layout do gráfico
        fig.update_layout(barmode="stack", xaxis_title="Ano e Mês", yaxis_title="Saldo")
        st.plotly_chart(fig)


if cat=="Resumo":
    
    lista = ['Captacoes','Carteira de Credito Classificada','Indice de Basileia','Patrimonio Liquido','Lucro liquido trimestral','ROAE']
    rf = resumo_financeiro[resumo_financeiro['NomeColuna'].isin(lista)]
    
    cr = capital_resumo[capital_resumo['NomeColuna'].str.contains('apital Principa', na=False)]
    df = pd.concat([rf, cr], ignore_index=True)
    
    tri = []
    for i in df['AnoMes']:
        if i not in tri:
            tri.append(i)
    
    def sort_key(val):
        year = int(val[-2:]) 
        num = int(val[0])
        return (year, num)  
    tri = sorted(tri, key=sort_key)


    col1, col2 = st.columns(2)
    with col1:
        empresass = st.multiselect("Selecione as empresas",empresas)
    with col2:
        # O slider seleciona um intervalo entre os trimestres disponíveis
        selected_range = st.select_slider(
                "Selecione os trimestres",
                options=tri,  # Passa a lista de trimestres como opções
                value=(tri[-4], tri[-1]),
        )
    
        # Obtendo os trimestres selecionados
        start_idx = tri.index(selected_range[0])
        end_idx = tri.index(selected_range[1])

        # Fatiando a lista tri com os índices encontrados
        tris = tri[start_idx:end_idx + 1]

    if len(empresass) > 0 and len(tris) > 2:
        dfs = []
        falt = pd.DataFrame([[0] * (3 * len(empresass) + 3)] * (len(lista)+1))
        for empresa in empresass:
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
                falt.loc[0, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[1, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[0, (len(empresass)+1)*2 - 1] = 1
                falt.loc[1, (len(empresass)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[0, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[1, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[0, (len(empresass)+1)*3 - 1] = 1
                falt.loc[1, (len(empresass)+1)*3 - 1] = 1
                
                
            #Patrimônio Líquido
            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[3]]
            ult[2] = list(df0['Saldo'])[-1]
            ltm[2] = df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[2] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[2, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[1, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[2, (len(empresass)+1)*2 - 1] = 1
                falt.loc[1, (len(empresass)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[2, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[1, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[2, (len(empresass)+1)*3 - 1] = 1
                falt.loc[1, (len(empresass)+1)*3 - 1] = 1
            
            
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
                falt.loc[3, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[3, (len(empresass)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[3, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[3, (len(empresass)+1)*3 - 1] = 1
                

            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[0]]
            ult[4] = list(df0['Saldo'])[-1]
            ltm[4] = 4*df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[4] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[4, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[4, (len(empresass)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[4, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[4, (len(empresass)+1)*3 - 1] = 1
            
            
            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == lista[2]]
            ult[5] = list(df0['Saldo'])[-1]
            ltm[5] = df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[5] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()

            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[5, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[5, (len(empresass)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[5, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[5, (len(empresass)+1)*3 - 1] = 1
            

            #CET1
            df0 = df[df['Empresa'] == empresa]
            df0 = df0[df0['NomeColuna'] == cr['NomeColuna'].unique()[1]]
            ult[6] = list(df0['Saldo'])[-1]
            ltm[6] = df0[-4:]['Saldo'].sum(skipna=True)/df0[-4:]['Saldo'].count()
            med[6] = df0[-len(tris):]['Saldo'].sum(skipna=True)/df0[-len(tris):]['Saldo'].count()
            
            if df0[-4:]['Saldo'].count() < 4:
                falt.loc[6, len(empresass) + empresass.index(empresa) + 1] = 1
                falt.loc[6, (len(empresass)+1)*2 - 1] = 1
            if df0[-len(tris):]['Saldo'].count() < len(tris):
                falt.loc[6, (len(empresass) + 1)*2 + empresass.index(empresa)] = 1
                falt.loc[6, (len(empresass)+1)*3 - 1] = 1
            

            df0 = pd.DataFrame([ult,ltm,med]).T  # Usando .T para transpor (mudar linhas por colunas)
            df0.columns = [tri[-1], 'LTM','Média ' + tris[0] + ' - ' + tris[-1]]
            df0.index = ['Lucro Líquido', 'ROAE', 'Patrimônio Líquido', 'Carteira', 'Captações', 'Basileia','CET1']
            dfs.append(df0)

        pd.DataFrame(falt)

        dfs0 = []
        for i in range(len(dfs[0].keys())):
            df0 = [df.iloc[:, i] for df in dfs]
            df0 = pd.DataFrame(df0).T
            df0['Média'] = df0.mean(axis=1)
            df0.columns = empresass + ['Média']
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
                return str(num)

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

    tri = []
    for i in capital_resumo['AnoMes']:
        if i not in tri:
            tri.append(i)
    
    def sort_key(val):
        year = int(val[-2:]) 
        num = int(val[0])
        return (year, num)  
    tri = sorted(tri, key=sort_key)


    col1, col2 = st.columns(2)
    with col1:
        empresa = st.selectbox("Selecione as empresas",empresas)
    with col2:
        # O slider seleciona um intervalo entre os trimestres disponíveis
        selected_range = st.select_slider(
                "Selecione os trimestres",
                options=tri,  # Passa a lista de trimestres como opções
                value=(tri[-4], tri[-1]),
        )
    
        # Obtendo os trimestres selecionados
        start_idx = tri.index(selected_range[0])
        end_idx = tri.index(selected_range[1])

        # Fatiando a lista tri com os índices encontrados
        tris = tri[start_idx:end_idx + 1]

    def csv(df):
        return df.to_csv(index=False).encode('utf-8')
    

    if len(empresa) > 0 and len(tris) > 2:
        
        
        col3, col4 = st.columns(2)
        with col3:
            demonstrativo = st.selectbox("Selecione o demonstrativo", ['Balanço patrimonial', 'DRE'])

            # Obtendo os trimestres selecionados
            start_idx = tri.index(selected_range[0])
            end_idx = tri.index(selected_range[1])

            # Fatiando a lista tri com os índices encontrados
            tris = tri[start_idx:end_idx + 1]

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
                return str(num)

        bpdown = []
        resdown = []

        if demonstrativo == 'Balanço patrimonial':
            ordem = []
            cols = []
            atv = ativo[ativo['Empresa'] == empresa]
            for i in ativo['NomeColuna'].unique():
                ordem.append( i[i.index("(")+1:i.index(")")] )
                cols.append( i )
            ind = sorted(range(len(ordem)), key=lambda i: ordem[i])
            ind = [cols[i] for i in ind]
            
            atri = []
            for i in tris[::-1]:
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
            for i in tris[::-1]:
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


            ordem = []
            cols = []
            res = dre[dre['Empresa'] == empresa]
            for i in dre['NomeColuna'].unique():
                ordem.append( i[i.index("(")+1:i.index(")")] )
                cols.append( i )
            ind = sorted(range(len(ordem)), key=lambda i: ordem[i])
            ind = [cols[i] for i in ind]
            
            rtri = []
            for i in tris[::-1]:
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
                    data=bpdown,
                    file_name="dre " + empresa + " " + tris[0] + "-" + tris[-1] + ".csv",
                    mime="text/csv"
                )
