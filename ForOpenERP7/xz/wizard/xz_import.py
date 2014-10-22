# -*- coding: utf-8 -*-  
'''
from osv import osv, fields  
import time, xlrd, base64  

class xz_import(osv.osv_memory):  
    _name = "xz.import"  
    _description = "xls import"  
    _columns = {  
        'excel': fields.binary('excel�ļ�', filters='*.xls'),  
    }    
    def bill_import(self, cr, uid, ids, context=None):  
        for wiz in self.browse(cr,uid,ids):  
            if not wiz.excel: continue  
            excel = xlrd.open_workbook(file_contents=base64.decodestring(wiz.excel))  
            sh = excel.sheet_by_index(0)  
            print sh.name, sh.nrows, sh.ncols  
            for rx in range(sh.nrows):  
                for ry in range(sh.ncols):  
                    print sh.cell(rx, ry).value  
                    # To Do
        return {'type': 'ir.actions.act_window_close'} 
'''