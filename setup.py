# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],
                     "excludes": ["tkinter"],
                     "optimize": 2,
                     "include_files": ["D:\\Python34\\Lib\\uuid.py",
                                       "D:\\Python34\\Lib\\site-packages\\_mssql.pyd",
                                       "D:\\Python34\\Lib\\site-packages\\win32\\lib\\win32timezone.py",
                                       "D:\\Python34\\Lib\\site-packages\\_curses_panel.pyd",
                                       "D:\\Python34\\Lib\\site-packages\\_curses.pyd",
                                       "C:\\Users\\wangzhong\\Desktop\\property.xml",
                                       "C:\\Users\\wangzhong\\Desktop\\readme.txt"]
                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
executables = [Executable(script='MonitorService.py',
               base=base,
               targetName="joker.exe",
               compress=True,
               icon="E:\\PythonProject\\DataRegulation\\icon\\ico-48.ico")]

setup  (name = "PyService4Windows",
        version = "1.0",
        description = "A python windows server for monitor backup!",
        options = {"build_exe": build_exe_options},
        executables=executables)

# How to use
# python setup.py bdist_msi
# python setup.py build
