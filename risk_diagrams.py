import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from get_data_brasil import run_crear_excel_brasil
from get_data_brasil_wcota import run_crear_excel_brasil_wcota
from get_data_pernambuco import run_crear_excel_recife
from get_data_ourworldindata import run_crear_excel_ourworldindata
from pandas import ExcelWriter
import colormap
import plotly.graph_objects as go
import base64
import os

matplotlib.use('agg')


def plotly_html(a_14_days, p_seven, dia, bra_title, save_path, filename_bg):

    for i in range(len(p_seven)):
        if p_seven[i] < 0.0:
            p_seven[i] = 0.0

    color_map = []
    for i in range(len(a_14_days)):
        if i < len(a_14_days) - 60:
            color_map.append('rgba(0, 0, 0, 0.1)')
        elif i == len(a_14_days) - 1:
            color_map.append('rgba(255, 255, 255, 0.6)')
        else:
            color_map.append('Blue')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a_14_days,
                             y=p_seven,
                             text=dia,
                             mode='lines+markers',
                             marker=dict(
                                 color=color_map,
                                 showscale=False,
                                 size=10,
                                 line=dict(
                                     color='Black',
                                     width=0.2)),
                             line=dict(
                                 color="Black",
                                 width=0.5,
                                 dash="dot"),
                             ))
    fig.add_shape(type="line",
                  x0=0,
                  y0=1,
                  x1=max(a_14_days),
                  y1=1,
                  line=dict(
                      color="Black",
                      width=1,
                      dash="dot",
                  ))

    image_filename = filename_bg
    img = base64.b64encode(open(image_filename, 'rb').read())
    x = round(a_14_days.max())
    y = round(p_seven.max())
    print(x, y)

    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(img.decode()),
            xref="x",
            yref="y",
            x=0,
            y=p_seven.max(),
            sizex=a_14_days.max(),
            sizey=p_seven.max(),
            xanchor="left",
            yanchor="top",
            sizing="stretch",
            opacity=0.95,
            layer="below"))
    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.9,
                            text="EPG > 100: High", showarrow=False))

    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.87, y1=0.89, fillcolor="Red", line_color="Red")

    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.86,
                            text=" 70 < EPG < 100: Moderate-high", showarrow=False))

    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.86, y1=0.78, fillcolor="Yellow", line_color="Yellow")

    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.82,
                            text=" 30 < EPG < 70 : Moderate", showarrow=False))

    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.78,
                            text="EPG < 30: Low", showarrow=False))
    fig.add_annotation(dict(font=dict(color='blue', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.728,
                            text="Last 60 days", showarrow=False))
    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.77, y1=0.74, fillcolor="Green", line_color="Green")
    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.725, y1=0.70, fillcolor="Blue", line_color="Blue")

    fig.update_layout(plot_bgcolor='rgb(255,255,255)',
                      width=800,
                      height=600,
                      xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      xaxis_title="Attack rate per 10⁵ inh. (last 14 days)",
                      yaxis_title="\u03C1 (mean of the last 7 days)",
                      title={
                          'text': bra_title,
                          'y': 0.9,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'},
                      )

    fig.update_xaxes(rangemode="tozero")

    fig.update_yaxes(rangemode="tozero")

    # fig.show()
    os.remove(filename_bg)

    fig.write_html(filename_bg+'.html', include_plotlyjs="cdn")

def run_risk_diagrams(argv_1, deaths, file_others_cases, file_others_pop, radio_valor, ourworldindata_country):

    if argv_1:
        last_days_time = 30
        html = False
        last_days = False

        if radio_valor == 1:
            last_days = True
        elif radio_valor == 2:
            html = True
        else:
            pass

        dataTable = []
        dataTable_EPG = []

        if argv_1 == 'brasil' and deaths == 'False':
            try:
                run_crear_excel_brasil()
                filename = 'data/Data_Brasil.xlsx'
                filename_population = 'data/pop_Brasil_v3.xlsx'
                sheet_name = 'Cases'
            except AttributeError:
                print('Error! Not found file or could not download!')
        elif argv_1 == 'brasil_regions' and deaths == 'False':
            try:
                run_crear_excel_brasil()
                filename = 'data/Data_Brasil.xlsx'
                filename_population = 'data/pop_Brasil_Regions_v3.xlsx'
                sheet_name = 'Regions'

            except AttributeError:
                print('Error! Not found file or could not download!')
        elif argv_1 == 'recife':
            try:
                run_crear_excel_recife()
                filename = 'data/cases-recife.xlsx'
                filename_population = 'data/pop_recife_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif argv_1 == 'WCOTA':
            try:
                run_crear_excel_brasil_wcota('SP')
                filename = 'data/cases-wcota.xlsx'
                filename_population = 'data/pop_SP_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif argv_1 == 'ourworldindata' and deaths == 'False':
            try:
                run_crear_excel_ourworldindata(ourworldindata_country)
                filename = 'data/ourworldindata.xlsx'
                filename_population = 'data/pop_ourworldindata_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif argv_1 == 'others' and deaths == 'False':
            try:
                filename = file_others_cases
                filename_population = file_others_pop
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        data = pd.read_excel(filename, sheet_name=sheet_name)
        population = pd.read_excel(filename_population)
        dia = pd.to_datetime(data['date']).dt.strftime('%d/%m/%Y')
        dia = dia.to_numpy()
        region = population.columns

        for ID in range(len(region)):
            cumulative_cases = data[region[ID]]
            cumulative_cases = cumulative_cases.to_numpy()
            new_cases = np.zeros((len(cumulative_cases)), dtype=int)
            for i in range(len(cumulative_cases)):
                if i != 0:
                    new_cases[i] = cumulative_cases[i] - \
                        cumulative_cases[i - 1]
                 
            p = np.zeros((len(new_cases)), dtype=float)
            for i in range(7, len(new_cases)):
                div = 0
                aux = new_cases[i - 5] + new_cases[i - 6] + new_cases[i - 7]
                if aux == 0:
                    div = 1
                else:
                    div = aux
                p[i] = min((new_cases[i] + new_cases[i - 1] +
                            new_cases[i - 2]) / div, 4)

            p_seven = np.zeros((len(new_cases)), dtype=float)
            n_14_days = np.zeros((len(new_cases)), dtype=float)
            a_14_days = np.zeros((len(new_cases)), dtype=float)
            risk = np.zeros((len(new_cases)), dtype=float)
            risk_per_10 = np.zeros((len(new_cases)), dtype=float)

            day13 = 13

            for i in range(day13, len(new_cases)):
                p_seven[i] = np.average(p[i - 6:i + 1])
                n_14_days[i] = np.sum(new_cases[i - day13: i + 1])
                pop = population[region[ID]]
                a_14_days[i] = n_14_days[i] / pop * 100000
                risk[i] = n_14_days[i] * p_seven[i]
                risk_per_10[i] = a_14_days[i] * p_seven[i]

            first_day = dia[day13]
            last_day = dia[len(dia) - 1]
            first_day = first_day.replace('/', '-')
            last_day = last_day.replace('/', '-')

            # For last 15 days
            if last_days:
                a_14_days_solo = []
                day13 = len(a_14_days) - last_days_time
                first_day = dia[day13]
                for i in range(len(a_14_days)):
                    if i >= len(a_14_days) - last_days_time:
                        a_14_days_solo.append(a_14_days[i])
                    else:
                        a_14_days_solo.append(None)

            save_path = 'static_graphic' + '/' + last_day + '-' + region[ID]
            save_path_temp = 'static_graphic' + '/interactive_graphic/' + last_day + '-' + region[ID]
            save_path_xlsx = 'static_graphic/xlsx/'

            fig1, ax1 = plt.subplots(sharex=True)
            del fig1

            if last_days:
                ax1.plot(a_14_days,  p_seven, 'ko--', fillstyle='none',
                         linewidth=0.5, color=(0, 0, 0, 0.15))
                ax1.plot(a_14_days_solo,  p_seven, 'ko--',
                         fillstyle='none', linewidth=0.5)  # For last 15 days
                ax1.plot(a_14_days_solo[len(a_14_days_solo) - 1],
                         p_seven[len(p_seven) - 1], 'bo')
            else:
                ax1.plot(a_14_days,  p_seven, 'ko--',
                         fillstyle='none', linewidth=0.5)
                ax1.plot(a_14_days[len(a_14_days) - 1],
                         p_seven[len(p_seven) - 1], 'bo')
            lim = ax1.get_xlim()
            x = np.ones(int(lim[1]))
            ax1.plot(x, 'k--', fillstyle='none', linewidth=0.5)
            ax1.set_ylim(0, 4)
            ax1.set_xlim(0, int(lim[1]))

            
            ax1.set_ylabel('$\u03C1$ (mean of the last 7 days)')
            ax1.set_xlabel('Attack rate per $10^5$ inh. (last 14 days)')
            ax1.annotate(first_day,
                         xy=(a_14_days[day13], p_seven[day13]
                             ), xycoords='data',
                         xytext=(len(x) - abs(len(x) / 1.5), 2.7), textcoords='data',
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="arc3", linewidth=0.4),
                         )
            ax1.annotate(last_day,
                         xy=(a_14_days[len(a_14_days) - 1],
                             p_seven[len(p_seven) - 1]), xycoords='data',
                         xytext=(len(x) - abs(len(x) / 2), 3), textcoords='data',
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="arc3", linewidth=0.4),
                         )

           
            bra_title = region[ID]
            plt.title(region[ID])
            plt.annotate(
                ' EPG > 100: High', xy=(len(x) - abs(len(x) / 3.5), 3.8), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
            plt.annotate(
                " 70 < EPG < 100: Moderate-high\n"
                " 30 < EPG < 70 : Moderate", xy=(len(x) - abs(len(x) / 3.5), 3.55), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
            plt.annotate(
                ' EPG < 30: Low', xy=(len(x) - abs(len(x) / 3.5), 3.3), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))

            plt.annotate(
                '  ', xy=(len(x) - abs(len(x) / 3.3), 3.8), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(1, 0, 0, .5), lw=0, pad=2))
            plt.annotate(
                "  \n", xy=(len(x) - abs(len(x) / 3.3), 3.55), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(1, 1, 0, .5), lw=0, pad=2))
            plt.annotate(
                '  ', xy=(len(x) - abs(len(x) / 3.3), 3.3), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 1, 0, .5), lw=0, pad=2))
               
            if ourworldindata_country is not None:
                plt.subplots_adjust(bottom=0.2)
                text_annotate = (
                    "*The risk diagram was developed using the Our World in Data database. Last update: " + str(last_day) + ".")

                plt.text(0, -1, text_annotate, fontsize=7, wrap=False)

            rh = np.arange(0, int(lim[1]), 1)
            ar = np.linspace(0, 4, 400)

            RH, AR = np.meshgrid(rh, ar)

            EPG = RH * AR

            for i in range(len(EPG)):
                for j in range(len(EPG[i])):
                    if EPG[i][j] > 100:
                        EPG[i][j] = 100
            c = colormap.Colormap()
            mycmap = c.cmap_linear('green(w3c)', 'yellow', 'red')
            ax1.pcolorfast([0, int(lim[1])], [0, 4],
                           EPG, cmap=mycmap, alpha=0.6)

            ax1.set_aspect('auto')

            if html:
                figt, axt = plt.subplots(sharex=True)
                axt.pcolorfast([0, int(lim[1])], [0, 4],
                               EPG, cmap=mycmap, alpha=0.6)
                axt.set_axis_off()
                figt.savefig(save_path_temp, format='png',
                             bbox_inches='tight', dpi=300, pad_inches=0)
                plotly_html(a_14_days, p_seven, dia, bra_title,
                            save_path_xlsx, save_path_temp)
            else:
                plt.savefig(save_path + '.png', bbox_inches='tight', dpi=300)
                plt.close('all')
            print(
                "\n\nPrediction for the region of " + region[
                    ID] + " performed successfully!\nPath:" + save_path)

    

            dataTable.append([region[ID], cumulative_cases[len(cumulative_cases) - 1], new_cases[len(new_cases) - 1], p[len(p) - 1], p_seven[len(
                p_seven) - 1], n_14_days[len(n_14_days) - 1], a_14_days[len(a_14_days) - 1], risk[len(risk) - 1], risk_per_10[len(risk_per_10) - 1]])

            for i in range(len(dia)):
                dataTable_EPG.append([dia[i], region[ID], risk_per_10[i]])

    df = pd.DataFrame(dataTable, columns=['State', 'Cumulative cases', 'New cases', 'ρ', 'ρ7', 'New cases last 14 days (N14)',
                                          'New cases last 14 days per 105 inhabitants (A14)', 'Risk (N14*ρ7)',  'Risk per 10^5 (A14*ρ7)'])
    df_EPG = pd.DataFrame(dataTable_EPG, columns=['DATE', 'CITY', 'EPG'])

    with ExcelWriter(save_path_xlsx + last_day + '_' + argv_1 + '_report.xlsx') as writer:
        df.to_excel(writer, sheet_name='Alt_Urgell')
    with ExcelWriter(save_path_xlsx + last_day + '_' + argv_1 + '_report_EPG.xlsx') as writer:
        df_EPG.to_excel(writer, sheet_name='Alt_Urgell')
