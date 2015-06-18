from os import walk
import csv
import random
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import os
##################################################################
#   Creates a csv where for each driver id we have the 
#   played_time and a classification [Eco, Gentle, Normal, Crazy]
##################################################################
fieldnames= ['driver_id', 'current_played_time', 'session', 'timestamp', 'acceleration', 'jerk']
with open('factors.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


##########################################################
# Custom Variables

MINIMUM_PLAYED_TIME_CONSIDERED = 240.0
ROLLING_WINDOW_SIZE = 1* 60.0
TRAINING_PERIOD = 120
ROLLING_WINDOW_INCREMENT= 10
SESSION_THRESHOLD = 15.0
##########################################################

fn = 'jerk_clusteringMins_2_3.csv'
os.remove(fn) if os.path.exists(fn) else None      

fn = 'jerk_clusteringMins_3_4.csv'
os.remove(fn) if os.path.exists(fn) else None   

fn = 'jerk_clusteringMins_4_5.csv'
os.remove(fn) if os.path.exists(fn) else None   

fn = 'jerk_clusteringMins_5_6.csv'
os.remove(fn) if os.path.exists(fn) else None   

fn = 'jerk_clusteringMins_6_7.csv'
os.remove(fn) if os.path.exists(fn) else None      

fn = 'jerk_clusteringMins_7_8.csv'
os.remove(fn) if os.path.exists(fn) else None   

fn = 'jerk_clusteringMins_8_9.csv'
os.remove(fn) if os.path.exists(fn) else None   

fn = 'jerk_clusteringMins_9_10.csv'
os.remove(fn) if os.path.exists(fn) else None  


f = []
for (dirpath, dirnames, filenames) in walk('./'):
    f.extend(filenames)
    break


rolling_window = []
driversIDList =[]



for driver in f:
    if driver[0]=='D':
        #driver file
        driver_id = driver.split('_')[1]
        #print driver_id
        df = open(driver, 'r')
        line = df.readline()
        df.readline()
        
        lines = df.readlines()
        played_time = line.split(' ')[3]
        #print driver_id + " played: "+ played_time

        user_data = [0, 0, 0,0,0,0,0,0,0]
        #accel ]-inf, -2[ , [-2, -1[ , [-1, 0[ , [0, 1[, [1 , 2[, [2, +inf[
        #speed [0,40 [  , [40, 80[, [80. +inf[
        #jerk ]-inf, -100[ , [-100, -90[ , [-90, -80[ , [-80, -70[, [-70 , 2[, [2, +inf[
        prev_speed = 0.0
        prev_ts = 0
        jerk = 0
        
        total_jerk = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        num_jerks=0
        
        if float(played_time) >=MINIMUM_PLAYED_TIME_CONSIDERED:
            #print  played_time
            
            
            rolling=0
            total_time = 0
            no_sessions = 1
            
            for line in lines:
                aux = line.split(',')
                idle_delta = 0.000001
                passo=False
                speed = float(aux[2])
                if prev_ts== 0:
                    prev_ts = float(aux[0])
                    prev_speed = speed
                    accel = 0
                    prev_accel =0
                    jerk = 0
                    rolling_window= []
                    rolling_window.append([prev_ts, 0, [0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0])

                    
                else:

                    
                    #calculate acceleration
                    accel = ((speed - prev_speed)*1000/3600.0) /  ((float(aux[0])-prev_ts)/10000000+0.0000001)
                    
                    if (float(aux[0])-prev_ts)/10000000 >SESSION_THRESHOLD :
                        no_sessions = no_sessions + 1

                        prev_accel = 0 

                        #reinitialize vector
                        rolling_window= []
                        rolling_window.append([prev_ts, 0, [0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0])

                        
                    
                        
                    else:

                        if (float(aux[0]) - rolling_window[-1][0])/10000000 >= ROLLING_WINDOW_INCREMENT:
                            rolling_window.append([prev_ts, 0, [0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0])
                        if (float(aux[0]) - rolling_window[0][0])/10000000 >= ROLLING_WINDOW_SIZE:
                            rolling_window.pop(0)

                        jerk= (accel -prev_accel) /  ((float(aux[0])-prev_ts)/10000000+0.0000001)
                        if prev_speed <0.001 and speed <0.001:
                            passo=True
                        else:
                            total_time = total_time +(float(aux[0])-prev_ts)/10000000
                            #print "Intermediate time  ", total_time
                        prev_speed = speed
                        prev_ts = float(aux[0])
                        prev_accel= accel
           # print "[First Filter] The total time is ", total_time    
            if float(total_time) >= 600:
                print driver_id, played_time, total_time
                driversIDList.append(driver_id)   

        df.close()
print driversIDList 
print "The total number of drivers who qualify for time-varying performance analysis are  ", len(driversIDList)


## The below is the code to take measurements based on time ranges 

for driver in f:
    if driver[0]=='D':
        driver_id = driver.split('_')[1]
        if driver_id in driversIDList:
            df = open(driver, 'r')
            line = df.readline()
            df.readline()
            lines = df.readlines()
            played_time = line.split(' ')[3]
            # print driver_id + " played: "+ played_time  + " total_time: "+ str(total_time)
            user_data = [0, 0, 0,0,0,0,0,0,0]
        
            prev_speed = 0.0
            prev_ts = 0
            jerk = 0
            
            total_jerk_2_3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_2_3=0

            total_jerk_3_4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_3_4=0

            total_jerk_4_5 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_4_5=0

            total_jerk_5_6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_5_6=0

            total_jerk_6_7 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_6_7=0

            total_jerk_7_8 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_7_8=0

            total_jerk_8_9 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_8_9=0

            total_jerk_9_10 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            num_jerks_9_10=0
            
            if float(played_time) >=MINIMUM_PLAYED_TIME_CONSIDERED:
                # print  played_time
                
                
                rolling=0
                total_time = 0
                no_sessions = 1
                
                for line in lines:
                    aux = line.split(',')
                    idle_delta = 0.000001
                    passo=False #The  flag
                    speed = float(aux[2])
                    if prev_ts== 0:
                        prev_ts = float(aux[0])
                        prev_speed = speed
                        accel = 0
                        prev_accel =0
                        jerk = 0
                        rolling_window= []
                        rolling_window.append([prev_ts, 0, [0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0])
    
                        
                    else:
    
                        
                        #calculate acceleration
                        accel = ((speed - prev_speed)*1000/3600.0) /  ((float(aux[0])-prev_ts)/10000000+0.0000001)
                        
                        if (float(aux[0])-prev_ts)/10000000 >SESSION_THRESHOLD :
                            no_sessions = no_sessions + 1
    
                            prev_accel = 0 
    
                            #reinitialize vector
                            rolling_window= []
                            rolling_window.append([prev_ts, 0, [0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0])
    
                            
                        
                            
                        else:
    
                            if (float(aux[0]) - rolling_window[-1][0])/10000000 >= ROLLING_WINDOW_INCREMENT:
                                rolling_window.append([prev_ts, 0, [0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0])
                            if (float(aux[0]) - rolling_window[0][0])/10000000 >= ROLLING_WINDOW_SIZE:
    
                                ##calculate acceleration factor
                                ##store in data frame
                                #calculate_factors(rolling_window[0],driver_id,total_time)
    
                                ##remove first element of rolling_window
                                rolling_window.pop(0)
                            
    
                            jerk= (accel -prev_accel) /  ((float(aux[0])-prev_ts)/10000000+0.0000001)
                            if prev_speed <0.001 and speed <0.001:
                                passo=True
                            else:
                                total_time = total_time +(float(aux[0])-prev_ts)/10000000
                            prev_speed = speed
                            prev_ts = float(aux[0])
                            prev_accel= accel

                    if not passo and 120.0 >= total_time and total_time < 180.0 :                     
                        if jerk < -100:
                            total_jerk_2_3[0] = total_jerk_2_3[0] +1
                        elif jerk <-90:
                             total_jerk_2_3[1] = total_jerk_2_3[1] +1
                        elif jerk <-80:
                             total_jerk_2_3[2] = total_jerk_2_3[2] +1
                        elif jerk <-70:
                             total_jerk_2_3[3] = total_jerk_2_3[3] +1
                        elif jerk <-60:
                             total_jerk_2_3[4] = total_jerk_2_3[4] +1
                        elif jerk <-50:
                             total_jerk_2_3[5] = total_jerk_2_3[5] +1
                        elif jerk <-40:
                             total_jerk_2_3[6] = total_jerk_2_3[6] +1
                        elif jerk <-30:
                             total_jerk_2_3[7] = total_jerk_2_3[7] +1
                        elif jerk <-20:
                             total_jerk_2_3[8] = total_jerk_2_3[8] +1
                        elif jerk <-10:
                             total_jerk_2_3[9] = total_jerk_2_3[9] +1
                        elif jerk <0:
                             total_jerk_2_3[10] = total_jerk_2_3[10] +1
                        elif jerk <10:
                             total_jerk_2_3[11] = total_jerk_2_3[11] +1
                        elif jerk <20:
                             total_jerk_2_3[12] = total_jerk_2_3[12] +1
                        elif jerk <30:
                             total_jerk_2_3[13] = total_jerk_2_3[13] +1
                        elif jerk <40:
                             total_jerk_2_3[14] = total_jerk_2_3[14] +1
                        elif jerk <50:
                             total_jerk_2_3[15] = total_jerk_2_3[15] +1
                        elif jerk <60:
                             total_jerk_2_3[16] = total_jerk_2_3[16] +1
                        elif jerk <70:
                             total_jerk_2_3[17] = total_jerk_2_3[17] +1
                        elif jerk <80:
                             total_jerk_2_3[18] = total_jerk_2_3[18] +1
                        elif jerk <90:
                             total_jerk_2_3[19] = total_jerk_2_3[19] +1
                        elif jerk <100:
                             total_jerk_2_3[20] = total_jerk_2_3[20] +1
                        else:
                            total_jerk_2_3[21] = total_jerk_2_3[21] +1
                        num_jerks_2_3 = num_jerks_2_3 + 1
                    passo=False 

                    if not passo and 180.0 >= total_time and total_time < 240.0 :                     
                        if jerk < -100:
                            total_jerk_3_4[0] = total_jerk_3_4[0] +1
                        elif jerk <-90:
                             total_jerk_3_4[1] = total_jerk_3_4[1] +1
                        elif jerk <-80:
                             total_jerk_3_4[2] = total_jerk_3_4[2] +1
                        elif jerk <-70:
                             total_jerk_3_4[3] = total_jerk_3_4[3] +1
                        elif jerk <-60:
                             total_jerk_3_4[4] = total_jerk_3_4[4] +1
                        elif jerk <-50:
                             total_jerk_3_4[5] = total_jerk_3_4[5] +1
                        elif jerk <-40:
                             total_jerk_3_4[6] = total_jerk_3_4[6] +1
                        elif jerk <-30:
                             total_jerk_3_4[7] = total_jerk_3_4[7] +1
                        elif jerk <-20:
                             total_jerk_3_4[8] = total_jerk_3_4[8] +1
                        elif jerk <-10:
                             total_jerk_3_4[9] = total_jerk_3_4[9] +1
                        elif jerk <0:
                             total_jerk_3_4[10] = total_jerk_3_4[10] +1
                        elif jerk <10:
                             total_jerk_3_4[11] = total_jerk_3_4[11] +1
                        elif jerk <20:
                             total_jerk_3_4[12] = total_jerk_3_4[12] +1
                        elif jerk <30:
                             total_jerk_3_4[13] = total_jerk_3_4[13] +1
                        elif jerk <40:
                             total_jerk_3_4[14] = total_jerk_3_4[14] +1
                        elif jerk <50:
                             total_jerk_3_4[15] = total_jerk_3_4[15] +1
                        elif jerk <60:
                             total_jerk_3_4[16] = total_jerk_3_4[16] +1
                        elif jerk <70:
                             total_jerk_3_4[17] = total_jerk_3_4[17] +1
                        elif jerk <80:
                             total_jerk_3_4[18] = total_jerk_3_4[18] +1
                        elif jerk <90:
                             total_jerk_3_4[19] = total_jerk_3_4[19] +1
                        elif jerk <100:
                             total_jerk_3_4[20] = total_jerk_3_4[20] +1
                        else:
                            total_jerk_3_4[21] = total_jerk_3_4[21] +1
                        num_jerks_3_4 = num_jerks_3_4 + 1
                    passo=False 

                    if not passo and 240.0 >= total_time and total_time < 300.0 :                     
                        if jerk < -100:
                            total_jerk_4_5[0] = total_jerk_4_5[0] +1
                        elif jerk <-90:
                             total_jerk_4_5[1] = total_jerk_4_5[1] +1
                        elif jerk <-80:
                             total_jerk_4_5[2] = total_jerk_4_5[2] +1
                        elif jerk <-70:
                             total_jerk_4_5[3] = total_jerk_4_5[3] +1
                        elif jerk <-60:
                             total_jerk_4_5[4] = total_jerk_4_5[4] +1
                        elif jerk <-50:
                             total_jerk_4_5[5] = total_jerk_4_5[5] +1
                        elif jerk <-40:
                             total_jerk_4_5[6] = total_jerk_4_5[6] +1
                        elif jerk <-30:
                             total_jerk_4_5[7] = total_jerk_4_5[7] +1
                        elif jerk <-20:
                             total_jerk_4_5[8] = total_jerk_4_5[8] +1
                        elif jerk <-10:
                             total_jerk_4_5[9] = total_jerk_4_5[9] +1
                        elif jerk <0:
                             total_jerk_4_5[10] = total_jerk_4_5[10] +1
                        elif jerk <10:
                             total_jerk_4_5[11] = total_jerk_4_5[11] +1
                        elif jerk <20:
                             total_jerk_4_5[12] = total_jerk_4_5[12] +1
                        elif jerk <30:
                             total_jerk_4_5[13] = total_jerk_4_5[13] +1
                        elif jerk <40:
                             total_jerk_4_5[14] = total_jerk_4_5[14] +1
                        elif jerk <50:
                             total_jerk_4_5[15] = total_jerk_4_5[15] +1
                        elif jerk <60:
                             total_jerk_4_5[16] = total_jerk_4_5[16] +1
                        elif jerk <70:
                             total_jerk_4_5[17] = total_jerk_4_5[17] +1
                        elif jerk <80:
                             total_jerk_4_5[18] = total_jerk_4_5[18] +1
                        elif jerk <90:
                             total_jerk_4_5[19] = total_jerk_4_5[19] +1
                        elif jerk <100:
                             total_jerk_4_5[20] = total_jerk_4_5[20] +1
                        else:
                            total_jerk_4_5[21] = total_jerk_4_5[21] +1
                        num_jerks_4_5 = num_jerks_4_5 + 1
                    passo=False 

                    if not passo and 300.0 >= total_time and total_time < 360.0 :                     
                        if jerk < -100:
                            total_jerk_5_6[0] = total_jerk_5_6[0] +1
                        elif jerk <-90:
                             total_jerk_5_6[1] = total_jerk_5_6[1] +1
                        elif jerk <-80:
                             total_jerk_5_6[2] = total_jerk_5_6[2] +1
                        elif jerk <-70:
                             total_jerk_5_6[3] = total_jerk_5_6[3] +1
                        elif jerk <-60:
                             total_jerk_5_6[4] = total_jerk_5_6[4] +1
                        elif jerk <-50:
                             total_jerk_5_6[5] = total_jerk_5_6[5] +1
                        elif jerk <-40:
                             total_jerk_5_6[6] = total_jerk_5_6[6] +1
                        elif jerk <-30:
                             total_jerk_5_6[7] = total_jerk_5_6[7] +1
                        elif jerk <-20:
                             total_jerk_5_6[8] = total_jerk_5_6[8] +1
                        elif jerk <-10:
                             total_jerk_5_6[9] = total_jerk_5_6[9] +1
                        elif jerk <0:
                             total_jerk_5_6[10] = total_jerk_5_6[10] +1
                        elif jerk <10:
                             total_jerk_5_6[11] = total_jerk_5_6[11] +1
                        elif jerk <20:
                             total_jerk_5_6[12] = total_jerk_5_6[12] +1
                        elif jerk <30:
                             total_jerk_5_6[13] = total_jerk_5_6[13] +1
                        elif jerk <40:
                             total_jerk_5_6[14] = total_jerk_5_6[14] +1
                        elif jerk <50:
                             total_jerk_5_6[15] = total_jerk_5_6[15] +1
                        elif jerk <60:
                             total_jerk_5_6[16] = total_jerk_5_6[16] +1
                        elif jerk <70:
                             total_jerk_5_6[17] = total_jerk_5_6[17] +1
                        elif jerk <80:
                             total_jerk_5_6[18] = total_jerk_5_6[18] +1
                        elif jerk <90:
                             total_jerk_5_6[19] = total_jerk_5_6[19] +1
                        elif jerk <100:
                             total_jerk_5_6[20] = total_jerk_5_6[20] +1
                        else:
                            total_jerk_5_6[21] = total_jerk_5_6[21] +1
                        num_jerks_5_6 = num_jerks_5_6 + 1
                    passo=False  

                    if not passo and 360.0 >= total_time and total_time < 420.0 :                     
                        if jerk < -100:
                            total_jerk_6_7[0] = total_jerk_6_7[0] +1
                        elif jerk <-90:
                             total_jerk_6_7[1] = total_jerk_6_7[1] +1
                        elif jerk <-80:
                             total_jerk_6_7[2] = total_jerk_6_7[2] +1
                        elif jerk <-70:
                             total_jerk_6_7[3] = total_jerk_6_7[3] +1
                        elif jerk <-60:
                             total_jerk_6_7[4] = total_jerk_6_7[4] +1
                        elif jerk <-50:
                             total_jerk_6_7[5] = total_jerk_6_7[5] +1
                        elif jerk <-40:
                             total_jerk_6_7[6] = total_jerk_6_7[6] +1
                        elif jerk <-30:
                             total_jerk_6_7[7] = total_jerk_6_7[7] +1
                        elif jerk <-20:
                             total_jerk_6_7[8] = total_jerk_6_7[8] +1
                        elif jerk <-10:
                             total_jerk_6_7[9] = total_jerk_6_7[9] +1
                        elif jerk <0:
                             total_jerk_6_7[10] = total_jerk_6_7[10] +1
                        elif jerk <10:
                             total_jerk_6_7[11] = total_jerk_6_7[11] +1
                        elif jerk <20:
                             total_jerk_6_7[12] = total_jerk_6_7[12] +1
                        elif jerk <30:
                             total_jerk_6_7[13] = total_jerk_6_7[13] +1
                        elif jerk <40:
                             total_jerk_6_7[14] = total_jerk_6_7[14] +1
                        elif jerk <50:
                             total_jerk_6_7[15] = total_jerk_6_7[15] +1
                        elif jerk <60:
                             total_jerk_6_7[16] = total_jerk_6_7[16] +1
                        elif jerk <70:
                             total_jerk_6_7[17] = total_jerk_6_7[17] +1
                        elif jerk <80:
                             total_jerk_6_7[18] = total_jerk_6_7[18] +1
                        elif jerk <90:
                             total_jerk_6_7[19] = total_jerk_6_7[19] +1
                        elif jerk <100:
                             total_jerk_6_7[20] = total_jerk_6_7[20] +1
                        else:
                            total_jerk_6_7[21] = total_jerk_6_7[21] +1
                        num_jerks_6_7 = num_jerks_6_7 + 1
                    passo=False  

                    if not passo and 420.0 >= total_time and total_time < 480.0 :                     
                        if jerk < -100:
                            total_jerk_7_8[0] = total_jerk_7_8[0] +1
                        elif jerk <-90:
                             total_jerk_7_8[1] = total_jerk_7_8[1] +1
                        elif jerk <-80:
                             total_jerk_7_8[2] = total_jerk_7_8[2] +1
                        elif jerk <-70:
                             total_jerk_7_8[3] = total_jerk_7_8[3] +1
                        elif jerk <-60:
                             total_jerk_7_8[4] = total_jerk_7_8[4] +1
                        elif jerk <-50:
                             total_jerk_7_8[5] = total_jerk_7_8[5] +1
                        elif jerk <-40:
                             total_jerk_7_8[6] = total_jerk_7_8[6] +1
                        elif jerk <-30:
                             total_jerk_7_8[7] = total_jerk_7_8[7] +1
                        elif jerk <-20:
                             total_jerk_7_8[8] = total_jerk_7_8[8] +1
                        elif jerk <-10:
                             total_jerk_7_8[9] = total_jerk_7_8[9] +1
                        elif jerk <0:
                             total_jerk_7_8[10] = total_jerk_7_8[10] +1
                        elif jerk <10:
                             total_jerk_7_8[11] = total_jerk_7_8[11] +1
                        elif jerk <20:
                             total_jerk_7_8[12] = total_jerk_7_8[12] +1
                        elif jerk <30:
                             total_jerk_7_8[13] = total_jerk_7_8[13] +1
                        elif jerk <40:
                             total_jerk_7_8[14] = total_jerk_7_8[14] +1
                        elif jerk <50:
                             total_jerk_7_8[15] = total_jerk_7_8[15] +1
                        elif jerk <60:
                             total_jerk_7_8[16] = total_jerk_7_8[16] +1
                        elif jerk <70:
                             total_jerk_7_8[17] = total_jerk_7_8[17] +1
                        elif jerk <80:
                             total_jerk_7_8[18] = total_jerk_7_8[18] +1
                        elif jerk <90:
                             total_jerk_7_8[19] = total_jerk_7_8[19] +1
                        elif jerk <100:
                             total_jerk_7_8[20] = total_jerk_7_8[20] +1
                        else:
                            total_jerk_7_8[21] = total_jerk_7_8[21] +1
                        num_jerks_7_8 = num_jerks_7_8 + 1
                    passo=False   

                    if not passo and 480.0 >= total_time and total_time < 540.0 :                     
                        if jerk < -100:
                            total_jerk_8_9[0] = total_jerk_8_9[0] +1
                        elif jerk <-90:
                             total_jerk_8_9[1] = total_jerk_8_9[1] +1
                        elif jerk <-80:
                             total_jerk_8_9[2] = total_jerk_8_9[2] +1
                        elif jerk <-70:
                             total_jerk_8_9[3] = total_jerk_8_9[3] +1
                        elif jerk <-60:
                             total_jerk_8_9[4] = total_jerk_8_9[4] +1
                        elif jerk <-50:
                             total_jerk_8_9[5] = total_jerk_8_9[5] +1
                        elif jerk <-40:
                             total_jerk_8_9[6] = total_jerk_8_9[6] +1
                        elif jerk <-30:
                             total_jerk_8_9[7] = total_jerk_8_9[7] +1
                        elif jerk <-20:
                             total_jerk_8_9[8] = total_jerk_8_9[8] +1
                        elif jerk <-10:
                             total_jerk_8_9[9] = total_jerk_8_9[9] +1
                        elif jerk <0:
                             total_jerk_8_9[10] = total_jerk_8_9[10] +1
                        elif jerk <10:
                             total_jerk_8_9[11] = total_jerk_8_9[11] +1
                        elif jerk <20:
                             total_jerk_8_9[12] = total_jerk_8_9[12] +1
                        elif jerk <30:
                             total_jerk_8_9[13] = total_jerk_8_9[13] +1
                        elif jerk <40:
                             total_jerk_8_9[14] = total_jerk_8_9[14] +1
                        elif jerk <50:
                             total_jerk_8_9[15] = total_jerk_8_9[15] +1
                        elif jerk <60:
                             total_jerk_8_9[16] = total_jerk_8_9[16] +1
                        elif jerk <70:
                             total_jerk_8_9[17] = total_jerk_8_9[17] +1
                        elif jerk <80:
                             total_jerk_8_9[18] = total_jerk_8_9[18] +1
                        elif jerk <90:
                             total_jerk_8_9[19] = total_jerk_8_9[19] +1
                        elif jerk <100:
                             total_jerk_8_9[20] = total_jerk_8_9[20] +1
                        else:
                            total_jerk_8_9[21] = total_jerk_8_9[21] +1
                        num_jerks_8_9 = num_jerks_8_9 + 1
                    passo=False

                    if not passo and 540.0 >= total_time and total_time < 600.0 :                     
                        if jerk < -100:
                            total_jerk_9_10[0] = total_jerk_9_10[0] +1
                        elif jerk <-90:
                             total_jerk_9_10[1] = total_jerk_9_10[1] +1
                        elif jerk <-80:
                             total_jerk_9_10[2] = total_jerk_9_10[2] +1
                        elif jerk <-70:
                             total_jerk_9_10[3] = total_jerk_9_10[3] +1
                        elif jerk <-60:
                             total_jerk_9_10[4] = total_jerk_9_10[4] +1
                        elif jerk <-50:
                             total_jerk_9_10[5] = total_jerk_9_10[5] +1
                        elif jerk <-40:
                             total_jerk_9_10[6] = total_jerk_9_10[6] +1
                        elif jerk <-30:
                             total_jerk_9_10[7] = total_jerk_9_10[7] +1
                        elif jerk <-20:
                             total_jerk_9_10[8] = total_jerk_9_10[8] +1
                        elif jerk <-10:
                             total_jerk_9_10[9] = total_jerk_9_10[9] +1
                        elif jerk <0:
                             total_jerk_9_10[10] = total_jerk_9_10[10] +1
                        elif jerk <10:
                             total_jerk_9_10[11] = total_jerk_9_10[11] +1
                        elif jerk <20:
                             total_jerk_9_10[12] = total_jerk_9_10[12] +1
                        elif jerk <30:
                             total_jerk_9_10[13] = total_jerk_9_10[13] +1
                        elif jerk <40:
                             total_jerk_9_10[14] = total_jerk_9_10[14] +1
                        elif jerk <50:
                             total_jerk_9_10[15] = total_jerk_9_10[15] +1
                        elif jerk <60:
                             total_jerk_9_10[16] = total_jerk_9_10[16] +1
                        elif jerk <70:
                             total_jerk_9_10[17] = total_jerk_9_10[17] +1
                        elif jerk <80:
                             total_jerk_9_10[18] = total_jerk_9_10[18] +1
                        elif jerk <90:
                             total_jerk_9_10[19] = total_jerk_9_10[19] +1
                        elif jerk <100:
                             total_jerk_9_10[20] = total_jerk_9_10[20] +1
                        else:
                            total_jerk_9_10[21] = total_jerk_9_10[21] +1
                        num_jerks_9_10 = num_jerks_9_10 + 1
                    passo=False             
             

                print driver_id, played_time, total_time              
                dff = open('jerk_clusteringMins_2_3.csv', 'a')
                total_jerk_2_3 = [str(x*1.0/num_jerks_2_3)+', ' for x in total_jerk_2_3]
                total_jerk_2_3[-1]=total_jerk_2_3[-1].replace(',', ' ')
                total_jerk_2_3.append('\n')
                dff.writelines(total_jerk_2_3)
                dff.close()

                dff = open('jerk_clusteringMins_3_4.csv', 'a')
                total_jerk_3_4 = [str(x*1.0/num_jerks_3_4)+', ' for x in total_jerk_3_4]
                total_jerk_3_4[-1]=total_jerk_3_4[-1].replace(',', ' ')
                total_jerk_3_4.append('\n')
                dff.writelines(total_jerk_3_4)
                dff.close()

                dff = open('jerk_clusteringMins_4_5.csv', 'a')
                total_jerk_4_5 = [str(x*1.0/num_jerks_4_5 )+', ' for x in total_jerk_4_5]
                total_jerk_4_5[-1]=total_jerk_4_5[-1].replace(',', ' ')
                total_jerk_4_5.append('\n')
                dff.writelines(total_jerk_4_5)
                dff.close()
                        
                dff = open('jerk_clusteringMins_5_6.csv', 'a')
                total_jerk_5_6 = [str(x*1.0/num_jerks_5_6 )+', ' for x in total_jerk_5_6]
                total_jerk_5_6[-1]=total_jerk_5_6[-1].replace(',', ' ')
                total_jerk_5_6.append('\n')
                dff.writelines(total_jerk_5_6)
                dff.close()

                dff = open('jerk_clusteringMins_6_7.csv', 'a')
                total_jerk_6_7 = [str(x*1.0/num_jerks_6_7 )+', ' for x in total_jerk_6_7]
                total_jerk_6_7[-1]=total_jerk_6_7[-1].replace(',', ' ')
                total_jerk_6_7.append('\n')
                dff.writelines(total_jerk_6_7)
                dff.close()

                dff = open('jerk_clusteringMins_7_8.csv', 'a')
                total_jerk_7_8 = [str(x*1.0/num_jerks_7_8 )+', ' for x in total_jerk_7_8]
                total_jerk_7_8[-1]=total_jerk_7_8[-1].replace(',', ' ')
                total_jerk_7_8.append('\n')
                dff.writelines(total_jerk_7_8)
                dff.close()

                dff = open('jerk_clusteringMins_8_9.csv', 'a')
                total_jerk_8_9 = [str(x*1.0/num_jerks_8_9 )+', ' for x in total_jerk_8_9]
                total_jerk_8_9[-1]=total_jerk_8_9[-1].replace(',', ' ')
                total_jerk_8_9.append('\n')
                dff.writelines(total_jerk_8_9)
                dff.close()

                dff = open('jerk_clusteringMins_9_10.csv', 'a')
                total_jerk_9_10 = [str(x*1.0/num_jerks_9_10 )+', ' for x in total_jerk_9_10]
                total_jerk_9_10[-1]=total_jerk_9_10[-1].replace(',', ' ')
                total_jerk_9_10.append('\n')
                dff.writelines(total_jerk_9_10)
                dff.close()
            df.close()
    
