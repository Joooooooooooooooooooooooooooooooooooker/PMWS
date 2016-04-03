1.打包前需要将文件夹下的python脚本复制到桌面上

2.需要以管理员身份打开cmd 并切换到桌面目录

3.cmd 执行cxfreeze MonitorService.py --target-dir dist 命令
  cmd 执行python setup.py bdist_msi 也可以

4.将ExtraPackage复制到打包生成的dist文件夹内
  如果是msi可以不需要这个过程

5.将文件夹内的property.xml配置文件复制到D盘根目录下
  配置文件内有注释

6.cmd 切换到dist文件夹 安装服务 执行 MonitorService.exe install
  如果是msi 需要切换到安装目录

7.运行服务 执行MonitorService.exe start

8.停止服务 执行MonitorService.exe stop

9.移除服务 执行MonitorService.exe remove

10.安装自启动服务 MonitorService.exe--startup auto install

11.重启服务 MonitorService.exe restart

12.日志文件在D盘根目录下PythonService.log
