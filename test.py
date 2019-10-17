# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 21:53:59 2019

@author: gallardj
"""

import function_json2
import Anclaje

df = f_datosent(p0_archivo = 'archivo_tradeview_2.xlsx')

test = Anclaje.pareto(df)
