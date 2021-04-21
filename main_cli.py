from risk_diagrams import run_risk_diagrams
import os, sys
import requests


if __name__ == "__main__":

    Africa = ['Nigeria', 'South Africa','Malawi', 'Morocco','Africa','Zambia', 'Namibia',
    'Senegal','Gabon', 'Botswana', 'Mozambique','Libya', 'Egypt', 'Sao Tome and Principe', 'Tunisia']
    Europe = ['Spain', 'Portugal', 'France', 'Italy', 'Sweden', 'United Kingdom', 'Andorra', 'Germany']
    South_America = ['Chile', 'Brazil', 'Argentina', 'Bolivia', 'Colombia', 'Ecuador', 'Peru', 'Paraguay', 'Uruguay', 'Suriname', 'Venezuela', 'Guyana']
    MiddleEast = ['Israel', 'Palestine', 'United Arab Emirates', 'Turkey']
    NorthAmerica = ['Canada', 'United States']
    Oceania = ['Australia','Papua New Guinea', 'New Zealand', 'Fiji']
    ourworldindata_country = [Africa, Europe, South_America, MiddleEast, NorthAmerica, Oceania]

    # 0 None | 1 last_days | 2 html 
    radio_valor = 1
    run_risk_diagrams('brasil_regions', 'False', None, None, radio_valor, None)
    radio_valor = 2
    run_risk_diagrams('brasil_regions', 'False', None, None, radio_valor, None)
    sys.exit()
    run_risk_diagrams('recife', 'False', None, None, radio_valor, None)
    run_risk_diagrams('brasil', 'False', None, None, radio_valor, None)
    #run_risk_diagrams('WCOTA', 'False', None, None, radio_valor, None)

    print('Donwload ourwoldindata')
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    r = requests.get(url)
    with open('data/owid-covid-data.csv', 'wb') as f:
        f.write(r.content)
    # Retrieve HTTP meta-data
    print(r.status_code)
    print(r.headers['content-type'])
    print(r.encoding)

    for i in range(len(ourworldindata_country)):
        for j in ourworldindata_country[i]:
            run_risk_diagrams('ourworldindata', 'False', None, None, radio_valor, j)

    sys.exit()
