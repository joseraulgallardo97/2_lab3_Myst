# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 21:53:59 2019

@author: gallardj
"""

import numpy as np
import pandas as pd
import function_json2 as fi
import f_bf_sanclaje as anc

df = fi.f_datosent(p0_archivo = 'archivo_tradeview_2.xlsx')
salida = anc.anclaje(df,4)