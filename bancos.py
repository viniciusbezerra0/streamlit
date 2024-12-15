import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

def baixar(arquivo, id):
    url = f'https://drive.google.com/uc?id={id}'
    gdown.download(url, arquivo, quiet=False)
    return pd.read_csv(arquivo)
    
ativo = baixar("ativo.csv", "d/1R_y8vtNABZO35PeoyuvZouEZDYIuBJdm")
passivo = baixar("passivo.csv", "1dhHMgSIC_bvdblg2OzMmr1kHYA7fYSIX")
dre = baixar("dre.csv", "1eiRk3ZnPlSRMyp4ZoiFKg-M4d7MQmSBz")

bp = pd.concat([ativo,passivo])

empresas=capital_resumo["Empresa"].unique()


cat=st.sidebar.selectbox("Escolha a categora",["Principais indicadores","Carteira","Resumo", "Demonstrativos"])

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
