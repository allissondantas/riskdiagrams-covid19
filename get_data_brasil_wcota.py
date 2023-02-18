import pandas as pd
from pandas import ExcelWriter
import sys


#url = "https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time.csv.gz"
pathToBrasil = "data/cases-brazil-cities-time.csv"


def run_crear_excel_brasil_wcota(sigla):
    try:
        dados = pd.read_csv(pathToBrasil)
        print('Data obtained from: ', pathToBrasil)
        dados_semTotal = dados[dados['state'] != 'TOTAL']
    except:
        print('Error! can\'t load data from web')
        sys.exit()
    dados_wcota = dados_semTotal[dados_semTotal['state'] == sigla]
    dados_wcota.set_index('date', 'state', inplace=True)
    unique_dates = dados_wcota.index.get_level_values('date').unique()
    dados_wcota['city'] = dados_wcota['city'].str.replace(u"/"+sigla, "")
    unique_city = dados_wcota['city'].unique()

    dfByTotalCases = dataFramePorColuna('totalCases', unique_dates, unique_city, dados_wcota)
    dfByTotalDeaths = dataFramePorColuna('deaths', unique_dates, unique_city, dados_wcota)

    with ExcelWriter('data/cases-wcota.xlsx') as writer:

        dfByTotalCases.to_excel(writer, sheet_name='Cases')
        dfByTotalDeaths.to_excel(writer, sheet_name='Deaths')

def dataFramePorColuna(coluna, unique_dates, siglasEstados, dados_semTotal):
    
    resul = pd.DataFrame(index=unique_dates, columns=siglasEstados)

    for city in siglasEstados:
        test = dados_semTotal.query('city == @city ')
        resul[city] = test[coluna]

    resul.fillna(0, inplace=True)
    resul['TOTAL'] = resul.sum(axis=1)
    return resul
