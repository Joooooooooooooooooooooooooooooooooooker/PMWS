#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import pymssql
import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class MYSQL:
    def __init__(self,host,user,pwd,db,port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,port=self.port,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):

        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        
    def InsertMany(self,sql,dataList):
        cur = self.__GetConnect()
        cur.executemany(sql,dataList)
        self.conn.commit()
        self.conn.close()


class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):

        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        
    def InsertMany(self,sql,dataList):
        cur = self.__GetConnect()
        cur.executemany(sql,dataList)
        self.conn.commit()
        self.conn.close()

class Oracle:
    def __init__(self,user,pwd,host,port,sid):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
        self.sid = sid

    def __GetConnect(self):
        self.dsn=cx_Oracle.makedsn(self.host,self.port,self.sid)
        self.con=cx_Oracle.connect(self.user,self.pwd,self.dsn)
        cur = self.con.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.con.close()
        return resList

    def ExecNonQuery(self,sql):

        cur = self.__GetConnect()
        cur.execute(sql)
        self.con.commit()
        self.con.close()
        
    def InsertMany(self,sql,dataList):
        cur = self.__GetConnect()
        cur.executemany(sql,dataList)
        self.con.commit()
        self.con.close()
