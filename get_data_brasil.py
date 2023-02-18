"""
Code by Renato Pessoa e Melo Neto

Returns:
    [String] -- [formated excel path]
"""

import pandas as pd
from pandas import ExcelWriter
import sys
import requests

pathToBrasil = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"

siglasEstados = ["AC", "AL", "AP", "AM", "BA", "CE",
                    "DF", "ES", "GO", "MA", "MT", "MS",
                    "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
                    "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]


nameEstados = ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará",
                    "Distrito Federal", "Espirito Santo", "Goias", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
                    "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro",
                    "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins", "TOTAL"]



def run_crear_excel_brasil():
    try:
        link = requests.get(pathToBrasil)
        dados = pd.read_csv(link.url)
        print('Data obtained from: ', pathToBrasil)
        dados_semTotal = dados[dados['state'] != 'TOTAL']
    except:
        print('Error! can\'t load data from web')
        sys.exit()

    dados_semTotal.set_index('date', 'state', inplace=True)
    
  

    unique_dates = dados_semTotal.index.get_level_values('date').unique()
    dfByTotalCases = dataFramePorColuna('totalCases', unique_dates, siglasEstados, dados_semTotal)
    
    dfByTotalCases.columns = nameEstados
    dfByTotalCasesRegions = crear_excel_brasil_estados(dfByTotalCases)

    with ExcelWriter('data/Data_Brasil.xlsx') as writer:

        dfByTotalCases.to_excel(writer, sheet_name='Cases')
        dfByTotalCasesRegions.to_excel(writer, sheet_name='Regions')


def dataFramePorColuna(coluna, unique_dates, siglasEstados, dados_semTotal):
    
    resul = pd.DataFrame(index=unique_dates, columns=siglasEstados)

    for estado in siglasEstados:
        test = dados_semTotal.query('state == @estado ')
        resul[estado] = test[coluna]

    resul.fillna(0, inplace=True)
    resul['TOTAL'] = resul.sum(axis=1)
    return resul

def crear_excel_brasil_estados(dfByTotalCases):
    df_regions = pd.DataFrame(columns=['Nordeste' , 'Norte', 'Centro-Oeste', 'Sudeste', 'Sul'])
    df_regions['Nordeste'] = dfByTotalCases['Alagoas'] + dfByTotalCases['Bahia'] + dfByTotalCases['Ceará'] + dfByTotalCases['Maranhão'] + dfByTotalCases['Paraíba']+ dfByTotalCases['Pernambuco']+ dfByTotalCases['Piauí'] + dfByTotalCases['Rio Grande do Norte'] + dfByTotalCases['Sergipe']
    df_regions['Norte'] = dfByTotalCases['Amazonas']+ dfByTotalCases['Pará']+ dfByTotalCases['Acre']+ dfByTotalCases['Rondônia']+ dfByTotalCases['Tocantins'] + dfByTotalCases['Amapá'] + dfByTotalCases['Roraima']
    df_regions['Centro-Oeste'] = dfByTotalCases['Mato Grosso']+ dfByTotalCases['Goias'] + dfByTotalCases['Mato Grosso do Sul']+ dfByTotalCases['Distrito Federal']
    df_regions['Sudeste'] = dfByTotalCases['Minas Gerais']+ dfByTotalCases['Espirito Santo'] + dfByTotalCases['São Paulo'] + dfByTotalCases['Rio de Janeiro']
    df_regions['Sul'] = dfByTotalCases['Paraná'] + dfByTotalCases['Santa Catarina'] + dfByTotalCases['Rio Grande do Sul']
    return df_regions

if __name__ == '__main__':
    run_crear_excel_brasil()
