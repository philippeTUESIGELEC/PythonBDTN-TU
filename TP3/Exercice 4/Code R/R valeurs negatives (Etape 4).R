#Author : TU Philippe
#Team Members : BERGEOT Melanie,LEGRAND Louis, PETERS Henri, TU Philippe,YU Hong
#Date : 23/02/2018
# This script takes out negative values of Lux columns
# Example of code for one input sensor file.
library(plyr)
library(dplyr)
as.numeric.factor <- function(x) {as.numeric(levels(x))[x]}

#FileNames

namefile_final_result_sensor_0<-"capteur_0"

#Column names
col_names_sensor<-c("Timestamp_coordinates","final_x","final_x","Lux")
#Opening files
sensor_0_dataframe<-read.csv(namefile_final_result_sensor_0,header=FALSE,sep=",")

colnames(sensor_0_dataframe)<-col_names_sensor

sensor_0_dataframe<-data.frame(sensor_0_dataframe[-1,])

#Separate Negative values and positive values and replace all negatives by 0
data_without_negative_values_sensor_0 = subset(sensor_0_dataframe,as.numeric.factor(Lux)>0)
data_negative_values_sensor_0 = subset(sensor_0_dataframe,as.numeric.factor(Lux)<0)
data_negative_values_sensor_0["Lux"]= as.numeric.factor(0)

#Merge rows of data_negative_values and data_without_negative_values
merged_data<-full_join(data_without_negative_values_sensor_0,data_negative_values_sensor_0)
merged_data_sensor_0<-rbind(data_without_negative_values_sensor_0,data_negative_values_sensor_0)
merged_data_sensor_0<-na.fill(merged_data_sensor_0,0)

write.csv(merged_data_sensor_0,file="final_results_0",row.names=FALSE)

