#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import sys
import os
import sendMail
import serverInfo
import dbHelper
import baseSetting

#日志
logging.basicConfig(
    filename = 'D:\\PythonService.log',
    level = logging.DEBUG, 
    format = '[PythonService] %(levelname)-7.7s %(message)s'
)

class MonitorService (win32serviceutil.ServiceFramework):
    #服务名
    _svc_name_ = "MonitorService"
    #服务显示名
    _svc_display_name_ = "MonitorService"
    #服务描述
    _svc_description_ = 'A Python Service For Checking Server Backup'
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('--%s-- Stop Python Monitor Service ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )
        self.main()

    def main(self):
        logging.info('--%s-- Start Python Monitor Service ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
        logging.info('--%s-- Start Load Job Setting ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
        excute_flag = False
        try :
            job = baseSetting.property_setting()
            job_list = job.job_setting()
            clock = job_list[0]['clock']
            interval = int(job_list[0]['interval'])
            excute_flag = True
        except Exception as e :
            logging.info('--%s-- Load Job Setting Error ... %s' %(time.strftime('%Y-%m-%d %H:%M:%S'),str(e)))
        logging.info('--%s-- Finish Load Job Setting ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
        if excute_flag :
            while 1:
                logging.info('--%s-- Excute Python Monitor Service ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
                if self.stop_requested:
                    logging.info('--%s-- A Stop Signal Was Received: Breaking Main Loop ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
                    break
                else :
                    try :                    
                        if time.strftime('%H') == clock :
                            logging.info('--%s-- Start Load base Setting ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
                            base = baseSetting.property_setting()
                            
                            senderList = base.sender_setting()
                            mail_user = senderList[0]['mailuser']
                            mail_pass = senderList[0]['mailpwd']
                            mail_postfix = senderList[0]['mailpostfix']
                            mail_host = senderList[0]['mailhost']
                            mail_success_subject = senderList[0]['successsubject']
                            mail_success_context = senderList[0]['successcontext']
                            mail_fail_subject = senderList[0]['failsubject']
                            mail_fail_context = senderList[0]['failcontext']
                            
                            mailto_list = base.reciever_setting()
                            
                            backupList = base.backup_setting()
                            file_path = backupList[0]['filepath']
                            file_name = backupList[0]['filename']

                            file_fullname = os.path.join(file_path,file_name) %time.strftime('%Y%m%d')
                            
                            databaseList = base.database_setting()
                            db_host = databaseList[0]['ip']
                            db_user = databaseList[0]['user']
                            db_pwd = databaseList[0]['password']
                            db_db = databaseList[0]['db']
                            db_port = databaseList[0]['port']
                            
                            logging.info('--%s-- Finish Load base Setting ...' %time.strftime('%Y-%m-%d %H:%M:%S'))
                            
                            if os.path.exists(file_fullname):
                                logging.info('--%s-- Backup Success' %time.strftime('%Y-%m-%d %H:%M:%S'))
                                mail_sub = mail_success_subject +'----' + time.strftime('%Y-%m-%d %H:%M:%S')
                                mail_context = mail_success_context
                                backup_flag = 1
                            else:                            
                                logging.info('--%s-- Backup Faild' %time.strftime('%Y-%m-%d %H:%M:%S'))
                                mail_sub =mail_fail_subject +'----' + time.strftime('%Y-%m-%d %H:%M:%S')
                                mail_context = mail_fail_context
                                backup_flag = 0
                                
                            logging.info('--%s-- Start Send E-Mail' %time.strftime('%Y-%m-%d %H:%M:%S'))
                            s = sendMail.send_mail(mail_host,mail_user,mail_pass,mail_postfix)                   
                            send_flag = s.send(mailto_list,mail_sub,mail_context)
                            logging.info('--%s-- Finish Send E-Mail' %time.strftime('%Y-%m-%d %H:%M:%S'))
                            conn = serverInfo.get_server_information()
                            ipList = conn.ip_desc()
                            driveList = conn.drive_desc()
                            dataList = []
                            for drive in driveList:
                                dataSubList = []
                                dataSubList.append([ipList[0]['IP']])
                                dataSubList.append(drive['DriveDesc'])
                                dataSubList.append(drive['DriveSize'])
                                dataSubList.append(drive['DriveFreeSpace'])
                                dataSubList.append(backup_flag)
                                dataSubList.append(send_flag)
                                dataList.append(tuple(dataSubList))
                            logging.info('--%s-- Start Insert Database' %time.strftime('%Y-%m-%d %H:%M:%S'))    
                            ms = dbHelper.MSSQL(db_host,db_user,db_pwd,db_db)
                            ms.InsertMany('INSERT INTO MS_Record ([IPV4],[Drive],[DriveSize],[DriveFree]\
                                                    ,[Backups],[SendMail]) VALUES (%s,%s,%s,%s,%s,%s)',dataList)
                            logging.info('--%s-- Finish Insert Database' %time.strftime('%Y-%m-%d %H:%M:%S'))
                        else :
                            pass
                    except Exception as e :
                        logging.info('--%s-- Python Monitor Service Error : %s' %(time.strftime('%Y-%m-%d %H:%M:%S'),str(e)))
                time.sleep(interval)
        else :
            pass
        return

if __name__ == '__main__':
    #下面的代码可以确保打包后的exe服务可以正常启动
    #如果只是python service.py install start stop remove 是没有问题的 但是如果打包成exe 不加下面的代码会出现1503的error
    #另外打包的时候需要把脚本直接放在桌面上打包 否则还是会出现上面的问题
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MonitorService)
##    win32serviceutil.HandleCommandLine(MonitorService)
