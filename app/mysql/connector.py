import pymysql.cursors
from mysql.logger import mysql_logger as logger
 
class MySQLConnector:
    def __init__(self, host='localhost', user='root', password='1234567890', database='hittv'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def connect(self):
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
        return conn
    
    def query(self, sql):
        logger.info(sql)

        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
            except Exception as e:
                print("Error query:", str(e))
            finally:
                cursor.close()

    def execute(self, sql):
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print("Error executing:", str(e))
            finally:
                cursor.close()
            
# Example usage of the MySQL connector class
connector = MySQLConnector()

# for row in result:
#     id, title, type, cover, director, scriptwriter, performer, release_date, introduce, tag, created_at = row
#     print(id)
#     print(title)
#     print(type)
#     print(cover)
#     print(director)
#     print(scriptwriter)
#     print(performer)
#     print(release_date)
#     print(introduce)
#     print(tag)
#     print(created_at)
