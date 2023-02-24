import pandas as pd
from pandas import ExcelWriter
import requests

path_recife = 'https://raw.githubusercontent.com/edneide/covid-19_Pernambuco/master/total_cases_PE.csv'
save_filename = 'data/cases-recife.xlsx'


def run_crear_excel_recife():
    link = requests.get(path_recife)
    data = pd.read_csv(link.url)
    data = data.rename(columns={'Data': 'date'})
    '''
    for i, j in enumerate(data['date'], start=0):
        aux = j[3:] + j[0:2] + '2020'
        data['date'][i] = datetime.strptime(aux, '%b%d%Y')
    
    data['date'] = pd.to_datetime(data['date']).dt.strftime("%Y-%m-%d")
    '''

    with ExcelWriter(save_filename) as writer:

        data.to_excel(writer, sheet_name='Cases', index=False)


if __name__ == '__main__':
    run_crear_excel_recife()
