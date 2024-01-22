# coding:utf-8

import json, pymysql, re, xlrd
from typing import Union,List

class ReadData:
    """
    读取mysql和.xlsx文件数据，提供一些方便的方法
    """
    def __init__(self,xlsx_mysql_sql:Union[str,List[List]],needful_field:List[str]=None,select_sql=None,xlsx_sheet_index=0):
        """
        :param name:.xlsx文件路径或者mysql数据库数据表名称信息关键字或者mysql查询语句  比如：内蒙古计划.xlsx/陕西计划、院校数据/select * from bk_school
        :param needful_field:需要保留的数据字段,只支持中文,表头字段名称会被(强制)自动转为中文表头名称,sql语句查询有筛选字段时,不支持保留字段  比如：['院校名称','专业名称']
        :param xlsx_sheet_index:.xlsx文件的索引默认第一个  比如：0
        :param select_sql:查询数据库数据表名时筛选部分的sql语句  比如：year=2022 and school_name like '%北%大学'
        """
        self.data=[]#所有数据以二维列表存放
        self.db = None

        data_info=xlsx_mysql_sql
        if type(data_info)==list:
            self.data=data_info
            self.data[0] = [str(f) for f in self.data[0]]  # 数据第一行必须作为列索引且为字段名称类型字符串
        elif data_info.endswith('.xlsx'):#判断是否为.xlsx文件读取数据
            self.read_xlsx(data_info,xlsx_sheet_index)
        else:
            self.read_mysql(data_info,select_sql)#当做查询数据库数据

        if len(self.data) < 2:
            raise ValueError('表格数据为空，此类(ReadData)读取数据第一行必须用作为索引')

        self.abnormal_inspection()#异常数据检查
        self.column_index = {field: i for i, field in enumerate(self.data[0])}#创建列索引
        for k,v in self.column_index.items():
            exec(f'self.{k}={v}')

        if needful_field and name.lower()[:8]!='select *':#判断是否有需要保留的字段，按保留的字段保留数据
            self.reserve_needful_field(needful_field)

        self.len_row=len(self.data)#行数
        self.len_col=len(self.data[0])#列数

    def connect_mysql(self):
        with open('c:/mysql_config.json', 'r', encoding='utf-8') as f:
            mysql_config=json.load(f)
        self.db = pymysql.connect(host=mysql_config['host'], port=3306, user='root', password=mysql_config['password'], database=mysql_config['database'])
        self.cursor = self.db.cursor()

    def select_mysql_data(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def read_mysql(self,name,select_sql):
        self.connect_mysql()

        def get_th(table_name):#获取表头字段
            return [k[0] for k in self.select_mysql_data(f"""SELECT COLUMN_NAME   
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = 'bk_data' AND TABLE_NAME = '{table_name}'   
                ORDER BY ORDINAL_POSITION ASC;""")]

        def replace_th_name(lit):#替换表头名称
            new_name = []
            for name in lit:
                new_name.append(th_dict.get(name,name))
            return new_name

        th_dict={k:v for k,v in (v[0].split(':') for v in self.select_mysql_data("""select * from 表头字段对应名称"""))}

        if name[:6].lower()=='select':
            self.data.append(replace_th_name(get_th(re.search('from\s([^\s]+)',name,re.IGNORECASE).group(1))))
            self.data+=[list(v) for v in self.select_mysql_data(name)]

        else:
            table_dict={k:v for k,v in (v[0].split(':') for v in self.select_mysql_data("""select * from 表名称对应关系"""))}
            table_name=table_dict.get(name,name)
            self.data.append(replace_th_name(get_th(table_name)))
            sql = f"""select * from `{table_name}`{' where '+select_sql if select_sql else ''}"""
            self.data+=[list(v) for v in self.select_mysql_data(sql)]

    def read_xlsx(self,file_path,sheet_index):
        """
        :param file_path:文件路径或路径下第一个文件
        :param sheet_index:工作表索引默认第一个
        """
        # 打开Excel文件并获取工作表
        workbook = xlrd.open_workbook(file_path)
        worksheet = workbook.sheet_by_index(sheet_index)
        # 遍历每一行数据
        for i in range(worksheet.nrows):
            self.data.append(worksheet.row_values(i))

        self.data[0] = [str(f) for f in self.data[0]]  # 数据第一行必须作为列索引且为字段名称类型字符串

    def abnormal_inspection(self):
        """
        数据异常检查
        """
        if ',' in ''.join(self.data[0]):
            raise ValueError('表头名称不允许出现英文逗号“,”')
        if '-' in ''.join(self.data[0]):
            raise ValueError('表头名称不允许出现减号“-”')
        for v in self.data[0]:
            if is_num(v):
                raise ValueError('表头名称不允许出现纯自然数')
        if len(self.data[0]) != len(set(self.data[0])):
            raise ValueError('表头字段不允许出现出重复名称')
        if len(self.data[0]) != len(set(self.data[0])):
            raise ValueError('表头字段不允许出现出重复名称')

    def reserve_needful_field(self,needful_field):
        """
        保留数据所需字段
        """
        data=[]
        for row in self.data:
            col=[]
            for field in needful_field:
                col.append(row[self.column_index[field]])
            data.append(col)
        self.data=data
        self.column_index = {field: i for i, field in enumerate(self.data[0])}  # 创建列索引

    def sel_cl(self,row_mark:str=None,column_mark:str=None,da_ts=1):
        """
        筛选行和列
        :param row_mark:行索引只支持自然数 比如'1,10-20'
        :param column_mark:列索引支持自然数和字段名 比如'1,10-20','1,院校名称,专业代码-最低分,14'
        :param da_ts:默认为1横向显示数据，2为纵向显示数据
        """
        def diiini(i):
            if i=='':
                i = self.len_col
            elif not is_num(i):
                i = self.column_index.get(i)
                if not i:
                    raise ValueError(f'传入索引错误{i}')
            return int(i)

        def index_split(mark,typ):
            rcis = []
            for i1 in mark.split(','):
                i2 = i1.split('-')
                if len(i2) == 1:
                    rcis.append(diiini(i2[0]) if typ=='col' else int(i2[0]))
                else:
                    [rcis.append(i) for i in range((diiini(i2[0]) if typ=='col' else int(i2[0] or 0)), (diiini(i2[1]) if typ=='col' else int(i2[1] or self.len_row)) + 1 or 0)]
            return sorted(list(set(rcis)))

        ris=index_split(row_mark,'row') if row_mark else range(self.len_row+1)
        cis=index_split(column_mark,'col') if column_mark else range(self.len_col+1)

        if da_ts == 1:
            for ri in ris:
                if ri < self.len_row-1:
                    row_data = []
                    for ci in cis:
                        if ci < self.len_col:
                            row_data.append(self.data[ri+1][ci])
                    yield row_data
        else:
            for ci in cis:
                if ci < self.len_col:
                    row_data = []
                    for ri in ris:
                        if ri < self.len_row-1:
                            row_data.append(self.data[ri+1][ci])
                    yield row_data

    def group(self,*args):
        data = {}
        for row in self.data[1:]:
            key=','.join([str(row[self.column_index[arg]]) for arg in args])
            if key in data:
                data[key].append(row)
            else:
                data[key]=[row]
        return data

    def __del__(self):
        if self.db:
            self.db.close()
            self.cursor.close()

#判断是否为纯数字
def is_num(s):
    if type(s) == int or re.search('^([0-9]+)$',str(s)):
        return True