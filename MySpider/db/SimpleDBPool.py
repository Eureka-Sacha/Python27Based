# -*- coding: utf-8 -*-
# 复制粘贴自DBUtils 中的SimpleDBPool
__author__ = '奎'
__version__ = '0.1'

import MySQLdb

class PooledDBError(Exception):
    """General PooledDB error.
    一般错误"""


class NotSupportedError(PooledDBError):
    """DB-API module not supported by PooledDB.
    不支持DB-API 接口的"""


class PooledDBConnection:
    """A proxy class for pooled database connections.
    You don't normally deal with this class directly,
    but use PooledDB to get new connections.
    使用这个类来获得数据库连接.
    """

    def __init__(self, pool, con):
        self._con = con
        self._pool = pool

    def close(self):
        """Close the pooled connection.关闭连接"""
        # Instead of actually closing the connection,
        # return it to the pool so it can be reused.
        if self._con is not None:
            self._pool.returnConnection(self._con)
            self._con = None

    def __getattr__(self, name):
        # All other members are the same.
        return getattr(self._con, name)

    def __del__(self):
        self.close()


class DBPool:
    """数据库连接池操作类
    """

    def __init__(self, dbapi, maxconnections, *args, **kwargs):
        try:
            threadsafety = dbapi.threadsafety
        except Exception:
            threadsafety = None
        if threadsafety == 0:
            raise NotSupportedError('Database module does not support any level of threading.')
        elif threadsafety == 1:
            from Queue import Queue

            self._queue = Queue(maxconnections)  # create the queue
            self.connection = self._unthreadsafe_get_connection
            self.addConnection = self._unthreadsafe_add_connection
            self.returnConnection = self._unthreadsafe_return_connection

        elif threadsafety in (2, 3):
            from threading import Lock

            self._lock = Lock()  # create a lock object to be used later   创建一个线程锁,供后面使用
            self._nextConnection = 0  # index of the next connection to be used  下一个将被获取的connection编号
            self._connections = []  # the list of connections
            self.connection = self._threadsafe_get_connection  #
            self.addConnection = self._threadsafe_add_connection
            self.returnConnection = self._threadsafe_return_connection
        else:
            raise NotSupportedError(
                "Database module threading support cannot be determined.")
        # Establish all database connections (it would be better to
        # only establish a part of them now, and the rest on demand).
        for i in range(int(maxconnections)):
            self.addConnection(dbapi.connect(*args, **kwargs))


    def _unthreadsafe_get_connection(self):
        """Get a connection from the pool.
        从连接池获取一个连接"""
        return PooledDBConnection(self, self._queue.get())

    def _unthreadsafe_add_connection(self, con):
        """Add a connection to the pool."""
        self._queue.put(con)

    def _unthreadsafe_return_connection(self, con):
        """Return a connection to the pool.
        In this case, the connections need to be put
        back into the queue after they have been used.
        This is done automatically when the connection is closed
        and should never be called explicitly outside of this module.
        """
        self._unthreadsafe_add_connection(con)

    # The following functions are used with DB-API 2 modules
    # that are threadsafe at the connection level, like psycopg.
    # Note: In this case, connections are shared between threads.
    # This may lead to problems if you use transactions.

    def _threadsafe_get_connection(self):
        """Get a connection from the pool."""
        self._lock.acquire()  # 锁定线程
        try:
            next = self._nextConnection  #
            con = PooledDBConnection(self, self._connections[next])
            next += 1
            if next >= len(self._connections):
                next = 0
            self._nextConnection = next
            return con
        finally:
            self._lock.release()

    def _threadsafe_add_connection(self, con):
        """Add a connection to the pool."""
        self._connections.append(con)

    def _threadsafe_return_connection(self, con):
        """Return a connection to the pool.
        In this case, the connections always stay in the pool,
        so there is no need to do anything here.
        """
        pass


class MySqlDBPool():
    __pool = None

    def __init__(self):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
        self._conn = MySqlDBPool.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        if MySqlDBPool.__pool is None:
            options = MySqlDBPool.DBConfParser()
            __pool = DBPool(creator=MySQLdb, maxcached=options['db_maxconn'],
                            host=options['db_host'], port=options['db_port'], user=options['db_user'],
                            passwd=options['db_pass'],
                            db=options['db_name'])
        return __pool.connection()

    @staticmethod
    def DBConfParser():
        """@staticmethod注解标识为静态方法 相当于java中的 static
        另: @classmethod注解的意思为类方法.
        """
        import ConfigParser

        conf = ConfigParser.ConfigParser()
        conf.readfp(open('../conf/conf.conf', 'r+'))
        option = conf.options('db')
        options = {}
        for o in option:
            something = conf.get('db', o)
            options[o] = something
        return options

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()


