#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wmi
import pythoncom

class get_server_information:
    def __init__(self):
        pass
    def __connect(self) :
        # wmi线程问题 必须加上下面这句
        pythoncom.CoInitialize()
        conn = wmi.WMI ()
        return conn

#    远程获取基本信息
#    def __init__(self,ip,user,pwd):
#        self.ip = ip
#        self.user = user
#        self.pwd = pwd
#    def __connect(self) :
#        conn = wmi.WMI (ip,user,pwd)
#        return conn
    
    def sys_version(self):
        c = self.__connect()
        tmplist = []
        try :
            for sys in c.Win32_OperatingSystem():
                tmpdict = {}
                tmpdict['VersionDesc'] = sys.Caption
                tmpdict['VersionNumber'] = sys.Caption
                tmpdict['SystemNumber'] = sys.OSArchitecture
                tmpdict['ProcessNumber'] = sys.NumberOfProcesses
                tmplist.append(tmpdict)
        except Exception as e:
            tmpdict = {}
            tmpdict['VersionDesc'] = 'Failed to get:'+str(e)
            tmpdict['VersionNumber'] = 'Failed to get:'+str(e)
            tmpdict['SystemNumber'] = 'Failed to get:'+str(e)
            tmpdict['ProcessNumber'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict)
        return tmplist
     
    def cpu_mem(self):
        c = self.__connect()
        tmplist = []
        try :
            for processor in c.Win32_Processor():
                tmpdict1 = {}
                tmpdict1['CPUDesc'] = processor.Name.strip()
                tmplist.append(tmpdict1)
        except Exception as e:
            tmpdict1 = {}
            tmpdict1['CPUDesc'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict1)
            
        try :
            for Memory in c.Win32_PhysicalMemory():
                tmpdict2 = {}
                tmpdict2['MemoryDesc'] = '%0.2f' %(int(Memory.Capacity)/1048576/1024)
                tmplist.append(tmpdict2)
        except Exception as e:
            tmpdict2 = {}
            tmpdict2['MemoryDesc'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict2)
        return tmplist

    def cpu_use(self):
        c = self.__connect()
        tmplist = []
        try :
            for cpu in c.Win32_Processor(): 
                tmpdict = {}
                tmpdict['DeviceID'] = str(cpu.DeviceID)
                tmpdict['Utilization'] = cpu.LoadPercentage
                tmplist.append(tmpdict)
        except Exception as e:
            tmpdict = {}
            tmpdict['DeviceID'] =  'Failed to get:'+str(e)
            tmpdict['Utilization'] =  'Failed to get:'+str(e)
            tmplist.append(tmpdict)
        return tmplist
                  
    def disk(self):
        c = self.__connect()
        tmplist = []
        try :
            for physical_disk in c.Win32_DiskDrive (): 
                for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"): 
                    for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
                        tmpdict1 = {}
                        tmpdict1['CaptionDesc'] = physical_disk.Caption
                        tmpdict1['PartitionDesc'] = partition.Caption
                        tmpdict1['DriveDesc'] = logical_disk.Caption
                        tmplist.append(tmpdict1)
        except Exception as e:
            tmpdict1 = {}
            tmpdict1['CaptionDesc'] = 'Failed to get:'+str(e)
            tmpdict1['PartitionDesc'] = 'Failed to get:'+str(e)
            tmpdict1['DriveDesc'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict1)
            
        try :
            for disk in c.Win32_LogicalDisk (DriveType=3):
                tmpdict2 = {}
                tmpdict2['DriveDesc'] = disk.Caption
                tmpdict2['DriveSize'] = '%0.2f' %(int(disk.Size)/1048576/1024)
                tmpdict2['DriveFreeSpace'] = '%0.2f' %(int(disk.FreeSpace)/1048576/1024)
                tmpdict2['DrivePercent'] = '%0.2f' %(100.0 * int(disk.FreeSpace)/int(disk.Size))
                tmplist.append(tmpdict2)
        except Exception as e:
            tmpdict2 = {}
            tmpdict2['DriveDesc'] = 'Failed to get:'+str(e)
            tmpdict2['DriveSize'] = 'Failed to get:'+str(e)
            tmpdict2['DriveFreeSpace'] = 'Failed to get:'+str(e)
            tmpdict2['DrivePercent'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict2)
        return tmplist

    def network(self):
        c = self.__connect()
        tmplist = []
        try :
            for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
                tmpdict1 = {}
                tmpdict1['MAC'] = interface.MACAddress
                tmplist.append(tmpdict1)
        except Exception as e:
            tmpdict1 = {}
            tmpdict1['MAC'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict1)
            
        try :
            for ip_address in interface.IPAddress:
                tmpdict2 = {}
                tmpdict2['IP'] = ip_address
                tmplist.append(tmpdict2)
        except Exception as e:
            tmpdict2 = {}
            tmpdict2['IP'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict2)
            
        try :
            for s in c.Win32_StartupCommand ():
                tmpdict3 = {}
                tmpdict3['AutoStartProcess'] = '[%s] %s <%s>' % (s.Location, s.Caption, s.Command)
                tmplist.append(tmpdict3)
        except Exception as e:
            tmpdict3 = {}
            tmpdict3['AutoStartProcess'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict3)    

        try :
            for process in c.Win32_Process ():
                tmpdict4 = {}
                tmpdict4['RunningProcessID'] = process.ProcessId
                tmpdict4['RunningProcessName'] = process.Name
                tmplist.append(tmpdict4)
        except Exception as e:
            tmpdict4 = {}
            tmpdict4['RunningProcessID'] = 'Failed to get:'+str(e)
            tmpdict4['RunningProcessName'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict4)
        return tmplist
    
    def ip_desc(self):
        c = self.__connect()
        tmplist = []
        try :
            for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
                pass
            for ip_address in interface.IPAddress:
                tmpdict = {}
                tmpdict['IP'] = ip_address
                tmplist.append(tmpdict)
        except Exception as e:
            tmpdict = {}
            tmpdict['IP'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict)
        return tmplist
            
    def drive_desc(self):
        c = self.__connect()
        tmplist = []
        try :
            for disk in c.Win32_LogicalDisk (DriveType=3):
                tmpdict = {}
                tmpdict['DriveDesc'] = disk.Caption
                tmpdict['DriveSize'] = '%0.2f' %(int(disk.Size)/1048576/1024)
                tmpdict['DriveFreeSpace'] = '%0.2f' %(int(disk.FreeSpace)/1048576/1024)
                tmpdict['DrivePercent'] = '%0.2f' %(100.0 * int(disk.FreeSpace)/int(disk.Size))
                tmplist.append(tmpdict)
        except Exception as e:
            tmpdict = {}
            tmpdict['DriveDesc'] = 'Failed to get:'+str(e)
            tmpdict['DriveSize'] = 'Failed to get:'+str(e)
            tmpdict['DriveFreeSpace'] = 'Failed to get:'+str(e)
            tmpdict['DrivePercent'] = 'Failed to get:'+str(e)
            tmplist.append(tmpdict)
        return tmplist
