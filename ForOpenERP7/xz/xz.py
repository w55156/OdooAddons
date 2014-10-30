# -*- encoding: utf-8 -*-

#################################################################################################
#                                                                                               #
# Created by OpenERP ModelBuilder, ChunLai Wang, NingBo ZheJiang China, @2013, QQ:363682158     #
#                                                                                               #
#################################################################################################
import datetime
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _  
from osv.osv import except_osv

#----------------------------------------------------#   
#                  全局变量定义                                                             #
#----------------------------------------------------#

    
#----------------------------------------------------#   
#                配置类                                                                                 #
#----------------------------------------------------#
class xz_groups(osv.osv):
    _name = 'xz.groups'
    _description = u'集体工资组'
    _columns = {
           'name' : fields.char(u'名称',required=True),  
           'employees' : fields.many2many('hr.employee', 'xz_groups_hr_employee', 'gid', 'eid',u'员工'),  
          }
    _sql_constraints = [
        ('name','unique(name)',u'名称不能重复'),
    ]

class xz_yibcs(osv.osv):
    _name = 'xz.yibcs'
    _description = u'一般参数'
    _log_access = True
    _auto = True
    _columns = {
           'name':fields.char(u'名称',required=True),
           'bianm' : fields.char(u'编码',required=True),  
           'zhi' : fields.char(u'值',required=True),  
          }
    _sql_constraints = {
           ('name','unique(name)',u'名称不能重复'),
           ('bianm','unique(bianm)',u'编码不能重复'),
        }

class xz_jiagsb(osv.osv):
    _name = 'xz.jiagsb'
    _description = u'加工设备'
    _log_access = True
    _auto = True
    _columns = {
           'name' : fields.char(u'名称'),  
          }
    _sql_constraints = [
        ('name', 'unique(name)', u'名称不允许重复')
    ]

class xz_gongx(osv.osv):
    _name = 'xz.gongx'
    _description = u'工序'
    _log_access = True
    _auto = True
    _columns = { 
           'chanp' : fields.many2one('product.product', u'产品', required=True), 
           'jiagsb' : fields.many2one('xz.jiagsb', u'加工设备', required=True), 
           'name' : fields.char(u'名称',required=True), 
           'xianjgsj' : fields.float(u'现加工时间(秒)',required=True), 
           'banc' : fields.float(u'班产(件/个)'),  
           'dinge' : fields.float(u'定额(RMB元)',digits=(8,3)),   
          }
    _defaults = {
        'xianjgsj':100    
    }
    _sql_constraints = [
        ('name', 'unique(name)', u'名称不允许重复'),
        ('chap_jiagsb', 'unique(chanp,jiagsb)', u'当前产品已存在同样的加工设备的工序')
    ]
    
    def onchange_xianjgsj(self,cr,uid,ids,xianjgsj,context=None):
        jjts = 10.0
        jjty = 80.0
        dm1 = [('bianm','=','JJTS')]
        dm2 = [('bianm','=','JJTY')]
        ybcs_obj = self.pool.get('xz.yibcs')
        id1 = ybcs_obj.search(cr,uid,dm1)
        id2 = ybcs_obj.search(cr,uid,dm2)
        if id1:
            ybcs1 = ybcs_obj.read(cr,uid,id1,['zhi'])
            jjts = float(ybcs1[0]['zhi'])
        if id2:
            ybcs2 = ybcs_obj.read(cr,uid,id2,['zhi'])
            jjty = float(ybcs2[0]['zhi'])  
        banc = jjts*3600/xianjgsj
        dinge = jjty/banc
        return {'value':{'banc':banc,'dinge':dinge}}
    def onchange_chanp_jiagsb(self, cr, uid, ids,product_id,jiagsb_id, name, context=None):
        """ Changes  mingc if chanp or jiagsb changes.
        @param name: Name of the field
        @param product_id: Changed product_id
        @param jiagsb_id: Changed jiagsb_id
        @return:  Dictionary of changed values
        """
        prod_name = ''
        jiagsb_name = ''
        if product_id:
            prod = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            prod_name = prod.name
        if jiagsb_id:
            jiagsb = self.pool.get('xz.jiagsb').browse(cr, uid, jiagsb_id, context=context)
            jiagsb_name = jiagsb.name
        return {'value': {'name': prod_name+'-'+jiagsb_name}}


