
--���ģ��ж�ز��ɾ����Գ�������SQL�������

--ģ�� �ֶ� SqlԼ��
select * from ir_model_fields where model like 'xz.%';
select * from ir_model_constraint where model in (select id from ir_model where model like 'xz.%');
select * from ir_model_relation where model in (select id from ir_model where model like 'xz.%');
select * from ir_model where model like 'xz.%';

--��ͼ ����
select * from ir_ui_view where model like 'xz.%';
select * from ir_act_window where res_model like 'xz.%';

--
select * from ir_act_window_view where view_id in (select id from ir_ui_view where model like 'xz.%');
select * from ir_act_window_view where act_window_id in (select id from ir_act_window where res_model like 'xz.%');


--
select * from ir_ui_menu order by id desc limit 50;
select * from ir_values order by id desc limit 50;


--�������
delete from ir_model_fields where model like 'xz.%';
delete from ir_model_constraint where model in (select id from ir_model where model like 'xz.%');
delete from ir_model_relation where model in (select id from ir_model where model like 'xz.%');
delete from ir_model where model like 'xz.%';

delete from ir_act_window where res_model like 'xz.%';
delete from ir_ui_view where model like 'xz.%';