import mysql.connector

class MysqlManager:
    """
    Manages MySQL connection and return cnx
    """
    cnx = None
    def __init__(self):
        try:
            if not MysqlManager.cnx:
                MysqlManager.cnx = mysql.connector.connect(
                    host="mysql",
                    port=3306,
                    user='root',
                    password='root',
                    database="digital_hunter"
                )
            self.cnx = MysqlManager.cnx
        except Exception as e:
            raise Exception(f'Could not connect to MySQL db, Error: {str(e)}')

    def get_cnx(self):
        """
        Return MySQL connection
        """
        return self.cnx