#----------------------------------------------------------------#   
#                       个人单据类                                                                                    #
#----------------------------------------------------------------#
class xz_baogongdan(osv.osv):
    STATE_SELECTION = [
    ('draft', u'待结算'),
    ('done', u'已关闭')
    ]
    _name = 'xz.baogongdan'
    _description = u'计件单'
    _log_access = True
    _auto = True
    _columns = {
           'name': fields.char(u'编号', size=64, required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'riq' : fields.date(u'日期',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'period_id' : fields.many2one('account.period',u'会计期间', required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'chanp': fields.many2one('product.product', u'产品', required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'gongx' : fields.many2one('xz.gongx',u'工序',domain=[('gongx','=',False)],required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'yuang' : fields.many2one('hr.employee',u'员工',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'shul' : fields.float(u'数量',required=True,readonly=True,states={'draft': [('readonly', False)]}),
           'gongz' : fields.float(u'工资', readonly=True,states={'draft': [('readonly', False)]}),
           'beiz' : fields.text(u'备注/说明', readonly=True,states={'draft': [('readonly', False)]}),
           'state': fields.selection(STATE_SELECTION, u'状态', readonly=True,states={'draft': [('readonly', False)]}),
          }

    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'xz.baogongdan') or '/',
        'riq':fields.date.context_today,  
        'shul':0.0,
        'state':lambda *a:'draft'
    }
    _sql_constraints = [
          ('name','unique(name)',u'名称不能重复'),
          ('riq_chanp_gongx_yuang', 'unique(riq,chanp,gongx,yuang)', u'特定的日期不能重复报工')
        ]
    def onchange_yuang(self,cr,uid,ids,riq,context=None):
        value = {
            'riq':False,
            'period_id':False
            }
        warning1 = {
            'title': _('Warning!'),
            'message' : _(u'没有选择日期，请重新选择，如果有需要，请联系管理员寻求帮助!')
            }
        if not riq:
            return {'warning':warning1,'value':value}
        riq_sp = riq.split('-')
        myear=riq_sp[1]+'/'+riq_sp[0]
        cr.execute('select id,name from account_period where state=\'draft\' and code=\''+myear+'\';')
        rt_set = cr.fetchone()
        if rt_set:
            return {'value':{'period_id':rt_set[0]}}
        else:
            warning2 = {
            'title': _('Warning!'),
            'message' : _(myear+u' 选择的会计期间已关闭，请重新选择日期，如果有需要，请联系管理员寻求帮助! ')
            }
            #raise osv.except_osv(_('Error'),_('会计期间已关闭，请重新选择日期'))
            return {'warning':warning2,'value':value}
        
    def product_id_change(self, cr, uid,ids,product_id,context=None):
        if not product_id:
            return {'value': {
                'gongx': False,
            }}
        gongx_id = False
        gongx_obj = self.pool.get('xz.gongx')
        gongx_ids = gongx_obj.search(cr,uid,[('chanp','=',product_id)])
        #raise osv.except_osv(_('Debug Info'),_(gongx_ids))
        if gongx_ids:
            gongx_id = gongx_ids[0] or False
        result = {
            'gongx': gongx_id
        }
        return {'value': result}
    
    def gongx_id_change(self, cr,uid,ids,gongx_id,shul,context=None):
        if not gongx_id:
            return {'value': {
                'gongz': False
            }}
        gongx_obj = self.pool.get('xz.gongx')
        reads = gongx_obj.read(cr, uid, gongx_id,['dinge'])
        dinge = 0.0
        #raise osv.except_osv(_('Debug Info'),_(reads))
        if reads.has_key('dinge'):
            dinge = reads['dinge']
        result = {
            'gongz': float(dinge)*float(shul)
        }    
        return {'value': result}

class xz_dagongdan(osv.osv):
    STATE_SELECTION = [
    ('draft', u'待结算'),
    ('done', u'已关闭')
    ]
    _name = 'xz.dagongdan'
    _description = u'大工单'
    _log_access = True
    _auto = True
    _columns = {
           'name': fields.char(u'编号', size=64, required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'riq' : fields.date(u'日期',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'period_id' : fields.many2one('account.period',u'会计期间', required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'yuang' : fields.many2one('hr.employee',u'员工',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'shul' : fields.float(u'数量(小时)',required=True,readonly=True,states={'draft': [('readonly', False)]}),
           'gongz' : fields.float(u'工资', readonly=True,states={'draft': [('readonly', False)]}),
           'beiz' : fields.text(u'备注/说明', readonly=True,states={'draft': [('readonly', False)]}),
           'state': fields.selection(STATE_SELECTION, u'状态', readonly=True,states={'draft': [('readonly', False)]}),
          }
    def _get_default_period_id(self,cr,uid,ids):
        riq_sp = datetime.datetime.strftime(datetime.date.today(),'%m/%Y/%d')
        myear=riq_sp[:7]
        return myear
    
    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'xz.dagongdan') or '/',
        'riq':fields.date.context_today, 
        'shul':0.0,
        'state':lambda *a:'draft'
    }
    
    _sql_constraints = [
        ('name','unique(name)',u'名称不能重复'),
        ('riq_yuang', 'unique(riq,yuang)', u'特定的日期不能重复报工')
    ]

    def onchange_yuang(self,cr,uid,ids,riq,context=None):
        value = {
            'riq':False,
            'period_id':False
            }
        warning1 = {
            'title': _('Warning!'),
            'message' : _(u'没有选择日期，请重新选择，如果有需要，请联系管理员寻求帮助!')
            }
        if not riq:
            return {'warning':warning1,'value':value}
        riq_sp = riq.split('-')
        myear=riq_sp[1]+'/'+riq_sp[0]
        cr.execute('select id,name from account_period where state=\'draft\' and code=\''+myear+'\';')
        rt_set = cr.fetchone()
        if rt_set:
            return {'value':{'period_id':rt_set[0]}}
        else:
            warning2 = {
            'title': _('Warning!'),
            'message' : _(myear+u' 会计期间已关闭，请重新选择日期，如果有需要，请联系管理员寻求帮助! ')
            }
            #raise osv.except_osv(_('Error'),_('会计期间已关闭，请重新选择日期'))
            return {'warning':warning2,'value':value}
             
    def onchange_shul(self,cr,uid,ids,shul,context=None):
        jjdg = 12.5
        dm1 = [('bianm','=','JJDG')]
        ybcs_obj = self.pool.get('xz.yibcs')
        id1 = ybcs_obj.search(cr,uid,dm1)
        if id1:
            ybcs1 = ybcs_obj.read(cr,uid,id1,['zhi'])
            jjdg = float(ybcs1[0]['zhi']) 
        gongz = jjdg*shul
        warning = {
                   'title':_('Warning'),
                   'message':_(u'数量太大了，如果有需要，请联系管理员寻求帮助!')
                   }
        value = {
                 'gongz':gongz
                 }
        if float(shul)>15:
            return {'value':value,'warning':warning}
        else:
            return {'value':value}
        
#----------------------------------------------------------------#   
#                       集体单据类                                                                                    #
#----------------------------------------------------------------#
class xz_gbaogongdan(osv.osv):
    STATE_SELECTION = [
    ('draft', u'待结算'),
    ('done', u'已关闭')
    ]
    _name = 'xz.gbaogongdan'
    _description = u'组计件单'
    _columns = {
           'name': fields.char(u'编号', size=64, required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'riq' : fields.date(u'日期',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'period_id' : fields.many2one('account.period',u'会计期间', required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'chanp': fields.many2one('product.product', u'产品', required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'gongx' : fields.many2one('xz.gongx',u'工序',domain=[('gongx','=',False)],required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'group_id' : fields.many2one('xz.groups',u'组',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'shul' : fields.float(u'数量',required=True,readonly=True,states={'draft': [('readonly', False)]}),
           'gongz' : fields.float(u'工资', readonly=True,states={'draft': [('readonly', False)]}),
           'beiz' : fields.text(u'备注/说明', readonly=True,states={'draft': [('readonly', False)]}),
           'state': fields.selection(STATE_SELECTION, u'状态', readonly=True,states={'draft': [('readonly', False)]}),
          }
       
    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'xz.gbaogongdan') or '/',
        'riq':fields.date.context_today, 
        'shul':0.0,
        'state':lambda *a:'draft'
    }
    _sql_constraints = [
        ('name','unique(name)',u'名称不能重复'),
        ('riq_chanp_gongx_group_id', 'unique(riq,chanp,gongx,group_id)', u'特定的日期不能重复报工')
    ]
    
    def onchange_group_id(self,cr,uid,ids,riq,context=None):
        if not riq:
            riq = '2000-01-01'
        riq_sp = riq.split('-')
        myear=riq_sp[1]+'/'+riq_sp[0]
        cr.execute('select id,name from account_period where state=\'draft\' and code=\''+myear+'\';')
        rt_set = cr.fetchone()
        if rt_set:
            return {'value':{'period_id':rt_set[0]}}
        else:
            warning = {
                'title': _('Warning!'),
                'message' : _(myear+u'当前会计期间已关闭，请重新选择日期，如果有需要，请联系管理员寻求帮助!')
                }
            #raise osv.except_osv(_('Error'),_('会计期间已关闭，请重新选择日期'))
            value = {
                'riq':False
                }
            return {'warning':warning,'value':value}
        
    def product_id_change(self, cr, uid,ids,product_id,context=None):
        if not product_id:
            return {'value': {
                'gongx': False,
            }}
        gongx_id = False
        gongx_obj = self.pool.get('xz.gongx')
        gongx_ids = gongx_obj.search(cr,uid,[('chanp','=',product_id)])
        #raise osv.except_osv(_('Debug Info'),_(gongx_ids))
        if gongx_ids:
            gongx_id = gongx_ids[0] or False
        result = {
            'gongx': gongx_id
        }
        return {'value': result}
    
    def gongx_id_change(self, cr,uid,ids,gongx_id,shul,context=None):
        if not gongx_id:
            return {'value': {
                'gongz': False
            }}
        gongx_obj = self.pool.get('xz.gongx')
        reads = gongx_obj.read(cr, uid, gongx_id,['dinge'])
        dinge = 0.0
        #raise osv.except_osv(_('Debug Info'),_(reads))
        if reads.has_key('dinge'):
            dinge = reads['dinge']
        result = {
            'gongz': float(dinge)*float(shul)
        }    
        return {'value': result}

class xz_gdagongdan(osv.osv):
    STATE_SELECTION = [
    ('draft', u'待结算'),
    ('done', u'已关闭')
    ]
    _name = 'xz.gdagongdan'
    _description = u'组大工单'
    _columns = {
           'name': fields.char(u'编号', size=64, required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'riq' : fields.date(u'日期',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'period_id' : fields.many2one('account.period',u'会计期间', required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'group_id' : fields.many2one('xz.groups',u'组',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'shul' : fields.float(u'数量(小时)',required=True,readonly=True,states={'draft': [('readonly', False)]}),
           'gongz' : fields.float(u'工资', readonly=True,states={'draft': [('readonly', False)]}),
           'beiz' : fields.text(u'备注/说明', readonly=True,states={'draft': [('readonly', False)]}),
           'state': fields.selection(STATE_SELECTION, u'状态', readonly=True,states={'draft': [('readonly', False)]}),
          }
       
    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'xz.gdagongdan') or '/',
        'riq':fields.date.context_today,  
        'shul':0.0,
        'state':lambda *a:'draft'
    }
    _sql_constraints = [
        ('name','unique(name)',u'名称不能重复'),
        ('riq_group_id', 'unique(riq,group_id)', u'特定的日期不能重复报工')
    ]

    def onchange_group_id(self,cr,uid,ids,riq,context=None):
        if not riq:
            riq = '2000-01-01'
        riq_sp = riq.split('-')
        myear=riq_sp[1]+'/'+riq_sp[0]
        cr.execute('select id,name from account_period where state=\'draft\' and code=\''+myear+'\';')
        rt_set = cr.fetchone()
        if rt_set:
            return {'value':{'period_id':rt_set[0]}}
        else:
            warning = {
                'title': _('Warning!'),
                'message' : _(myear+u'当前会计期间已关闭，请重新选择日期，如果有需要，请联系管理员寻求帮助!')
                }
            value = {
                'riq':False
                }
            return {'warning':warning,'value':value}
             
    def onchange_shul(self,cr,uid,ids,shul,context=None):
        jjdg = 12.5
        dm1 = [('bianm','=','JJDG')]
        ybcs_obj = self.pool.get('xz.yibcs')
        id1 = ybcs_obj.search(cr,uid,dm1)
        if id1:
            ybcs1 = ybcs_obj.read(cr,uid,id1,['zhi'])
            jjdg = float(ybcs1[0]['zhi']) 
        gongz = jjdg*shul
        value = {
                 'gongz':gongz
                 }
        return {'value':value}
        
class xz_chuqgs(osv.osv):
    STATE_SELECTION = [
    ('draft', u'待结算'),
    ('done', u'已关闭')
    ]              
    _name = 'xz.chuqgs'
    _description = u'出勤工时'
    _columns = {
           'name': fields.char(u'编号', size=64, required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'period_id' : fields.many2one('account.period',u'会计期间',domain="[('state','=','draft'),('special','=',False)]", required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'group_id' : fields.many2one('xz.groups',u'组', required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'employee_id' : fields.many2one('hr.employee',u'员工',domain="[('id','in',gdomain)]",required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'shul' : fields.float(u'数量(小时)',required=True,readonly=True,states={'draft': [('readonly', False)]}),
           'beiz' : fields.text(u'备注/说明', readonly=True,states={'draft': [('readonly', False)]}),
           'state': fields.selection(STATE_SELECTION, u'状态', readonly=True,states={'draft': [('readonly', False)]}),
           'gdomain':fields.text(u'gdomain')
          }
    
    def _get_default_period_id(self,cr,uid,ids):
        riq_sp = datetime.datetime.strftime(datetime.date.today(),'%m/%Y/%d')
        myear=riq_sp[:7]
        cr.execute('select id from account_period where state = \'draft\' and code = \''+myear+'\';')
        period_id=cr.fetchone()
        if not period_id:
            return False
        else:
            return period_id[0]
         
    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'xz.chuqgs') or '/', 
        'shul':0.0,
        'period_id':_get_default_period_id,
        'state':lambda *a:'draft'
    }
    _sql_constraints = [
        ('name','unique(name)',u'名称不能重复'),
        ('period_id_group_id_employee_id', 'unique(period_id,group_id,employee_id)', u'员工在选择的会计期间存在重复')
    ]
    
    def on_change_group_id(self,cr,uid,ids,group_id,context=None):
        if not group_id:
            return {'value':{'gdomain':False,'employee_id':False}}
        else:
            cr.execute('select id,name_related as name from hr_employee where id in (select eid from xz_groups_hr_employee where gid='+str(group_id)+');')
            tmp_list=cr.fetchall()
            if not tmp_list:
                return {'value':{'gdomain':False,'employee_id':False}}
            else:
                rt_list=[]
                for item in tmp_list:
                    rt_list.append(item[0])
                return {'value':{'gdomain':rt_list,'employee_id':False}} 
           
