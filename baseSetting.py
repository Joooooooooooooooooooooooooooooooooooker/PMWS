#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sys

class property_setting :
      def __init__(self) :
            pass
      
      def __get_property(self):
            tree = ET.parse('D:\\property.xml')
            root = tree.getroot()
            return root
      
      def job_setting(self) :
            root = self.__get_property()
            temlist = []
            for j in root.findall('job'):
                  tmpdict = {}
                  tmpdict['clock'] = j.find('clock').text
                  tmpdict['interval'] = j.find('interval').text
                  temlist.append(tmpdict)
            return temlist
      
      def sender_setting(self) :
            root = self.__get_property()
            temlist = []
            for s in root.findall('sender'):
                  tmpdict = {}
                  tmpdict['mailuser'] = s.find('mailuser').text
                  tmpdict['mailpwd'] = s.find('mailpassword').text
                  tmpdict['mailpostfix'] = s.find('mailpostfix').text
                  tmpdict['mailhost'] = s.find('mailhost').text
                  tmpdict['successsubject'] = s.find('successsubject').text
                  tmpdict['successcontext'] = s.find('successcontext').text
                  tmpdict['failsubject'] = s.find('failsubject').text
                  tmpdict['failcontext'] = s.find('failcontext').text
                  temlist.append(tmpdict)
            return temlist
      
      def reciever_setting(self) :
            root = self.__get_property()
            temlist = []
            for r in root.findall('reciever'):                  
                  temlist.append(r.find('mailaddress').text)
            return temlist

      def backup_setting(self):
            root = self.__get_property()
            temlist = []
            for b in root.findall('backup'):
                  tmpdict = {}
                  tmpdict['filepath'] = b.find('filepath').text
                  tmpdict['filename'] = b.find('filename').text
                  temlist.append(tmpdict)
            return temlist

      def database_setting(self) :
            root = self.__get_property()
            temlist = []
            for d in root.findall('database'):
                  tmpdict = {}
                  tmpdict['ip'] = d.find('ip').text
                  tmpdict['user'] = d.find('user').text
                  tmpdict['password'] = d.find('password').text
                  tmpdict['db'] = d.find('db').text
                  tmpdict['port'] = d.find('port').text
                  temlist.append(tmpdict)
            return temlist
