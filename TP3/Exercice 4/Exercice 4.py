# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:51:41 2018

@author: Philippe Tu

This script is divided in 4 parts : 
    - Volt to Lux conversion
    - GPS processing 
    - Interpolation processing (GPS Data)
    - Cleaning Lux values
"""

# Import libraries
import pandas as pd
import seaborn as sns
import numpy as np
import dask.dataframe as dd
# Part 1 : Volt to Lux conversion
def volt_to_lux(path):
    colnames =['TimeStamp','V1','V2']
    df_lux = pd.read_csv(path,sep=';')
    df_lux.columns=colnames
    minute = df_lux.iloc[0]['TimeStamp'] + 60000000
    df_lux.columns = colnames
    minute_data = df_lux[df_lux['TimeStamp']<minute]
    U0 = ( minute_data['V1'].mean() + minute_data['V2'].mean() ) / 2
    Umax = 3.3
    Lmax = 3000
    coeff = Lmax / (Umax-U0)
    
    data_1 = df_lux[df_lux['TimeStamp']>minute]
    data_v1 = data_1[['TimeStamp','V1']]
    data_v2 = data_1[['TimeStamp','V2']]
    
    T1 = data_v2['TimeStamp']
    T2 = T1.copy()
    T2.drop(T1.head(1).index,inplace=True)
    T3 = (T1+T2) / 2 
    data_v2['TimeStamp'] = T3
    data_v2.drop(data_v2.head(230981).index,inplace=True)
    
    data_v1.columns = ['TimeStamp','Volt']
    data_v2.columns = ['TimeStamp','Volt']
    # Using dask.dataframe library, useful here because I can do merges without having memory problems
    data_volt = dd.merge(data_v1,data_v2,how='outer',on=['TimeStamp','Volt']) 
    
    lux = data_volt['Volt']*coeff
    data_lux = data_volt.copy()
    data_lux['Volt'] = lux
    return data_lux
data_1_path = "C:/Users/user/Desktop/RepositoryTP/PythonBDTN-TU/TP3/Exercice 4/AllDatas_20160329_205341_ch0_output.csv"
data_2_path = "C:/Users/user/Desktop/RepositoryTP/PythonBDTN-TU/TP3/Exercice 4/AllDatas_20160329_205341_ch1_output.csv"
data_3_path = "C:/Users/user/Desktop/RepositoryTP/PythonBDTN-TU/TP3/Exercice 4/AllDatas_20160329_205341_ch2_output.csv"

data_1_lux = volt_to_lux(data_1_path)
data_2_lux = volt_to_lux(data_2_path)
data_3_lux = volt_to_lux(data_3_path)
