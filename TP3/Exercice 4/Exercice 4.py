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


data_1_path = "C:/Users/user/Desktop/AllDatas_20160329_205341_ch0_output.csv"
data_2_path = "C:/Users/user/Desktop/AllDatas_20160329_205341_ch1_output.csv"
data_3_path = "C:/Users/user/Desktop/AllDatas_20160329_205341_ch2_output.csv"

data_1_lux = volt_to_lux(data_1_path)
data_2_lux = volt_to_lux(data_2_path)
data_3_lux = volt_to_lux(data_3_path)

# GPS Data conversion :
from pyproj import Proj, transform
import pandas as pd
import numpy as np

def convert_to_wgs_84(df):
    wgs84 = Proj(init='EPSG:4326')
    epsg5254 = Proj(init='epsg:5254')
    x,y = transform(wgs84,epsg5254,df['Latitude'],df['Longitude'])
    return x,y

gps_path = "C:/Users/user/Desktop/AllDatas2_20160329_205341_NmeaTimeLatLongSatnbAtlHSpeedVSpeed_output.csv"

df_gps = pd.read_csv(gps_path,sep=';')
colnames_gps=['TimeStamp','Heure','Longitude','Latitude','Nbr statellites','Precision','Altitude','Vitesse horizontale','Vitesse verticale']
df_gps.columns = colnames_gps
result = df_gps.apply(convert_to_wgs_84,axis=1)
result = pd.DataFrame(result)
result.columns = ['mergedXY']
result = result['mergedXY'].astype('str')
result = result.str.replace("(","")
result = result.str.replace(")","")
result = pd.DataFrame(result.str.split(',',1).tolist(),columns = ['X','Y'])
result['X'] = result['X'].astype(float)
result['Y'] = result['Y'].astype(float)
result = pd.DataFrame.reset_index(result,drop=True)
result = pd.concat([result,df_gps['TimeStamp']],axis=1)
interpolation = result

# Now GPS transformation is done.
del df_gps
del result

# Interpolation

#Shifting TimeStamp column to one row
interpolation['decale'] = interpolation['TimeStamp'].copy()
interpolation['decale'] = interpolation.decale.shift(-1)
interpolation.drop(interpolation.tail(1).index,inplace=True)

# Creating a delta column which corresponds to Timestamp(t) - Timestamp(t+1)

interpolation['deltaTimeStamp'] = interpolation['decale'] - interpolation['TimeStamp']

# Taking out first minute of Interpolation dataframe 
minute = data_1.iloc[0].TimeStamp
interpolation = interpolation.drop(interpolation[interpolation.TimeStamp<minute].index)

# Creating x_offset and y_offset on interpolation dataframe
interpolation['x_offset'] = interpolation['X'].copy()
interpolation['x_offset'] = interpolation.x_offset.shift(-1)
interpolation.drop(interpolation.tail(1).index,inplace=True)

interpolation['y_offset'] = interpolation['Y'].copy()
interpolation['y_offset'] = interpolation.y_offset.shift(-1)
interpolation.drop(interpolation.tail(1).index,inplace=True)

# Merging sensor dataframe and Interpolation dataframe
data_1_append = data_1.append(interpolation)
data_1_append = data_1_append.sort_values(by='TimeStamp')

#  On duplique le contenu des colonnes récemment créées 
# afin de faire correspondre des données GPS à chaque mesure de Luxmètre

#Calculate final (x,y) values.
