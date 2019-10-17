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
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
        
    # Construcción del DataFrame a utilizar para el pareto
    pareto = pd.DataFrame({'Percentage':(df['Symbol'].value_counts()/df['Symbol'].count())*100}) #% de participación
    pareto = pareto.sort_values(by='Percentage',ascending=False) #Sort de mayor a menor % para línea
    pareto['TransactionC'] = list(df['Symbol'].value_counts()) #Conteo de valores para gráfico de barras
        
    # Definicipón del gráfico
    fig, ax = plt.subplots()
    ax.bar(pareto.index, pareto['TransactionC'], color="g") # Barras del gráfico
    ax2 = ax.twinx() # Tener dos valores distintos en los ejes y
    ax2.plot(pareto.index, pareto['Percentage'].cumsum(), color="k", marker="o") #Graficando la línea
    ax2.yaxis.set_major_formatter(PercentFormatter()) #Formato de porcentaje al eje de línea
    ax.set_xlabel('Currency') #Título del xlabel
    ax.set_ylabel('Count')
    ax2.set_ylabel('Percentage')
        
    ax.tick_params(axis='y', colors='g') #Color del eje de las barras para relacionar los valores
    ax2.tick_params(axis='y', colors='k') #Color del eje de las líneas para relacionar valores
    plt.setp(ax.get_xticklabels(), rotation=40, horizontalalignment='right') #Rotando etiquetas para que sean vistas
    plt.title('Proporción de las divisas')
        
    plt.grid()
    plt.show()
    
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    df['PipSL'] = abs(df['openPrice']-df['S/L'])*10000
    df['PipTP'] = abs(df['openPrice']-df['T/P'])*10000
    
    return fig

    # Retorno de salidas en Diccionario INVESTIGAR