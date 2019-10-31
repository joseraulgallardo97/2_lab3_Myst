# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 08:28:42 2019

@author: gallardj
"""
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.offline as py

def f_bf_anclaje(p0_df,p1_n=0):
    # Grafico pareto para analizar principales divisas transaccionadas
    """
    :param p0_df: dataframe con el historico de transacciones
    :param p1_1: transaccion de la cual se empezara a analizar (numero), si no se indica un index por default es 0.
    :return: diccionario con 4 llaves (datos, grafica, explicacion y escala)
    
    debbuging
    data = df
    """

        
    # Construccion del DataFrame a utilizar para el pareto
    pareto = pd.DataFrame({'Percentage':(p0_df['Symbol'].value_counts()/p0_df['Symbol'].count())*100}) #% de participacion
    pareto = pareto.sort_values(by='Percentage',ascending=False) #Sort de mayor a menor % para linea
    pareto['TransactionC'] = list(p0_df['Symbol'].value_counts()) #Conteo de valores para grafico de barras
    
    # Construccion del gráfico
    fig = go.Figure()
    fig = make_subplots(specs=[[{'secondary_y': True}]]) #Activar eje secundario para porcentaje
    fig.add_trace(go.Bar(x=pareto.index, y=pareto['TransactionC'],name='Conteo',
                         hovertemplate = '<i>Transacciones</i>: %{y}'
                        '<br><b>Divisa</b>: %{x}<br>'),secondary_y=False)
    fig.add_trace(go.Scatter(x=pareto.index, y=pareto['Percentage'].cumsum(), name='Porcentaje',
                              hovertemplate = '<i>Porcentaje de transacción acumulado</i>: %{y}'
                        '<br><b>Divisa</b>: %{x}<br>'),secondary_y=True)
    
    # Título del grafico
    fig.update_layout(title_text='Pareto de transacciones')
    
    # Titulo eje x
    fig.update_xaxes(title_text='Divisas')
    
    # Titulo eje y
    fig.update_yaxes(title_text='<b>Conteo</b> de transacciones', secondary_y=False)
    fig.update_yaxes(title_text='<b>Porcentaje total</b> de transacciones', secondary_y=True)
    
    #fig.show()
    py.offline.init_notebook_mode(connected=False)
#    py.iplot(fig, filename='Pareto de transacciones')
    
    # Calculando Pips Stop Loss y Take Profit
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    p0_df['PipSL'] = abs(p0_df['openPrice']-p0_df['S/L'])*10000
    p0_df['PipTP'] = abs(p0_df['openPrice']-p0_df['T/P'])*10000
    
    # Poniendo 0 donde no hubo un Stop Loss y un Take Profit
    p0_df.loc[p0_df['S/L'] == 0, 'PipSL'] = 0
    p0_df.loc[p0_df['T/P'] == 0, 'PipTP'] = 0
    
    # Armando un DataFrame con la divisa que mas se opero
    fx = p0_df['Symbol'].value_counts().idxmax() # Divisa que mas se opero
    ndf = p0_df[p0_df['Symbol'] == fx].sort_values(by ='openTime').reset_index().drop(['index'], 1) #DataFrame de solo esa divisa
    ndf = ndf.iloc[p1_n:,:] # Filtrando transacciones de acuerdo a la operacion solicitada
    
    # Contando los casos donde se cumple que sean la mimsa cantidad de pips
    cases = len(ndf[(ndf['PipSL'] == ndf['PipSL'].iloc[0]) & (ndf['PipTP'] == ndf['PipTP'].iloc[0])])
    
    # Cumplimiento de sesgo en porcentaje
    rate = (cases/len(ndf))*100
    
    if rate > 50:
        sesgo = 'Y'
    else:
        sesgo = 'N'
    
    # Diccionario para crear el df de salida
    data = {'Divisa': [fx], 
            'Total de transacciones': [len(ndf)],
            'Transacciones c/mismos pips': [cases],
            'Cumplimiento del sesgo (%)': [rate],
            'Sesgo': [sesgo]}
    
    df_salida = pd.DataFrame(data)
    
    return {'datos':df_salida, 
            'grafica': fig,
            'explicacion': "Anclaje: El sesgo consiste en que el individuo realiza operaciones con la misma divisa y con límites (pips de stop loss y take profit) iguales esperando tener un resultado positivo.",
            'escala': rate}