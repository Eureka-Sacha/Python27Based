# -*- coding: utf-8 -*-
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
            import Queue

            self._queue = Queue(maxconnections)  # create the queue
            self.connection = self._unthreadsafe_get_connection
            self.addConnection = self._unthreadsafe_add_connection
            self.returnConnection = self._unthreadsafe_return_connection

        elif threadsafety in (2, 3):
            from threading import Lock

            self._lock = Lock()  # create a lock object to be used later
            self._nextConnection = 0  # index of the next connection to be used
            self._connections = []  # the list of connections
            self.connection = self._threadsafe_get_connection
            self.addConnection = self._threadsafe_add_connection
            self.returnConnection = self._threadsafe_return_connection
        else:
            raise NotSupportedError(
                "Database module threading support cannot be determined.")
        # Establish all database connections (it would be better to
        # only establish a part of them now, and the rest on demand).
        for i in range(maxconnections):
            self.addConnection(dbapi.connect(*args, **kwargs))


    def _unthreadsafe_get_connection(self):
        """Get a connection from the pool."""
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
        self._lock.acquire()
        try:
            next = self._nextConnection
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


pool = DBPool(MySQLdb, 10, host='localhost', port='3306', user='root', password='', database='mypythondatabase')

db = pool.connection()
cursor = db.cursor()
sql = u'select * from proxyIP '
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print row[0]
        print row[1]
except Exception, e:
    print e
db.close()
