# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 08:28:42 2019

@author: gallardj
"""

def pareto(df):
    # Grafico pareto para analizar principales divisas transaccionadas
    """
    :param tickers: columna de dataframe con los tickers de las divisas
    :return grafica
    
    debbuging
    tickers = df
    """
    import numpy as np
    import pandas as pd
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots
        
    # Construcción del DataFrame a utilizar para el pareto
    pareto = pd.DataFrame({'Percentage':(df['Symbol'].value_counts()/df['Symbol'].count())*100}) #% de participación
    pareto = pareto.sort_values(by='Percentage',ascending=False) #Sort de mayor a menor % para línea
    pareto['TransactionC'] = list(df['Symbol'].value_counts()) #Conteo de valores para gráfico de barras
    
    # Construcción del gráfico
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=pareto.index, y=pareto['TransactionC'],name='Conteo'),secondary_y=False)
    fig.add_trace(go.Scatter(x=pareto.index, y=pareto['Percentage'].cumsum(), name='Porcentaje'),secondary_y=True)
    
    # Título del gráfico
    fig.update_layout(title_text='Pareto de transacciones')
    
    # Set x-axis title
    fig.update_xaxes(title_text='Divisas')
    
    # Set y-axes titles
    fig.update_yaxes(title_text='<b>Conteo</b> de transacciones', secondary_y=False)
    fig.update_yaxes(title_text='<b>Porcentaje total</b> de transaccinoes', secondary_y=True)
    
    fig.show()
    
    # Calculando Pips Stop Loss y Take Profit
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    df['PipSL'] = abs(df['openPrice']-df['S/L'])*10000
    df['PipTP'] = abs(df['openPrice']-df['T/P'])*10000
    
    # Poniendo 0 donde no hubo un Stop Loss y un Take Profit
    df.loc[df['S/L'] == 0, 'PipSL'] = 0
    df.loc[df['T/P'] == 0, 'PipTP'] = 0
    
    # Armando un DataFrame con la divida que más se operó
    fx = df['Symbol'].value_counts().argmax()
    ndf = df[df['Symbol'] == fx].sort_values(by ='openTime').reset_index().drop(['index'], 1)
    
    # Contando los casos donde se cumple que sean la mimsa cantidad de pips
    cases = len(ndf[(ndf['PipSL'] == df['PipSL'].iloc[0]) & (ndf['PipTP'] == df['PipTP'].iloc[0])])
    
    if cases > len(ndf):
        ses = 'Existe un sesgo de anclaje, se cumplen %d de %d casos' % (cases, len(ndf))
    else:
        ses = 'No existe un sesgo de anclaje, se cumplen %d de %d casos' % (cases, len(ndf))
    
    return fig, ses
    # Retorno de salidas en Diccionario INVESTIGAR