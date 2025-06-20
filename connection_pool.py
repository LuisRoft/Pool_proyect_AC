from psycopg2 import pool
import threading

class ConnectionPool:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_config):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.pool = pool.SimpleConnectionPool(1, 5, **db_config)
        return cls._instance

    def getconn(self):
        return self.pool.getconn()

    def putconn(self, conn):
        self.pool.putconn(conn)

    def closeall(self):
        self.pool.closeall()
