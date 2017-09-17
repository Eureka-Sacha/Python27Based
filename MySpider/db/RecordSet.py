# -*- coding: utf-8 -*-
__author__ = '奎'
# from SimpleDBPool import DBPool
import MySQLdb
from DBUtils.PooledDB import PooledDB


class RecordSet:
    __POOL = None

    def __init__(self):
        self._conn = RecordSet.__get_conn()  # 实例化时调用静态方法获取一个connection
        self._cursor = self._conn.cursor()  # 开启一个游标
        self._array = ()  # 返回值
        self._counts = -1  # 游标记录
        self._index = {}  # 列名和下标的k,v对应
        self._influenced = 0  # 受影响的行数

    @staticmethod
    def __get_conn():
        """
        静态方法,获取连接池中的连接
        """
        if RecordSet.__POOL is None:
            options = RecordSet.__db_conf_parser()
            RecordSet.__POOL = PooledDB(MySQLdb, int(options['db_maxconn']),
                                        host=str(options['db_host']), port=int(options['db_port']),
                                        user=str(options['db_user']),
                                        passwd=str(options['db_pass']),
                                        db=str(options['db_name']), charset='utf8')
        return RecordSet.__POOL.connection()

    @staticmethod
    def __db_conf_parser():
        """
        @staticmethod注解标识为静态方法 相当于java中的 static
        @classmethod注解的意思为类方法.
        """
        import ConfigParser

        conf = ConfigParser.ConfigParser()
        conf.readfp(open('conf.conf', 'r+'))
        option = conf.options('db')
        options = {}
        for o in option:
            something = conf.get('db', o)
            options[o] = something
        return options

    def execute_sql(self, sql, param=None, num=None, autocommit=False):
        """
        自动创建事物并执行SQL
        @sql=数据库语句
        @num=返回条数(并不等于分页)
        @param=insert,update参数(tuple or  list)
        """
        self.begin(autocommit)  # 开始一个事物
        result = False
        try:
            if param is None:  # 如果没有参数则直接执行sql
                count = self._cursor.execute(sql)
            else:
                if type(param[0]) == tuple or type(param) == list:  # 如果是一个二维数组则使用executemany
                    count = self._cursor.executemany(sql, param)
                else:
                    count = self._cursor.execute(sql, param)
            self._influenced = count  # 记录受影响的行数
            if count > 0:
                self._counts = -1  # 每次查询后重置游标
                i = 0
                self._index = {}
                if self._cursor.description:
                    for index in self._cursor.description:  # 每次查询后重置列名与序号的键值对
                        self._index[index[0]] = i
                        i += 1
                if self._cursor._rows:  # 根据是否有行数来判断设置arrays
                    if num is not None:  # 如果没有设置返回条数则默认返回全部
                        self._array = self._cursor.fetchmany(num)
                    elif num == 1:
                        self._array = self._cursor.fetchone()
                    else:
                        self._array = self._cursor.fetchall()
                else:
                    self._array = ()  # 无法返回值则清空array
                result = True
                self.dispose(1)  # 释放连接提并 commit
        except Exception, e:
            self.dispose(0)  # 报错,释放连接并 rollback
            raise e
        return result

    def getvalue(self, name):
        """
        根据列名获取值
        """
        if name is None:
            return False
        return self.getvalue_by_index(int(self._index[name]))

    def getvalue_by_index(self, index):
        """
        根据index获取值
        """
        if index is None:
            return False
        return self._array[self._counts][int(index)]

    def _get_insert_id(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０  有错误 停用
        """
        self.execute_sql("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]

    def next(self):
        """
        如果有下一行 返回true 并将游标+1
        """
        if len(self._array) < 1:
            return False
        if self._counts < (len(self._array) - 1):
            self._counts += 1
            return True
        return False

    def previous(self):
        """
        如果有上一行  返回true 并将游标-1
        """
        if len(self._array) < 1:
            return False
        if (self._counts > 0) and (self._counts <= len(self._array)):
            self._counts -= 1
            return True
        return False

    def begin(self, autocommit=False):
        """
        开启事务
        """
        if self._conn is None:
            self._conn = RecordSet.__get_conn()
            self._cursor = self._conn.cursor()
        # self._conn.set_character_set('utf8')
        # self._conn.begin()
        self._conn.autocommit = autocommit

    def end(self, option='commit'):
        """
         结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
         释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
        self._conn = None
        self._cursor = None

    def get_influenced(self):
        return self._influenced


if __name__ == '__main__':
    sql = ur'insert into proxyIP(ip,prot,incognito,type,address,verificationtime,flag,others) values(%s,%s,%s,%s,%s,%s,%s,%s)'
    t = ("1.1.1.1", "233", "0", "0", "address", "2016-01-01", "0", "")
    rs = RecordSet()
    rs.execute_sql('select * from proxyIP')
    while rs.next():
        print rs._array[rs._counts]
    if rs.execute_sql(sql, param=t):
        print rs.get_influenced()
        # print rs.get_insert_id()
