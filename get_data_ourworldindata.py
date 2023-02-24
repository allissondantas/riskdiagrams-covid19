import pandas as pd
from pandas import ExcelWriter

save_filename = 'data/ourworldindata.xlsx'
save_filename_pop = 'data/pop_ourworldindata_v1.xlsx'

def run_crear_excel_ourworldindata(country):
    data = pd.read_csv('data/owid-covid-data.csv')
    is_country = data['location'] == country
    data_country = data[is_country]
    
    data_country.set_index('date', 'location', inplace=True)
    unique_dates = data_country.index.get_level_values('date').unique()
    unique_country = data_country['location'].unique()
    unique_pop = data_country['population'].unique()
    
    dfByTotalCases = dataFramePorColuna('total_cases', unique_dates, unique_country, data_country)

    pop_owd_df = pd.DataFrame(unique_pop, columns=unique_country)

    with ExcelWriter(save_filename) as writer:
        dfByTotalCases.to_excel(writer, sheet_name='Cases')
    
    with ExcelWriter(save_filename_pop) as writer:
        pop_owd_df.to_excel(writer, index=False)

def dataFramePorColuna(coluna, unique_dates, unique_country, data):
    
    resul = pd.DataFrame(index=unique_dates, columns=unique_country)
    
    for location_ in unique_country:
        test = data.query('location == @location_')
        test = test[~test.index.duplicated()]
        resul[location_] = test[coluna]
   
    resul.fillna(0, inplace=True)
    resul['TOTAL'] = resul.sum(axis=1)
    
    return resul
