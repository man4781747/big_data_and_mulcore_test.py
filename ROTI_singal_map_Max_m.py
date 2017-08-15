# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:49:00 2017

@author: Chuanping_LASC_PC
"""
import matplotlib
matplotlib.use('Agg')
import scipy.io
import numpy as np
import os
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import multiprocessing as mp

def job(time_chose):      
    
    global year,day,databox,time_box,time_range
#    print 'job start'
    (lat_max,lat_min) = (75.,5.)                 
    (long_max,long_min) = (-65.,-125.)
    net_chose_range = 1.   
    ### ROTI 部份 ###
#    print 'ROTI start'
    ROTI_chose = databox[13,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    lat_chose = databox[6,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    lon_chose = databox[7,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    ang_chose = databox[8,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    
    lon_net = np.arange(long_min,long_max+1,net_chose_range)
    lat_net = np.arange(lat_min,lat_max+1,net_chose_range)

    net_lon,net_lat = np.meshgrid(lon_net,lat_net)    
    
    ROTI_net = np.zeros((len(lat_net),len(lon_net)))    
    
    lon_net_chose_num = 0
    while lon_net_chose_num < len(lon_net)-1:
        lat_net_chose_num = 0
        while lat_net_chose_num < len(lat_net)-1:
            ROTI_lat_lon_chose = ROTI_chose[np.where((
                                            (lat_chose >= lat_net[lat_net_chose_num])
                                           &(lat_chose < lat_net[lat_net_chose_num+1])
                                           &(lon_chose >= lon_net[lon_net_chose_num])
                                           &(lon_chose < lon_net[lon_net_chose_num+1])
                                           &(ang_chose > 21.)
                                           ))]
            if len(ROTI_lat_lon_chose) != 0.:              
                ROTI_lat_lon_chose_max = max(ROTI_lat_lon_chose)
                ROTI_net[lat_net_chose_num,lon_net_chose_num] = ROTI_lat_lon_chose_max
            lat_net_chose_num += 1
        lon_net_chose_num += 1
    ROTI_chose = []
    
    ### ROTI 部分結束 ###
    ### Lose 部份開始 ###
#    print 'Lose start'
    L1_chose = databox[0,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    L2_chose = databox[1,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    P1_chose = databox[2,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    P2_chose = databox[3,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    C1_chose = databox[4,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    
    lat_chose_num = np.copy(lat_chose)
    lat_chose_num[np.where(lat_chose_num != 0)] = 1
    lon_chose_num = np.copy(lon_chose)
    lon_chose_num[np.where(lon_chose_num != 0)] = 1
    ang_chose_num = np.copy(ang_chose)
    ang_chose_num[np.where(ang_chose_num != 0)] = 1  
    lon_chose_sum_all = np.zeros((0,32))
    lat_chose_sum_all = np.zeros((0,32))
    ang_chose_sum_all = np.zeros((0,32))
    station_num = 0
    while station_num < len(databox[5]):
        lat_chose_sum = np.array([sum(lat_chose[station_num])/sum(lat_chose_num[station_num])])
        lat_chose_sum_all = np.concatenate((lat_chose_sum_all , lat_chose_sum))        
        lon_chose_sum = np.array([sum(lon_chose[station_num])/sum(lon_chose_num[station_num])])
        lon_chose_sum_all = np.concatenate((lon_chose_sum_all , lon_chose_sum))        
        ang_chose_sum = np.array([sum(ang_chose[station_num])/sum(ang_chose_num[station_num])])
        ang_chose_sum_all = np.concatenate((ang_chose_sum_all , ang_chose_sum))        
        station_num += 1

    lat_lose_data_sum = np.copy(lat_chose_sum_all)
    lon_lose_data_sum = np.copy(lon_chose_sum_all)
    ang_lose_data_sum = np.copy(ang_chose_sum_all)    
        
    L1_lose_data_sum_all = np.zeros((0,32))
    L2_lose_data_sum_all = np.zeros((0,32))
    P1_lose_data_sum_all = np.zeros((0,32))
    P2_lose_data_sum_all = np.zeros((0,32))
    C1_lose_data_sum_all = np.zeros((0,32))
    lat_lose_data_sum_all = np.zeros((0,32))
    lon_lose_data_sum_all = np.zeros((0,32))
    ang_lose_data_sum_all = np.zeros((0,32))
    
    station_num_lose = 0
    while station_num_lose < len(databox[1]):       
        L1_lose_data_sum = np.array([sum(L1_chose[station_num_lose])/2])
        L1_lose_data_sum_all = np.concatenate((L1_lose_data_sum_all , L1_lose_data_sum))
        L2_lose_data_sum = np.array([sum(L2_chose[station_num_lose])/2])
        L2_lose_data_sum_all = np.concatenate((L2_lose_data_sum_all , L2_lose_data_sum))
        P1_lose_data_sum = np.array([sum(P1_chose[station_num_lose])/2])
        P1_lose_data_sum_all = np.concatenate((P1_lose_data_sum_all , P1_lose_data_sum))
        P2_lose_data_sum = np.array([sum(P2_chose[station_num_lose])/2])
        P2_lose_data_sum_all = np.concatenate((P2_lose_data_sum_all , P2_lose_data_sum))
        C1_lose_data_sum = np.array([sum(C1_chose[station_num_lose])/2])
        C1_lose_data_sum_all = np.concatenate((C1_lose_data_sum_all , C1_lose_data_sum))
        lat_lose_data_sum_all = np.concatenate((lat_lose_data_sum_all , np.array([lat_lose_data_sum[station_num_lose]])))
        lon_lose_data_sum_all = np.concatenate((lon_lose_data_sum_all , np.array([lon_lose_data_sum[station_num_lose]])))
        ang_lose_data_sum_all = np.concatenate((ang_lose_data_sum_all , np.array([ang_lose_data_sum[station_num_lose]])))
        
        station_num_lose += 1
    
    L1_chose = []
    L2_chose = []
    P1_chose = []
    P2_chose = []
    C1_chose = []
    
    L1_lose_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
    L2_lose_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
    P1_lose_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
    P2_lose_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
    C1_lose_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
                         
    ### Lose 部分結束 ###
    ### Slip 部份開始 ###
#    print 'slip start'
    L1_slip = np.copy(databox[9,0:,time_range*time_chose:time_range*(time_chose+1),0:])
    L2_slip = databox[10,0:,time_range*time_chose:time_range*(time_chose+1),0:]
#    P1_slip = databox[11,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    P2_slip = databox[11,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    C1_slip = databox[12,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    
    L1_slip_data_sum_all = np.zeros((0,32))
    L2_slip_data_sum_all = np.zeros((0,32))
#    P1_slip_data_sum_all = np.zeros((0,32))
    P2_slip_data_sum_all = np.zeros((0,32))
    C1_slip_data_sum_all = np.zeros((0,32))
    
    station_num_slip = 0
    while station_num_slip < len(databox[1]):
        L1_slip_data_sum = np.array([sum(L1_slip[station_num_slip])])
        L1_slip_data_sum_all = np.concatenate((L1_slip_data_sum_all , L1_slip_data_sum))
        L2_slip_data_sum = np.array([sum(L2_slip[station_num_slip])])
        L2_slip_data_sum_all = np.concatenate((L2_slip_data_sum_all , L2_slip_data_sum))
#        P1_slip_data_sum = np.array([sum(P1_slip[station_num_slip])])
#        P1_slip_data_sum_all = np.concatenate((P1_slip_data_sum_all , P1_slip_data_sum))
        P2_slip_data_sum = np.array([sum(P2_slip[station_num_slip])])
        P2_slip_data_sum_all = np.concatenate((P2_slip_data_sum_all , P2_slip_data_sum))
        C1_slip_data_sum = np.array([sum(C1_slip[station_num_slip])])
        C1_slip_data_sum_all = np.concatenate((C1_slip_data_sum_all , C1_slip_data_sum))

        station_num_slip += 1

    L1_slip = []
    L2_slip = []
    P2_slip = []
    C1_slip = []

    L1_slip_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
    L2_slip_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
#    P1_slip_data_sum_all[np.where(ang_lose_data_sum_all < 15.)] = 0.
    P2_slip_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.
    C1_slip_data_sum_all[np.where(ang_lose_data_sum_all < 21.)] = 0.        

    ### Slip 部份結束 ###     
    ### TEC 部份開始 ###
#    print 'TEC start'
    TEC_chose = databox[5,0:,time_range*time_chose:time_range*(time_chose+1),0:]
    
    TEC_net = np.zeros((len(lat_net),len(lon_net)))    
    
    lon_net_chose_num = 0
    while lon_net_chose_num < len(lon_net)-1:
        lat_net_chose_num = 0
        while lat_net_chose_num < len(lat_net)-1:
            TEC_lat_lon_chose = TEC_chose[np.where((
                                            (lat_chose >= lat_net[lat_net_chose_num])
                                           &(lat_chose < lat_net[lat_net_chose_num+1])
                                           &(lon_chose >= lon_net[lon_net_chose_num])
                                           &(lon_chose < lon_net[lon_net_chose_num+1])
                                           &(ang_chose > 21.)
                                           ))]
            if len(TEC_lat_lon_chose) != 0.:
                TEC_lat_lon_chose_max = max(TEC_lat_lon_chose)
                TEC_net[lat_net_chose_num,lon_net_chose_num] = TEC_lat_lon_chose_max
            lat_net_chose_num += 1
        lon_net_chose_num += 1
        
    TEC_chose = []
    ### TEC 部分結束 ###
#    print 'plt start'
    ### 底圖 ###
    coast_long = scipy.io.loadmat('coast.mat')['long']
    coast_lat = scipy.io.loadmat('coast.mat')['lat']   
    
    cm2inch = 1./2.54            
    figszX = 32.                                                    # unit in cm
    figszY = 18.                                                    # unit in cm
    figdpi = 300                                                    # dpi
    figfacecolor='w'
    figedgecolor='k'
                
    xlimit_max = long_max
    xlimit_min = long_min
    xlimit_range = 3.
    xlimit = [xlimit_min, xlimit_max,  xlimit_range]
            
    ylimit_max = lat_max+10
    ylimit_min = lat_min-10
    ylimit_range = 2.
    ylimit = [  ylimit_min, ylimit_max, ylimit_range]

    cmin =  0.    # if fixclim=='dynamic', cmin & cmax is useless   #""" 主圖數值下標 """
    cmax =  0.015  # if fixclim=='dynamic', cmin & cmax is useless
    
    wdsz_title=5
    wdsz_ctitle=5
    wdsz_axis_tick = 5
    wdsz_axis_label = 5
    title ="data_name[num_data]"
    axis_font  = {'size': str(wdsz_axis_label), 'color': 'black', 'weight': 'bold'}     
    title_font = {'size': str(wdsz_title), 'color': 'black', 'weight': 'bold',
                  'verticalalignment': 'bottom'}  # Bottom vertical alignment for more space
                  
    x_fig1_LowerLeft   = 0.1                                         # 左下角x值
    y_fig1_LowerLeft   = 0.07                                        # 右下角x值
    width_fig1  = 0.2                                                # 寬
    height_fig1 = 0.35
    
    x_fig2_LowerLeft   = 0.35                                         # 左下角x值
    y_fig2_LowerLeft   = 0.07                                        # 右下角x值
    width_fig2  = 0.2                                                # 寬
    height_fig2 = 0.35
    
    x_fig3_LowerLeft   = 0.63                                         # 左下角x值
    y_fig3_LowerLeft   = 0.07                                        # 右下角x值
    width_fig3  = 0.2                                                # 寬
    height_fig3 = 0.35
    
    x_fig4_LowerLeft   = 0.1                                         # 左下角x值
    y_fig4_LowerLeft   = 0.55                                        # 右下角x值
    width_fig4  = 0.2                                                # 寬
    height_fig4 = 0.35
    
    x_fig5_LowerLeft   = 0.35                                         # 左下角x值
    y_fig5_LowerLeft   = 0.55                                        # 右下角x值
    width_fig5  = 0.2                                                # 寬
    height_fig5 = 0.35
    
    x_fig6_LowerLeft   = 0.56                                         # 左下角x值
    y_fig6_LowerLeft   = 0.55                                      # 右下角x值
    width_fig6  = 0.025                                                # 寬
    height_fig6 = 0.35

    x_fig7_LowerLeft   = 0.85                                         # 左下角x值
    y_fig7_LowerLeft   = 0.07                                      # 右下角x值
    width_fig7  = 0.025                                                # 寬
    height_fig7 = 0.35

#    x_fig8_LowerLeft   = 0.63                                         # 左下角x值
#    y_fig8_LowerLeft   = 0.55                                        # 右下角x值
#    width_fig8  = 0.2                                                # 寬
#    height_fig8 = 0.35
    
    coast_xlimit_max = long_max
    coast_xlimit_min = long_min
    coast_xlimit_range = 30.
    coast_xlimit = [coast_xlimit_min, coast_xlimit_max,  coast_xlimit_range]
    
    coast_ylimit_max = lat_max
    coast_ylimit_min = lat_min
    coast_ylimit_range = 10.
    coast_ylimit = [  coast_ylimit_min, coast_ylimit_max, coast_ylimit_range]           
    
    coast_xticks = np.arange(coast_xlimit[0], coast_xlimit[1] + coast_xlimit[2], coast_xlimit[2])
    coast_yticks = np.arange(coast_ylimit[0], coast_ylimit[1] + coast_ylimit[2], coast_ylimit[2])
    
    
    cmap = cm.jet
    
    xticks = np.arange(xlimit[0], xlimit[1] + xlimit[2], xlimit[2])
    yticks = np.arange(ylimit[0], ylimit[1] + ylimit[2], ylimit[2])
    
    fig1 = plt.figure(num=1, figsize=(figszX*cm2inch, figszY*cm2inch),
                      dpi = figdpi, facecolor=figfacecolor, edgecolor=figedgecolor)
                      
                      
    ax_fig1 = fig1.add_axes([x_fig1_LowerLeft, y_fig1_LowerLeft, width_fig1, height_fig1])
    ax_fig2 = fig1.add_axes([x_fig2_LowerLeft, y_fig2_LowerLeft, width_fig2, height_fig2])
    ax_fig3 = fig1.add_axes([x_fig3_LowerLeft, y_fig3_LowerLeft, width_fig3, height_fig3])
    ax_fig4 = fig1.add_axes([x_fig4_LowerLeft, y_fig4_LowerLeft, width_fig4, height_fig4])
    ax_fig5 = fig1.add_axes([x_fig5_LowerLeft, y_fig5_LowerLeft, width_fig5, height_fig5])
    ax_fig6 = fig1.add_axes([x_fig6_LowerLeft, y_fig6_LowerLeft, width_fig6, height_fig6]) 
    ax_fig7 = fig1.add_axes([x_fig7_LowerLeft, y_fig7_LowerLeft, width_fig7, height_fig7]) 
#    ax_fig8 = fig1.add_axes([x_fig8_LowerLeft, y_fig8_LowerLeft, width_fig8, height_fig8]) 
        
    plt_coast = ax_fig1.plot(coast_long, coast_lat,color='black',linewidth=0.5 )
    plt_coast = ax_fig2.plot(coast_long, coast_lat,color='black',linewidth=0.5 )
    plt_coast = ax_fig3.plot(coast_long, coast_lat,color='black',linewidth=0.5 )
    plt_coast = ax_fig4.plot(coast_long, coast_lat,color='black',linewidth=0.5 )
    plt_coast = ax_fig5.plot(coast_long, coast_lat,color='black',linewidth=0.5 )
#    plt_coast = ax_fig8.plot(coast_long, coast_lat,color='black',linewidth=0.5 )
    
    
    
#    ax_fig1.axis('equal')
    ax_fig1.set_xlim(coast_xlimit[0:1+1])
    ax_fig1.set_ylim(coast_ylimit[0:1+1])
    ax_fig1.set_xticks(coast_xticks)
    ax_fig1.set_yticks(coast_yticks)
#    ax_fig2.axis('equal')
    ax_fig2.set_xlim(coast_xlimit[0:1+1])
    ax_fig2.set_ylim(coast_ylimit[0:1+1])
    ax_fig2.set_xticks(coast_xticks)
    ax_fig2.set_yticks(coast_yticks)
#    ax_fig3.axis('equal')
    ax_fig3.set_xlim(coast_xlimit[0:1+1])
    ax_fig3.set_ylim(coast_ylimit[0:1+1])
    ax_fig3.set_xticks(coast_xticks)
    ax_fig3.set_yticks(coast_yticks)
#    ax_fig4.axis('equal')
    ax_fig4.set_xlim(coast_xlimit[0:1+1])
    ax_fig4.set_ylim(coast_ylimit[0:1+1])
    ax_fig4.set_xticks(coast_xticks)
    ax_fig4.set_yticks(coast_yticks)
#    ax_fig5.axis('equal')
    ax_fig5.set_xlim(coast_xlimit[0:1+1])
    ax_fig5.set_ylim(coast_ylimit[0:1+1])
    ax_fig5.set_xticks(coast_xticks)
    ax_fig5.set_yticks(coast_yticks)
#    ax_fig8.axis('equal')
#    ax_fig8.set_xlim(coast_xlimit[0:1+1])
#    ax_fig8.set_ylim(coast_ylimit[0:1+1])
#    ax_fig8.set_xticks(coast_xticks)
#    ax_fig8.set_yticks(coast_yticks)
        
    dc_plt = 100.   # useless now
    dc_label = 4.e5 # useless now
    
    c_plt = [cmin, cmax, dc_plt]
    c_label = [cmin, cmax, dc_label]
    
    ax_fig1.set_title("L1")
    ax_fig2.set_title("L2")
    ax_fig3.set_title("TEC")
    ax_fig4.set_title("P2")
    ax_fig5.set_title("C1")
    ax_fig6.set_title(time_box[time_range*time_chose])   
#    ax_fig8.set_title("GUVI")
    
    cmap = plt.cm.get_cmap("jet")
    cmap.set_under("white")      

#===================== plt_ROTI =================
    plt_all_1 = ax_fig1.scatter(net_lon[np.where(ROTI_net != 0.)], net_lat[np.where(ROTI_net != 0.)], c=ROTI_net[np.where(ROTI_net != 0.)],
                             s=7*net_chose_range, marker='o', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=5)
    plt_all_2 = ax_fig2.scatter(net_lon[np.where(ROTI_net != 0.)], net_lat[np.where(ROTI_net != 0.)], c=ROTI_net[np.where(ROTI_net != 0.)],
                             s=7*net_chose_range, marker='o', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=5)
    plt_all_3 = ax_fig3.scatter(net_lon[np.where(TEC_net != 0.)], net_lat[np.where(TEC_net != 0.)], c=TEC_net[np.where(TEC_net != 0.)],
                             s=7*net_chose_range, marker='o', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=5)
    plt_all_4 = ax_fig4.scatter(net_lon[np.where(ROTI_net != 0.)], net_lat[np.where(ROTI_net != 0.)], c=ROTI_net[np.where(ROTI_net != 0.)],
                             s=7*net_chose_range, marker='o', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=5)
    plt_all_5 = ax_fig5.scatter(net_lon[np.where(ROTI_net != 0.)], net_lat[np.where(ROTI_net != 0.)], c=ROTI_net[np.where(ROTI_net != 0.)],
                             s=7*net_chose_range, marker='o', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=5)
                             
    plt_all_1.set_clim(vmin=cmin,vmax=cmax)
    plt_all_2.set_clim(vmin=cmin,vmax=cmax)
    plt_all_3.set_clim(vmin=0.,vmax=120.) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    plt_all_4.set_clim(vmin=cmin,vmax=cmax)
    plt_all_5.set_clim(vmin=cmin,vmax=cmax)

    plt_all_1.set_cmap('summer')
    plt_all_2.set_cmap('summer')
    plt_all_3.set_cmap('summer')
    plt_all_4.set_cmap('summer')
    plt_all_5.set_cmap('summer')
    
    cb1 = fig1.colorbar(plt_all_1, cax=ax_fig6)
    cb1.ax.tick_params(pad=2, labelsize=wdsz_axis_label)
#                cb1.set_label(ctitle, fontsize = wdsz_ctitle,weight='bold')
#    cb1.formatter.set_powerlimits((0, 2))
    cb1.update_ticks()    
    
#===================== slip
    plt_slip_L1 = ax_fig1.scatter(lon_lose_data_sum_all[np.where(L1_slip_data_sum_all > 0.)], 
                                  lat_lose_data_sum_all[np.where(L1_slip_data_sum_all > 0.)], 
                                c= '#FF0000',
                             s=10, marker='x', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)
    plt_slip_L2 = ax_fig2.scatter(lon_lose_data_sum_all[np.where(L2_slip_data_sum_all > 0.)], 
                                  lat_lose_data_sum_all[np.where(L2_slip_data_sum_all > 0.)], 
                                c= '#FF0000',
                             s=10, marker='x', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)
#    plt_slip_P1 = ax_fig1.scatter(lon_lose_data_sum_all[np.where(P1_slip_data_sum_all > 0.)], 
#                                  lat_lose_data_sum_all[np.where(P1_slip_data_sum_all > 0.)], 
#                                c= '	#FF0000',
#                             s=25, marker='x', cmap=cmap, edgecolors=None ,
#                             linewidths=0, zorder=10)
    plt_slip_P2 = ax_fig4.scatter(lon_lose_data_sum_all[np.where(P2_slip_data_sum_all > 0.)], 
                                  lat_lose_data_sum_all[np.where(P2_slip_data_sum_all > 0.)], 
                                c= '#FF0000',
                             s=10, marker='x', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)
    plt_slip_C1 = ax_fig5.scatter(lon_lose_data_sum_all[np.where(C1_slip_data_sum_all > 0.)], 
                                  lat_lose_data_sum_all[np.where(C1_slip_data_sum_all > 0.)], 
                                c= '#FF0000',
                             s=10, marker='x', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)

#===================== loss of lock
    plt_lose_L1 = ax_fig1.scatter(lon_lose_data_sum_all[np.where(L1_lose_data_sum_all > 0.1)], 
                                  lat_lose_data_sum_all[np.where(L1_lose_data_sum_all > 0.1)], 
                                c= '#FF00FF',
                             s=25, marker='*', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)
    plt_lose_L2 = ax_fig2.scatter(lon_lose_data_sum_all[np.where(L2_lose_data_sum_all > 0.1)], 
                                  lat_lose_data_sum_all[np.where(L2_lose_data_sum_all > 0.1)], 
                                c= '#FF00FF',
                             s=25, marker='*', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)
#    plt_lose_P1 = ax_fig3.scatter(lon_lose_data_sum_all[np.where(P1_lose_data_sum_all > 0.1)], 
#                                  lat_lose_data_sum_all[np.where(P1_lose_data_sum_all > 0.1)], 
#                                c= '#FF00FF',
#                             s=25, marker='*', cmap=cmap, edgecolors=None ,
#                             linewidths=0, zorder=10)
    plt_lose_P2 = ax_fig4.scatter(lon_lose_data_sum_all[np.where(P2_lose_data_sum_all > 0.1)], 
                                  lat_lose_data_sum_all[np.where(P2_lose_data_sum_all > 0.1)], 
                                c= '#FF00FF',
                             s=25, marker='*', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)
    plt_lose_C1 = ax_fig5.scatter(lon_lose_data_sum_all[np.where(C1_lose_data_sum_all > 0.1)], 
                                  lat_lose_data_sum_all[np.where(C1_lose_data_sum_all > 0.1)], 
                                c= '#FF00FF',
                             s=25, marker='*', cmap=cmap, edgecolors=None ,
                             linewidths=0, zorder=10)
                             
    cb2 = plt.colorbar(plt_all_3, cax=ax_fig7)
    cb2.ax.tick_params(pad=2)

    save_address = "./data20{0}{1}/ROTI_singal_Max_{0}{1}_{2}/".format(year,day,time_range)
    save_name = "ROTI_singal_Max_{0}{1}{2}{3}".format(year,day,time_range,time_chose)    
    plt.savefig(os.path.join(save_address, save_name), bbox_inches = 'tight', dpi = figdpi)
    
    plt.clf()     

    return time_box[time_range*time_chose]


def multucore(processes_num):
    pool = mp.Pool(processes=processes_num)
#    multi_res = [pool.apply_async(job,(data_name,)) for data_name in data_list ]
#    print [res.get() for res in multi_res]
    global time_range
    res = [pool.apply_async(job, (i,)) for i in range(2880/time_range)]
    print [R.get() for R in res]


if __name__ == '__main__':
    import time    
    t1 = time.time()
    
    
    year = input("year(str):")
    day  = input("day(str):")
    
    processes_num = int(input("processes_num(str):"))

    time_range = input("time_range(int):")    

    if os.path.exists('./data20{0}{1}/ROTI_singal_Max_{0}{1}_{2}'.format(year,day,time_range)) == False:
        os.makedirs('./data20{0}{1}/ROTI_singal_Max_{0}{1}_{2}'.format(year,day,time_range))    

    databox = np.load('./data20{0}{1}/databox{0}{1}.npy'.format(year,day)) 
    print 'databox losd OK!!'
    time_box_for = "{hh:02d}:{mm:02d}:{ss:02d}"
    time_box = [time_box_for.format(hh=hh,mm=mm,ss=ss) for hh in range(0,24) for mm in range(0,60) for ss in [0,30]]
    
    multucore(processes_num)
    
    t2 = time.time()
    print t2-t1