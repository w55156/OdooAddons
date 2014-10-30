# -*- encoding: utf-8 -*-


{
  'name': '薪资系统',
  'version': '0.1',
  'description': "拓普公司  制动  辅助车间员工 工资计算自动化",
  'author': '王春来  QQ 363682158',
  'website': 'www.tuopu.com',
  'depends': ['hr','sale'],
  'data': [
           'xz_view.xml','xz_data.xml',
           'report/xz_report_view.xml',
           'security/xz_security.xml',
           'security/ir.model.access.csv',
           'wizard/xz_jiesuan_view.xml',
           ],
  'sequence':1,
  'demo': [],
  'test': [],
  'images': [],
  'css': ['static/src/css/xz.css',],
  'qweb':[],
  'installable': True,
  'application': True,
  'auto_install': False
}
