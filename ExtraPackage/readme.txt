1.���ǰ��Ҫ���ļ����µ�python�ű����Ƶ�������

2.��Ҫ�Թ���Ա��ݴ�cmd ���л�������Ŀ¼

3.cmd ִ��cxfreeze MonitorService.py --target-dir dist ����
  cmd ִ��python setup.py bdist_msi Ҳ����

4.��ExtraPackage���Ƶ�������ɵ�dist�ļ�����
  �����msi���Բ���Ҫ�������

5.���ļ����ڵ�property.xml�����ļ����Ƶ�D�̸�Ŀ¼��
  �����ļ�����ע��

6.cmd �л���dist�ļ��� ��װ���� ִ�� MonitorService.exe install
  �����msi ��Ҫ�л�����װĿ¼

7.���з��� ִ��MonitorService.exe start

8.ֹͣ���� ִ��MonitorService.exe stop

9.�Ƴ����� ִ��MonitorService.exe remove

10.��װ���������� MonitorService.exe--startup auto install

11.�������� MonitorService.exe restart

12.��־�ļ���D�̸�Ŀ¼��PythonService.log
