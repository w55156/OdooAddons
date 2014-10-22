# -*- encoding: utf-8 -*-

#################################################################################################
#                                                                                               #
# Created by OpenERP ModelBuilder, ChunLai Wang, NingBo ZheJiang China, @2013, QQ:363682158     #
#                                                                                               #
#################################################################################################

import time
from openerp.osv import fields, osv

class xz_gzavg(osv.osv):
    _name = 'xz.gzavg'
    _description = u'计件组平均工资中间表'
    _columns = {
           'group_id' : fields.many2one('xz.groups',u'组'),  
           'gz_avg' : fields.float(u'平均工资'),  
           'period_id' : fields.many2one('account.period',u'会计期间'),  
           'fm_type' : fields.char(u'类型'), 
           'fm_type_name' : fields.char(u'类型名称')
          }

class xz_gzdetail(osv.osv):
    _name = 'xz.gzdetail'
    _description = u'工资明细 中间表'
    _columns = {
           'employee_id' : fields.many2one('hr.employee',u'员工'),  
           'group_id' : fields.many2one('xz.groups',u'组'), 
           'gongz' : fields.float(u'工资'),  
           'period_id' : fields.many2one('account.period',u'会计期间'),  
           'fm_type' : fields.char(u'类型'), 
           'fm_type_name' : fields.char(u'类型名称')
          }
    
class xz_gzdetail2(osv.osv):
    _name = 'xz.gzdetail2'
    _description = u'月度计件工资明细'
    _columns = {
           'employee_id' : fields.many2one('hr.employee',u'员工'),  
           'gongz' : fields.float(u'工资'),  
           'period_id' : fields.many2one('account.period',u'会计期间'),  
           'fm_type' : fields.char(u'类型'), 
           'fm_type_name' : fields.char(u'类型名称')
          }
    
class xz_gzdetail3(osv.osv):
    _name = 'xz.gzdetail3'
    _description = u'计件工资总表'
    _columns = {
           'employee_id' : fields.many2one('hr.employee',u'员工'),  
           'gongz' : fields.float(u'工资'),  
           'period_id' : fields.many2one('account.period',u'会计期间'),  
          }
    