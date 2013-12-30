#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:22:36 2013

@author: zealot
"""

import subprocess
import time
import psutil



now_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
webserver_process = "tomcat"
database_process = "mysql"




class PSU(object):
    def __init__(self):
        self.warning_report = ""
        
    def get_system_status(self):
       
        system_info = []
        
        get_sys_cpu_info = str(psutil.cpu_percent(interval=int(psutil.NUM_CPUS))) + "%"
        get_sys_mem_info = "total phymem: " + str(int(psutil.TOTAL_PHYMEM ) /1000 /1000) + " MB"
        get_sys_virtmem_info = "total virtmem: " + str(int(psutil.total_virtmem()) /1000 /1000) + " MB"
        system_info.append([get_sys_cpu_info,get_sys_mem_info,get_sys_virtmem_info])
                
        return system_info
        
    def get_system_disk_status(self):
        
        get_sys_disk_partitions_list = []

        for get_sys_disk_partitions_info in psutil.disk_partitions():
            get_sys_disk_partitions_list.append(get_sys_disk_partitions_info.mountpoint)
        
        get_sys_disk_usage_list = []
        
        for get_sys_disk_partitions in get_sys_disk_partitions_list:
            disk_usage = psutil.disk_usage(get_sys_disk_partitions)
            get_sys_disk_usage_list.append([str(int(disk_usage.total) /1000 /1000 ) + "MB",str(int(disk_usage.used) /1000 /1000) + "MB" ,str(int(disk_usage.free) /1000 /1000) + "MB" ,str(disk_usage.percent) + "%"])
            
        disk_info_dict = dict(zip(get_sys_disk_partitions_list,get_sys_disk_usage_list))
        
        return disk_info_dict
        
            
    def get_apps_status(self):
        
        process_list = psutil.get_process_list()
        
        if webserver_process in process_list:
            apps_ststus = "alive"
        else:
            apps_ststus = "dead"
        
        
        return apps_ststus
        
    
    def get_database_ststus(self):
        
        process_list = psutil.get_process_list()
        
        if database_process in process_list:
            database_status = "alive"
        else:
            database_status = "dead"
            
        return database_status
        
        
    def get_network_ststus(self):
       
        network_io_ststus = []        
        
        network_stats_list = psutil.network_io_counters()
        
        network_in_bytes = int(network_stats_list.bytes_recv)
        network_out_bytes = int(network_stats_list.bytes_sent)
        network_in_packets = int(network_stats_list.packets_recv)
        network_out_packets = int(network_stats_list.packets_sent)
       
#        print network_out_bytes
        time.sleep(2)
        network_stats_list = psutil.network_io_counters()
        network_in_bytes_new = int(network_stats_list.bytes_recv)
        network_out_bytes_new = int(network_stats_list.bytes_sent)
        network_in_packets_new = int(network_stats_list.packets_recv)
        network_out_packets_new = int(network_stats_list.packets_sent)
        
#        print network_out_bytes_new
        network_in_bytes_ststus = int(network_in_bytes_new) - int(network_in_bytes)
        network_out_bytes_ststus = int(network_out_bytes_new) - int(network_out_bytes)
#        network_in_packets_ststus = int(network_in_packets_new) - int(network_in_packets)
#        network_out_packets_ststus = int(network_out_packets_new) - int(network_out_packets)
        
        network_io_ststus.append([network_in_bytes_ststus,network_out_bytes_ststus])
        
        return network_io_ststus
        
    


mypc = PSU()
system_info = mypc.get_system_status()
disk_info = mypc.get_system_disk_status()
apps_ststus = mypc.get_apps_status()
network_io = mypc.get_network_ststus()
print now_time
print system_info
print disk_info
print apps_ststus
print network_io       