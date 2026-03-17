import mysql.connector

class MysqlManager:
    """
    Manages MySQL connection and return cnx
    """
    cnx = None
    def __init__(self):
        if not MysqlManager.cnx:
            MysqlManager.cnx = mysql.connector.connect(
                host="localhost",
                port=3306,
                user='root',
                password='root',
                database="digital_hunter"
            )
        self.cnx = MysqlManager.cnx

    def get_cnx(self):
        """
        Return MySQL connection
        """
        return self.cnx