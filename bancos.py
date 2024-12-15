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

bp = pd.concat([ativo,passivo])

empresas=capital_resumo["Empresa"].unique()


cat=st.sidebar.selectbox("Escolha a categora",["Demonstrativos"])

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
