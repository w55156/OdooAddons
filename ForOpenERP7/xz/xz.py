# -*- encoding: utf-8 -*-

########################################################################################################################################
#
#    Created by OpenERP ModelBuilder, ChunLai Wang, NingBo ZheJiang China, @2013, QQ:363682158
#
#-------------------------------------------对象定义的完整属性说明-----------------------------------------------------------------
#
#_auto：是否自动创建对象对应的Table，缺省值为: True,
#　　当安装或升级模块时，OpenERP会自动在数据库中为模块中定义的每个对象创建相应的Table,
#　　当这个属性设为False时，OpenERP不会自动创建Table，这通常表示数据库表已经存在，
#　　例如，当对象是从数据库视图（View）中读取数据时，通常设为False,当_auto的值为False时，
#　　OE不会自动在数据库中创建相应的表，开发者可以在对应类的init()方法中定义表或视图的SQL。
#_name：对象的唯一标识符，必须是全局唯一,
#　　这个标识符用于存取对象，其格式通常是 ModuleName.ClassName,
#　　对应的，系统会字段创建数据库表 ModuleName_ClassName。
#　　当使用_inherit时可以与被继承的类的_name一致，_name一致表示不创建新的数据库表，而直接在原表上修改
#_descript：对象说明性文字，任意文字。
#_log_access：是否自动在对应的数据表中增加create_uid, create_date, write_uid, write_date
#　　四个字段，缺省值为True，即字段增加,这四个字段分布记录record的创建人，
#　　创建日期，修改人，修改日期。这四个字段值可以 用对象的方法（perm_read）读取。
#_constraints: 定义于对象上的约束（constraints），通常是定义一个检查函数。
#　　用法：_constraints = [(method,'error message',list_of_field_names),] 
#_defaults: 定义字段的缺省值。当创建一条新记录（record or resource）时，记录中各字段的缺省值在此定义。
#　　用法：_defaults = {'field_name':function,}
#_order: 定义search()和read()方法的结果记录的排序规则，和SQL语句中的order 类似，缺省值是id,即按id升序排序。
#_rec_name: 标识record name的字段。缺省情况（name_get没被重载的话）方法name_get()返回本字段值。_rec_name通常用于记录的显示，
#　　例如，销售订单中包含业务伙伴，当在销售订单上显示业务伙伴时，系统缺省的是显示业务伙伴记录的_rec_name。
#_sequence: 数据库表的id字段的序列采集器，缺省值为: None。OpenERP创建数据库表时，会自动增加id字段作为主键，并自动为该表创建一个序列
#　　（名字通常是“表名_id_seq”）作为id字段值的采集器。如果想使用数据库中已有的序列器，则在此处定义序列器名。
#_sql: _auto为True时，可以在这里定义创建数据库表的SQL语句。不过5.0以后好像不支持了，不建议使用。
#_sql_constraints: 定义于对象上的约束（constraints），和SQL文中的约束类似，用法：_sql_constraints =
#　　 [('code_company_uniq', 'unique (code,company_id)', 'The code of the account must be unique per company !'), ]
#_table: 待创建的数据库表名，缺省值是和_name一样，只是将.替换成_
#_inherits,_inherit: _inherits和_inherit都用于对象的继承。
#
######################################################################################################################################


from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _  
from osv.osv import except_osv

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

class xz_baogongdan(osv.osv):
    STATE_SELECTION = [
        ('draft', u'草稿'),
        ('done', u'已结算')
    ]
    _name = 'xz.baogongdan'
    _description = u'报工单'
    _log_access = True
    _auto = True
    _columns = {
           'name': fields.char(u'编号', size=64, required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'riq' : fields.date(u'日期',required=True, readonly=True,states={'draft': [('readonly', False)]}),
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
        'shul':50,
        'state':lambda *a:'draft'
    }
    _sql_constraints = [
        ('name','unique(name)',u'名称不能重复'),
        ('riq_chanp_gongx_yuang', 'unique(riq,chanp,gongx,yuang)', u'特定的日期不能重复报工')
    ]
    
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
        ('draft', u'草稿'),
        ('done', u'已结算')
    ]
    _name = 'xz.dagongdan'
    _description = u'大工单'
    _log_access = True
    _auto = True
    _columns = {
           'name': fields.char(u'编号', size=64, required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'riq' : fields.date(u'日期',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'yuang' : fields.many2one('hr.employee',u'员工',required=True, readonly=True,states={'draft': [('readonly', False)]}),
           'shul' : fields.float(u'数量(小时)',required=True,readonly=True,states={'draft': [('readonly', False)]}),
           'gongz' : fields.float(u'工资', readonly=True,states={'draft': [('readonly', False)]}),
           'beiz' : fields.text(u'备注/说明', readonly=True,states={'draft': [('readonly', False)]}),
           'state': fields.selection(STATE_SELECTION, u'状态', readonly=True,states={'draft': [('readonly', False)]}),
          }
    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'xz.dagongdan') or '/',
        'riq':fields.date.context_today,  
        'shul':50,
        'state':lambda *a:'draft'
    }
    _sql_constraints = [
        ('name','unique(name)',u'名称不能重复'),
        ('riq_yuang', 'unique(riq,yuang)', u'特定的日期不能重复报工')
    ]

    def onchange_yuang(self,cr,uid,ids,riq,context=None):
        if not riq:
            riq = '2000-01-01'
        riq_sp = riq.split('-')
        myear=riq_sp[1]+'/'+riq_sp[0]
        cr.execute('select name from account_period where state=\'draft\' and code=\''+myear+'\';')
        if len(cr.fetchall())>0:
            return True
        else:
            warning = {
                'title': _('Warning!'),
                'message' : _(u'当前会计期间已关闭，请重新选择日期，如果有需要，请联系管理员寻求帮助!')
                }
            #raise osv.except_osv(_('Error'),_('会计期间已关闭，请重新选择日期'))
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
