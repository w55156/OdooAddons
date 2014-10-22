# -*- encoding: utf-8 -*-

#################################################################################################
#                                                                                               #
# Created by OpenERP ModelBuilder, ChunLai Wang, NingBo ZheJiang China, @2013, QQ:363682158     #
#                                                                                               #
#################################################################################################

import time
from openerp.osv import fields, osv

class xz_jiesuan(osv.osv_memory):
    _name = 'xz.jiesuan'
    _description = u'工资月度结算'
    _columns = {
       'period_id': fields.many2one('account.period',u'会计期间',domain="[('state','=','draft'),('special','=',False)]",required=True),
    }
    
    def _avg_dict_get(self,cr,period_id,fm_type):
        cr.execute('select group_id,gz_avg from xz_gzavg where fm_type=\''+fm_type+'\' and period_id='+str(period_id))
        avg_list = cr.fetchall()
        if not avg_list:return False
        avg_dict = dict(avg_list)
        return avg_dict
    
    def _action_before(self,cr,period_id):
        #关闭选择的会计期间 
        #cr.execute('update account_period set state=\'done\' where id='+str(period_id))
        #所选择的会计期间下 用户单据状态设置为结束
        #cr.execute('update xz_baogongdan set state=\'done\' where period_id='+str(period_id))
        #cr.execute('update xz_dagongdan set state=\'done\' where period_id='+str(period_id))
        #cr.execute('update xz_gbaogongdan set state=\'done\' where period_id='+str(period_id))
        #cr.execute('update xz_gdagongdan set state=\'done\' where period_id='+str(period_id))
        #cr.execute('update xz_chuqgs set state=\'done\' where period_id'+str(period_id))
        #所选择的会计期间下 清除组平均工资表 和整个计件工资表明细
        cr.execute('delete from xz_gzdetail3 where period_id='+str(period_id))
        cr.execute('delete from xz_gzdetail2 where period_id='+str(period_id))
        cr.execute('delete from xz_gzdetail where period_id='+str(period_id))
        cr.execute('delete from xz_gzavg where period_id='+str(period_id))
     
    def _action_doing(self,cr,period_id,table_gz):
        cr.execute('select group_id,sum(gongz) as gongz from '+table_gz+' where period_id='+str(period_id)+ ' group by group_id')
        gz_byg_list=cr.fetchall()
        if not gz_byg_list:
            return False
        gz_byg_dict=dict(gz_byg_list)
        cr.execute('select group_id,sum(shul) as shul from xz_chuqgs where period_id = '+str(period_id)+' group by group_id')
        sl_byg_list=cr.fetchall()
        if not sl_byg_list:
            return False
        type_name = u'集体大工'
        if table_gz == 'xz_gbaogongdan':
            type_name = u'集体计件'
        rows_list=[]
        for sl_byg in sl_byg_list:
            sl=sl_byg[1]
            if not sl>0:continue
            gid=sl_byg[0]
            gz = gz_byg_dict.get(gid,0)
            avg=gz/sl
            row_tup=(gid,avg,period_id,table_gz,type_name)
            rows_list.append(row_tup)
        sql_str='insert into xz_gzavg(group_id,gz_avg,period_id,fm_type,fm_type_name) values(%s,%s,%s,%s,%s)'
        cr.executemany(sql_str,rows_list)
        return True
    
    def _import_to_detail(self,cr,period_id):
        #按员工分组取出每个员工的出勤工时
        cr.execute('select employee_id,group_id,shul from xz_chuqgs where period_id='+str(period_id))
        cqgs_list = cr.fetchall()
        #计算集体计件工资分配
        bavg_dict = self._avg_dict_get(cr, period_id,'xz_gbaogongdan')
        davg_dict = self._avg_dict_get(cr, period_id,'xz_gdagongdan')
        insert_list = []
        for cqgs in cqgs_list:
            eid = cqgs[0]
            gid = cqgs[1]
            shul = cqgs[2]
            bavg = bavg_dict.get(gid,0)
            davg = davg_dict.get(gid,0)
            bgz = shul*bavg
            dgz = shul*davg
            b_tup = (eid,gid,bgz,period_id,'xz_gbaogongdan',u'集体计件')
            d_tup = (eid,gid,dgz,period_id,'xz_gdagongdan',u'集体大工')
            insert_list.append(b_tup)
            insert_list.append(d_tup)
        #插入中间表 临时用 xz_gzdetail    
        sql_str='insert into xz_gzdetail(employee_id,group_id,gongz,period_id,fm_type,fm_type_name) values(%s,%s,%s,%s,%s,%s)'
        cr.executemany(sql_str,insert_list)
        #集体  分配后的个人计件和大工工资写入 工资明细表 xz_gzdetail2
        sql_str2='insert into xz_gzdetail2(employee_id,gongz,period_id,fm_type,fm_type_name) select employee_id,\
        gongz,period_id,fm_type,fm_type_name from (select employee_id,sum(gongz) as gongz,max(period_id) as period_id,max(fm_type) \
        as fm_type,max(fm_type_name) as fm_type_name from xz_gzdetail where fm_type=\'xz_gbaogongdan\' and period_id='+str(period_id)+' group by employee_id union select \
        employee_id,sum(gongz) as gongz,max(period_id) as period_id,max(fm_type) as fm_type,max(fm_type_name) as fm_type_name from \
        xz_gzdetail where fm_type=\'xz_gdagongdan\' and period_id='+str(period_id)+' group by employee_id) as tmp'
        cr.execute(sql_str2)
        
        #计算个人的计件和大工工资  写入 工资明细表 xz_gzdetail2
        rows_list = []
        cr.execute('select yuang as employee_id,sum(gongz) as gongz,max(period_id) as period_id from xz_baogongdan where period_id='+str(period_id)+' group by yuang')
        baog_list = cr.fetchall()
        cr.execute('select yuang as employee_id,sum(gongz) as gongz,max(period_id) as period_id from xz_dagongdan where period_id='+str(period_id)+' group by yuang')
        dag_list = cr.fetchall()
        #个人计件
        for baog in baog_list:
            row_tup = (baog[0],baog[1],period_id,'xz_baogongdan',u'个人计件')
            rows_list.append(row_tup)
        #个人大工
        for dag in dag_list:
            row_tup = (dag[0],dag[1],period_id,'xz_dagongdan',u'个人大工')
            rows_list.append(row_tup)
        sql_str='insert into xz_gzdetail2(employee_id,gongz,period_id,fm_type,fm_type_name) values(%s,%s,%s,%s,%s)'
        cr.executemany(sql_str,rows_list)
        cr.execute('insert into xz_gzdetail3(period_id,employee_id,gongz) select max(period_id) as period_id,employee_id,sum(gongz) as gongz from xz_gzdetail2 where period_id='+str(period_id)+' group by employee_id')
            
    def action_generate(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)
        period_id = data[0]['period_id'][0]
        #预处理
        self._action_before(cr,period_id)
        
        #处理集体计件工资 写入平均计件工次
        self._action_doing(cr,period_id,'xz_gbaogongdan')
        #处理集体计时工资 写入平均计时工次
        self._action_doing(cr,period_id,'xz_gdagongdan')
        #集中处理 写稿最终的工资表 （员工，工资，会计期间，表单类型，表单类型说明）
        self._import_to_detail(cr, period_id)
        return True
