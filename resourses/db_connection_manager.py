import sqlite3


class DbConn:
    def __init__(self, host):
        self.conn = None
        self.cursor = None
        self.host = host

    def __enter__(self):
        self.conn = sqlite3.connect(self.host)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb or exc_val or exc_type:
            self.conn.close()
        else:
            self.conn.commit()
            self.conn.close()
